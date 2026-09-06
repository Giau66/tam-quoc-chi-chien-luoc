# -*- coding: utf-8 -*-
"""
Recommender Engine for Tam Quoc Chi - Chien Luoc.
v3.0 - AI-Enhanced Scoring: synergy bonus, faction purity, role coverage, farm suggestions.
"""
import json
import os
import re
import unicodedata
from typing import List, Dict, Any, Set, Tuple, Optional

# Tactic synonyms / translation variations mapping
TAC_ALIASES = {
    # Damage reduction / heal
    "an ui quan dan": "Quân Dân Khích Lệ",
    "an ủi quân dân": "Quân Dân Khích Lệ",
    "quan dan khich le": "Quân Dân Khích Lệ",
    "quân dân khích lệ": "Quân Dân Khích Lệ",
    "quan dan": "Quân Dân Khích Lệ",
    "quân dân": "Quân Dân Khích Lệ",
    "thuyen co muon ten": "Thảo Thuyền Mượn Tên",
    "thuyền cỏ mượn tên": "Thảo Thuyền Mượn Tên",
    "thao thuyen muon ten": "Thảo Thuyền Mượn Tên",
    "thảo thuyền mượn tên": "Thảo Thuyền Mượn Tên",
    "thao thuyen": "Thảo Thuyền Mượn Tên",
    "thảo thuyền": "Thảo Thuyền Mượn Tên",
    "tam lanh song gio": "Tạm Thời Tránh Mũi Nhọn",
    "tạm lánh sóng gió": "Tạm Thời Tránh Mũi Nhọn",
    "tam thoi tranh mui nhon": "Tạm Thời Tránh Mũi Nhọn",
    "tạm thời tránh mũi nhọn": "Tạm Thời Tránh Mũi Nhọn",
    "tam tranh mui nhon": "Tạm Thời Tránh Mũi Nhọn",
    "tạm tránh mũi nhọn": "Tạm Thời Tránh Mũi Nhọn",
    "linh giap may": "Đằng Giáp Binh",
    "lính giáp mây": "Đằng Giáp Binh",
    "dang giap binh": "Đằng Giáp Binh",
    "đằng giáp binh": "Đằng Giáp Binh",
    "bat mon kim toa tran": "Bát Môn Kim Tỏa Trận",
    "bát môn kim tọa trận": "Bát Môn Kim Tỏa Trận",
    "bát môn kim tỏa trận": "Bát Môn Kim Tỏa Trận",
    "bat mon": "Bát Môn Kim Tỏa Trận",
    "bát môn": "Bát Môn Kim Tỏa Trận",
    "phong thi tran": "Phong Thỉ Trận",
    "phong thi trận": "Phong Thỉ Trận",
    "phong thỉ trận": "Phong Thỉ Trận",
    "phong thị trận": "Phong Thỉ Trận",
    "cao xuong tri doc": "Cắt Xương Trị Độc",
    "cạo xương trị độc": "Cắt Xương Trị Độc",
    "cat xuong tri doc": "Cắt Xương Trị Độc",
    "cắt xương trị độc": "Cắt Xương Trị Độc",
    "cho doi xuat phat": "Chờ Đợi Xuất Phát",
    "chờ đời xuất phát": "Chờ Đợi Xuất Phát",
    "chờ đợi xuất phát": "Chờ Đợi Xuất Phát",
    "duong suc doi chien": "Chờ Đợi Xuất Phát",
    "dưỡng sức đợi chiến": "Chờ Đợi Xuất Phát",
    "tiem long tran": "Tiềm Long Trận",
    "tiềm long trần": "Tiềm Long Trận",
    "tiềm long trận": "Tiềm Long Trận",
    "dung vo thong than": "Dụng Võ Thần Thông",
    "dùng võ thông thần": "Dụng Võ Thần Thông",
    "dụng võ thần thông": "Dụng Võ Thần Thông",
    "hoanh tao thien quan": "Hoành Tảo Thiên Quân",
    "hoành tào thiên quân": "Hoành Tảo Thiên Quân",
    "hoành tảo thiên quân": "Hoành Tảo Thiên Quân",
    "loa y huyet chien": "Lõa Y Huyết Chiến",
    "lõa y huyết chiến": "Lõa Y Huyết Chiến",
    "khoa y huyet chien": "Lõa Y Huyết Chiến",
    "khỏa y huyết chiến": "Lõa Y Huyết Chiến",
    "duong phong thoi quyet": "Đương Phong Thôi Quyết",
    "đương phong thôi quyết": "Đương Phong Thôi Quyết",
    "đương phong tồi quyết": "Đương Phong Thôi Quyết",
    "lac phung": "Lạc Phượng",
    "lạc phụng": "Lạc Phượng",
    "lạc phượng": "Lạc Phượng",
    "bach nhi binh": "Bạch Nhị Binh",
    "bạch nhi binh": "Bạch Nhị Binh",
    "bạch nhị binh": "Bạch Nhị Binh",
    "tinh linh dan duong": "Lính Đan Dương",
    "lính đan dương": "Lính Đan Dương",
    "tinh linh thanh chau": "Lính Thanh Châu",
    "lính thanh châu": "Lính Thanh Châu",
    "tinh ho bao ky": "Hổ Báo Kỵ",
    "hổ báo kỵ": "Hổ Báo Kỵ",
    "tinh phi hung quan": "Phi Hùng Quân",
    "phi hùng quân": "Phi Hùng Quân",
    "tinh tu si tien phong": "Tử Sĩ Tiên Phong",
    "tử sĩ tiên phong": "Tử Sĩ Tiên Phong",
    "tinh giai phien ve": "Giải Phiền Vệ",
    "giải phiền vệ": "Giải Phiền Vệ",
    "thinh khi linh dich": "Thịnh Khí Lăng Địch",
    "thịnh khí linh địch": "Thịnh Khí Lăng Địch",
    "thinh khi lang dich": "Thịnh Khí Lăng Địch",
    "thịnh khí lăng địch": "Thịnh Khí Lăng Địch",
    "thinh khi": "Thịnh Khí Lăng Địch",
    "thịnh khí": "Thịnh Khí Lăng Địch",
    "pha quan uy thang": "Phá Quân Uy Thắng",
    "phá quân uy thắng": "Phá Quân Uy Thắng",
    "pha quan uy thang": "Phá Quân Uy Thắng",
    "phá quân uy thăng": "Phá Quân Uy Thắng",
    "danh bai quan dich": "Đánh Bại Quân Địch",
    "đánh bại quân địch": "Đánh Bại Quân Địch",
    "be gay mui nhon": "Đánh Bại Quân Địch",
    "bẻ gãy mũi nhọn": "Đánh Bại Quân Địch",
    "chiet xung ngu vu": "Đánh Bại Quân Địch",
    "chiết xung ngự vũ": "Đánh Bại Quân Địch",
    "mau gianh loi the": "Mau Giành Lợi Thế",
    "mau giành lợi thế": "Mau Giành Lợi Thế",
    "toc thua ky kiet": "Mau Giành Lợi Thế",
    "tốc thừa kỳ kiệt": "Mau Giành Lợi Thế",
    "so huong phi me": "Đánh Đâu Thắng Đó",
    "sở hướng phi mễ": "Đánh Đâu Thắng Đó",
    "danh dau thang do": "Đánh Đâu Thắng Đó",
    "đánh đâu thắng đó": "Đánh Đâu Thắng Đó",
    "thai binh dao phap": "Thái Bình Đạo Pháp",
    "thái bình đạo pháp": "Thái Bình Đạo Pháp",
    "thai binh": "Thái Bình Đạo Pháp",
    "thái bình": "Thái Bình Đạo Pháp",
    "si biet tam nhat": "Sĩ Biệt Tam Nhật",
    "sĩ biệt tam nhật": "Sĩ Biệt Tam Nhật",
    "si biet": "Sĩ Biệt Tam Nhật",
    "sĩ biệt": "Sĩ Biệt Tam Nhật",
    "doat hon hiep phach": "Đoạt Hồn Hiệp Phách",
    "đoạt hồn hiệp phách": "Đoạt Hồn Hiệp Phách",
    "doat hon": "Đoạt Hồn Hiệp Phách",
    "đoạt hồn": "Đoạt Hồn Hiệp Phách",
    "tam the tran": "Tam Thế Trận",
    "tam thế trận": "Tam Thế Trận",
    "bach ma nghia tong": "Bạch Mã Nghĩa Tòng",
    "bạch mã nghĩa tòng": "Bạch Mã Nghĩa Tòng",
    "bach ma": "Bạch Mã Nghĩa Tòng",
    "bạch mã": "Bạch Mã Nghĩa Tòng",
    "vo dang phi quan": "Vô Đương Phi Quân",
    "vô đang phi quân": "Vô Đương Phi Quân",
    "vo duong phi quan": "Vô Đương Phi Quân",
    "vô đương phi quân": "Vô Đương Phi Quân",
    "ham tran doanh": "Hãm Trận Doanh",
    "hãm trận doanh": "Hãm Trận Doanh",
    "linh ham tran": "Hãm Trận Doanh",
    "lính hãm trận": "Hãm Trận Doanh",
    "ngu dich binh chuong": "Ngự Địch Bình Chướng",
    "ngự địch bình chướng": "Ngự Địch Bình Chướng",
    "ngu dich": "Ngự Địch Bình Chướng",
    "ngự địch": "Ngự Địch Bình Chướng",
    "cu thuy doan kieu": "Cứ Thủy Đoạn Kiều",
    "cứ thủy đoạn kiều": "Cứ Thủy Đoạn Kiều",
    "nhanh chan tranh dat": "Nhanh Chân Tranh Đất",
    "nhanh chân tranh đất": "Nhanh Chân Tranh Đất",
    "thoi phong doan nhan": "Thôi Phong Đoạn Nhẫn",
    "thôi phong đoạn nhẫn": "Thôi Phong Đoạn Nhẫn",
    "dong long hop suc": "Đồng Lòng Hợp Sức",
    "đồng lòng hợp sức": "Đồng Lòng Hợp Sức",
    "thoi co chien thang": "Thời Cơ Chiến Thắng",
    "thời cơ chiến thắng": "Thời Cơ Chiến Thắng",
    "van quyet tinh ke": "Vận Quyết Tính Kế",
    "vận quyết tính kế": "Vận Quyết Tính Kế",
    "van quyet uy thang": "Vận Quyết Tính Kế",
    "vận quyết uy thắng": "Vận Quyết Tính Kế",
    "van quyet tinh ke/van vo": "Vận Quyết Tính Kế",
    "uy muu vo dich": "Uy Mưu Vô Địch",
    "uy mưu vô địch": "Uy Mưu Vô Địch",
    "thiet ky khu tri": "Thiết Kỵ Khu Trì",
    "thiết kỵ khu trì": "Thiết Kỵ Khu Trì",
    "phong tro hoa the": "Phong Trợ Hỏa Thế",
    "phong trợ hỏa thế": "Phong Trợ Hỏa Thế",
    "me hoac": "Mê Hoặc",
    "mê hoặc": "Mê Hoặc"
}

