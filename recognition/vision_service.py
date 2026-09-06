# -*- coding: utf-8 -*-
"""
Vision & Recognition Service for Tam Quoc Chi - Chien Luoc.
Supports:
1. High-speed Offline Local OCR (via RapidOCR / ONNX) with Card Grid Detection & SP Badge Resolution.
2. Google Gemini 1.5/2.0 Flash Vision API if API key is provided.
"""
import os
import json
import re
import difflib
import base64
import requests
import unicodedata
from typing import List, Dict, Any, Optional

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from rapidocr_onnxruntime import RapidOCR
    HAS_RAPID_OCR = True
except ImportError:
    HAS_RAPID_OCR = False

def remove_accents(text: str) -> str:
    text = unicodedata.normalize('NFD', str(text))
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower().replace('đ', 'd').replace('  ', ' ').strip()

def clean_ocr_line(text: str) -> str:
    text = remove_accents(text)
    # Don't strip SP! Only strip lone leading single letters if followed by space or symbols
    text = re.sub(r'^[a-z]\s+', '', text)
    text = re.sub(r'^[\[\]\(\)\.\s\d]+', '', text)
    text = re.sub(r'\b(40th|co|pk|s1|s2|s3|thuc tinh|thire tinh|thure tinh)\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Common OCR distortions for game font cards
GENERAL_ALIASES = {
    "gia ho": "Giả Hủ",
    "gia hu": "Giả Hủ",
    "quan vi": "Quan Vũ",
    "quan vu": "Quan Vũ",
    "ter thuog": "Tôn Thượng Hương",
    "ter thuong": "Tôn Thượng Hương",
    "tor thudng": "Tôn Thượng Hương",
    "ton thuong": "Tôn Thượng Hương",
    "ton thuong huong": "Tôn Thượng Hương",
    "bang diuc": "Bàng Đức",
    "bang duc": "Bàng Đức",
    "manh hoach": "Mạnh Hoạch",
    "ma quan": "Mã Quân",
    "ma sieu": "Mã Siêu",
    "luc ton": "Lục Tốn",
    "lu bo": "Lữ Bố",
    "lu b6": "Lữ Bố",
    "ton kien": "Tôn Kiên",
    "dieu thuyen": "Điêu Thuyền",
    "tu ma y": "Tư Mã Ý",
    "bang thong": "Bàng Thống",
    "chuc dung": "Chúc Dung",
    "khuong duy": "Khương Duy",
    "tao thao": "Tào Tháo",
    "luu bi": "Lưu Bị",
    "trieu van": "Triệu Vân",
    "truong phi": "Trương Phi",
    "gia cat luong": "Gia Cát Lượng",
    "chu du": "Chu Du",
    "chu thai": "Chu Thái",
    "thai su tu": "Thái Sử Từ",
    "trinh pho": "Trình Phổ",
    "cam ninh": "Cam Ninh",
    "lang thong": "Lăng Thống",
    "lo tuc": "Lỗ Túc",
    "hoang nguyet anh": "Hoàng Nguyệt Anh",
    "quan ngan binh": "Quan Ngân Bình",
    "phap chinh": "Pháp Chính",
    "nguy dien": "Ngụy Diên",
    "truong bao": "Trương Bào",
    "quan hung": "Quan Hưng",
    "truong giac": "Trương Giác",
    "ta tu": "Tả Từ",
    "vu cat": "Vu Cát",
    "hoa da": "Hoa Đà",
    "vien thieu": "Viên Thiệu",
    "dong trac": "Đổng Trác",
    "man sung": "Mãn Sủng",
    "hac chieu": "Hác Chiêu",
    "ha hau uyen": "Hạ Hầu Uyên",
    "ha hau don": "Hạ Hầu Đôn",
    "quach gia": "Quách Gia",
    "trinh duc": "Trình Dục",
    "dien vi": "Điển Vi",
    "hua chu": "Hứa Chử",
    "tao nhan": "Tào Nhân",
    "tuan uc": "Tuân Úc",
    "tuan du": "Tuân Du",
    "tao phi": "Tào Phi"
}

# Noise keywords in game UI that should not match generals or tactics
NOISE_WORDS = {
    "chu dong", "bi dong", "chi huy", "dot kich", "phap tran", "binh chung", "noi chinh",
    "1/1", "100%", "50%", "40%", "35%", "30%", "25%", "thuc tinh", "ten chien phap",
    "phat dong", "huong dan", "loai hinh", "co the thiet lap", "sat thuong", "binh dao",
    "muu luoc", "quan dich", "quan ta", "chu tuong", "trang thai", "thiet lap", "toan bo",
    "chieumo", "tmhansw", "quan ket tran", "chieumodudc"
}

# Comprehensive Stem & Regex Patterns for all tactics in game screenshots
TACTIC_PATTERNS = {
    "Đoạt Hồn Hiệp Phách": [r"doat\s*hon", r"hiep\s*phach"],
    "Thảo Thuyền Mượn Tên": [r"thao\s*thuyen", r"thuyen\s*co", r"muon\s*ten"],
    "Quân Dân Khích Lệ": [r"quan\s*dan", r"khich\s*le", r"an\s*ui\s*quan"],
    "Tạm Thời Tránh Mũi Nhọn": [r"tam\s*thoi\s*tranh", r"tranh\s*mui", r"tam\s*lanh\s*song"],
    "Cắt Xương Trị Độc": [r"cat\s*xuong", r"cao\s*xuong", r"tri\s*doc"],
    "Chờ Đợi Xuất Phát": [r"cho\s*doi\s*xuat", r"xuat\s*phat", r"duong\s*suc\s*doi"],
    "Bát Môn Kim Tỏa Trận": [r"bat\s*mon", r"kim\s*toa"],
    "Thịnh Khí Lăng Địch": [r"thinh\s*khi", r"lang\s*dich", r"linh\s*dich"],
    "Phong Thỉ Trận": [r"phong\s*thi\s*tran", r"phong\s*thi"],
    "Tiềm Long Trận": [r"tiem\s*long"],
    "Tam Thế Trận": [r"tam\s*the\s*tran", r"tam\s*the"],
    "Vũ Phong Trận": [r"vu\s*phong"],
    "Đằng Giáp Binh": [r"dang\s*giap", r"giap\s*may"],
    "Hãm Trận Doanh": [r"ham\s*tran"],
    "Vô Đương Phi Quân": [r"vo\s*duong\s*phi", r"vo\s*dang\s*phi", r"voduongphi", r"vodangphi"],
    "Bạch Mã Nghĩa Tòng": [r"bach\s*ma\s*nghia", r"bach\s*ma"],
    "Hổ Báo Kỵ": [r"h[oôổ]?\s*bao\s*ky", r"ho\s*bao", r"\bbao\s*ky\b"],
    "Tây Lương Thiết Kỵ": [r"tay\s*luong\s*thiet", r"tay\s*luong"],
    "Lính Thanh Châu": [r"thanh\s*chau"],
    "Lính Đan Dương": [r"dan\s*duong"],
    "Bạch Nhị Binh": [r"bach\s*nhi"],
    "Tử Sĩ Tiên Phong": [r"tu\s*si\s*tien"],
    "Giải Phiền Vệ": [r"giai\s*phien"],
    "Phi Hùng Quân": [r"phi\s*hung"],
    "Tượng Binh": [r"tuong\s*binh"],
    "Đại Kích Sĩ": [r"dai\s*kich\s*si", r"dai\s*kich"],
    "Hoành Tảo Thiên Quân": [r"hoanh\s*tao", r"tao\s*thien\s*quan"],
    "Phá Quân Uy Thắng": [r"pha\s*quan\s*uy", r"pha\s*quan"],
    "Đánh Đâu Thắng Đó": [r"danh\s*dau\s*thang", r"so\s*huong\s*phi"],
    "Phá Trận Thôi Kiên": [r"pha\s*tran\s*thoi", r"thoi\s*kien"],
    "Gió Táp Mưa Sa": [r"gio\s*tap", r"mua\s*sa"],
    "Cứ Thủy Đoạn Kiều": [r"cu\s*thuy", r"doan\s*kieu"],
    "Xế Đao Chước Địch": [r"xe\s*dao", r"chuoc\s*dich"],
    "Trung Dũng Nghĩa Liệt": [r"trung\s*dung\s*nghia", r"nghia\s*liet"],
    "Cưỡi Ngựa Nghìn Dặm": [r"cuoi\s*ngua\s*nghin", r"nghin\s*dam"],
    "Huyết Đao Tranh Giành": [r"huyet\s*dao"],
    "Trấn Mục Hoành Mâu": [r"tran\s*muc", r"hoanh\s*mau"],
    "Hoành Qua Dược Mã": [r"hoanh\s*qua", r"duoc\s*ma"],
    "Tuyệt Địa Phản Kích": [r"tuyet\s*dia", r"phan\s*kich"],
    "Đánh Bại Quân Địch": [r"danh\s*bai\s*quan", r"be\s*gay\s*mui", r"chiet\s*xung"],
    "Mau Giành Lợi Thế": [r"mau\s*gianh", r"loi\s*the", r"toc\s*thua\s*ky"],
    "Bách Kỵ Kiếp Doanh": [r"bach\s*ky\s*kiep", r"kiep\s*doanh"],
    "Nhất Kỵ Đương Thiên": [r"nhat\s*ky\s*duong", r"duong\s*thien"],
    "Bạo Lệ Vô Nhân": [r"bao\s*le\s*vo", r"bao\s*le"],
    "Đương Phong Thôi Quyết": [r"duong\s*phong\s*thoi", r"duong\s*phong\s*toi", r"duong\s*phong"],
    "Thôi Phong Đoạn Nhẫn": [r"thoi\s*phong", r"doan\s*nhan"],
    "Lõa Y Huyết Chiến": [r"loa\s*y\s*huyet", r"khoa\s*y", r"loa\s*y"],
    "Thiết Kỵ Khu Trì": [r"thiet\s*ky\s*khu", r"khu\s*tri"],
    "Quỷ Thần Đình Uy": [r"quy\s*than\s*dinh", r"dinh\s*uy"],
    "Thái Bình Đạo Pháp": [r"thai\s*binh\s*dao", r"thai\s*binh"],
    "Sĩ Biệt Tam Nhật": [r"si\s*biet\s*tam", r"si\s*biet"],
    "Dụng Võ Thần Thông": [r"dung\s*vo\s*thong", r"dung\s*vo"],
    "Sợ Bóng Sợ Gió": [r"so\s*bong", r"so\s*gio"],
    "Phong Trợ Hỏa Thế": [r"phong\s*tro\s*hoa", r"phong\s*tro"],
    "Thượng Binh Phạt Mưu": [r"thuong\s*binh\s*phat", r"phat\s*muu"],
    "Binh Vô Thường Thế": [r"binh\s*vo\s*thuong", r"thuong\s*the"],
    "Văn Võ Song Toàn": [r"van\s*vo\s*song", r"song\s*toan"],
    "Vận Quyết Tính Kế": [r"van\s*quyet"],
    "Uy Mưu Vô Địch": [r"uy\s*muu"],
    "Mê Hoặc": [r"\bme\s*hoac\b"],
    "Nhanh Chân Tranh Đất": [r"nhanh\s*chan", r"tranh\s*dat"],
    "Vạn Quân Đoạt Sư": [r"van\s*quan\s*doat", r"doat\s*su", r"doat\s*soai"],
    "Vạn Tiễn Tề Phát": [r"van\s*tien\s*te", r"van\s*tien"],
    "Dụ Địch Thâm Nhập": [r"du\s*dich\s*tham", r"tham\s*nhap"],
    "Ngụy Thư Tương Gian": [r"nguy\s*thu\s*tuong", r"tuong\s*gian"],
    "Kế Hay Mưu Giỏi": [r"ke\s*hay\s*muu", r"kehaymuu"],
    "Thiêu Đốt Doanh Lũy": [r"thieu\s*dot\s*doanh", r"doanh\s*luy"],
    "Cốc Thần Tinh": [r"coc\s*than"],
    "Họa Sĩ": [r"\bhoa\s*si\b"],
    "Đẹp Lòng Người": [r"dep\s*dong", r"dong\s*long\s*nguoi", r"khuynh\s*quoc"],
    "Thời Cơ Chiến Thắng": [r"thoi\s*co\s*chien"],
    "Truyền Âm Nhập Mật": [r"truyen\s*am"],
    "Đồng Lòng Hợp Sức": [r"dong\s*long\s*hop"],
    "Toàn Quân Đồng Lòng": [r"toan\s*quan\s*dong"],
    "Khí Lăng Tam Quân": [r"khi\s*lang\s*tam"],
    "Lấy Ít Đánh Nhiều": [r"lay\s*it\s*danh"],
    "Dũng Giả Hàng Đầu": [r"dung\s*gia\s*hang"],
    "Tứ Diện Sở Ca": [r"tu\s*dien\s*so"],
    "Nhất Lực Cự Thủ": [r"nhat\s*luc\s*cu"],
    "Quân Cẩm Phàm": [r"quan\s*cam\s*pham", r"cam\s*pham"],
    "Tiên Thành Kỳ Lự": [r"tien\s*thanh\s*ky"],
    "Dốc Sức Tính Kế": [r"doc\s*suc\s*tinh"],
    "Loạn Cung Ẩm Vũ": [r"loan\s*cung\s*am"],
    "Ngự Địch Bình Chướng": [r"ngu\s*dich\s*binh", r"ngu\s*dich"],
    "Tị Thực Kích Hư": [r"ti\s*thuc\s*kich", r"kich\s*hu"],
    "Lạc Phượng": [r"lac\s*phuong", r"lac\s*phung"],
    "Bất Nhục Sứ Mệnh": [r"bat\s*nhuc\s*su", r"su\s*menh"],
    "Ám Tàng Huyền Cơ": [r"am\s*tang\s*huyen", r"am\s*tang"],
    "Nhất Cử Tiệm Diệt": [r"nhat\s*cu\s*tiem", r"tiem\s*diet"],
    "Phấn Đột": [r"\bphan\s*dot\b"],
    "Tài Khí Quá Nhân": [r"tai\s*khi\s*qua"],
    "Tọa Chi Nộ Hạp": [r"toa\s*chi\s*no"],
    "Lỗ Mãng": [r"\blo\s*mang\b"],
    "Cường Công": [r"\bcuong\s*cong\b"],
    "Cường Dũng": [r"\bcuong\s*dung\b"],
    "Mưu Lược Tung Hoành": [r"muu\s*luoc\s*tung"],
    "Yêu Thuật": [r"\byeu\s*thuat\b"],
    "Thần Thượng Sứ": [r"than\s*thuong\s*su"],
    "Lạc Lôi": [r"\blac\s*loi\b"],
    "Bạch Mi": [r"\bbach\s*mi\b"],
    "Lửa Cháy Đồng Nội": [r"lua\s*chay\s*dong", r"dong\s*noi"],
    "Tự Lành": [r"\btu\s*lanh\b"],
    "Trá Hàng": [r"\btra\s*hang\b"],
    "Tịnh Hóa": [r"\btinh\s*hoa\b"],
    "Lư Giang Thượng Giáp": [r"lu\s*giang\s*thuong"],
    "Thiên Lý Trị Viện": [r"thien\s*ly\s*tri", r"tri\s*vien"],
    "Tọa Thủ Cô Thành": [r"toa\s*thu\s*co"],
    "Khinh Dũng Phi Yến": [r"khinh\s*dung\s*phi", r"phi\s*yen"],
    "Thả Lính Cướp Đoạt": [r"tha\s*linh\s*cuop", r"cuop\s*doat"],
    "Thần Thương Thiệt Chiến": [r"than\s*thuong\s*thiet"],
    "Xuất Kì Bất Ý": [r"xuat\s*ky\s*bat", r"xuat\s*ki\s*bat"],
    "Phong Thanh Hạc Lệ": [r"phong\s*thanh\s*hac", r"thanh\s*hac"],
    "Thiên Giáng Hỏa Vũ": [r"thien\s*giang\s*ha", r"thien\s*giang\s*hoa"],
    "Thi Khí Đao Lạc": [r"thi\s*khai\s*dao", r"thi\s*khi\s*dao"],
    "Hậu Phát Chế Nhân": [r"hau\s*phat\s*che"],
    "Truyền Hịch Tuyên Uy": [r"truyen\s*hich\s*tuyen"],
    "Xua Đuổi": [r"\bxua\s*duoi\b"],
    "Ỷ Thế Cầm Quyền": [r"y\s*the\s*cam"],
    "Kiêu Kiện Thần Hành": [r"kieu\s*kien\s*than"],
    "Thi Chí Bất Di": [r"thi\s*chi\s*bat"],
    "Đánh Vào Chỗ Đau": [r"danh\s*vao\s*cho\s*dau", r"danh\s*cho\s*dau"],
}

class VisionService:
    def __init__(self, db_dir: str = None):
        if db_dir is None:
            db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
        
        self.ocr_engine = RapidOCR() if HAS_RAPID_OCR else None

        with open(os.path.join(db_dir, "generals.json"), "r", encoding="utf-8") as f:
            self.generals = json.load(f)
            self.general_names = [g["name"] for g in self.generals]
            
        with open(os.path.join(db_dir, "tactics.json"), "r", encoding="utf-8") as f:
            self.tactics = json.load(f)
            self.tactic_names = [t["name"] for t in self.tactics]

        # Normalized lookup maps (Do NOT overwrite regular names with SP!)
        self.gen_norm_map = {}
        for g in self.generals:
            norm = remove_accents(g["name"])
            self.gen_norm_map[norm] = g["name"]

        self.tac_norm_map = {}
        for t in self.tactics:
            norm = remove_accents(t["name"])
            self.tac_norm_map[norm] = t["name"]

    def recognize_image(self, image_path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Unified image recognition pipeline:
        1. Tries Gemini Vision if API key provided.
        2. Falls back to local RapidOCR offline engine.
        """
        if api_key and len(api_key.strip()) > 10:
            res = self.recognize_with_gemini(image_path, api_key.strip())
            if res.get("success") and (res.get("generals") or res.get("tactics")):
                return res

        return self.recognize_with_local_ocr(image_path)

    def _recognize_grid_cards(self, image_path: str, w: int, h: int) -> List[str]:
        """
        Dedicated recognizer for game hero card grids.
        Crops each card slot, eliminates top ticker noise, resolves bottom name bar and SP badges.
        """
        if not HAS_PIL or not self.ocr_engine:
            return []

        # Determine grid dimension: card aspect ratio in game is ~1.44 (height / width)
        num_rows = 2 if h >= 280 else 1
        row_h = h / float(num_rows)
        card_w = row_h / 1.44
        num_cols = max(1, int(round(w / card_w)))
        col_w = w / float(num_cols)

        found_cards = set()
        tmp_crop_path = f"{image_path}_tmp_cell.png"

        try:
            with Image.open(image_path) as im:
                for r in range(num_rows):
                    for c in range(num_cols):
                        x1 = int(c * col_w)
                        x2 = int(min(w, (c + 1) * col_w))
                        # Avoid top world broadcast ticker on top row
                        top_offset = 25 if r == 0 else 0
                        y1 = int(r * row_h) + top_offset
                        y2 = int(min(h, (r + 1) * row_h))

                        if x2 - x1 < 20 or y2 - y1 < 20:
                            continue

                        crop = im.crop((x1, y1, x2, y2))
                        crop.save(tmp_crop_path)

                        c_res, _ = self.ocr_engine(tmp_crop_path)
                        if not c_res:
                            continue

                        # Check for SP badge in card text
                        has_sp = any(
                            it[1].strip().upper() == 'SP' or 
                            re.search(r'\bSP\b', it[1].upper())
                            for it in c_res
                        )

                        # Sort text lines by Y descending (bottom-up), hero names are at the bottom!
                        sorted_lines = sorted(c_res, key=lambda it: it[0][0][1], reverse=True)

                        card_gen = None
                        for it in sorted_lines:
                            raw = it[1]
                            clean = clean_ocr_line(raw)
                            norm = remove_accents(raw)

                            if not clean or any(noise in norm for noise in ['thuc tinh', 'chieumo', 'tmhansw', 'quan ket tran']):
                                continue

                            # 1. Check exact aliases
                            if clean in GENERAL_ALIASES:
                                card_gen = GENERAL_ALIASES[clean]
                                break

                            # 2. Check norm map
                            if clean in self.gen_norm_map:
                                card_gen = self.gen_norm_map[clean]
                                break

                            # 3. Fuzzy match aliases
                            for k, v in GENERAL_ALIASES.items():
                                if len(clean) >= 4 and abs(len(clean) - len(k)) <= 2:
                                    if difflib.SequenceMatcher(None, clean, k).ratio() >= 0.80:
                                        card_gen = v
                                        break
                            if card_gen:
                                break

                            # 4. Fuzzy match norm map
                            for k, v in self.gen_norm_map.items():
                                if len(clean) >= 5 and abs(len(clean) - len(k)) <= 2:
                                    if difflib.SequenceMatcher(None, clean, k).ratio() >= 0.84:
                                        card_gen = v
                                        break
                            if card_gen:
                                break

                        if card_gen:
                            # If SP badge found, check if SP version exists in database
                            sp_candidate = f"SP {card_gen}" if not card_gen.startswith("SP ") else card_gen
                            if has_sp and sp_candidate in self.general_names:
                                found_cards.add(sp_candidate)
                            else:
                                found_cards.add(card_gen)

        except Exception as err:
            print(f"Grid card recognition error: {err}")
        finally:
            if os.path.exists(tmp_crop_path):
                try:
                    os.remove(tmp_crop_path)
                except Exception:
                    pass

        return list(found_cards)

    def recognize_with_local_ocr(self, image_path: str) -> Dict[str, Any]:
        """
        Use RapidOCR to read game screenshot text and match against database.
        Combines pattern scanning, card grid resolution, and line matching.
        """
        if not self.ocr_engine:
            return {"success": False, "error": "RapidOCR engine is not installed", "generals": [], "tactics": []}

        im_w, im_h = 0, 0
        try:
            with Image.open(image_path) as im:
                im_w, im_h = im.size
        except Exception:
            pass

        # 1. Full image OCR
        ocr_target = image_path
        tmp_resized = None
        try:
            if max(im_w, im_h) > 1300:
                scale = 1300.0 / max(im_w, im_h)
                with Image.open(image_path) as im:
                    resized = im.resize((int(im_w * scale), int(im_h * scale)), Image.Resampling.BILINEAR)
                    tmp_resized = f"{image_path}_ocr_opt.jpg"
                    resized.convert("RGB").save(tmp_resized, "JPEG", quality=85)
                    ocr_target = tmp_resized
        except Exception:
            ocr_target = image_path

        try:
            res, _ = self.ocr_engine(ocr_target)
        except Exception as e:
            return {"success": False, "error": f"Lỗi OCR: {str(e)}", "generals": [], "tactics": []}
        finally:
            if tmp_resized and os.path.exists(tmp_resized):
                try:
                    os.remove(tmp_resized)
                except Exception:
                    pass

        if not res:
            return {"success": True, "generals": [], "tactics": [], "source": "local_ocr"}

        raw_lines = []
        for box, text, score in res:
            try:
                sc = float(score)
            except:
                sc = 1.0
            if sc > 0.35 and text.strip():
                raw_lines.append(text.strip())

        found_generals = set()
        found_tactics = set()

        joined_raw = " ".join(raw_lines)
        joined_norm = remove_accents(joined_raw)

        # 2. First-pass: Scan TACTIC_PATTERNS across entire image text
        for canon_tac, patterns in TACTIC_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, joined_norm):
                    found_tactics.add(canon_tac)
                    break

        # 3. Check if image appears to be a Card Grid
        grid_gens = []
        has_card_hints = any(
            any(hint in l.lower() for hint in ['thuc tinh', 's1', 's2', 's3', 'danh tuong', 'ton kien', 'dieu thuyen', 'lu bo']) 
            for l in raw_lines
        )
        if (has_card_hints or (im_w > 400 and im_h > 180 and im_w / max(1, im_h) > 1.3)) and not found_tactics:
            grid_gens = self._recognize_grid_cards(image_path, im_w, im_h)
            for g in grid_gens:
                found_generals.add(g)

        # 4. Standard line matching for non-grid images or tactics
        candidate_lines = list(raw_lines)
        for i in range(len(raw_lines) - 1):
            candidate_lines.append(f"{raw_lines[i]} {raw_lines[i+1]}")

        for raw_line in candidate_lines:
            line_clean = clean_ocr_line(raw_line)
            line_norm = remove_accents(raw_line)

            if not line_clean and not line_norm:
                continue

            if line_clean in NOISE_WORDS or line_norm in NOISE_WORDS:
                continue

            # Check general aliases (only if not already resolved by grid)
            if not grid_gens and line_clean in GENERAL_ALIASES:
                found_generals.add(GENERAL_ALIASES[line_clean])

            # Match Generals via dictionary (only if not already resolved by grid)
            if not grid_gens:
                for norm_g, canon_g in self.gen_norm_map.items():
                    if len(norm_g) < 3:
                        continue
                    if norm_g == "chuc dung" and ("chu dong" in line_norm or "chi dong" in line_norm):
                        continue

                    if norm_g == line_clean:
                        found_generals.add(canon_g)
                    elif len(norm_g) >= 5 and re.search(r'\b' + re.escape(norm_g) + r'\b', line_norm):
                        found_generals.add(canon_g)
                    elif len(norm_g) >= 6 and norm_g in line_norm:
                        found_generals.add(canon_g)
                    else:
                        if len(line_clean) >= 5 and abs(len(line_clean) - len(norm_g)) <= 2:
                            ratio = difflib.SequenceMatcher(None, line_clean, norm_g).ratio()
                            if ratio >= 0.85:
                                found_generals.add(canon_g)

            # Match Tactics via standard dictionary lookup
            for norm_t, canon_t in self.tac_norm_map.items():
                if len(norm_t) < 4:
                    continue
                if norm_t == "tinh hoa" and "thuc tinh" in line_norm:
                    continue

                if norm_t == line_clean:
                    found_tactics.add(canon_t)
                elif len(norm_t) >= 6 and (norm_t in line_norm or norm_t in line_clean):
                    found_tactics.add(canon_t)
                else:
                    if len(line_clean) >= 6 and abs(len(line_clean) - len(norm_t)) <= 2:
                        ratio = difflib.SequenceMatcher(None, line_clean, norm_t).ratio()
                        if ratio >= 0.86:
                            found_tactics.add(canon_t)

        return {
            "success": True,
            "generals": sorted(list(found_generals)),
            "tactics": sorted(list(found_tactics)),
            "source": "local_ocr",
            "lines_detected": len(raw_lines)
        }

    def recognize_with_gemini(self, image_path: str, api_key: str) -> Dict[str, Any]:
        """
        Use Google Gemini 2.0 / 1.5 Flash Vision API with optimized payloads.
        """
        if not api_key:
            return {"error": "API Key không được để trống", "generals": [], "tactics": []}

        try:
            mime_type = "image/jpeg"
            try:
                with Image.open(image_path) as im:
                    w, h = im.size
                    if max(w, h) > 1200:
                        scale = 1200.0 / max(w, h)
                        im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.BILINEAR)
                    import io
                    buf = io.BytesIO()
                    im.convert("RGB").save(buf, format="JPEG", quality=85)
                    image_bytes = buf.getvalue()
            except Exception:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()

            b64_image = base64.b64encode(image_bytes).decode("utf-8")

            all_gen_names = ", ".join(self.general_names)
            all_tac_names = ", ".join(self.tactic_names)

            prompt = f"""Bạn là chuyên gia game Tam Quốc Chí - Chiến Lược (Three Kingdoms Strategy - RTK).
Nhiệm vụ: Nhận diện chính xác tất cả các TƯỚNG và CHIẾN PHÁP trong ảnh chụp game.

DANH SÁCH TƯỚNG CHUẨN (chỉ trả về đúng các tên này):
{all_gen_names}

DANH SÁCH CHIẾN PHÁP CHUẨN (chỉ trả về đúng các tên này):
{all_tac_names}

Quy tắc nhận diện:
1. Chỉ nhận diện các tên tướng và chiến pháp xuất hiện RÕ RÀNG trong ảnh.
2. Nếu tướng có huy hiệu SP màu đỏ/cam, trả về tên 'SP <Tên Tướng>' nếu có trong danh sách chuẩn.
3. Không đoán mò. Nếu không chắc, bỏ qua.
4. Trả về JSON hợp lệ: {{"generals": ["Tên 1", ...], "tactics": ["Tên 1", ...]}}"""

            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": mime_type, "data": b64_image}}
                        ]
                    }
                ],
                "generationConfig": {
                    "response_mime_type": "application/json",
                    "temperature": 0.1
                }
            }

            models = ["gemini-2.0-flash", "gemini-1.5-flash"]
            resp = None
            for m in models:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
                    r = requests.post(url, headers=headers, json=payload, timeout=20)
                    if r.status_code == 200:
                        resp = r
                        break
                except Exception:
                    continue

            if resp is not None and resp.status_code == 200:
                data = resp.json()
                text_out = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text_out.startswith("```json"):
                    text_out = text_out[7:]
                if text_out.endswith("```"):
                    text_out = text_out[:-3]
                result = json.loads(text_out.strip())
                valid_gens = [g for g in result.get("generals", []) if g in self.general_names]
                valid_tacs = [t for t in result.get("tactics", []) if t in self.tactic_names]
                return {
                    "success": True,
                    "generals": valid_gens,
                    "tactics": valid_tacs,
                    "source": "gemini_vision"
                }
            else:
                return {"success": False, "error": f"Lỗi Gemini Vision: {resp.status_code if resp else 'Không phản hồi'}", "generals": [], "tactics": []}
        except Exception as e:
            return {"success": False, "error": str(e), "generals": [], "tactics": []}
