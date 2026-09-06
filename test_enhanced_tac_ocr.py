# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import glob
import unicodedata
import json
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
files = sorted(glob.glob('uploads/*.png'))
unique_by_size = {}
for f in files:
    sz = os.path.getsize(f)
    if sz not in unique_by_size:
        unique_by_size[sz] = f

def remove_accents(text: str) -> str:
    text = unicodedata.normalize('NFD', str(text))
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower().replace('đ', 'd').strip()

# Common abbreviations & OCR patterns
TAC_PATTERNS = {
    "doat hon": "Đoạt Hồn Hiệp Phách",
    "hiep phach": "Đoạt Hồn Hiệp Phách",
    "bat mon": "Bát Môn Kim Tỏa Trận",
    "phong thi": "Phong Thỉ Trận",
    "phong tro": "Phong Trợ Hỏa Thế",
    "tri ke": "Trí Kế",
    "danh dau thang do": "Đánh Đâu Thắng Đó",
    "thinh khi": "Thịnh Khí Lăng Địch",
    "gio tap": "Gió Táp Mưa Sa",
    "thoi phong": "Thôi Phong Đoạn Nhẫn",
    "quy than": "Quỷ Thần Đình Uy",
    "duong phong": "Đương Phong Thôi Quyết",
    "bach ma": "Bạch Mã Nghĩa Tòng",
    "me hoac": "Mê Hoặc",
    "van vo": "Văn Võ Song Toàn",
    "binh vo": "Binh Vô Thường Thế",
    "ham tran": "Hãm Trận Doanh",
    "ho bao": "Hổ Báo Kỵ",
    "tu dien": "Tứ Diện Sở Ca",
    "mau gianh": "Mau Giành Lợi Thế",
    "van quan": "Vạn Quân Đoạt Soái",
    "lac phuong": "Lạc Phượng",
    "xuat ky": "Xuất Kì Bất Ý",
    "phong thanh": "Phong Thanh Hạc Lệ",
    "thien ly": "Thiên Lý Trì Viện",
    "toa thu": "Tọa Thủ Cô Thành",
    "khinh dung": "Khinh Dũng Phi Yến",
    "tinh hoa": "Tịnh Hóa",
    "xua duoi": "Xua Đuổi",
    "the cam quyen": "Ỷ Thế Cầm Quyền",
    "yeu thuat": "Yêu Thuật",
    "nhat cu": "Nhất Cử Tiệm Diệt",
    "bat nhuc": "Bất Nhục Sứ Mệnh",
    "am tang": "Ám Tàng Huyền Cơ",
    "tra hang": "Trá Hàng",
    "ti thuc": "Tị Thực Kích Hư",
    "tu lanh": "Tự Lành",
    "kieu kien": "Kiêu Kiện Thần Hành",
    "thi chi bat di": "Thi Chí Bất Di",
    "than thuong su": "Thần Thượng Sứ",
    "lu giang": "Lư Giang Thượng Giáp",
    "muu luoc": "Mưu Lược Tung Hoành"
}

all_detected_tactics = set()
for sz, f in unique_by_size.items():
    res, _ = engine(f)
    if res:
        lines = [line[1] for line in res]
        full_norm = " ".join([remove_accents(l) for l in lines])
        found_in_img = set()
        for pat, canon in TAC_PATTERNS.items():
            if pat in full_norm:
                found_in_img.add(canon)
                all_detected_tactics.add(canon)
        if found_in_img:
            print(f"{os.path.basename(f)}: {sorted(list(found_in_img))}")

print(f"\nTOTAL DISTINCT TACTICS RECOGNIZED: {len(all_detected_tactics)}")
print(sorted(list(all_detected_tactics)))