# Tactic substitution dictionary: Maps high-tier tactics to viable A-tier or alternate S-tier equivalents
TACTIC_SUBSTITUTE_GUIDE = {
    # Physical burst / damage active
    "Phá Quân Uy Thắng": ["Tị Thực Kích Hư", "Lạc Phượng", "Bất Nhục Sứ Mệnh", "Đánh Vào Chỗ Đau", "Đánh Vào Chỗ Hiểm", "Nhất Cử Tiệm Diệt", "Ám Tàng Huyền Cơ"],
    "Hoành Tảo Thiên Quân": ["Lạc Phượng", "Bất Nhục Sứ Mệnh", "Đánh Đâu Thắng Đó", "Gió Táp Mưa Sa", "Phấn Đột", "Đánh Vào Chỗ Đau"],
    "Đánh Đâu Thắng Đó": ["Phá Trận Thôi Kiên", "Lạc Phượng", "Bất Nhục Sứ Mệnh", "Nhất Cử Tiệm Diệt", "Đánh Vào Chỗ Đau", "Gió Táp Mưa Sa"],
    "Phá Trận Thôi Kiên": ["Đánh Đâu Thắng Đó", "Lạc Phượng", "Bất Nhục Sứ Mệnh", "Tị Thực Kích Hư", "Đánh Vào Chỗ Hiểm"],
    "Gió Táp Mưa Sa": ["Hoành Tảo Thiên Quân", "Lạc Phượng", "Bất Nhục Sứ Mệnh", "Đánh Đâu Thắng Đó", "Phấn Đột"],
    "Cứ Thủy Đoạn Kiều": ["Lạc Phượng", "Bất Nhục Sứ Mệnh", "Tị Thực Kích Hư", "Phấn Đột", "Đánh Vào Chỗ Đau"],
    "Xế Đao Chước Địch": ["Phá Trận Thôi Kiên", "Tị Thực Kích Hư", "Bất Nhục Sứ Mệnh", "Lạc Phượng"],
    "Trung Dũng Nghĩa Liệt": ["Phấn Đột", "Tài Khí Quá Nhân", "Bất Nhục Sứ Mệnh"],
    "Cưỡi Ngựa Nghìn Dặm": ["Bách Kỵ Kiếp Doanh", "Lõa Y Huyết Chiến", "Bất Nhục Sứ Mệnh", "Phấn Đột"],

    # Normal Attack / Combo / Pursuit (Đột kích)
    "Đánh Bại Quân Địch": ["Ám Tàng Huyền Cơ", "Bạo Lệ Vô Nhân", "Mau Giành Lợi Thế", "Thôi Phong Đoạn Nhẫn", "Thi Chí Bất Di", "Phấn Đột"],
    "Mau Giành Lợi Thế": ["Ám Tàng Huyền Cơ", "Bạo Lệ Vô Nhân", "Thôi Phong Đoạn Nhẫn", "Đánh Bại Quân Địch", "Bách Kỵ Kiếp Doanh", "Thi Chí Bất Di"],
    "Bách Kỵ Kiếp Doanh": ["Ám Tàng Huyền Cơ", "Bạo Lệ Vô Nhân", "Nhất Kỵ Đương Thiên", "Mau Giành Lợi Thế", "Thôi Phong Đoạn Nhẫn"],
    "Nhất Kỵ Đương Thiên": ["Bách Kỵ Kiếp Doanh", "Bạo Lệ Vô Nhân", "Ám Tàng Huyền Cơ", "Mau Giành Lợi Thế"],
    "Bạo Lệ Vô Nhân": ["Ám Tàng Huyền Cơ", "Mau Giành Lợi Thế", "Bách Kỵ Kiếp Doanh", "Thôi Phong Đoạn Nhẫn", "Bất Nhục Sứ Mệnh"],
    "Đương Phong Thôi Quyết": ["Binh Vô Thường Thế", "Ám Tàng Huyền Cơ", "Bạo Lệ Vô Nhân", "Mau Giành Lợi Thế"],
    "Thôi Phong Đoạn Nhẫn": ["Mau Giành Lợi Thế", "Bạo Lệ Vô Nhân", "Ám Tàng Huyền Cơ", "Bách Kỵ Kiếp Doanh", "Thi Chí Bất Di"],
    "Lõa Y Huyết Chiến": ["Cường Dũng", "Phấn Đột", "Thi Chí Bất Di"],

    # Intellect / Magic Active & Passive
    "Thái Bình Đạo Pháp": ["Mưu Lược Tung Hoành", "Yêu Thuật", "Thần Thượng Sứ", "Lạc Lôi", "Bạch Mi"],
    "Sĩ Biệt Tam Nhật": ["Văn Võ Song Toàn", "Mưu Lược Tung Hoành", "Yêu Thuật", "Thần Thượng Sứ", "Dụng Võ Thần Thông"],
    "Dụng Võ Thần Thông": ["Sĩ Biệt Tam Nhật", "Mưu Lược Tung Hoành", "Yêu Thuật", "Thần Thượng Sứ"],
    "Đoạt Hồn Hiệp Phách": ["Trí Kế", "Lạc Lôi", "Mưu Lược Tung Hoành", "Yêu Thuật"],
    "Sợ Bóng Sợ Gió": ["Mưu Lược Tung Hoành", "Yêu Thuật", "Thần Thượng Sứ", "Lạc Lôi", "Phong Trợ Hỏa Thế"],
    "Phong Trợ Hỏa Thế": ["Mưu Lược Tung Hoành", "Yêu Thuật", "Lửa Cháy Đồng Nội", "Thần Thượng Sứ"],
    "Thượng Binh Phạt Mưu": ["Sợ Bóng Sợ Gió", "Mưu Lược Tung Hoành", "Yêu Thuật", "Lạc Lôi"],
    "Binh Vô Thường Thế": ["Văn Võ Song Toàn", "Tự Lành", "Mưu Lược Tung Hoành"],
    "Cốc Thần Tinh": ["Mưu Lược Tung Hoành", "Yêu Thuật", "Thần Thượng Sứ"],

    # Defense / Heal / Damage Reduction
    "Quân Dân Khích Lệ": ["Ngự Địch Bình Chướng", "Tạm Thời Tránh Mũi Nhọn", "Lư Giang Thượng Giáp", "Tự Lành", "Trá Hàng"],
    "Tạm Thời Tránh Mũi Nhọn": ["Ngự Địch Bình Chướng", "Quân Dân Khích Lệ", "Lư Giang Thượng Giáp", "Tự Lành", "Trá Hàng"],
    "Thảo Thuyền Mượn Tên": ["Cắt Xương Trị Độc", "Tịnh Hóa", "Ngự Địch Bình Chướng", "Tự Lành", "Trá Hàng"],
    "Cắt Xương Trị Độc": ["Thảo Thuyền Mượn Tên", "Tịnh Hóa", "Tự Lành", "Trá Hàng", "Ngự Địch Bình Chướng"],
    "Chờ Đợi Xuất Phát": ["Cắt Xương Trị Độc", "Tự Lành", "Ngự Địch Bình Chướng", "Trá Hàng"],
    "Bát Môn Kim Tỏa Trận": ["Ngự Địch Bình Chướng", "Tạm Thời Tránh Mũi Nhọn", "Lạc Phượng"],
    "Thịnh Khí Lăng Địch": ["Ngự Địch Bình Chướng", "Xuất Kì Bất Ý", "Lạc Phượng", "Bất Nhục Sứ Mệnh"],
    "Phong Thỉ Trận": ["Tiềm Long Trận", "Tam Thế Trận", "Ngự Địch Bình Chướng"],
    "Tiềm Long Trận": ["Phong Thỉ Trận", "Tam Thế Trận", "Vũ Phong Trận", "Ngự Địch Bình Chướng"],
    "Tam Thế Trận": ["Tiềm Long Trận", "Phong Thỉ Trận", "Vũ Phong Trận", "Ngự Địch Bình Chướng"],
    "Đằng Giáp Binh": ["Hãm Trận Doanh", "Ngự Địch Bình Chướng"],
    "Hãm Trận Doanh": ["Đằng Giáp Binh", "Ngự Địch Bình Chướng", "Tự Lành"],
    "Vô Đương Phi Quân": ["Bạch Mã Nghĩa Tòng", "Mưu Lược Tung Hoành", "Yêu Thuật"],
    "Bạch Mã Nghĩa Tòng": ["Vô Đương Phi Quân", "Ngự Địch Bình Chướng", "Tị Thực Kích Hư"],
    "Hổ Báo Kỵ": ["Tây Lương Thiết Kỵ", "Ngự Địch Bình Chướng"],
    "Tây Lương Thiết Kỵ": ["Hổ Báo Kỵ", "Ngự Địch Bình Chướng"],
    "Lính Thanh Châu": ["Đại Kích Sĩ", "Ngự Địch Bình Chướng"]
}

GEN_ALIASES = {
    "lục tốṇ": "Lục Tốn",
    "giả hư": "Giả Hủ",
    "gia hu": "Giả Hủ",
    "giả hu": "Giả Hủ",
    "gia ho": "Giả Hủ",
    "giả hủ": "Giả Hủ",
    "thào tháo": "Tào Tháo",
    "lăm thống": "Lăng Thống",
    "sp quãn vũ": "SP Quan Vũ",
    "sp quan vu": "SP Quan Vũ",
    "spđổng trác": "SP Đổng Trác",
    "sp dong trac": "SP Đổng Trác",
    "bái sư hứa du": "Hứa Du",
    "bái sư lỗ túc": "Lỗ Túc",
    "bái sư pháp chính": "Pháp Chính",
    "bái sư sp tuân úc": "SP Tuân Úc",
    "lữ bố 40th": "Lữ Bố",
    "co tinh thái": "Trương Tinh Thái",
    "tinh thái": "Trương Tinh Thái",
    "trương tinh thái": "Trương Tinh Thái",
    "co đại kiều": "Đại Kiều",
    "co tiểu kiều": "Tiểu Kiều",
    "lữ linh khởi": "Lữ Linh Khởi",
    "lữ linh ỷ": "Lữ Linh Khởi",
    "lu linh y": "Lữ Linh Khởi",
    "lu linh khoi": "Lữ Linh Khởi",
    "thái sử từ": "Thái Sử Từ",
    "thai su tu": "Thái Sử Từ",
    "thái sừ tử": "Thái Sử Từ",
    "chu thái": "Chu Thái",
    "chu thai": "Chu Thái",
    "cam ninh": "Cam Ninh",
    "tôn thượng hương": "Tôn Thượng Hương",
    "ton thuong huong": "Tôn Thượng Hương",
    "tôn thương hương": "Tôn Thượng Hương",
    "tà tử": "Tả Từ",
    "ta tu": "Tả Từ",
    "tả từ": "Tả Từ",
    "điểm vi": "Điển Vi",
    "điển vi": "Điển Vi",
    "dien vi": "Điển Vi",
    "vũ cát": "Vu Cát",
    "vu cát": "Vu Cát",
    "vu cat": "Vu Cát",
    "sp viên thiẹu": "SP Viên Thiệu"
}

# ─────────────────────────────────────────────────────────────
# SYNERGY: Tổ hợp tướng → chiến pháp lý tưởng (BIS role match)
# ─────────────────────────────────────────────────────────────
# Maps tướng main → list chiến pháp có synergy cao
GEN_SYNERGY_TACTICS = {
    "Tào Tháo":     ["Hoành Tảo Thiên Quân", "Đánh Bại Quân Địch", "Mau Giành Lợi Thế"],
    "Tư Mã Ý":      ["Sĩ Biệt Tam Nhật", "Binh Vô Thường Thế", "Thượng Binh Phạt Mưu"],
    "Quách Gia":    ["Sợ Bóng Sợ Gió", "Thượng Binh Phạt Mưu", "Mê Hoặc"],
    "Gia Cát Lượng":["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật", "Binh Vô Thường Thế"],
    "Quan Vũ":      ["Bạch Mã Nghĩa Tòng", "Vô Đương Phi Quân", "Cưỡi Ngựa Nghìn Dặm"],
    "Lưu Bị":       ["Quân Dân Khích Lệ", "Đồng Lòng Hợp Sức", "Thịnh Khí Lăng Địch"],
    "Triệu Vân":    ["Phá Quân Uy Thắng", "Đánh Đâu Thắng Đó", "Cưỡi Ngựa Nghìn Dặm"],
    "Trương Phi":   ["Lõa Y Huyết Chiến", "Phá Quân Uy Thắng", "Đánh Đâu Thắng Đó"],
    "Lữ Bố":        ["Hoành Tảo Thiên Quân", "Phá Quân Uy Thắng", "Đánh Đâu Thắng Đó"],
    "Chu Du":       ["Phong Trợ Hỏa Thế", "Thái Bình Đạo Pháp", "Lửa Cháy Đồng Nội"],
    "Lục Tốn":      ["Phong Trợ Hỏa Thế", "Sợ Bóng Sợ Gió", "Binh Vô Thường Thế"],
    "Tôn Quyền":    ["Thịnh Khí Lăng Địch", "Đồng Lòng Hợp Sức", "Quân Dân Khích Lệ"],
    "Cam Ninh":     ["Bách Kỵ Kiếp Doanh", "Nhất Kỵ Đương Thiên", "Mau Giành Lợi Thế"],
    "SP Quan Vũ":   ["Bạch Mã Nghĩa Tòng", "Phá Quân Uy Thắng", "Hoành Tảo Thiên Quân"],
    "Trương Liêu":  ["Đánh Bại Quân Địch", "Bách Kỵ Kiếp Doanh", "Hoành Tảo Thiên Quân"],
    "Hứa Chử":      ["Lõa Y Huyết Chiến", "Đánh Bại Quân Địch", "Hoành Tảo Thiên Quân"],
    "Mã Siêu":      ["Thiết Kỵ Khu Trì", "Hổ Báo Kỵ", "Phá Quân Uy Thắng"],
    "Hoàng Trung":  ["Phá Quân Uy Thắng", "Gió Táp Mưa Sa", "Đánh Đâu Thắng Đó"],
    "Viên Thiệu":   ["Thịnh Khí Lăng Địch", "Bát Môn Kim Tỏa Trận", "Quân Dân Khích Lệ"],
    "Trương Giác":  ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật", "Dụng Võ Thần Thông"],
}

# Tactic role categories for coverage analysis
TACTIC_ROLES = {
    "damage": {
        "Hoành Tảo Thiên Quân", "Phá Quân Uy Thắng", "Đánh Đâu Thắng Đó",
        "Phá Trận Thôi Kiên", "Gió Táp Mưa Sa", "Cứ Thủy Đoạn Kiều",
        "Xế Đao Chước Địch", "Cưỡi Ngựa Nghìn Dặm", "Trung Dũng Nghĩa Liệt",
        "Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật", "Dụng Võ Thần Thông",
        "Đoạt Hồn Hiệp Phách", "Phong Trợ Hỏa Thế", "Sợ Bóng Sợ Gió",
        "Thượng Binh Phạt Mưu", "Lõa Y Huyết Chiến", "Binh Vô Thường Thế"
    },
    "pursuit": {
        "Đánh Bại Quân Địch", "Mau Giành Lợi Thế", "Bách Kỵ Kiếp Doanh",
        "Nhất Kỵ Đương Thiên", "Bạo Lệ Vô Nhân", "Đương Phong Thôi Quyết",
        "Thôi Phong Đoạn Nhẫn"
    },
    "defense": {
        "Quân Dân Khích Lệ", "Tạm Thời Tránh Mũi Nhọn", "Thảo Thuyền Mượn Tên",
        "Cắt Xương Trị Độc", "Chờ Đợi Xuất Phát", "Ngự Địch Bình Chướng",
        "Bát Môn Kim Tỏa Trận", "Thịnh Khí Lăng Địch", "Phong Thỉ Trận",
        "Tiềm Long Trận", "Tam Thế Trận", "Đằng Giáp Binh", "Hãm Trận Doanh",
        "Tự Lành", "Trá Hàng", "Tịnh Hóa"
    },
    "troop": {
        "Vô Đương Phi Quân", "Bạch Mã Nghĩa Tòng", "Hổ Báo Kỵ",
        "Tây Lương Thiết Kỵ", "Lính Thanh Châu", "Lính Đan Dương",
        "Bạch Nhị Binh", "Tử Sĩ Tiên Phong", "Giải Phiền Vệ",
        "Phi Hùng Quân", "Đại Kích Sĩ", "Thiết Kỵ Khu Trì"
    }
}

# Farm difficulty map: How hard is it to get a general (affects farm suggestion priority)
GEN_FARM_DIFFICULTY = {
    # Tướng T0 khó farm nhất
    "Lữ Bố": 5, "Tào Tháo": 5, "Gia Cát Lượng": 5, "Quan Vũ": 5,
    "SP Quan Vũ": 5, "Tư Mã Ý": 5, "SP Đổng Trác": 5, "SP Tuân Úc": 5,
    # T1 trung bình
    "Triệu Vân": 4, "Chu Du": 4, "Lục Tốn": 4, "Trương Phi": 4,
    "Mã Siêu": 4, "Hoàng Trung": 4, "Cam Ninh": 4, "Trương Liêu": 4,
    "Hứa Chử": 4, "Tôn Quyền": 3, "Lưu Bị": 3, "Viên Thiệu": 3,
    "Trương Giác": 3, "Quách Gia": 4, "Lỗ Túc": 3, "Pháp Chính": 4,
    # Tướng dễ farm hơn
    "Hứa Du": 2, "Lữ Linh Ỷ": 2, "Thái Sử Từ": 2, "Chu Thái": 2,
}

def remove_accents(text: str) -> str:
    text = unicodedata.normalize('NFD', str(text))
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower().replace('đ', 'd').strip()

class TeamRecommender:
    def __init__(self, db_dir: str = None):
        if db_dir is None:
            db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
        
        with open(os.path.join(db_dir, "generals.json"), "r", encoding="utf-8") as f:
            self.generals = json.load(f)
            self.general_map = {g["id"]: g for g in self.generals}
            self.general_name_map = {g["name"].lower(): g for g in self.generals}
            self.general_norm_map = {remove_accents(g["name"]): g for g in self.generals}
            
        with open(os.path.join(db_dir, "tactics.json"), "r", encoding="utf-8") as f:
            self.tactics = json.load(f)
            self.tactic_map = {t["id"]: t for t in self.tactics}
            self.tactic_name_map = {t["name"].lower(): t for t in self.tactics}
            self.tactic_norm_map = {remove_accents(t["name"]): t for t in self.tactics}
            
        with open(os.path.join(db_dir, "meta_teams.json"), "r", encoding="utf-8") as f:
            self.meta_teams = json.load(f)

        port_file = os.path.join(db_dir, "coexisting_portfolios.json")
        if os.path.exists(port_file):
            with open(port_file, "r", encoding="utf-8") as f:
                self.coexisting_portfolios = json.load(f)
        else:
            self.coexisting_portfolios = []

        starter_file = os.path.join(db_dir, "starter_teams.json")
        if os.path.exists(starter_file):
            with open(starter_file, "r", encoding="utf-8") as f:
                self.starter_data = json.load(f)
        else:
            self.starter_data = {"starter_teams": [], "touch_scout_teams": [], "mines_guide": {}}

    def canonical_tactic(self, name: str) -> str:
        """Resolve tactic synonym or variation to canonical name."""
        if not name:
            return ""
        name_clean = name.strip()
        name_lower = name_clean.lower()
        if name_lower in TAC_ALIASES:
            return TAC_ALIASES[name_lower]
        norm = remove_accents(name_clean)
        if norm in TAC_ALIASES:
            return TAC_ALIASES[norm]
        if norm in self.tactic_norm_map:
            return self.tactic_norm_map[norm]["name"]
        if name_clean in self.tactic_map:
            return self.tactic_map[name_clean]["name"]
        return name_clean

    def canonical_general(self, name: str) -> str:
        """Resolve general name or alias to canonical name."""
        if not name:
            return ""
        name_clean = name.strip()
        name_lower = name_clean.lower()
        if name_lower in GEN_ALIASES:
            return GEN_ALIASES[name_lower]
        norm = remove_accents(name_clean)
        if norm in self.general_norm_map:
            return self.general_norm_map[norm]["name"]
        return name_clean

    def normalize_owned_generals(self, owned_generals: List[str]) -> Set[str]:
        """Convert list of names or IDs to set of canonical general IDs and name variations."""
        normalized = set()
        CROSS_ID_MAP = {
            "Giả Hủ": ["nguy_gia_hu", "quan_gia_hu"],
            "Lỗ Túc": ["ngo_lo_tuc", "quan_lo_tuc"],
            "Tả Từ": ["quan_ta_tu"],
            "Thái Sử Từ": ["ngo_thai_su_tu", "quan_thai_su_tu"],
            "Tôn Thượng Hương": ["ngo_ton_thuong_huong", "quan_ton_thuong_huong"],
            "Điển Vi": ["nguy_dien_vi", "quan_diem_vi"],
            "Từ Hoảng": ["nguy_tu_hoang", "quan_tu_hoang"],
            "Nhạc Tiến": ["nguy_nhac_tien", "quan_nhac_tien"],
            "Lữ Linh Khởi": ["quan_lu_linh_khoi", "quan_lu_linh_y"],
        }
        for item in owned_generals:
            if not item:
                continue
            item_clean = item.strip()
            item_lower = item_clean.lower()
            canon_name = self.canonical_general(item_clean)
            norm = remove_accents(item_clean)

            # Always add raw, lower, norm, canon
            normalized.add(item_clean)
            normalized.add(item_lower)
            normalized.add(norm)
            if canon_name:
                normalized.add(canon_name)
                normalized.add(canon_name.lower())
                normalized.add(remove_accents(canon_name))
                if canon_name in CROSS_ID_MAP:
                    normalized.update(CROSS_ID_MAP[canon_name])

            if item_clean in self.general_map:
                normalized.add(item_clean)
                gen_name = self.general_map[item_clean].get("name", "")
                if gen_name:
                    normalized.add(gen_name)
                    normalized.add(gen_name.lower())
                    if gen_name in CROSS_ID_MAP:
                        normalized.update(CROSS_ID_MAP[gen_name])
            elif canon_name.lower() in self.general_name_map:
                gid = self.general_name_map[canon_name.lower()]["id"]
                normalized.add(gid)
            elif item_lower in self.general_name_map:
                gid = self.general_name_map[item_lower]["id"]
                normalized.add(gid)
            elif norm in self.general_norm_map:
                gid = self.general_norm_map[norm]["id"]
                normalized.add(gid)

        return normalized

    def normalize_owned_tactics(self, owned_tactics: List[str]) -> Set[str]:
        """Convert list of tactic names or IDs to set of canonical tactic names."""
        normalized = set()
        for item in owned_tactics:
            item_clean = item.strip()
            canon_name = self.canonical_tactic(item_clean)
            if canon_name in self.tactic_name_map or canon_name in [t["name"] for t in self.tactics]:
                normalized.add(canon_name)
            else:
                normalized.add(item_clean)
        return normalized

    # ─────────────────────────────────────────────────────────
    # SMART SCORING HELPERS
    # ─────────────────────────────────────────────────────────

    def compute_synergy_bonus(self, gen_names: List[str], tactic_names: List[str]) -> int:
        """Return synergy bonus points (0-15) when owned generals match their ideal tactics."""
        bonus = 0
        for gname in gen_names:
            ideal = GEN_SYNERGY_TACTICS.get(gname, [])
            matches = sum(1 for t in ideal if t in tactic_names)
            bonus += matches * 3  # +3 per synergy tactic
        return min(bonus, 15)

    def compute_faction_purity_bonus(self, gen_ids: List[str]) -> Tuple[int, bool]:
        """Return (bonus_points, is_pure_faction). Pure faction = all 3 from same faction."""
        factions = []
        for gid in gen_ids:
            g = self.general_map.get(gid)
            if g:
                factions.append(g.get("faction", ""))
        if len(set(factions)) == 1 and len(factions) == 3:
            return 8, True
        return 0, False

    def compute_tactic_role_coverage(self, tactic_names: List[str]) -> Dict[str, Any]:
        """Analyze whether the team has balanced tactic roles (damage+defense+pursuit)."""
        covered = {role: False for role in TACTIC_ROLES}
        for role, role_set in TACTIC_ROLES.items():
            if any(t in role_set for t in tactic_names):
                covered[role] = True
        score = sum(1 for v in covered.values() if v)
        return {
            "covered": covered,
            "coverage_score": score,  # 0-4
            "is_balanced": covered["damage"] and covered["defense"]
        }

    def suggest_farm_generals(self, meta_team: Dict[str, Any], owned_gen_ids: Set[str]) -> List[Dict[str, Any]]:
        """For each general the user doesn't own, suggest farming priority."""
        suggestions = []
        for gen_spec in meta_team["generals"]:
            gid = gen_spec["general_id"]
            if gid not in owned_gen_ids:
                difficulty = GEN_FARM_DIFFICULTY.get(gen_spec["name"], 3)
                suggestions.append({
                    "name": gen_spec["name"],
                    "general_id": gid,
                    "difficulty": difficulty,
                    "difficulty_label": ["Rất Dễ", "Dễ", "Trung Bình", "Khó", "Rất Khó", "Cực Khó"][min(difficulty, 5)],
                    "position": gen_spec.get("position", "?")
                })
        suggestions.sort(key=lambda x: x["difficulty"])
        return suggestions

    def evaluate_team(self, meta_team: Dict[str, Any], owned_gen_ids: Set[str], owned_tactic_names: Set[str]) -> Dict[str, Any]:
        """
        Evaluate how well the user can build a specific meta team directly from the Excel reference.
        No artificial tactic replacements: strictly checks if standard generals & tactics are owned.
        Calculates exact match rate (%) against the Excel lineup.
        """
        team_generals_eval = []
        pure_owned_count = 0
        used_generals = []
        used_tactics = []
        total_tactics_count = 0
        matched_tactics_count = 0
        owned_bis_count = 0

        # Pre-normalize owned tactics for fast matching
        canonical_owned_tactics = {self.canonical_tactic(t) for t in owned_tactic_names}
        available_owned_tactics = set(canonical_owned_tactics)

        for gen_spec in meta_team["generals"]:
            target_gen_id = gen_spec["general_id"]
            target_name = gen_spec["name"]
            pos = gen_spec["position"]
            bis_tactics = [self.canonical_tactic(b) for b in gen_spec.get("bis_tactics", [])]

            # Check general ownership comprehensively
            active_gen = self.general_map.get(target_gen_id)
            target_canon = self.canonical_general(target_name)
            target_norm = remove_accents(target_name)
            target_lower = target_name.strip().lower()

            is_owned = False
            if (target_gen_id in owned_gen_ids or
                target_name in owned_gen_ids or
                target_canon in owned_gen_ids or
                target_norm in owned_gen_ids or
                target_lower in owned_gen_ids or
                (active_gen and (active_gen.get("id") in owned_gen_ids or active_gen.get("name") in owned_gen_ids))):
                is_owned = True
                pure_owned_count += 1
                used_generals.append(target_gen_id)

            # Check tactics for this general directly against Excel standard
            tactic_eval = []
            for bis in bis_tactics:
                total_tactics_count += 1
                if bis in available_owned_tactics and bis not in used_tactics:
                    matched_tactics_count += 1
                    owned_bis_count += 1
                    used_tactics.append(bis)
                    available_owned_tactics.discard(bis)
                    tactic_eval.append({
                        "name": bis,
                        "status": "BIS",
                        "status_label": "✓ Có",
                        "is_owned": True,
                        "is_substitute": False
                    })
                else:
                    tactic_eval.append({
                        "name": bis,
                        "status": "MISSING",
                        "status_label": "❌ Thiếu",
                        "is_owned": False,
                        "is_substitute": False,
                        "suggested_subs": []
                    })

            team_generals_eval.append({
                "position": pos,
                "target_name": target_name,
                "target_id": target_gen_id,
                "active_general": active_gen,
                "is_main": is_owned,
                "is_owned": is_owned,
                "is_sub": False,
                "binh_thu": gen_spec.get("binh_thu", []),
                "tactics": tactic_eval,
                "alt_generals_available": []
            })

        # Calculate exact Match Rate (% similarity with Excel lineup)
        # 3 generals (weight 3 each = 9) + total tactics (weight 1 each = 6) = 15 points total
        total_points = (3 * 3) + (total_tactics_count if total_tactics_count > 0 else 6)
        earned_points = (pure_owned_count * 3) + matched_tactics_count
        base_score = round((earned_points / total_points) * 100.0) if total_points > 0 else 0

        gen_score = round((pure_owned_count / 3.0) * 100.0)
        tactic_score = round((matched_tactics_count / total_tactics_count) * 100.0) if total_tactics_count > 0 else 0

        # ── Smart Scoring Additions ──────────────────────────────
        owned_gen_names = [
            self.general_map[gid]["name"] for gid in used_generals
            if gid in self.general_map
        ]
        all_used_tactics = list(canonical_owned_tactics)
        synergy_bonus = self.compute_synergy_bonus(owned_gen_names, all_used_tactics)
        faction_bonus, is_pure_faction = self.compute_faction_purity_bonus(used_generals)
        role_coverage = self.compute_tactic_role_coverage(used_tactics)
        farm_suggestions = self.suggest_farm_generals(meta_team, owned_gen_ids)

        # Overall score includes bonuses (capped at 100)
        overall_score = min(100, base_score + (synergy_bonus // 3) + (faction_bonus // 4))

        if pure_owned_count == 3 and matched_tactics_count == total_tactics_count:
            rating_label = "CHUẨN 100% EXCEL (ĐỦ TƯỚNG & CHIẾN PHÁP)"
            badge_class = "badge-perfect"
        elif pure_owned_count == 3:
            rating_label = f"ĐỦ 3 TƯỚNG (CÓ {matched_tactics_count}/{total_tactics_count} CHIẾN PHÁP CHUẨN)"
            badge_class = "badge-strong"
        elif pure_owned_count == 2:
            rating_label = f"CÓ 2/3 TƯỚNG (CÓ {matched_tactics_count}/{total_tactics_count} CHIẾN PHÁP CHUẨN)"
            badge_class = "badge-viable"
        else:
            rating_label = f"THIẾU TƯỚNG (SỞ HỮU {pure_owned_count}/3 TƯỚNG)"
            badge_class = "badge-lacking"

        return {
            "meta_team": meta_team,
            "overall_score": overall_score,
            "base_score": base_score,
            "gen_score": gen_score,
            "tactic_score": tactic_score,
            "owned_gen_count": pure_owned_count,
            "effective_gen_count": pure_owned_count,
            "owned_bis_count": owned_bis_count,
            "owned_sub_count": 0,
            "total_tactics_count": total_tactics_count,
            "rating_label": rating_label,
            "badge_class": badge_class,
            "generals_eval": team_generals_eval,
            "used_generals": used_generals,
            "used_tactics": used_tactics,
            # ── Smart scoring fields ──
            "synergy_bonus": synergy_bonus,
            "faction_bonus": faction_bonus,
            "is_pure_faction": is_pure_faction,
            "role_coverage": role_coverage,
            "farm_suggestions": farm_suggestions
        }

    def recommend(self, owned_generals: List[str], owned_tactics: List[str],
                  season_filter: str = "All", faction_filter: str = "All",
                  troop_filter: str = "All", min_score: int = 30) -> List[Dict[str, Any]]:
        """
        Returns ranked list of candidate teams based on user's collection.
        STRICT HIERARCHY:
        1. Teams where user owns ALL 3 generals appear first!
        2. Sorted by Match Rate % (highest similarity with Excel lineup).
        3. Teams with 2/3 owned generals appear second.
        4. Excludes teams with < 2 owned generals by default (unless min_score <= 15).
        """
        owned_gen_ids = self.normalize_owned_generals(owned_generals)
        owned_tactic_names = self.normalize_owned_tactics(owned_tactics)

        results = []
        for team in self.meta_teams:
            if season_filter != "All" and team.get("season") != season_filter:
                if season_filter == "S1" and team.get("season") != "S1":
                    continue
                elif season_filter == "S2" and team.get("season") not in ["S1", "S2"]:
                    continue
                elif season_filter == "S3" and team.get("season") not in ["S1", "S2", "S3"]:
                    continue

            if faction_filter != "All" and team.get("faction") != faction_filter:
                continue

            if troop_filter != "All" and team.get("troop") != troop_filter:
                continue

            eval_res = self.evaluate_team(team, owned_gen_ids, owned_tactic_names)

            # FILTER: Must own at least 1 general in the team to recommend
            if eval_res["owned_gen_count"] < 1:
                continue

            if eval_res["overall_score"] >= min_score:
                results.append(eval_res)

        # SORTING HIERARCHY:
        # 1. Full 3/3 Generals Owned ALWAYS FIRST!
        # 2. 2/3 Generals Owned second.
        # 3. Match Rate % (overall_score) DESC (tỉ lệ giống cao nhất)
        # 4. Number of owned standard tactics DESC
        # 5. Meta tier bonus (T0 > T0.5 > T1 > T2)
        tier_order = {"T0": 3, "T0.5": 2, "T1": 1, "T2": 0}

        def sort_key(item):
            is_full_3 = 1 if item["owned_gen_count"] >= 3 else 0
            is_has_2 = 1 if item["owned_gen_count"] >= 2 else 0
            tier_val = tier_order.get(item["meta_team"].get("tier", "T1"), 0)
            return (
                is_full_3,                   # 1. Full 3 generals first
                is_has_2,                   # 2. 2 generals second
                item["overall_score"],      # 3. Highest match rate %
                item["owned_bis_count"],    # 4. Most owned tactics
                item["tactic_score"],       # 5. Tactic completeness
                tier_val                    # 6. Meta tier bonus
            )

        results.sort(key=sort_key, reverse=True)
        return results

    def recommend_starter_teams(self, owned_generals: List[str], owned_tactics: List[str]) -> Dict[str, Any]:
        """
        Evaluate and recommend Starter Teams (Đội hình Khai Hoang) from database/starter_teams.json.
        Returns evaluated starter teams, touch scout teams, and land difficulty guide.
        """
        owned_gen_ids = self.normalize_owned_generals(owned_generals)
        owned_tactic_names = self.normalize_owned_tactics(owned_tactics)
        canon_owned_tactics = {self.canonical_tactic(t) for t in owned_tactic_names}

        starter_teams = self.starter_data.get("starter_teams", [])
        results = []

        for st in starter_teams:
            team_gens = st.get("generals", [])
            evaluated_gens = []
            owned_count = 0
            total_tactics_count = 0
            owned_tactics_count = 0

            for g_spec in team_gens:
                raw_name = g_spec.get("name", "")
                alt_options = [self.canonical_general(p.strip()) for p in raw_name.split("/")]
                
                active_name = None
                is_owned = False
                for opt in alt_options:
                    opt_id = self.general_name_map.get(opt.lower(), {}).get("id")
                    if opt_id and opt_id in owned_gen_ids:
                        active_name = opt
                        is_owned = True
                        break
                    elif opt.lower() in [g.lower() for g in owned_generals]:
                        active_name = opt
                        is_owned = True
                        break

                if is_owned:
                    owned_count += 1
                else:
                    active_name = alt_options[0]

                # Evaluate early tactic (Lv 1 - 19)
                cp_early_raw = g_spec.get("cp_early", "")
                early_options = [self.canonical_tactic(p.strip()) for p in cp_early_raw.split("/")]
                cp_early_name = early_options[0]
                early_owned = any(opt in canon_owned_tactics for opt in early_options)
                total_tactics_count += 1
                if early_owned:
                    owned_tactics_count += 1

                # Evaluate Lv 20 tactics
                lv20_tactics = []
                for cp in g_spec.get("cp_lv20", []):
                    cp_opts = [self.canonical_tactic(p.strip()) for p in cp.split("/")]
                    opt_matched = any(o in canon_owned_tactics for o in cp_opts)
                    total_tactics_count += 1
                    if opt_matched:
                        owned_tactics_count += 1
                    lv20_tactics.append({
                        "name": cp_opts[0],
                        "options": cp_opts,
                        "is_owned": opt_matched
                    })

                evaluated_gens.append({
                    "target_name": raw_name,
                    "active_name": active_name,
                    "is_owned": is_owned,
                    "cp_early": {
                        "name": cp_early_name,
                        "options": early_options,
                        "is_owned": early_owned
                    },
                    "tactics_before_lv20": {
                        "name": cp_early_name,
                        "options": early_options,
                        "is_owned": early_owned
                    },
                    "cp_lv20": lv20_tactics,
                    "tactics_after_lv20": lv20_tactics
                })

            total_gens = len(team_gens)
            gen_pct = (owned_count / total_gens) * 100.0 if total_gens > 0 else 0
            tactic_pct = (owned_tactics_count / total_tactics_count) * 100.0 if total_tactics_count > 0 else 0

            if owned_count == total_gens and tactic_pct >= 70:
                starter_rating = "SẴN SÀNG KHAI HOANG (100%)"
                badge_class = "badge-perfect"
            elif owned_count == total_gens:
                starter_rating = "ĐỦ 3 TƯỚNG MỞ ĐẤT"
                badge_class = "badge-strong"
            elif owned_count == 2:
                starter_rating = "CÓ 2/3 TƯỚNG (CẦN TƯỚNG PHỤ)"
                badge_class = "badge-viable"
            else:
                starter_rating = "THIẾU TƯỚNG KHAI HOANG"
                badge_class = "badge-lacking"

            results.append({
                "id": st.get("id"),
                "troop": st.get("troop"),
                "troop_lv20": st.get("troop_lv20", st.get("troop")),
                "note": st.get("note", ""),
                "starter_note": st.get("note", ""),
                "total_generals": total_gens,
                "owned_generals_count": owned_count,
                "gen_percentage": round(gen_pct),
                "tactic_percentage": round(tactic_pct),
                "starter_rating": starter_rating,
                "badge_class": badge_class,
                "is_ready": (owned_count == total_gens),
                "generals": evaluated_gens
            })

        # Sort: Teams with full generals first, then high general count, then high tactics count
        results.sort(key=lambda x: (
            1 if x["owned_generals_count"] == x["total_generals"] else 0,
            x["owned_generals_count"],
            x["tactic_percentage"],
            x["gen_percentage"]
        ), reverse=True)

        return {
            "starter_teams": results,
            "touch_scout_teams": self.starter_data.get("touch_scout_teams", []),
            "mines_guide": self.starter_data.get("mines_guide", {})
        }

    def build_multi_team_portfolio(self, owned_generals: List[str], owned_tactics: List[str], max_teams: int = 4) -> List[Dict[str, Any]]:
        """
        Finds 2-5 simultaneous active teams that DO NOT share any general or tactic.
        Optimizes overall fighting strength and tier for alliance PVP.
        """
        owned_gen_ids = set(self.normalize_owned_generals(owned_generals))
        owned_tactic_names = set(self.normalize_owned_tactics(owned_tactics))

        portfolio = []
        remaining_gen_ids = set(owned_gen_ids)
        remaining_tactic_names = set(owned_tactic_names)

        tier_rank = {"T0": 100, "T0.5": 80, "T1": 60, "T2": 40}

        while len(portfolio) < max_teams:
            candidates = []
            for team in self.meta_teams:
                if any(p["meta_team"]["id"] == team["id"] for p in portfolio):
                    continue
                
                eval_res = self.evaluate_team(team, remaining_gen_ids, remaining_tactic_names)
                # Only consider teams where user owns AT LEAST 2 generals
                if eval_res["owned_gen_count"] >= 2 and eval_res["overall_score"] >= 45:
                    score = (
                        eval_res["overall_score"] * 1.5 +
                        tier_rank.get(team.get("tier", "T1"), 50) +
                        (200 if eval_res["owned_gen_count"] >= 3 else 50)
                    )
                    candidates.append((score, eval_res))

            if not candidates:
                break

            candidates.sort(key=lambda x: x[0], reverse=True)
            best_score, best_team = candidates[0]
            portfolio.append(best_team)

            # Deduct used generals and tactics
            for gid in best_team["used_generals"]:
                remaining_gen_ids.discard(gid)
            for tname in best_team["used_tactics"]:
                remaining_tactic_names.discard(tname)

        return portfolio
