# -*- coding: utf-8 -*-
"""
Script to generate COMPREHENSIVE database of Generals, Tactics, and Meta Teams
for Tam Quoc Chi - Chien Luoc (Three Kingdoms: Tactics).
Updated with 80+ generals, 60+ tactics, 25+ meta teams (2025 - PK season).
"""
import json
import os

generals_data = [
    # ================================================================
    # THỤC QUỐC (SHU HAN)
    # ================================================================
    {
        "id": "thuc_khuong_duy",
        "name": "Khương Duy",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Nghĩa Đảm Hùng Tâm",
        "role": ["Sát thương hỗn hợp", "Giảm thuộc tính địch", "Khống chế chấn nhiếp"],
        "season": "PK"
    },
    {
        "id": "thuc_bang_thong",
        "name": "Bàng Thống",
        "faction": "Thục",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Liên Hoàn Kế",
        "role": ["Pháp sư nổ dame diện rộng", "Nối xích", "Kích hoạt Thái Bình"],
        "season": "S2"
    },
    {
        "id": "thuc_gia_cat_luong",
        "name": "Gia Cát Lượng",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "B", "Khiên": "B", "Cung": "S", "Thương": "S", "Khí": "A"},
        "inherent_skill": "Thần Cơ Diệu Toán",
        "role": ["Ngắt chiêu chủ động địch", "Phản sát thương phép", "Khống chế"],
        "season": "S1"
    },
    {
        "id": "thuc_sp_gia_cat_luong",
        "name": "SP Gia Cát Lượng",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "S", "Thương": "S", "Khí": "A"},
        "inherent_skill": "Vũ Hầu Xuất Trận",
        "role": ["Hỗ trợ và tấn công lưỡng dụng", "Câm lặng đối phương", "Buff team"],
        "season": "PK"
    },
    {
        "id": "thuc_luu_bi",
        "name": "Lưu Bị",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "S", "Cung": "A", "Thương": "A", "Khí": "B"},
        "inherent_skill": "Nhân Đức Trạch Chúng",
        "role": ["Hồi phục cực mạnh", "Hư nhược địch", "Buffer"],
        "season": "S1"
    },
    {
        "id": "thuc_quan_vu",
        "name": "Quan Vũ",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Uy Chấn Hoa Hạ",
        "role": ["Khống chế diện rộng", "Sát thương vật lý"],
        "season": "S1"
    },
    {
        "id": "thuc_sp_quan_vu",
        "name": "SP Quan Vũ",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Hán Thọ Đình Hầu",
        "role": ["Bạo kích liên kích vật lý", "Buff Võ lực cả đội"],
        "season": "PK"
    },
    {
        "id": "thuc_truong_phi",
        "name": "Trương Phi",
        "faction": "Thục",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "C", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Yểm Nhân Hống",
        "role": ["Giảm giáp địch", "Sát thương ổn định hiệp 2,4"],
        "season": "S1"
    },
    {
        "id": "thuc_trieu_van",
        "name": "Triệu Vân",
        "faction": "Thục",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Nhất Thân Thị Đảm",
        "role": ["Miễn nhiễm khống chế", "Cộng 40-50 mọi thuộc tính"],
        "season": "S1"
    },
    {
        "id": "thuc_quan_ngan_binh",
        "name": "Quan Ngân Bình",
        "faction": "Thục",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Tướng Môn Hổ Nữ",
        "role": ["Chấn nhiếp liên tục", "Kích hoạt chuỗi sát thương"],
        "season": "PK"
    },
    {
        "id": "thuc_hoang_trung",
        "name": "Hoàng Trung",
        "faction": "Thục",
        "cost": 6,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Bách Bộ Xuyên Dương",
        "role": ["Bạo kích vật lý", "Sát thương bất ngờ"],
        "season": "S1"
    },
    {
        "id": "thuc_sp_hoang_trung",
        "name": "SP Hoàng Trung",
        "faction": "Thục",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "A", "Cung": "S", "Thương": "A", "Khí": "B"},
        "inherent_skill": "Liệt Hỏa Thiêu Thương",
        "role": ["Sát thương cung phép kết hợp", "Thiêu đốt"],
        "season": "S3"
    },
    {
        "id": "thuc_ma_sieu",
        "name": "Mã Siêu",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "C", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Tố Y Cấp Huyết",
        "role": ["Đánh lan toàn đội", "Sát thương vật lý"],
        "season": "S1"
    },
    {
        "id": "thuc_sp_ma_sieu",
        "name": "SP Mã Siêu",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "C", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Tây Lương Chiến Thần",
        "role": ["T0 sát thương vật lý bùng nổ", "Hiệp chiến cực khủng", "Phá giáp sâu"],
        "season": "PK"
    },
    {
        "id": "thuc_phap_chinh",
        "name": "Pháp Chính",
        "faction": "Thục",
        "cost": 4,
        "troop": {"Kỵ": "C", "Khiên": "A", "Cung": "S", "Thương": "C", "Khí": "B"},
        "inherent_skill": "Dĩ Dật Đãi Lao",
        "role": ["Hồi máu", "Miễn thương nhiều tầng", "Giải khống"],
        "season": "S1"
    },
    {
        "id": "thuc_sp_phap_chinh",
        "name": "SP Pháp Chính",
        "faction": "Thục",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "A"},
        "inherent_skill": "Kỳ Sách Liên Châu",
        "role": ["Hỗ trợ mưu sĩ", "Kích hoạt chiến pháp phép", "Tăng sát thương mưu trí"],
        "season": "PK"
    },
    {
        "id": "thuc_hoang_nguyet_anh",
        "name": "Hoàng Nguyệt Anh",
        "faction": "Thục",
        "cost": 3,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "C", "Thương": "C", "Khí": "S"},
        "inherent_skill": "Cơ Quan Tiên Nữ",
        "role": ["Tiên phong hiệp đầu", "Tăng sát thương đội tốc chiến"],
        "season": "S1"
    },
    {
        "id": "thuc_nguy_dien",
        "name": "Ngụy Diên",
        "faction": "Thục",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Kỳ Binh Gian Đạo",
        "role": ["Bỏ lượt sạc chiêu chủ động", "Sát thương đột biến"],
        "season": "PK"
    },
    {
        "id": "thuc_truong_bao",
        "name": "Trương Bão",
        "faction": "Thục",
        "cost": 5,
        "troop": {"Kỵ": "A", "Khiên": "A", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Hổ Uy",
        "role": ["Chia sát thương cho đồng minh", "Phản kích"],
        "season": "S1"
    },
    {
        "id": "thuc_luu_phong",
        "name": "Lưu Phong",
        "faction": "Thục",
        "cost": 4,
        "troop": {"Kỵ": "B", "Khiên": "S", "Cung": "B", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Mãnh Quốc Diệt Phong",
        "role": ["Tăng giáp toàn đội", "Đỡ sát thương"],
        "season": "S1"
    },
    {
        "id": "thuc_huang_hao",
        "name": "Hoàng Hạo",
        "faction": "Thục",
        "cost": 3,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "B", "Thương": "C", "Khí": "B"},
        "inherent_skill": "Nịnh Thần Gian Báo",
        "role": ["Trừ sát thương địch", "Hư nhược"],
        "season": "S1"
    },
    {
        "id": "thuc_xu_su",
        "name": "Từ Thứ",
        "faction": "Thục",
        "cost": 5,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "B"},
        "inherent_skill": "Nhất Kế Phá Kỳ Mưu",
        "role": ["Phản chiến pháp địch", "Buff mưu trí"],
        "season": "S1"
    },

    # ================================================================
    # NGỤY QUỐC (CAO WEI)
    # ================================================================
    {
        "id": "nguy_tao_thao",
        "name": "Tào Tháo",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "S", "Cung": "A", "Thương": "A", "Khí": "B"},
        "inherent_skill": "Loạn Thế Gian Hùng",
        "role": ["Buff sát thương đồng đội", "Giảm sát thương nhận vào"],
        "season": "S1"
    },
    {
        "id": "nguy_tu_ma_y",
        "name": "Tư Mã Ý",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "S", "Thương": "A", "Khí": "S"},
        "inherent_skill": "Ưng Thị Lang Cố",
        "role": ["Late-game carry", "Bạo kích pháp thuật hiệp 5-8"],
        "season": "S2"
    },
    {
        "id": "nguy_man_sung",
        "name": "Mãn Sủng",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "B", "Khiên": "S", "Cung": "A", "Thương": "B", "Khí": "A"},
        "inherent_skill": "Trấn Ngạc Nghênh Địch",
        "role": ["Khiêu khích bảo vệ", "Hồi phục liên tục", "Xóa buff địch"],
        "season": "PK"
    },
    {
        "id": "nguy_hac_chieu",
        "name": "Hác Chiêu",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "B", "Khiên": "S", "Cung": "A", "Thương": "B", "Khí": "S"},
        "inherent_skill": "Kim Thành Thang Trì",
        "role": ["Sát thương kép lửa/vật lý", "Hồi phục không sợ câm lặng"],
        "season": "S3"
    },
    {
        "id": "nguy_truong_lieu",
        "name": "Trương Liêu",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "C", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Hãm Trận Tỏa Hướng",
        "role": ["Chuyên trảm chủ tướng", "Đột kích liên hoàn"],
        "season": "S2"
    },
    {
        "id": "nguy_ha_hau_uyen",
        "name": "Hạ Hầu Uyên",
        "faction": "Ngụy",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "S", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Tật Phong Sậu Vũ",
        "role": ["Đột kích tốc độ cao", "Câm lặng tướng địch"],
        "season": "S1"
    },
    {
        "id": "nguy_ha_hau_don",
        "name": "Hạ Hầu Đôn",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Độc Nhãn Cự Ma",
        "role": ["Đỡ đòn bao che", "Tự hồi phục", "Kích hoạt phản đòn"],
        "season": "S1"
    },
    {
        "id": "nguy_gia_hu",
        "name": "Giả Hủ",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Thần Cơ Mạc Trắc",
        "role": ["Hỗn loạn cực đoan", "Giải hiệu ứng xấu cho đội"],
        "season": "S3"
    },
    {
        "id": "nguy_quach_gia",
        "name": "Quách Gia",
        "faction": "Ngụy",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "C", "Cung": "A", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Thập Thắng Thập Bại",
        "role": ["Chống khống chế cho chủ tướng", "Giảm 50% sát thương 2 hiệp đầu"],
        "season": "S1"
    },
    {
        "id": "nguy_sp_quach_gia",
        "name": "SP Quách Gia",
        "faction": "Ngụy",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "C", "Cung": "A", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Quỷ Toán Kỳ Mưu",
        "role": ["Dự đoán và giải trừ chiến pháp địch", "Phản sát thương"],
        "season": "PK"
    },
    {
        "id": "nguy_trinh_duc",
        "name": "Trình Dục",
        "faction": "Ngụy",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "C", "Cung": "A", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Thập Diện Mai Phục",
        "role": ["Sát thương chuẩn xuyên thủ", "Cấm hồi máu địch"],
        "season": "S1"
    },
    {
        "id": "nguy_tuan_uc",
        "name": "SP Tuân Úc",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "A", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Cảnh Trí Thiết Bích",
        "role": ["Khiên phản khống chế", "Giảm sát thương bùng nổ"],
        "season": "PK"
    },
    {
        "id": "nguy_dien_vi",
        "name": "Điển Vi",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "S", "Cung": "C", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Cổ Chi Ác Lai",
        "role": ["Đỡ đòn cho chủ tướng", "Phản kích vật lý"],
        "season": "S1"
    },
    {
        "id": "nguy_sp_dien_vi",
        "name": "SP Điển Vi",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "S", "Cung": "C", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Thiết Vệ Thần Dũng",
        "role": ["Đỡ toàn bộ sát thương 3 hiệp đầu", "Hồi phục theo sát thương chịu"],
        "season": "PK"
    },
    {
        "id": "nguy_tao_nhan",
        "name": "Tào Nhân",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "B", "Thương": "S", "Khí": "A"},
        "inherent_skill": "Cố Nhược Kim Thang",
        "role": ["Khiêu khích toàn bộ quân địch", "Tăng mạnh giáp bản thân"],
        "season": "S1"
    },
    {
        "id": "nguy_xu_chu",
        "name": "Hứa Chử",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "C", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Dũng Lực Quán Quân",
        "role": ["Bộc phát sát thương thô vật lý cực khủng", "Phá giáp"],
        "season": "S1"
    },
    {
        "id": "nguy_nhan_luong",
        "name": "Nhan Lương",
        "faction": "Ngụy",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "C", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Trủng Dũng Trên Lệnh",
        "role": ["Sát thương vật lý liên tục", "Tăng cơ hội ra chiêu 35%"],
        "season": "S2"
    },
    {
        "id": "nguy_van_chou",
        "name": "Văn Xú",
        "faction": "Ngụy",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Hà Bắc Dũng Tướng",
        "role": ["Tăng sát thương theo lượng giáp đối phương", "Khống chế"],
        "season": "S1"
    },
    {
        "id": "nguy_sp_hoang_phu_tung",
        "name": "SP Hoàng Phủ Tung",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Hổ Tinh Sạ Khải",
        "role": ["Phối với SP Mã Siêu T0", "Giảm giáp địch liên tục", "Buff hiệp chiến"],
        "season": "PK"
    },
    {
        "id": "nguy_hu_du",
        "name": "Hứa Du",
        "faction": "Ngụy",
        "cost": 4,
        "troop": {"Kỵ": "B", "Khiên": "B", "Cung": "A", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Mộ Hư Kê Thực",
        "role": ["Combo với SP Mã Siêu", "Lấy thông tin đối thủ", "Giảm chỉ số trí lực"],
        "season": "PK"
    },
    {
        "id": "nguy_tao_pi",
        "name": "Tào Phi",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "A"},
        "inherent_skill": "Tào Ngụy Vũ Đế",
        "role": ["Tăng thuộc tính toàn đội Ngụy", "Sát thương pháp cung"],
        "season": "S3"
    },
    {
        "id": "nguy_gia_xu",
        "name": "Gia Cát Đản",
        "faction": "Ngụy",
        "cost": 5,
        "troop": {"Kỵ": "B", "Khiên": "S", "Cung": "A", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Thành Tiết Chiến Tử",
        "role": ["Hồi phục liên tục", "Xây tường chắn sát thương"],
        "season": "S2"
    },
    {
        "id": "nguy_duc_luong",
        "name": "Đặng Ngải",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "B", "Cung": "S", "Thương": "S", "Khí": "B"},
        "inherent_skill": "Đảm Trí Dũng Kiêm",
        "role": ["Tập kích hiểm hóc bất ngờ", "Sát thương chuẩn cao"],
        "season": "S3"
    },

    # ================================================================
    # ĐÔNG NGÔ (EASTERN WU)
    # ================================================================
    {
        "id": "ngo_luc_ton",
        "name": "Lục Tốn",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "B", "Cung": "S", "Thương": "S", "Khí": "A"},
        "inherent_skill": "Hỏa Thiêu Liên Doanh",
        "role": ["Pháp sư đốt lửa nổ dam", "Chấn nhiếp", "Khai hoang quốc dân"],
        "season": "S1"
    },
    {
        "id": "ngo_luc_khang",
        "name": "Lục Kháng",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "A", "Thương": "S", "Khí": "B"},
        "inherent_skill": "Kháng Địch Bảo Biên",
        "role": ["Phòng thủ trâu bò", "Phản sát thương phép", "Giải trừ buff địch"],
        "season": "S3"
    },
    {
        "id": "ngo_thai_su_tu",
        "name": "Thái Sử Từ",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "C", "Cung": "S", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Thần Xạ",
        "role": ["Liên kích vĩnh viễn (đánh thường 2 lần)", "Giảm giáp", "Đột kích"],
        "season": "S1"
    },
    {
        "id": "ngo_chu_thai",
        "name": "Chu Thái",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "S", "Cung": "A", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Dục Huyết Phấn Chiến",
        "role": ["Hấp thu sát thương cho đồng đội", "Buff bạo lực sát thương"],
        "season": "PK"
    },
    {
        "id": "ngo_ton_thuong_huong",
        "name": "Tôn Thượng Hương",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "S", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Cung Yêu Binh Nhanh",
        "role": ["Sát thương vật lý bùng nổ theo số lượng buff", "Tốc chiến"],
        "season": "S2"
    },
    {
        "id": "ngo_lang_thong",
        "name": "Lăng Thống",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "A", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Quốc Sĩ Chi Phong",
        "role": ["Tiên phong Tất trúng (bỏ qua né đòn)", "Tăng sát thương đội"],
        "season": "S3"
    },
    {
        "id": "ngo_trinh_pho",
        "name": "Trình Phổ",
        "faction": "Ngô",
        "cost": 5,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Dũng Quan Tam Quân",
        "role": ["Chấn nhiếp phản đòn", "Giải trừ trạng thái xấu bản thân"],
        "season": "S1"
    },
    {
        "id": "ngo_chu_du",
        "name": "Chu Du",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "S", "Thương": "A", "Khí": "B"},
        "inherent_skill": "Thần Hỏa Kế",
        "role": ["Sát thương phép diện rộng theo số lần tung chiêu"],
        "season": "S1"
    },
    {
        "id": "ngo_sp_chu_du",
        "name": "SP Chu Du",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "S", "Thương": "A", "Khí": "A"},
        "inherent_skill": "Hùng Tài Đại Lược",
        "role": ["Thiêu đốt liên tục + phóng điện chấn nhiếp", "Kích hoạt Thái Bình chuỗi"],
        "season": "PK"
    },
    {
        "id": "ngo_lo_tuc",
        "name": "Lỗ Túc",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "A"},
        "inherent_skill": "Tế Bần Cứu Nhược",
        "role": ["Chuyển giao 40% thuộc tính cho đồng đội thấp máu nhất", "Hồi phục"],
        "season": "S3"
    },
    {
        "id": "ngo_ton_quyen",
        "name": "Tôn Quyền",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "A", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Tọa Đoán Đông Nam",
        "role": ["Tích lũy 5 đại buff: Liên kích, Động sát, Phá trận, Tiên phong, Tất trúng"],
        "season": "S1"
    },
    {
        "id": "ngo_lu_mong",
        "name": "Lữ Mông",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "S", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Bạch Y Độ Giang",
        "role": ["Khiên hộ vệ hiệp 1", "Câm lặng tướng địch"],
        "season": "S1"
    },
    {
        "id": "ngo_ton_sach",
        "name": "Tôn Sách",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Tiểu Bá Vương",
        "role": ["Sát thương vật lý bộc phát", "Miễn thương hiệp đầu", "Tiên phong mạnh"],
        "season": "S3"
    },
    {
        "id": "ngo_hoang_cai",
        "name": "Hoàng Cái",
        "faction": "Ngô",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "S", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Khổ Nhục Kế",
        "role": ["Tự thương để kích hoạt sát thương thiêu đốt khổng lồ", "Phá Đằng Giáp"],
        "season": "S1"
    },
    {
        "id": "ngo_dai_kieu",
        "name": "Đại Kiều",
        "faction": "Ngô",
        "cost": 4,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "B", "Thương": "C", "Khí": "B"},
        "inherent_skill": "Quốc Sắc Thiên Hương",
        "role": ["Hồi phục đội", "Giảm sát thương nhận vào cho đồng đội"],
        "season": "S1"
    },
    {
        "id": "ngo_tieu_kieu",
        "name": "Tiểu Kiều",
        "faction": "Ngô",
        "cost": 4,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "B", "Thương": "C", "Khí": "B"},
        "inherent_skill": "Nhu Tình Vạn Trượng",
        "role": ["Tăng né đòn đội", "Hỗn loạn đối phương"],
        "season": "S1"
    },
    {
        "id": "ngo_vosong_dai_kieu",
        "name": "Vô Song Đại Kiều",
        "faction": "Ngô",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "A", "Thương": "C", "Khí": "A"},
        "inherent_skill": "Hoa Dung Đại Kiều",
        "role": ["Hồi phục cực mạnh", "Phản sát thương phép", "Combo Vô Song Kiều"],
        "season": "PK"
    },
    {
        "id": "ngo_vosong_tieu_kieu",
        "name": "Vô Song Tiểu Kiều",
        "faction": "Ngô",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "A", "Thương": "C", "Khí": "S"},
        "inherent_skill": "Ngọc Tuyết Tiểu Kiều",
        "role": ["Né đòn cực cao", "Gây hỗn loạn diện rộng", "Combo Vô Song Kiều"],
        "season": "PK"
    },
    {
        "id": "ngo_cam_ning",
        "name": "Cam Ninh",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "S", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Cẩm Phàm Tặc Tử",
        "role": ["Đột kích nhanh", "Đột kích quán xuyến", "Tốc chiến"],
        "season": "S2"
    },
    {
        "id": "ngo_ding_feng",
        "name": "Đinh Phụng",
        "faction": "Ngô",
        "cost": 5,
        "troop": {"Kỵ": "B", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Trảm Tướng Phong Vân",
        "role": ["Trảm tướng đơn mục tiêu", "Buff tốc độ"],
        "season": "S2"
    },

    # ================================================================
    # QUẦN HÙNG (WARLORDS / INDEPENDENTS)
    # ================================================================
    {
        "id": "quan_lu_bo",
        "name": "Lữ Bố",
        "faction": "Quần",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Thiên Hạ Vô Song",
        "role": ["Quyết đấu tay đôi 3 lần", "Sát thương vật lý hủy diệt"],
        "season": "S1"
    },
    {
        "id": "quan_truong_giac",
        "name": "Trương Giác",
        "faction": "Quần",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "S", "Thương": "B", "Khí": "A"},
        "inherent_skill": "Ngũ Lôi Oanh Đỉnh",
        "role": ["Sấm sét giật liên tiếp 5-6 lần", "Chấn nhiếp liên tục", "Pháp sư"],
        "season": "S1"
    },
    {
        "id": "quan_ta_tu",
        "name": "Tả Từ",
        "faction": "Quần",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "C", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Kim Đan Bí Thuật",
        "role": ["Né đòn 35% cho toàn đội 2 hiệp đầu", "Hồi phục cực mạnh các hiệp sau"],
        "season": "S1"
    },
    {
        "id": "quan_vu_cat",
        "name": "Vu Cát",
        "faction": "Quần",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "B", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Hưng Vân Bố Vũ",
        "role": ["Mưa nước độc gây sát thương liên tục 5 hiệp"],
        "season": "S1"
    },
    {
        "id": "quan_hoa_da",
        "name": "Hoa Đà",
        "faction": "Quần",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "A", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Thanh Nang Thư",
        "role": ["Hồi máu khi bị đánh 4 hiệp đầu", "Tăng Thống soái"],
        "season": "S1"
    },
    {
        "id": "quan_vien_thieu",
        "name": "Viên Thiệu",
        "faction": "Quần",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "S"},
        "inherent_skill": "Lũy Thạch Nghênh Địch",
        "role": ["Tăng giáp cả đội", "Sát thương đốt cháy"],
        "season": "S1"
    },
    {
        "id": "quan_sp_vien_thieu",
        "name": "SP Viên Thiệu",
        "faction": "Quần",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "A"},
        "inherent_skill": "Cao Lũy Trọng Bộc",
        "role": ["Bắn tiễn tháp tước khí địch ngay hiệp đầu", "Khống chế đánh thường"],
        "season": "PK"
    },
    {
        "id": "quan_dong_trac",
        "name": "Đổng Trác",
        "faction": "Quần",
        "cost": 7,
        "troop": {"Kỵ": "B", "Khiên": "S", "Cung": "B", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Tửu Trì Nhục Lâm",
        "role": ["Tự tăng sức mạnh & hút máu", "Sát thương toàn trường từ hiệp 5"],
        "season": "S1"
    },
    {
        "id": "quan_dieu_thuyen",
        "name": "Điêu Thuyền",
        "faction": "Quần",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "B", "Thương": "C", "Khí": "C"},
        "inherent_skill": "Bế Nguyệt Tu Hoa",
        "role": ["Hỗn loạn / Hư nhược địch", "Chuyển hướng sát thương"],
        "season": "S1"
    },
    {
        "id": "quan_hoa_xiong",
        "name": "Hoa Hùng",
        "faction": "Quần",
        "cost": 5,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Quán Trảm Chư Tướng",
        "role": ["Tốc chiến trảm tướng đơn", "Sát thương vật lý cao"],
        "season": "S1"
    },
    {
        "id": "quan_gon_rong",
        "name": "SP Quan Vũ (Ngũ Quan)",
        "faction": "Quần",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Ngũ Quan Trảm Tướng",
        "role": ["Trảm liên hoàn 5 đòn", "Sát thương vật lý khổng lồ"],
        "season": "PK"
    },
    {
        "id": "quan_zhang_ning",
        "name": "Trương Ninh",
        "faction": "Quần",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "C", "Khí": "A"},
        "inherent_skill": "Nương Tử Quân",
        "role": ["Trạng thái đặc biệt", "Khống chế diện rộng", "Pháp sư"],
        "season": "PK"
    },
    {
        "id": "quan_sun_jian",
        "name": "Tôn Kiên",
        "faction": "Quần",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "A", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Giang Đông Mãnh Hổ",
        "role": ["Hỗn chiến sát thương vật lý", "Hút máu", "Kích hoạt buff đột kích"],
        "season": "S1"
    },

    # ================================================================
    # TƯỚNG LIÊN KẾT (COLLAB / SPECIAL)
    # ================================================================
    {
        "id": "sp_ma_chao_alt",
        "name": "SP Mã Tắc",
        "faction": "Thục",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "B", "Khí": "C"},
        "inherent_skill": "Thất Giới Mê Trận",
        "role": ["Mê trận khống chế", "Giảm mạnh Trí lực địch"],
        "season": "S2"
    },

    # ================================================================
    # TƯỚNG MỚI - TRÍCH XUẤT TỪ 98 ẢNH QUÉT
    # ================================================================

    # --- NGÔ MỚI ---
    {
        "id": "ngo_dai_kieu_co",
        "name": "CO Đại Kiều",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "C", "Khí": "A"},
        "inherent_skill": "Hoa Kiên Cường",
        "role": ["Cung S hỗ trợ hồi phục", "Tăng Kinh Hồng (Võ Lực)", "Tinh Hổ Báo Kỵ duyên phận"],
        "season": "PK"
    },
    {
        "id": "ngo_tieu_kieu_co",
        "name": "CO Tiểu Kiều",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "C", "Khí": "A"},
        "inherent_skill": "Hoa Thuần Khiết",
        "role": ["Cung S tinh Hổ Báo Kỵ", "Lâm Nguy Cứu Chủ hỗ trợ", "Duyên phận Hổ Thần Cung"],
        "season": "PK"
    },
    {
        "id": "ngo_co_tinh_thai",
        "name": "CO Tinh Thái",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "S", "Khiên": "B", "Cung": "A", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Tinh Lĩnh Đan Dương",
        "role": ["Kỵ S tinh Linh Đan Dương", "Tăng toàn bộ Thống soái", "Kết hợp SP Quan Vũ / SP Pháp Chính"],
        "season": "PK"
    },
    {
        "id": "ngo_chu_du",
        "name": "Chu Du",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "A"},
        "inherent_skill": "Đoạt Hồn Hiệp Phách",
        "role": ["Cướp thuộc tính địch", "Pháp sư sát thương cao", "Đội Cung pháp"],
        "season": "S1"
    },
    {
        "id": "ngo_luc_ton",
        "name": "Lục Tốn",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "A"},
        "inherent_skill": "Đồng Lòng Hợp Sức",
        "role": ["Hỗ trợ Cung binh", "Tinh Nhanh Trí Động Não", "Đội Chu Du Lục Tốn"],
        "season": "S1"
    },
    {
        "id": "ngo_thai_su_tu",
        "name": "Thái Sử Từ",
        "faction": "Ngô",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Nghịch Giang Diêu Lộ",
        "role": ["Cung S tốc độ cao", "Đội hình Lữ Bố thay thế", "Thôi Phong Đoạn Nhẫn"],
        "season": "S1"
    },
    {
        "id": "ngo_ton_quan",
        "name": "Tôn Quyền",
        "faction": "Ngô",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "A", "Cung": "S", "Thương": "A", "Khí": "B"},
        "inherent_skill": "Nhất Ký Đường Thiên",
        "role": ["Cung S chủ tướng đa năng", "Tinh Hổ Báo Kỵ", "Đội Tôn Quyền - Lăng Thống - Chu Thái"],
        "season": "S1"
    },

    # --- THỤC MỚI ---
    {
        "id": "thuc_quan_hung",
        "name": "Quan Hưng",
        "faction": "Thục",
        "cost": 5,
        "troop": {"Kỵ": "A", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Cuỡi Ngựa Nghìn Dặm",
        "role": ["Cung S phó tướng hỗ trợ", "Tăng Võ lực đội Cung", "Đội Bắc Phạt Khiên"],
        "season": "S1"
    },
    {
        "id": "thuc_truong_bao",
        "name": "Trương Bảo",
        "faction": "Thục",
        "cost": 5,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "B", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Xông Pha Khói Lửa",
        "role": ["Khiên S bảo vệ", "Không Đánh Mà Thắng", "Đội Bắc Phạt Khiên"],
        "season": "S1"
    },
    {
        "id": "thuc_luu_bi",
        "name": "Lưu Bị",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "B", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Hãm Trận Doanh",
        "role": ["Chủ tướng Khiên S trị liệu", "Buff toàn đội", "Đội Huy Quân Kết Trận"],
        "season": "S1"
    },
    {
        "id": "thuc_truong_phi",
        "name": "Trương Phi",
        "faction": "Thục",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Vô Địch Can Trường",
        "role": ["Khiên S / Thương S sát thương", "Huy Quân Kết Trận combo", "Kích Kỳ Nọa Quy"],
        "season": "S1"
    },
    {
        "id": "thuc_quan_vu",
        "name": "Quan Vũ",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "S", "Khiên": "A", "Cung": "B", "Thương": "S", "Khí": "C"},
        "inherent_skill": "Uy Mưu Võ Địch",
        "role": ["Kỵ S + Thương S linh hoạt", "Huy Quân Kết Trận chủ tướng", "Combo Thục tam anh"],
        "season": "S1"
    },
    {
        "id": "thuc_sp_phap_chinh",
        "name": "SP Pháp Chính",
        "faction": "Thục",
        "cost": 7,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "S"},
        "inherent_skill": "Tinh Phi Hùng Quân",
        "role": ["Cung S T0 PK", "Tốc độ kích hoạt cực nhanh", "Đội Thục Trí Phi Hùng Cung"],
        "season": "PK"
    },

    # --- NGỤY MỚI ---
    {
        "id": "nguy_sp_lo_truc",
        "name": "SP Lô Trực",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "C", "Khiên": "S", "Cung": "A", "Thương": "A", "Khí": "A"},
        "inherent_skill": "Tinh Tử Sĩ Tiên Phong",
        "role": ["Khiên S Thống soái cao", "Tử Sĩ Tiên Phong né đòn chết lại", "Đội Lữ Bố - Điêu Thuyền"],
        "season": "PK"
    },
    {
        "id": "nguy_sp_dieu_thuyen",
        "name": "SP Điêu Thuyền",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "B", "Thương": "C", "Khí": "A"},
        "inherent_skill": "Thâm Tàng Nhược Hư",
        "role": ["Giảm sát thương nhận vào", "Cường Nhu Kết Hợp", "Đội Lữ Bố Thái Sư Cung"],
        "season": "PK"
    },
    {
        "id": "nguy_sp_dong_trac",
        "name": "SP Đổng Trác",
        "faction": "Ngụy",
        "cost": 7,
        "troop": {"Kỵ": "B", "Khiên": "S", "Cung": "B", "Thương": "A", "Khí": "B"},
        "inherent_skill": "Chuyển Phi Hùng Quân",
        "role": ["Khiên S Thống soái cực cao", "Chuyển Cung kích hoạt Phi Hùng", "Đội Thái Sư Cung"],
        "season": "PK"
    },
    {
        "id": "nguy_tao_phi",
        "name": "Tào Phi",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "B", "Cung": "A", "Thương": "A", "Khí": "B"},
        "inherent_skill": "Đế Vương Chi Tư",
        "role": ["Buff toàn đội linh hoạt", "Phó tướng đa năng", "Điểm thêm mạnh"],
        "season": "S2"
    },
    {
        "id": "nguy_vuong_di",
        "name": "Vương Dị",
        "faction": "Ngụy",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "B", "Cung": "S", "Thương": "A", "Khí": "C"},
        "inherent_skill": "Đoạt Hồn Hiệp Phách",
        "role": ["Cung S Trí cao", "Đoạt thuộc tính địch", "Đội Ngũ Mưu Thần Bạch Nhị Cung"],
        "season": "PK"
    },
    {
        "id": "nguy_thu_thu",
        "name": "Thư Thụ",
        "faction": "Quần",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "A", "Thương": "C", "Khí": "B"},
        "inherent_skill": "Bát Môn Kim Tỏa Trận",
        "role": ["Hỗ trợ Trí lực đội Quần Hùng", "Mê trận bảo vệ", "Phó tướng giá rẻ hiệu quả"],
        "season": "S1"
    },
    {
        "id": "quan_sp_vien_thieu_pk",
        "name": "SP Viên Thiệu (PK)",
        "faction": "Quần",
        "cost": 7,
        "troop": {"Kỵ": "A", "Khiên": "A", "Cung": "S", "Thương": "B", "Khí": "A"},
        "inherent_skill": "Vô Đương Phi Quân",
        "role": ["Tinh Vô Đương Phi Quân", "Sát thương vật lý cung binh", "Đội Vô Đương Phi Quân"],
        "season": "PK"
    },
    {
        "id": "quan_sp_chu_tuan_khien",
        "name": "SP Chu Tuấn (Khiên)",
        "faction": "Quần",
        "cost": 6,
        "troop": {"Kỵ": "A", "Khiên": "S", "Cung": "A", "Thương": "A", "Khí": "A"},
        "inherent_skill": "Tinh Vô Đương Phi Quân",
        "role": ["Khiên S Thống soái cao", "Thiêu Đốt Doanh Lũy", "Đội Vô Đương Phi Quân"],
        "season": "PK"
    },
    {
        "id": "quan_vuong_di_qu",
        "name": "Vương Dị (Quần)",
        "faction": "Quần",
        "cost": 6,
        "troop": {"Kỵ": "C", "Khiên": "B", "Cung": "S", "Thương": "C", "Khí": "A"},
        "inherent_skill": "Nhạn Hình Trận",
        "role": ["Phó tướng Cung pháp Quần Hùng", "Hãm Trận Doanh hỗ trợ", "Đội Lữ Bố Cung"],
        "season": "PK"
    },
    {
        "id": "quan_hua_du_cung",
        "name": "Hứa Du (Cung)",
        "faction": "Quần",
        "cost": 5,
        "troop": {"Kỵ": "C", "Khiên": "C", "Cung": "A", "Thương": "C", "Khí": "S"},
        "inherent_skill": "Nhạn Hình Trận",
        "role": ["Phó tướng Cung S hỗ trợ", "Lâm Nguy Cứu Chủ", "Đội Cam Ninh Lữ Bố"],
        "season": "PK"
    }
]

# ================================================================
# CHIẾN PHÁP (TACTICS DATABASE)
# ================================================================
tactics_data = [
    # --- TRẬN PHÁP (FORMATION) ---
    {
        "id": "bat_mon_kim_toa",
        "name": "Bát Môn Kim Tỏa",
        "type": "Trận pháp",
        "quality": "S",
        "description": "3 hiệp đầu, giảm 30-50% sát thương của 2 kẻ địch và chủ tướng nhận Tiên phong. Chiến pháp bảo vệ đỉnh cao.",
        "season": "S1"
    },
    {
        "id": "tam_the_tran",
        "name": "Tam Thế Trận",
        "type": "Trận pháp",
        "quality": "S",
        "description": "Khi 3 tướng thuộc 3 phe khác nhau: tăng 16% xác suất chiến pháp chủ động của chủ tướng, phó tướng yếu hơn nhận thêm hộ thuẫn, phó tướng mạnh hơn tăng sát thương.",
        "season": "S3"
    },
    {
        "id": "phong_thi_tran",
        "name": "Phong Thỉ Trận",
        "type": "Trận pháp",
        "quality": "S",
        "description": "Tăng 30% sát thương cho chủ tướng (nhưng nhận thêm 20%); phó tướng nhận ít hơn 25% sát thương nhưng giảm 15% sát thương gây ra.",
        "season": "S1"
    },
    {
        "id": "ngu_phien_tran",
        "name": "Ngũ Phiên Trận",
        "type": "Trận pháp",
        "quality": "S",
        "description": "Chủ tướng khiêu khích đối phương, phó tướng thay phiên tích lũy sát thương và bùng nổ ở các hiệp sau.",
        "season": "PK"
    },
    {
        "id": "long_doan_tran",
        "name": "Long Đoạn Trận",
        "type": "Trận pháp",
        "quality": "S",
        "description": "Chủ tướng tăng sát thương theo % HP đã mất, phó tướng nhận khiên bảo vệ khi chủ tướng bị đánh.",
        "season": "PK"
    },
    {
        "id": "vu_bao_tran",
        "name": "Vũ Báo Trận",
        "type": "Trận pháp",
        "quality": "S",
        "description": "Đội hình Cung binh: Tất cả lần đánh thường đều có cơ hội bắn thêm 1 phát đạn bổ sung. Phá giáp diện rộng.",
        "season": "PK"
    },

    # --- BINH CHỦNG (ARMAMENT) ---
    {
        "id": "bach_ma_nghia_tung",
        "name": "Bạch Mã Nghĩa Tùng",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Cung binh: Toàn đội tăng tốc hành quân và nhận Tiên phong 2 hiệp đầu, tăng 10% tỷ lệ kích hoạt chiến pháp chủ động.",
        "season": "S1"
    },
    {
        "id": "cam_phan_quan",
        "name": "Cẩm Phàm Quân",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Cung binh: Khi đánh thường có xác suất gây Loạn Trận (chảy máu) và hồi phục binh lực.",
        "season": "S3"
    },
    {
        "id": "ham_tran_doanh",
        "name": "Hãm Trận Doanh",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Khiên binh: Tăng Thống soái và Võ lực cho toàn đội, 3 hiệp đầu hồi phục liên tục khi bị đánh trúng.",
        "season": "S1"
    },
    {
        "id": "dang_giap_binh",
        "name": "Đằng Giáp Binh",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Khiên binh: Giảm cực mạnh sát thương vật lý (lên đến 40%), nhưng nếu bị đốt lửa sẽ chịu gấp 2.5 lần sát thương và hỗn loạn.",
        "season": "S1"
    },
    {
        "id": "ho_bao_ky",
        "name": "Hổ Báo Kỵ",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Kỵ binh: Toàn đội tăng Võ lực, tăng 10% tỷ lệ kích hoạt các chiến pháp Đột Kích trong 3 hiệp đầu.",
        "season": "S1"
    },
    {
        "id": "tay_luong_thiet_ky",
        "name": "Tây Lương Thiết Kỵ",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Kỵ binh: 3 hiệp đầu tăng 25% tỷ lệ Bạo Kích sát thương vật lý cho toàn đội.",
        "season": "S1"
    },
    {
        "id": "thanh_chau_binh",
        "name": "Thanh Châu Binh",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Thương binh: Đòn đánh có cơ hội giảm sát thương địch gây ra, và ở hiệp 3 hồi lượng máu khổng lồ theo lượng sát thương đã nhận.",
        "season": "S3"
    },
    {
        "id": "bach_nhi_binh",
        "name": "Bạch Nhĩ Binh",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Thương binh: Đòn đánh thường kèm theo đòn mưu trí sát thương cao (chịu ảnh hưởng Trí lực).",
        "season": "S1"
    },
    {
        "id": "tuong_binh",
        "name": "Tượng Binh",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Kỵ binh: Khi bị đánh có cơ hội phản công toàn bộ địch, và hồi phục HP theo số quân địch bị đánh.",
        "season": "PK"
    },
    {
        "id": "quan_ho_ve",
        "name": "Quân Hổ Vệ",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Dành cho Khiên binh: Chủ động tạo khiên lớn vào đầu trận, hấp thụ 40% tổng HP dưới dạng khiên.",
        "season": "PK"
    },
    {
        "id": "ky_binh_siet_chen",
        "name": "Kỵ Binh Siết Chặt",
        "type": "Binh chủng",
        "quality": "A",
        "description": "Dành cho Kỵ binh: Mỗi hiệp tăng cộng dồn 10 Võ lực, và giảm Tốc độ địch.",
        "season": "S2"
    },

    # --- CHỈ HUY (COMMAND) ---
    {
        "id": "thai_binh_dao_phap",
        "name": "Thái Bình Đạo Pháp",
        "type": "Bị động",
        "quality": "S",
        "description": "Tăng tỷ lệ kích hoạt chiến pháp chủ động và mang lại tỷ lệ Bạo kích phép thuật (Kỳ mưu) cực khủng. Chiến pháp đắt giá nhất game.",
        "season": "S2"
    },
    {
        "id": "si_biet_tam_nhat",
        "name": "Sĩ Biệt Tam Nhật",
        "type": "Bị động",
        "quality": "S",
        "description": "3 hiệp đầu không thể đánh thường nhưng nhận 30% né đòn; đến hiệp 4 tăng Trí lực và gây sát thương diện rộng toàn bộ quân địch.",
        "season": "S1"
    },
    {
        "id": "quan_dan_khich_le",
        "name": "Quân Dân Khích Lệ",
        "type": "Chỉ huy",
        "quality": "S",
        "description": "3 hiệp đầu giảm sát thương nhận vào của 2 đồng minh (lên đến 40-50%), sau đó hồi phục binh lực ở hiệp 4.",
        "season": "S3"
    },
    {
        "id": "thao_thuyen_muon_ten",
        "name": "Thảo Thuyền Mượn Tên",
        "type": "Chủ động",
        "quality": "S",
        "description": "Giải trừ toàn bộ trạng thái tiêu cực cho 2-3 đồng minh, đồng thời cho trạng thái sơ cứu hồi máu khi bị công kích trong 2 hiệp.",
        "season": "PK"
    },
    {
        "id": "tam_nhat_tranh_mùi_nhon",
        "name": "Tạm Thời Tránh Mũi Nhọn",
        "type": "Chỉ huy",
        "quality": "S",
        "description": "3 hiệp đầu, tướng Trí cao nhất giảm 40-60% sát thương vật lý, tướng Võ cao nhất giảm 40-60% sát thương mưu trí.",
        "season": "S1"
    },
    {
        "id": "ngu_dich_boi_hop",
        "name": "Ngự Địch Bối Hợp",
        "type": "Chỉ huy",
        "quality": "A",
        "description": "4 hiệp đầu giảm 25% toàn bộ sát thương cho 2 tướng đồng minh. Chiến pháp A quốc dân siêu phổ biến.",
        "season": "S1"
    },
    {
        "id": "man_thien_qua_hai",
        "name": "Mạn Thiên Quá Hải",
        "type": "Chỉ huy",
        "quality": "S",
        "description": "Phân tán sát thương từ đòn đánh đơn mục tiêu sang toàn đội, giảm hiệu quả của các đòn tập trung.",
        "season": "PK"
    },
    {
        "id": "sat_khi_dong_troi",
        "name": "Thịnh Khí Lăng Nhân",
        "type": "Chỉ huy",
        "quality": "S",
        "description": "2 hiệp đầu, 90% tỷ lệ khiến 2 kẻ địch rơi vào trạng thái Tước Khí (không thể đánh thường). Khắc chế cứng đội đột kích.",
        "season": "S1"
    },
    {
        "id": "an_ui_quan_dan",
        "name": "An Ủi Quân Dân",
        "type": "Chỉ huy",
        "quality": "S",
        "description": "Toàn đội giảm sát thương nhận vào 20%, đồng thời hồi phục liên tục mỗi hiệp. Phiên bản nâng cao của Ngự Địch.",
        "season": "PK"
    },
    {
        "id": "bien_phap_an_dan",
        "name": "Biến Pháp Yên Dân",
        "type": "Chỉ huy",
        "quality": "S",
        "description": "Tăng toàn bộ chỉ số cơ bản cho đội hình trong 3 hiệp đầu, sau đó tướng nhận buff tấn công lớn.",
        "season": "S3"
    },

    # --- CHỦ ĐỘNG (ACTIVE TACTICS) ---
    {
        "id": "pha_tran_thoi_kien",
        "name": "Phá Trận Kiên Tồi",
        "type": "Chủ động",
        "quality": "S",
        "description": "1 hiệp chuẩn bị, giảm mạnh Thống soái và Trí lực của 2 kẻ địch trong 2 hiệp, sau đó gây sát thương vật lý cực mạnh.",
        "season": "S1"
    },
    {
        "id": "doat_hon_hiep_phach",
        "name": "Đoạt Hồn Hiếp Phách",
        "type": "Chủ động",
        "quality": "S",
        "description": "Cướp 38-76 điểm Võ, Trí, Thống, Tốc của mục tiêu cộng vào bản thân trong 2 hiệp (có thể cộng dồn 2 lần).",
        "season": "S1"
    },
    {
        "id": "coc_sat_nghiem_tuc",
        "name": "Cốc Sát Nghiêm Túc",
        "type": "Chủ động",
        "quality": "S",
        "description": "Gây sát thương liên tục qua nhiều hiệp và giải trừ buff của đối phương. Sát thương tổng cộng rất cao.",
        "season": "S2"
    },
    {
        "id": "lac_phung",
        "name": "Lạc Phụng",
        "type": "Chủ động",
        "quality": "A",
        "description": "Gây 250% sát thương vật lý cho 1 tướng địch và áp đặt trạng thái Kế Cùng (câm lặng 1 hiệp).",
        "season": "S1"
    },
    {
        "id": "tung_binh_kiep_luoc",
        "name": "Túng Binh Kiếp Lược",
        "type": "Chủ động",
        "quality": "A",
        "description": "Gây sát thương vật lý và chấn nhiếp kẻ địch 1 hiệp. Rất phổ biến vì chi phí thấp.",
        "season": "S1"
    },
    {
        "id": "bach_mi",
        "name": "Bạch Mi",
        "type": "Bị động",
        "quality": "A",
        "description": "Tăng 12% tỷ lệ kích hoạt tất cả chiến pháp chủ động của bản thân. Chiến pháp thay thế phổ biến nhất.",
        "season": "S1"
    },
    {
        "id": "hoa_si_nguyen_lieu",
        "name": "Hỏa Sí Nguyên Liêu",
        "type": "Chủ động",
        "quality": "S",
        "description": "1 hiệp chuẩn bị, gây sát thương lửa + đao kiếm + độc tố lên nhiều mục tiêu. Mạnh với tướng Trí cao.",
        "season": "S2"
    },
    {
        "id": "khoa_giang_tuyet_canh",
        "name": "Tuyệt Địa Phản Kích",
        "type": "Bị động",
        "quality": "S",
        "description": "Mỗi lần chịu đòn đánh tăng Võ lực. Đến hiệp 5 giải phóng toàn bộ sát thương quét sạch phe địch.",
        "season": "S1"
    },
    {
        "id": "cuong_cung_bao_thi",
        "name": "Cường Cung Bạo Thỉ",
        "type": "Chủ động",
        "quality": "S",
        "description": "Bắn một loạt 5-6 mũi tên tập trung vào 1 mục tiêu, mỗi mũi gây sát thương độc lập. Sát thương tổng rất cao khi tướng Võ cao.",
        "season": "PK"
    },
    {
        "id": "chi_luc_phan_ke",
        "name": "Trí Lực Phản Kế",
        "type": "Bị động",
        "quality": "S",
        "description": "Khi bị tấn công bằng chiến pháp chủ động, 40% cơ hội giải trừ và phản trả lại 1 lần sát thương phép lên kẻ tấn công.",
        "season": "PK"
    },
    {
        "id": "cam_phan_chuyen_phong",
        "name": "Lâm Điện Phong Âm",
        "type": "Chủ động",
        "quality": "S",
        "description": "Giảm tốc độ và Trí lực của toàn bộ đối phương trong 2 hiệp, sau đó gây sát thương sét diện rộng.",
        "season": "S3"
    },
    {
        "id": "cuong_nu_giao_phong",
        "name": "Quyết Mệnh Liên Tiễn",
        "type": "Đột kích",
        "quality": "S",
        "description": "Sau đòn đánh thường, bắn thêm 2 mũi tên ngẫu nhiên vào địch. Mỗi mũi có thể kích hoạt hiệu ứng bổ sung.",
        "season": "PK"
    },

    # --- ĐỘT KÍCH (ASSAULT TACTICS) ---
    {
        "id": "nhat_dao_duong_danh",
        "name": "Nhất Đao Đương Thiên",
        "type": "Đột kích",
        "quality": "S",
        "description": "Sau đòn đánh thường, gây sát thương vật lý cực khủng lên toàn bộ 3 tướng địch. Tuyệt kỹ của Lữ Bố / Trương Liêu.",
        "season": "S1"
    },
    {
        "id": "quy_than_dinh_hoan",
        "name": "Quỷ Thần Đình Uy",
        "type": "Đột kích",
        "quality": "S",
        "description": "Gây sát thương vật lý; nếu máu mục tiêu dưới 50% sẽ gây thêm một lượng sát thương hủy diệt.",
        "season": "S2"
    },
    {
        "id": "tram_hoang_triet_ky",
        "name": "Bách Lăng Kỵ Tiệp",
        "type": "Đột kích",
        "quality": "S",
        "description": "Gây sát thương vật lý và đánh thẳng vào chủ tướng địch bất kể vị trí.",
        "season": "S1"
    },
    {
        "id": "uong_khi_tuyet_dao",
        "name": "Dũng Giả Đắc Tiền",
        "type": "Đột kích",
        "quality": "S",
        "description": "Nhận khiên hộ thuẫn và tăng 80% sát thương của chiến pháp chủ động tiếp theo. Kết hợp cực mạnh với Phá Trận.",
        "season": "S2"
    },
    {
        "id": "tram_dong_kiem",
        "name": "Trảm Tướng Đoạt Kỳ",
        "type": "Đột kích",
        "quality": "A",
        "description": "Đột kích gây sát thương và tước khí đối phương 1 hiệp.",
        "season": "S1"
    },
    {
        "id": "hiep_chien_phan_tren",
        "name": "Hiệp Chiến Phản Thủ",
        "type": "Đột kích",
        "quality": "S",
        "description": "Khi đồng minh bị tấn công, có cơ hội lao vào tham chiến ngẫu nhiên. Được khuếch đại theo số lần kích hoạt.",
        "season": "PK"
    },
    {
        "id": "van_trung_guong",
        "name": "Vạn Trùng Khám Phá",
        "type": "Đột kích",
        "quality": "S",
        "description": "Gây sát thương theo % HP hiện tại của địch. Cực mạnh chống lại các đội hình trâu bò nhiều máu.",
        "season": "PK"
    },
    {
        "id": "hoành_tao_thien_quan",
        "name": "Hoành Tảo Thiên Quân",
        "type": "Đột kích",
        "quality": "S",
        "description": "Sau đòn đánh thường, quét toàn bộ hàng địch gây sát thương diện rộng + giảm Thống soái đối thủ.",
        "season": "S2"
    },
    {
        "id": "sat_the_an_ma",
        "name": "Sát Thần Ám Mạt",
        "type": "Đột kích",
        "quality": "S",
        "description": "Khi giết chết 1 tướng địch, kích hoạt ngay 1 đòn tấn công bổ sung lên tướng địch khác.",
        "season": "PK"
    },

    # --- BỊ ĐỘNG (PASSIVE TACTICS) ---
    {
        "id": "can_chinh_tri_oc",
        "name": "Cân Chính Trí Ốc",
        "type": "Bị động",
        "quality": "S",
        "description": "Tăng tỷ lệ né đòn và miễn thương toàn đội khi HP dưới 50%. Cực mạnh cho đội phòng thủ.",
        "season": "S3"
    },
    {
        "id": "bien_thu_tu_cuong",
        "name": "Bền Thủ Tự Cường",
        "type": "Bị động",
        "quality": "A",
        "description": "Mỗi lần bị đánh hồi phục 1 lượng máu nhỏ. Rẻ và ổn định, phù hợp cho tướng Thống cao.",
        "season": "S1"
    },
    {
        "id": "cuu_vien_bi_thuật",
        "name": "Cứu Binh Bí Quyết",
        "type": "Chủ động",
        "quality": "A",
        "description": "Hồi phục binh lực cho 2 tướng đồng minh. Giá rẻ, hiệu quả ổn định.",
        "season": "S1"
    },
    {
        "id": "đường_phong_tối_quyết",
        "name": "Đương Phong Tồi Quyết",
        "type": "Bị động",
        "quality": "S",
        "description": "Giải trừ tất cả hiệu ứng Chỉ Huy và Bị Động của đối phương khi bắt đầu mỗi hiệp. Khắc chế cứng đội Tư Mã Ý / Tào Tháo.",
        "season": "S3"
    },
    {
        "id": "phan_ke_nguyen_muu",
        "name": "Phản Kế Nguyên Mưu",
        "type": "Bị động",
        "quality": "S",
        "description": "Khi chiến pháp Chỉ Huy của đối phương kích hoạt, 50% cơ hội phản trả với sát thương phép bằng 200% Trí lực.",
        "season": "PK"
    },
    {
        "id": "chia_sat_thuong",
        "name": "Cộng Nguy Tương Cứu",
        "type": "Bị động",
        "quality": "S",
        "description": "Khi đồng minh bị đánh xuống dưới 30% HP, tự động tạo 1 lớp khiên lớn cho toàn đội.",
        "season": "S3"
    },

    # ================================================================
    # CHIẾN PHÁP MỚI - TRÍCH XUẤT TỪ 98 ẢNH QUÉT
    # ================================================================
    {
        "id": "tinh_tu_si_tien_phong",
        "name": "Tinh Tử Sĩ Tiên Phong",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Khi tướng chủ đội Tử Sĩ Tiên Phong bị hạ, có thể hồi sinh với một lượng HP nhỏ và tiếp tục chiến đấu trong 1-2 hiệp. Cực kỳ khó bị trừ khử hoàn toàn.",
        "season": "PK"
    },
    {
        "id": "tinh_linh_dan_duong",
        "name": "Tinh Lĩnh Đan Dương",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Tăng Thống soái toàn đội, giúp tướng hỗ trợ dùng được các chiến pháp cần Thống soái cao. Phù hợp với CO Tinh Thái.",
        "season": "PK"
    },
    {
        "id": "tinh_ho_bao_ky",
        "name": "Tinh Hổ Báo Kỵ",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Phiên bản nâng cấp Hổ Báo Kỵ: Tăng mạnh hơn tỷ lệ bạo kích và kích hoạt đột kích, đặc biệt hiệu quả với CO Đại Kiều / CO Tiểu Kiều.",
        "season": "PK"
    },
    {
        "id": "huy_quan_ket_tran",
        "name": "Huy Quân Kết Trận",
        "type": "Chủ động",
        "quality": "S",
        "description": "Tăng 16% tỷ lệ kích hoạt chiến pháp chủ động của bản thân và có thể dựa vào Võ Lực cao / Thống Soái cao của toàn đội để gây thêm sát thương hoặc trị liệu. Đặc biệt mạnh với Quan Vũ.",
        "season": "S1"
    },
    {
        "id": "tinh_quan_ho_ve",
        "name": "Tinh Quân Hổ Vệ",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Phiên bản tinh Quân Hổ Vệ: Tăng thêm phòng thủ và hồi phục cho đội Khiên, đặc biệt khi kết hợp với Đằng Giáp Binh.",
        "season": "PK"
    },
    {
        "id": "tinh_phi_hung_quan",
        "name": "Tinh Phi Hùng Quân",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Phiên bản tinh Phi Hùng Quân / Huy Quân Kết Trận: Tốc độ kích hoạt cực nhanh, xác suất chiến pháp chủ động tăng gấp đôi. Đặc biệt với SP Pháp Chính.",
        "season": "PK"
    },
    {
        "id": "chuyen_bach_nhi_binh",
        "name": "Chuyển Bạch Nhĩ Binh",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Bạch Nhĩ Binh nâng cấp chuyển đổi: Đòn đánh thường đi kèm đòn phép Trí lực, thường dùng cho SP Tuân Úc trong đội Ngũ Mưu Thần.",
        "season": "PK"
    },
    {
        "id": "tinh_giai_phien_ve",
        "name": "Tinh Giải Phiền Vệ",
        "type": "Chủ động",
        "quality": "S",
        "description": "Lâm Nguy Cứu Chủ tinh: Giải trừ trạng thái tiêu cực và hồi phục binh lực mạnh hơn bình thường. Đặc biệt dùng bởi Hứa Du trong đội SP Mã Siêu.",
        "season": "PK"
    },
    {
        "id": "tinh_ho_bao_ky_cung",
        "name": "Tinh Hổ Báo Kỵ (Cung)",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Hổ Báo Kỵ đặc biệt dành cho Cung binh, kết hợp bắn tên và bạo kích diện rộng. Dùng cho CO Đại Kiều / CO Tiểu Kiều.",
        "season": "PK"
    },
    {
        "id": "tinh_dan_duong_linh",
        "name": "Tinh Đan Dương Linh",
        "type": "Binh chủng",
        "quality": "S",
        "description": "Linh Đan Dương phiên bản nâng: Tăng hàng loạt chỉ số Thống soái toàn đội, phù hợp với đội Pháp Quan Khiên Tinh Lĩnh Đan Dương.",
        "season": "PK"
    }
]

# ================================================================
# ĐỘI HÌNH META (META TEAMS DATABASE) - 25 Teams
# ================================================================
meta_teams = [
    # 1. THỤC CUNG T0 (KHƯƠNG DUY - BÀNG THỐNG - GIA CÁT LƯỢNG)
    {
        "id": "meta_thuc_cung_khuong_bang_gia",
        "name": "Thục Cung Chủ Lực (Khương Duy - Bàng Thống - Gia Cát Lượng)",
        "tier": "T0",
        "season": "PK",
        "faction": "Thục",
        "troop": "Cung",
        "description": "Đội hình pháp sư toàn diện nhất meta PK. Khương Duy liên tục trừ chỉ số địch qua nhiều nhịp, Gia Cát Lượng ngắt chiêu bằng Thần Cơ Diệu Toán, Bàng Thống kích hoạt Thái Bình Đạo Pháp tạo chuỗi sát thương phép diệt sạch đối thủ. Khắc chế mạnh nhất các đội hình dựa vào chiêu chủ động.",
        "strengths": ["Khắc chế đội hình dựa vào chiêu chủ động", "Sát thương dồn nén qua nhiều hiệp", "Trừ chỉ số khiến địch ngày càng yếu"],
        "weaknesses": ["Sợ Tốc Chiến Tước Khí (Lăng Thống + Chu Thái)", "Cần đúng bộ chiến pháp BIS mới đạt tối đa"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_khuong_duy",
                "name": "Khương Duy",
                "bis_tactics": ["Đoạt Hồn Hiếp Phách", "Cốc Sát Nghiêm Túc"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Bát Môn Kim Tỏa", "Lạc Phụng"],
                "alt_generals": ["thuc_trieu_van"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_bang_thong",
                "name": "Bàng Thống",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Bạch Mi", "Lạc Phụng", "Hỏa Sí Nguyên Liêu"],
                "alt_generals": ["thuc_phap_chinh"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_gia_cat_luong",
                "name": "Gia Cát Lượng",
                "bis_tactics": ["Bát Môn Kim Tỏa", "Thảo Thuyền Mượn Tên"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Tạm Thời Tránh Mũi Nhọn", "An Ủi Quân Dân"],
                "alt_generals": ["thuc_luu_bi", "thuc_sp_gia_cat_luong"]
            }
        ]
    },

    # 2. SP MÃ SIÊU T0 (SP MÃ SIÊU - SP HOÀNG PHỦ TUNG - HỨA DU)
    {
        "id": "meta_sp_ma_sieu_t0",
        "name": "SP Mã Siêu Chiến Thần (SP Mã Siêu - SP Hoàng Phủ Tung - Hứa Du)",
        "tier": "T0",
        "season": "PK",
        "faction": "Thục",
        "troop": "Kỵ",
        "description": "Đội hình T0 mùa Đồng Quan (PK). SP Mã Siêu với kỹ năng Tây Lương Chiến Thần gây sát thương vật lý bùng nổ cực khủng, SP Hoàng Phủ Tung liên tục giảm giáp địch và kích hoạt hiệp chiến, Hứa Du lấy thông tin kẻ địch và giảm Trí lực để SP Mã Siêu tối đa hóa sát thương.",
        "strengths": ["Sát thương vật lý bùng nổ hàng đầu meta", "Hiệp chiến kích hoạt liên hoàn", "Phá giáp cực nhanh"],
        "weaknesses": ["Sợ các đội có Tước Khí + Đằng Giáp Binh", "Phụ thuộc vào việc SP Mã Siêu ra chiêu sớm"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_sp_ma_sieu",
                "name": "SP Mã Siêu",
                "bis_tactics": ["Hổ Báo Kỵ", "Quỷ Thần Đình Uy"],
                "sub_tactics": ["Tây Lương Thiết Kỵ", "Nhất Đao Đương Thiên", "Bách Lăng Kỵ Tiệp"],
                "alt_generals": ["thuc_ma_sieu"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_sp_hoang_phu_tung",
                "name": "SP Hoàng Phủ Tung",
                "bis_tactics": ["Tạm Thời Tránh Mũi Nhọn", "Ngự Địch Bối Hợp"],
                "sub_tactics": ["An Ủi Quân Dân", "Thảo Thuyền Mượn Tên", "Quân Dân Khích Lệ"],
                "alt_generals": ["thuc_quan_vu", "nguy_quach_gia"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_hu_du",
                "name": "Hứa Du",
                "bis_tactics": ["Phong Thỉ Trận", "Thịnh Khí Lăng Nhân"],
                "sub_tactics": ["Bát Môn Kim Tỏa", "Ngự Địch Bối Hợp", "Đương Phong Tồi Quyết"],
                "alt_generals": ["nguy_tao_thao", "thuc_hoang_nguyet_anh"]
            }
        ]
    },

    # 3. NGỤY KHIÊN TƯ MÃ Ý (TƯ MÃ Ý - TÀO THÁO - MÃN SỦNG / HÁC CHIÊU)
    {
        "id": "meta_nguy_khien_tu_ma_y",
        "name": "Ngụy Khiên Thái Sư (Tư Mã Ý - Tào Tháo - Mãn Sủng)",
        "tier": "T0",
        "season": "PK",
        "faction": "Ngụy",
        "troop": "Khiên",
        "description": "Pháo đài bất khả xâm phạm. Tào Tháo và Mãn Sủng hồi phục + đỡ đòn liên tục, câu giờ để Tư Mã Ý tích lũy và bùng nổ bạo kích pháp thuật Sĩ Biệt Tam Nhật quét sạch sàn đấu ở hiệp 4+.",
        "strengths": ["Trâu bò nhất game, hồi phục không ngừng", "Gần như bất bại trước sát thương vật lý", "Càng đánh lâu càng mạnh"],
        "weaknesses": ["Bị Đằng Giáp thiêu đốt bởi Lục Tốn", "Bị Đương Phong Tồi Quyết giải trừ hết buff"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_tu_ma_y",
                "name": "Tư Mã Ý",
                "bis_tactics": ["Sĩ Biệt Tam Nhật", "Lâm Điện Phong Âm"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Thái Bình Đạo Pháp", "Cốc Sát Nghiêm Túc"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_tao_thao",
                "name": "Tào Tháo",
                "bis_tactics": ["Quân Dân Khích Lệ", "Đằng Giáp Binh"],
                "sub_tactics": ["Hãm Trận Doanh", "Tạm Thời Tránh Mũi Nhọn", "An Ủi Quân Dân"],
                "alt_generals": ["nguy_tao_nhan"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_man_sung",
                "name": "Mãn Sủng",
                "bis_tactics": ["Phong Thỉ Trận", "Thảo Thuyền Mượn Tên"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Cứu Binh Bí Quyết", "Quân Hổ Vệ"],
                "alt_generals": ["nguy_hac_chieu", "nguy_dien_vi", "nguy_sp_dien_vi"]
            }
        ]
    },

    # 4. NGÔ KỴ TỐC CHIẾN (TÔN THƯỢNG HƯƠNG - CHU THÁI - LĂNG THỐNG)
    {
        "id": "meta_ngo_ky_ton_thuong_huong",
        "name": "Ngô Kỵ Tốc Chiến (Tôn Thượng Hương - Chu Thái - Lăng Thống)",
        "tier": "T0",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Kỵ",
        "description": "Đội hình sốc sát thương nhanh nhất Tam Quốc Chí. Lăng Thống trao buff Tiên phong và Tất trúng (bỏ qua né đòn), Chu Thái gánh máu và tăng 35%+ sát thương, Tôn Thượng Hương xả tên kết liễu trận đấu trong 2-3 hiệp đầu. Khắc tinh cứng của Tam Thế Lữ Bố / Tả Từ né đòn.",
        "strengths": ["Bỏ qua né tránh - khắc tinh của Tả Từ", "Hạ gục đối thủ cực nhanh", "Khai hoang hiệu quả"],
        "weaknesses": ["Sợ Thịnh Khí Lăng Nhân (tước khí 2 hiệp đầu)", "Sợ Đằng Giáp Binh giảm sát thương vật lý"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_ton_thuong_huong",
                "name": "Tôn Thượng Hương",
                "bis_tactics": ["Cường Cung Bạo Thỉ", "Quyết Mệnh Liên Tiễn"],
                "sub_tactics": ["Nhất Đao Đương Thiên", "Bách Lăng Kỵ Tiệp", "Trảm Tướng Đoạt Kỳ"],
                "alt_generals": ["ngo_thai_su_tu"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_chu_thai",
                "name": "Chu Thái",
                "bis_tactics": ["Tây Lương Thiết Kỵ", "Thịnh Khí Lăng Nhân"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Hổ Báo Kỵ", "Phong Thỉ Trận"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_lang_thong",
                "name": "Lăng Thống",
                "bis_tactics": ["Phá Trận Kiên Tồi", "Hoành Tảo Thiên Quân"],
                "sub_tactics": ["Lạc Phụng", "Túng Binh Kiếp Lược", "Trảm Tướng Đoạt Kỳ"],
                "alt_generals": ["ngo_trinh_pho"]
            }
        ]
    },

    # 5. VÔ SONG KIỀU NGÔ (VÔ SONG ĐẠI KIỀU - VÔ SONG TIỂU KIỀU - LỖ TÚC)
    {
        "id": "meta_ngo_vo_song_kieu",
        "name": "Hổ Thần Cung Ngô (Vô Song Đại Kiều - Vô Song Tiểu Kiều - Lỗ Túc)",
        "tier": "T0",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Cung",
        "description": "Đội hình 'Hổ Thần Cung' siêu mạnh meta PK nhờ duyên phận Vô Song Kiều. Vô Song Tiểu Kiều gây hỗn loạn diện rộng khiến địch tự đánh nhau, Vô Song Đại Kiều hồi phục mạnh và phản sát thương phép, Lỗ Túc cung cấp chỉ số khổng lồ và giải trừ debuff.",
        "strengths": ["Hỗn loạn diện rộng tê liệt đội địch", "Hồi phục + phản sát thương phép cực khủng", "Duyên phận Vô Song Kiều cộng thuộc tính lớn"],
        "weaknesses": ["Cần đúng bộ Vô Song Kiều (hiếm)", "Sợ đội hình câm lặng sớm Tiểu Kiều"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_vosong_dai_kieu",
                "name": "Vô Song Đại Kiều",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Bát Môn Kim Tỏa"],
                "sub_tactics": ["Sĩ Biệt Tam Nhật", "Phản Kế Nguyên Mưu", "An Ủi Quân Dân"],
                "alt_generals": ["ngo_dai_kieu"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_vosong_tieu_kieu",
                "name": "Vô Song Tiểu Kiều",
                "bis_tactics": ["Trí Lực Phản Kế", "Cốc Sát Nghiêm Túc"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Lạc Phụng", "Đoạt Hồn Hiếp Phách"],
                "alt_generals": ["ngo_tieu_kieu"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_lo_tuc",
                "name": "Lỗ Túc",
                "bis_tactics": ["Quân Dân Khích Lệ", "Thảo Thuyền Mượn Tên"],
                "sub_tactics": ["An Ủi Quân Dân", "Bát Môn Kim Tỏa", "Tạm Thời Tránh Mũi Nhọn"],
                "alt_generals": ["ngo_trinh_pho"]
            }
        ]
    },

    # 6. TAM THẾ LỮ BỐ (LỮ BỐ - QUÁCH GIA - HOÀNG NGUYỆT ANH)
    {
        "id": "meta_tam_the_lu_bo",
        "name": "Tam Thế Lữ Bố (Lữ Bố - Quách Gia - Hoàng Nguyệt Anh)",
        "tier": "T0.5",
        "season": "S3",
        "faction": "Tam Thế",
        "troop": "Kỵ",
        "description": "Đội hình 'Chó Điên' trứ danh. Hoàng Nguyệt Anh + Quách Gia ban miễn khống chế 2 hiệp đầu, Lữ Bố liên tục phát động Thiên Hạ Vô Song quyết đấu đập nát đội địch mà không sợ bị ngắt chiêu.",
        "strengths": ["Miễn khống chế trong 2 hiệp đầu", "Sát thương đột biến cực cao", "Dễ ghép liên phe"],
        "weaknesses": ["Phụ thuộc nhân phẩm Lữ Bố", "Sợ Tất Trúng (Lăng Thống) kết liễu nhanh"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "quan_lu_bo",
                "name": "Lữ Bố",
                "bis_tactics": ["Nhất Đao Đương Thiên", "Quỷ Thần Đình Uy"],
                "sub_tactics": ["Bách Lăng Kỵ Tiệp", "Trảm Tướng Đoạt Kỳ", "Dũng Giả Đắc Tiền"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_quach_gia",
                "name": "Quách Gia",
                "bis_tactics": ["Hổ Báo Kỵ", "Tây Lương Thiết Kỵ"],
                "sub_tactics": ["Đương Phong Tồi Quyết", "Ngự Địch Bối Hợp", "Trảm Tướng Đoạt Kỳ"],
                "alt_generals": ["ngo_chu_thai", "nguy_sp_quach_gia"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_hoang_nguyet_anh",
                "name": "Hoàng Nguyệt Anh",
                "bis_tactics": ["Tam Thế Trận", "Thịnh Khí Lăng Nhân"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Bạch Mã Nghĩa Tùng", "Bát Môn Kim Tỏa"],
                "alt_generals": ["quan_ta_tu", "quan_hoa_da"]
            }
        ]
    },

    # 7. ĐÀO VIÊN KẾT NGHĨA (LƯU BỊ - QUAN VŨ - TRƯƠNG PHI)
    {
        "id": "meta_dao_vien_ket_nghia",
        "name": "Đào Viên Kết Nghĩa (Lưu Bị - Quan Vũ - Trương Phi)",
        "tier": "T1",
        "season": "S1",
        "faction": "Thục",
        "troop": "Khiên",
        "description": "Bộ ba Thục quốc quốc dân huyền thoại từ mùa 1 đến PK. Vừa có hồi phục từ Lưu Bị, khống chế diện rộng từ Quan Vũ, vừa có giảm giáp từ Trương Phi. Hiệp 6 nhận khiên phòng ngự duyên phận Đào Viên.",
        "strengths": ["Duyên phận Đào Viên tăng phòng thủ hiệp 6", "Linh hoạt chuyển đổi Khiên S hoặc Thương S", "Cực kỳ bền bỉ, cày cấp ít hao lính"],
        "weaknesses": ["Sát thương thiếu bùng nổ để kết liễu đội hồi máu khủng"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_luu_bi",
                "name": "Lưu Bị",
                "bis_tactics": ["Hãm Trận Doanh", "Tạm Thời Tránh Mũi Nhọn"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Thịnh Khí Lăng Nhân", "An Ủi Quân Dân"],
                "alt_generals": ["thuc_phap_chinh"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_quan_vu",
                "name": "Quan Vũ",
                "bis_tactics": ["Phá Trận Kiên Tồi", "Dũng Giả Đắc Tiền"],
                "sub_tactics": ["Lạc Phụng", "Hoành Tảo Thiên Quân", "Bạch Mi"],
                "alt_generals": ["thuc_trieu_van", "thuc_sp_quan_vu"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_truong_phi",
                "name": "Trương Phi",
                "bis_tactics": ["Thịnh Khí Lăng Nhân", "Hoành Tảo Thiên Quân"],
                "sub_tactics": ["Lạc Phụng", "Túng Binh Kiếp Lược", "Tuyệt Địa Phản Kích"],
                "alt_generals": ["thuc_nguy_dien", "thuc_hoang_trung"]
            }
        ]
    },

    # 8. NGÔ THƯƠNG LỤC TỐN (LỤC TỐN - LỖ TÚC - TRÌNH PHỔ)
    {
        "id": "meta_ngo_thuong_luc_ton",
        "name": "Ngô Thương Lục Tốn (Lục Tốn - Lỗ Túc - Trình Phổ)",
        "tier": "T0",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Thương",
        "description": "Đội hình thiêu đốt + phép bùng nổ đỉnh cao khi Lục Tốn được cấp chiến pháp Thái Bình Đạo Pháp. Lỗ Túc bơm chỉ số, Trình Phổ chấn nhiếp phản đòn tạo khoảng trống cho Lục Tốn thiêu rụi quân địch.",
        "strengths": ["Thiêu đốt Đằng Giáp Binh hiệu quả 250%", "Lỗ Túc bơm chỉ số biến Lục Tốn thành quái vật", "Sát thương diện rộng liên tục"],
        "weaknesses": ["Cần bảo vật chuyển hệ Thương S cho Lục Tốn ở mùa PK"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_luc_ton",
                "name": "Lục Tốn",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Đương Phong Tồi Quyết", "Hỏa Sí Nguyên Liêu", "Cốc Sát Nghiêm Túc"],
                "alt_generals": ["ngo_sp_chu_du"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_lo_tuc",
                "name": "Lỗ Túc",
                "bis_tactics": ["Tạm Thời Tránh Mũi Nhọn", "Bạch Nhĩ Binh"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "An Ủi Quân Dân", "Thảo Thuyền Mượn Tên"],
                "alt_generals": ["ngo_chu_thai"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_trinh_pho",
                "name": "Trình Phổ",
                "bis_tactics": ["Thảo Thuyền Mượn Tên", "Quân Dân Khích Lệ"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Thịnh Khí Lăng Nhân", "Tam Thế Trận"],
                "alt_generals": ["ngo_luc_khang"]
            }
        ]
    },

    # 9. TRƯƠNG GIÁC TAM TIÊN QUẦN KHIÊN
    {
        "id": "meta_quan_khien_truong_giac",
        "name": "Tam Tiên Quần Khiên (Trương Giác - Vu Cát - Tả Từ)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Quần",
        "troop": "Khiên",
        "description": "Bộ ba Duyên phận Tam Tiên huyền thoại. Tả Từ ban né đòn 35%, Vu Cát mưa độc tạo môi trường Thủy Kích để Trương Giác giật sấm sét liên hoàn kèm tỷ lệ chấn nhiếp 100%.",
        "strengths": ["Duyên phận Tam Tiên tăng né tránh và thuộc tính", "Chấn nhiếp sấm sét liên tục", "Sát thương phép bùng nổ bất ngờ"],
        "weaknesses": ["Sợ Tất Trúng (Lăng Thống)", "Chỉ số Thống soái cơ bản hơi thấp"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "quan_truong_giac",
                "name": "Trương Giác",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Dũng Giả Đắc Tiền", "Lâm Điện Phong Âm", "Cốc Sát Nghiêm Túc"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "quan_vu_cat",
                "name": "Vu Cát",
                "bis_tactics": ["Phong Thỉ Trận", "Đằng Giáp Binh"],
                "sub_tactics": ["Hãm Trận Doanh", "Ngự Địch Bối Hợp", "Tạm Thời Tránh Mũi Nhọn"],
                "alt_generals": ["nguy_tao_thao"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "quan_ta_tu",
                "name": "Tả Từ",
                "bis_tactics": ["Thảo Thuyền Mượn Tên", "Quân Dân Khích Lệ"],
                "sub_tactics": ["An Ủi Quân Dân", "Bát Môn Kim Tỏa", "Cứu Binh Bí Quyết"],
                "alt_generals": ["quan_hoa_da"]
            }
        ]
    },

    # 10. THỤC THƯƠNG CỔ ĐIỂN (GIA CÁT - TRIỆU VÂN - TRƯƠNG PHI)
    {
        "id": "meta_thuc_thuong_co_dien",
        "name": "Thục Thương Hoàng Gia (Gia Cát Lượng - Triệu Vân - Trương Phi)",
        "tier": "T1",
        "season": "S1",
        "faction": "Thục",
        "troop": "Thương",
        "description": "Đội hình thống trị từ S1 đến S2. Gia Cát phản chiêu chủ động, Triệu Vân miễn mọi hiệu ứng xả sát thương vật lý, Trương Phi trừ giáp và khống chế tước khí.",
        "strengths": ["Cực kỳ ổn định", "Dễ build ngay từ S1", "Khắc chế mọi đội hình kỵ binh"],
        "weaknesses": ["Hiệu quả giảm dần ở các mùa PK"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_gia_cat_luong",
                "name": "Gia Cát Lượng",
                "bis_tactics": ["Đoạt Hồn Hiếp Phách", "Bát Môn Kim Tỏa"],
                "sub_tactics": ["Bạch Nhĩ Binh", "Cốc Sát Nghiêm Túc", "Ngự Địch Bối Hợp"],
                "alt_generals": ["thuc_luu_bi"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_trieu_van",
                "name": "Triệu Vân",
                "bis_tactics": ["Phá Trận Kiên Tồi", "Hoành Tảo Thiên Quân"],
                "sub_tactics": ["Lạc Phụng", "Dũng Giả Đắc Tiền", "Tuyệt Địa Phản Kích"],
                "alt_generals": ["thuc_quan_vu"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_truong_phi",
                "name": "Trương Phi",
                "bis_tactics": ["Thịnh Khí Lăng Nhân", "Lạc Phụng"],
                "sub_tactics": ["Túng Binh Kiếp Lược", "Hoành Tảo Thiên Quân", "Bạch Nhĩ Binh"],
                "alt_generals": ["thuc_ma_sieu"]
            }
        ]
    },

    # 11. NGỤY KỴ GIAN HÙNG (TÀO THÁO - TRƯƠNG LIÊU - HẠ HẦU UYÊN)
    {
        "id": "meta_nguy_ky_gian_hung",
        "name": "Ngụy Kỵ Bộc Đầu (Tào Tháo - Trương Liêu - Hạ Hầu Uyên)",
        "tier": "T0.5",
        "season": "S2",
        "faction": "Ngụy",
        "troop": "Kỵ",
        "description": "Đội hình chuyên săn đầu tướng đối phương. Trương Liêu và Hạ Hầu Uyên dồn toàn bộ sát thương đột kích thẳng vào chủ tướng địch, kết thúc trận đấu chỉ sau 2-3 lượt.",
        "strengths": ["Trảm chủ tướng bỏ qua 2 phó tướng", "Tốc độ chiến đấu cực nhanh"],
        "weaknesses": ["Gặp Thịnh Khí Lăng Nhân là tắt điện 2 hiệp đầu", "Sợ Đằng Giáp bảo vệ"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_truong_lieu",
                "name": "Trương Liêu",
                "bis_tactics": ["Nhất Đao Đương Thiên", "Quỷ Thần Đình Uy"],
                "sub_tactics": ["Bách Lăng Kỵ Tiệp", "Trảm Tướng Đoạt Kỳ", "Dũng Giả Đắc Tiền"],
                "alt_generals": ["nguy_ha_hau_uyen"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_tao_thao",
                "name": "Tào Tháo",
                "bis_tactics": ["Hổ Báo Kỵ", "Thiết Kỵ Siết Chặt"],
                "sub_tactics": ["Tây Lương Thiết Kỵ", "Phong Thỉ Trận", "Ngự Địch Bối Hợp"],
                "alt_generals": ["nguy_quach_gia"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_ha_hau_uyen",
                "name": "Hạ Hầu Uyên",
                "bis_tactics": ["Bách Lăng Kỵ Tiệp", "Tuyệt Địa Phản Kích"],
                "sub_tactics": ["Trảm Tướng Đoạt Kỳ", "Lạc Phụng", "Túng Binh Kiếp Lược"],
                "alt_generals": ["nguy_quach_gia", "nguy_nhan_luong"]
            }
        ]
    },

    # 12. SP GIA CÁT LƯỢNG THỤC KỲ (SP GIA CÁT - KHƯƠNG DUY - LƯU BỊ)
    {
        "id": "meta_sp_gia_cat_thuc_ky",
        "name": "Thục Trí SP (SP Gia Cát Lượng - Khương Duy - Bàng Thống)",
        "tier": "T0",
        "season": "PK",
        "faction": "Thục",
        "troop": "Cung",
        "description": "Phiên bản nâng cấp của Thục Cung khi thay Gia Cát thường bằng SP Gia Cát Lượng. SP Gia Cát có khả năng vừa tấn công vừa câm lặng và buff team, tạo ra áp lực tổng hợp cao hơn nhiều.",
        "strengths": ["Toàn diện hơn Thục Cung thường", "SP Gia Cát vừa tấn công vừa hỗ trợ", "Linh hoạt thích ứng nhiều tình huống"],
        "weaknesses": ["Cần SP Gia Cát Lượng - nhân vật hiếm"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_khuong_duy",
                "name": "Khương Duy",
                "bis_tactics": ["Đoạt Hồn Hiếp Phách", "Cốc Sát Nghiêm Túc"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Bát Môn Kim Tỏa", "Lạc Phụng"],
                "alt_generals": ["thuc_trieu_van"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_bang_thong",
                "name": "Bàng Thống",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Bạch Mi", "Lạc Phụng", "Hỏa Sí Nguyên Liêu"],
                "alt_generals": ["thuc_sp_phap_chinh"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_sp_gia_cat_luong",
                "name": "SP Gia Cát Lượng",
                "bis_tactics": ["Bát Môn Kim Tỏa", "Thảo Thuyền Mượn Tên"],
                "sub_tactics": ["An Ủi Quân Dân", "Tạm Thời Tránh Mũi Nhọn", "Quân Dân Khích Lệ"],
                "alt_generals": ["thuc_gia_cat_luong"]
            }
        ]
    },

    # 13. NGÔ THƯƠNG TÔN SÁCH (TÔN SÁCH - HOÀNG CÁI - LỖ TÚC)
    {
        "id": "meta_ngo_thuong_ton_sach",
        "name": "Ngô Thương Tiểu Bá (Tôn Sách - Hoàng Cái - Lỗ Túc)",
        "tier": "T0.5",
        "season": "S3",
        "faction": "Ngô",
        "troop": "Thương",
        "description": "Đội hình Ngô độc đáo dựa vào cơ chế Khổ Nhục Kế của Hoàng Cái. Khi Hoàng Cái tự thương sẽ phát động đòn thiêu đốt cực mạnh (2.5x sát thương Đằng Giáp), Tôn Sách tiên phong gánh đòn đầu, Lỗ Túc duy trì sinh lực đội.",
        "strengths": ["Cơ chế Khổ Nhục Kế độc đáo", "Khắc tinh của Đằng Giáp Binh", "Tôn Sách tiên phong miễn sát thương hiệp 1"],
        "weaknesses": ["Cần quản lý HP Hoàng Cái cẩn thận", "Có thể bị khai thác nếu đội địch biết cách"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_ton_sach",
                "name": "Tôn Sách",
                "bis_tactics": ["Phá Trận Kiên Tồi", "Hoành Tảo Thiên Quân"],
                "sub_tactics": ["Lạc Phụng", "Dũng Giả Đắc Tiền", "Trảm Tướng Đoạt Kỳ"],
                "alt_generals": ["ngo_thai_su_tu"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_hoang_cai",
                "name": "Hoàng Cái",
                "bis_tactics": ["Hỏa Sí Nguyên Liêu", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Thái Bình Đạo Pháp", "Cốc Sát Nghiêm Túc", "Bạch Mi"],
                "alt_generals": ["ngo_luc_ton"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_lo_tuc",
                "name": "Lỗ Túc",
                "bis_tactics": ["Thảo Thuyền Mượn Tên", "Bạch Nhĩ Binh"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "An Ủi Quân Dân", "Tạm Thời Tránh Mũi Nhọn"],
                "alt_generals": ["ngo_trinh_pho"]
            }
        ]
    },

    # 14. NGÔ KỴ TÔN QUYỀN (TÔN QUYỀN - THÁI SỬ TỪ - LỖ TÚC)
    {
        "id": "meta_ngo_kiem_ton_quyen",
        "name": "Ngô Kiếm Tôn Quyền (Tôn Quyền - Thái Sử Từ - Lỗ Túc)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Cung",
        "description": "Tôn Quyền khi tích đủ 5 tầng buff trở thành vị thần vô địch (Động sát + Phá trận + Liên kích + Tiên phong + Tất trúng). Thái Sử Từ giảm giáp và giải trừ buff Chỉ Huy/Bị Động của đối phương bằng Đương Phong Tồi Quyết.",
        "strengths": ["Khi Tôn Quyền tích đủ buff thì không ai cản nổi", "Đương Phong vô hiệu hóa Tư Mã Ý / Tào Tháo"],
        "weaknesses": ["Cần 2-3 hiệp tích lũy", "Thái Sử Từ bị tước khí thì Tôn Quyền chậm buff"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_ton_quyen",
                "name": "Tôn Quyền",
                "bis_tactics": ["Đương Phong Tồi Quyết", "Biến Pháp Yên Dân"],
                "sub_tactics": ["Nhất Đao Đương Thiên", "Quỷ Thần Đình Uy", "Bách Lăng Kỵ Tiệp"],
                "alt_generals": ["ngo_luc_ton"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_thai_su_tu",
                "name": "Thái Sử Từ",
                "bis_tactics": ["Cường Cung Bạo Thỉ", "Quyết Mệnh Liên Tiễn"],
                "sub_tactics": ["Lạc Phụng", "Túng Binh Kiếp Lược", "Cẩm Phàm Quân"],
                "alt_generals": ["ngo_chu_thai"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_lo_tuc",
                "name": "Lỗ Túc",
                "bis_tactics": ["Bát Môn Kim Tỏa", "An Ủi Quân Dân"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Thảo Thuyền Mượn Tên", "Tạm Thời Tránh Mũi Nhọn"],
                "alt_generals": ["ngo_trinh_pho"]
            }
        ]
    },

    # 15. NGỤY KỴ NGŨ MƯU THẦN (GIẢ HỦ - SP TUÂN ÚC - QUÁCH GIA)
    {
        "id": "meta_nguy_ky_ngu_muu_than",
        "name": "Ngụy Kỵ Ngũ Mưu Thần (Giả Hủ - SP Tuân Úc - Quách Gia)",
        "tier": "T0",
        "season": "PK",
        "faction": "Ngụy",
        "troop": "Kỵ",
        "description": "SP Tuân Úc tạo khiên phản khống chế, Giả Hủ gây hỗn loạn đối phương tự đánh lẫn nhau, Quách Gia kích hoạt chuỗi sát thương phép liên hoàn. Đội Ngụy ma thuật kỵ binh bá đạo nhất mùa PK.",
        "strengths": ["Phản đòn khống chế cực mạnh", "Hỗn loạn khiến mọi kẻ địch tự hủy", "Sát thương phép dày đặc"],
        "weaknesses": ["Phụ thuộc vào bảo vật và tướng đỏ sao để tối ưu"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_tuan_uc",
                "name": "SP Tuân Úc",
                "bis_tactics": ["Phản Kế Nguyên Mưu", "Thảo Thuyền Mượn Tên"],
                "sub_tactics": ["Tạm Thời Tránh Mũi Nhọn", "Ngự Địch Bối Hợp", "An Ủi Quân Dân"],
                "alt_generals": ["nguy_tao_thao"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_gia_hu",
                "name": "Giả Hủ",
                "bis_tactics": ["Đoạt Hồn Hiếp Phách", "Cốc Sát Nghiêm Túc"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Sĩ Biệt Tam Nhật", "Thái Bình Đạo Pháp"],
                "alt_generals": ["nguy_trinh_duc"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_quach_gia",
                "name": "Quách Gia",
                "bis_tactics": ["Đương Phong Tồi Quyết", "Biến Pháp Yên Dân"],
                "sub_tactics": ["Trảm Tướng Đoạt Kỳ", "Hổ Báo Kỵ", "Bách Lăng Kỵ Tiệp"],
                "alt_generals": ["nguy_trinh_duc", "nguy_sp_quach_gia"]
            }
        ]
    },

    # 16. NGÔ CUNG ĐÔ ĐỐC (SP CHU DU - LỤC TỐN - LỖ TÚC)
    {
        "id": "meta_ngo_cung_do_doc",
        "name": "Ngô Cung Đô Đốc (SP Chu Du - Lục Tốn - Lỗ Túc)",
        "tier": "T0.5",
        "season": "S3",
        "faction": "Ngô",
        "troop": "Cung",
        "description": "Duyên phận Đô Đốc Đông Ngô với SP Chu Du thiêu đốt + giật điện chấn nhiếp, Lục Tốn là cỗ máy thiêu rụi liên tục, Lỗ Túc bơm chỉ số khổng lồ. Khắc tinh tuyệt đối của Đằng Giáp Binh.",
        "strengths": ["Thiêu đốt vô địch, diệt Đằng Giáp 100%", "Duyên phận Đô Đốc tăng thuộc tính lớn"],
        "weaknesses": ["Sợ câm lặng hoặc tước khí sớm"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_sp_chu_du",
                "name": "SP Chu Du",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Cốc Sát Nghiêm Túc", "Lâm Điện Phong Âm", "Hỏa Sí Nguyên Liêu"],
                "alt_generals": ["ngo_chu_du"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_luc_ton",
                "name": "Lục Tốn",
                "bis_tactics": ["Đoạt Hồn Hiếp Phách", "Bạch Mã Nghĩa Tùng"],
                "sub_tactics": ["Bạch Mi", "Đương Phong Tồi Quyết", "Cốc Sát Nghiêm Túc"],
                "alt_generals": ["ngo_lu_mong"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_lo_tuc",
                "name": "Lỗ Túc",
                "bis_tactics": ["Bát Môn Kim Tỏa", "Thảo Thuyền Mượn Tên"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Tạm Thời Tránh Mũi Nhọn", "An Ủi Quân Dân"],
                "alt_generals": ["ngo_lu_mong", "ngo_trinh_pho"]
            }
        ]
    },

    # 17. THỤC KỴ CHẤN NHIẾP (KHƯƠNG DUY - QUAN NGÂN BÌNH - LƯU BỊ)
    {
        "id": "meta_thuc_ky_chan_nhiep",
        "name": "Thục Kỵ Khống Chế (Khương Duy - Quan Ngân Bình - Lưu Bị)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Thục",
        "troop": "Kỵ",
        "description": "Đội hình khống chế chấn nhiếp liên hoàn bậc nhất mùa PK. Quan Ngân Bình gắn hiệu ứng Tướng Môn Hổ Nữ kích hoạt chuỗi chấn nhiếp, Khương Duy gây sát thương nhiều nhịp liên tục, Lưu Bị duy trì sinh lực và hồi phục.",
        "strengths": ["Chấn nhiếp dày đặc đối thủ hầu như không được chơi", "Hồi phục dồi dào từ Lưu Bị", "Linh hoạt khai hoang và pvp"],
        "weaknesses": ["Sợ các đội có Động Sát (Triệu Vân, Quách Gia buff)"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_khuong_duy",
                "name": "Khương Duy",
                "bis_tactics": ["Đoạt Hồn Hiếp Phách", "Cốc Sát Nghiêm Túc"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Lạc Phụng", "Sĩ Biệt Tam Nhật"],
                "alt_generals": ["thuc_trieu_van"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_quan_ngan_binh",
                "name": "Quan Ngân Bình",
                "bis_tactics": ["Hoành Tảo Thiên Quân", "Cường Cung Bạo Thỉ"],
                "sub_tactics": ["Lạc Phụng", "Túng Binh Kiếp Lược", "Trảm Tướng Đoạt Kỳ"],
                "alt_generals": ["thuc_nguy_dien"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_luu_bi",
                "name": "Lưu Bị",
                "bis_tactics": ["Tượng Binh", "Thịnh Khí Lăng Nhân"],
                "sub_tactics": ["Tạm Thời Tránh Mũi Nhọn", "An Ủi Quân Dân", "Bát Môn Kim Tỏa"],
                "alt_generals": ["thuc_phap_chinh", "quan_ta_tu"]
            }
        ]
    },

    # 18. QUẦN CUNG SP KHỐNG CHẾ (SP VIÊN THIỆU - SP CHU TUẤN - ĐIÊU THUYỀN)
    {
        "id": "meta_quan_cung_sp",
        "name": "Quần Cung Khống Chế (SP Viên Thiệu - SP Chu Tuấn - Điêu Thuyền)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Quần",
        "troop": "Cung",
        "description": "SP Viên Thiệu tước khí ngay từ hiệp đầu bằng bắn tiễn tháp, SP Chu Tuấn gây sát thương chuẩn bỏ qua giáp, Điêu Thuyền gài bẫy hỗn loạn khiến đối thủ tự đánh đồng đội.",
        "strengths": ["Tước khí tự động", "Sát thương chuẩn ổn định", "Chi phí chiến pháp vừa phải"],
        "weaknesses": ["Thiếu khả năng dứt điểm sốc sát thương trong 1 hiệp"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "quan_sp_vien_thieu",
                "name": "SP Viên Thiệu",
                "bis_tactics": ["Lạc Phụng", "Cường Cung Bạo Thỉ"],
                "sub_tactics": ["Hoành Tảo Thiên Quân", "Phá Trận Kiên Tồi", "Túng Binh Kiếp Lược"],
                "alt_generals": ["quan_vien_thieu"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "quan_sp_chu_tuan",
                "name": "SP Chu Tuấn",
                "bis_tactics": ["Trí Lực Phản Kế", "Bát Môn Kim Tỏa"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Cốc Sát Nghiêm Túc", "Đoạt Hồn Hiếp Phách"],
                "alt_generals": ["quan_truong_giac"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "quan_dieu_thuyen",
                "name": "Điêu Thuyền",
                "bis_tactics": ["Thảo Thuyền Mượn Tên", "Quân Dân Khích Lệ"],
                "sub_tactics": ["An Ủi Quân Dân", "Ngự Địch Bối Hợp", "Bạch Mã Nghĩa Tùng"],
                "alt_generals": ["quan_ta_tu", "quan_hoa_da"]
            }
        ]
    },

    # 19. THỤC KỴ SP QUAN VŨ (SP QUAN VŨ - TRƯƠNG PHI - LƯU BỊ)
    {
        "id": "meta_thuc_sp_quan_vu",
        "name": "Thục Kỵ SP Quan Vũ (SP Quan Vũ - Trương Phi - Lưu Bị)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Thục",
        "troop": "Kỵ",
        "description": "SP Quan Vũ gây bạo kích vật lý liên kích cực lớn và buff Võ lực toàn đội, Trương Phi giảm giáp địch và khống chế, Lưu Bị duy trì sinh lực. Đội hình kỵ binh Thục linh hoạt nhất mùa PK.",
        "strengths": ["Buff Võ lực toàn đội từ SP Quan Vũ", "Liên kích bạo kích cực cao", "Cân bằng tấn công - phòng thủ"],
        "weaknesses": ["Sợ Tước Khí sớm làm tắt toàn bộ chuỗi liên kích"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_sp_quan_vu",
                "name": "SP Quan Vũ",
                "bis_tactics": ["Nhất Đao Đương Thiên", "Quỷ Thần Đình Uy"],
                "sub_tactics": ["Bách Lăng Kỵ Tiệp", "Dũng Giả Đắc Tiền", "Trảm Tướng Đoạt Kỳ"],
                "alt_generals": ["thuc_quan_vu"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_truong_phi",
                "name": "Trương Phi",
                "bis_tactics": ["Thịnh Khí Lăng Nhân", "Hoành Tảo Thiên Quân"],
                "sub_tactics": ["Lạc Phụng", "Phá Trận Kiên Tồi", "Túng Binh Kiếp Lược"],
                "alt_generals": ["thuc_nguy_dien", "thuc_quan_ngan_binh"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_luu_bi",
                "name": "Lưu Bị",
                "bis_tactics": ["Hãm Trận Doanh", "Tạm Thời Tránh Mũi Nhọn"],
                "sub_tactics": ["An Ủi Quân Dân", "Ngự Địch Bối Hợp", "Thảo Thuyền Mượn Tên"],
                "alt_generals": ["thuc_phap_chinh"]
            }
        ]
    },

    # 20. NGỤY CUNG SP HỦ (SP QUÁCH GIA - GIẢN PHỦ - TRÌNH DỤC)
    {
        "id": "meta_nguy_muu_than_sp",
        "name": "Ngụy Mưu Thần Cường Sát (SP Quách Gia - Giả Hủ - Trình Dục)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Ngụy",
        "troop": "Cung",
        "description": "Đội hình Ngụy Mưu Sĩ chuyên cấm hồi máu và hỗn loạn. SP Quách Gia dự đoán và phản chiến pháp địch, Giả Hủ gây hỗn loạn toàn diện, Trình Dục cấm hồi máu triệt tiêu đội trâu bò.",
        "strengths": ["Cấm hồi máu - khắc tinh đội phòng thủ", "Hỗn loạn phản kế không thể ngăn chặn"],
        "weaknesses": ["Cần SP Quách Gia hiếm", "Chỉ số Thống soái đội hơi thấp"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_sp_quach_gia",
                "name": "SP Quách Gia",
                "bis_tactics": ["Trí Lực Phản Kế", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Thái Bình Đạo Pháp", "Cốc Sát Nghiêm Túc", "Đoạt Hồn Hiếp Phách"],
                "alt_generals": ["nguy_quach_gia"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_gia_hu",
                "name": "Giả Hủ",
                "bis_tactics": ["Đoạt Hồn Hiếp Phách", "Phản Kế Nguyên Mưu"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Lâm Điện Phong Âm", "Bạch Mi"],
                "alt_generals": ["nguy_tao_pi"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_trinh_duc",
                "name": "Trình Dục",
                "bis_tactics": ["Bát Môn Kim Tỏa", "Ngự Địch Bối Hợp"],
                "sub_tactics": ["Thảo Thuyền Mượn Tên", "An Ủi Quân Dân", "Quân Dân Khích Lệ"],
                "alt_generals": ["nguy_tuan_uc"]
            }
        ]
    },

    # 21. KHAI HOANG THẦN TỐC (KHƯƠNG DUY - QUAN NGÂN BÌNH - THÁI SỬ TỪ)
    {
        "id": "meta_khai_hoang_khuong_quan_thai",
        "name": "Khai Hoang Thần Tốc (Khương Duy - Quan Ngân Bình - Thái Sử Từ)",
        "tier": "T0",
        "season": "PK",
        "faction": "Thục",
        "troop": "Kỵ",
        "description": "Đội hình mở mỏ đất 4, 5, 6 chuẩn chỉ bậc nhất mùa giải PK. Sát thương đa nhịp liên tục kích hoạt chấn nhiếp khiến quân canh mỏ không thể đánh trả, giảm thiểu tối đa hao hụt binh lực.",
        "strengths": ["Mở mỏ đất cấp 5, cấp 6 sớm nhất server", "Hao tổn lính cực thấp", "Chuyển đổi sang Thục Kỵ hoặc Thục Cung ở giai đoạn 20 Cost"],
        "weaknesses": ["Chỉ tối ưu trong 48 giờ mở đất đầu mùa"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_khuong_duy",
                "name": "Khương Duy",
                "bis_tactics": ["Cốc Sát Nghiêm Túc", "Đoạt Hồn Hiếp Phách"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Lạc Phụng"],
                "alt_generals": ["ngo_luc_ton"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_quan_ngan_binh",
                "name": "Quan Ngân Bình",
                "bis_tactics": ["Hoành Tảo Thiên Quân", "Thịnh Khí Lăng Nhân"],
                "sub_tactics": ["Lạc Phụng", "Túng Binh Kiếp Lược"],
                "alt_generals": ["thuc_truong_phi"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_thai_su_tu",
                "name": "Thái Sử Từ",
                "bis_tactics": ["Cường Cung Bạo Thỉ", "Trảm Tướng Đoạt Kỳ"],
                "sub_tactics": ["Lạc Phụng", "Cứu Binh Bí Quyết"],
                "alt_generals": ["quan_ta_tu", "thuc_hoang_nguyet_anh"]
            }
        ]
    },

    # 22. LỤC KHÁNG NGÔ PHÒNG THỦ (LỤC KHÁNG - LỖ TÚC - ĐINH PHỤNG)
    {
        "id": "meta_ngo_phong_thu_luc_khang",
        "name": "Ngô Khiên Phòng Thủ (Lục Kháng - Lỗ Túc - Đinh Phụng)",
        "tier": "T1",
        "season": "S3",
        "faction": "Ngô",
        "troop": "Khiên",
        "description": "Đội hình phòng thủ bền bỉ của Đông Ngô. Lục Kháng phản sát thương phép và giải buff địch, Lỗ Túc hồi phục và bơm chỉ số, Đinh Phụng trảm tướng và tăng tốc hành quân.",
        "strengths": ["Phòng thủ rất bền", "Giải trừ buff địch liên tục", "Hồi phục ổn định"],
        "weaknesses": ["Sát thương đầu ra không đủ mạnh để thắng đội T0"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_luc_khang",
                "name": "Lục Kháng",
                "bis_tactics": ["Đương Phong Tồi Quyết", "Phản Kế Nguyên Mưu"],
                "sub_tactics": ["Bát Môn Kim Tỏa", "Tạm Thời Tránh Mũi Nhọn", "An Ủi Quân Dân"],
                "alt_generals": ["ngo_lu_mong"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_lo_tuc",
                "name": "Lỗ Túc",
                "bis_tactics": ["Thảo Thuyền Mượn Tên", "Quân Dân Khích Lệ"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Cứu Binh Bí Quyết", "An Ủi Quân Dân"],
                "alt_generals": ["ngo_trinh_pho"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_ding_feng",
                "name": "Đinh Phụng",
                "bis_tactics": ["Trảm Tướng Đoạt Kỳ", "Lạc Phụng"],
                "sub_tactics": ["Túng Binh Kiếp Lược", "Hoành Tảo Thiên Quân", "Bạch Nhĩ Binh"],
                "alt_generals": ["ngo_cam_ning"]
            }
        ]
    },

    # 23. NGỤY KHIÊN SP ĐIỂN VI (SP ĐIỂN VI - TÀO NHÂN - HÁC CHIÊU)
    {
        "id": "meta_nguy_khien_sp_dien_vi",
        "name": "Ngụy Khiên SP Điển Vi (SP Điển Vi - Tào Nhân - Hác Chiêu)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Ngụy",
        "troop": "Khiên",
        "description": "Đội hình Ngụy phòng thủ phiên bản thay thế không cần Tư Mã Ý. SP Điển Vi đỡ toàn bộ sát thương 3 hiệp đầu và hồi phục theo đòn chịu, Tào Nhân khiêu khích và tăng giáp, Hác Chiêu gây sát thương kép lửa + vật lý.",
        "strengths": ["Không cần Tư Mã Ý vẫn rất bền", "SP Điển Vi đỡ đòn 3 hiệp đầu = miễn sát thương", "Hác Chiêu không sợ câm lặng"],
        "weaknesses": ["Đội tấn công yếu hơn bộ Tư Mã Ý"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_sp_dien_vi",
                "name": "SP Điển Vi",
                "bis_tactics": ["Phong Thỉ Trận", "Quân Hổ Vệ"],
                "sub_tactics": ["Hãm Trận Doanh", "Đằng Giáp Binh", "Tạm Thời Tránh Mũi Nhọn"],
                "alt_generals": ["nguy_dien_vi"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_tao_nhan",
                "name": "Tào Nhân",
                "bis_tactics": ["Quân Dân Khích Lệ", "An Ủi Quân Dân"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Thảo Thuyền Mượn Tên", "Cứu Binh Bí Quyết"],
                "alt_generals": ["nguy_ha_hau_don"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_hac_chieu",
                "name": "Hác Chiêu",
                "bis_tactics": ["Hỏa Sí Nguyên Liêu", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Thái Bình Đạo Pháp", "Bạch Mi", "Cốc Sát Nghiêm Túc"],
                "alt_generals": ["nguy_man_sung"]
            }
        ]
    },

    # 24. HOÀNG CÁI QUẦN KHỔNG NHỤC KẾ (HOÀNG CÁI - TRƯƠNG GIÁC - TÀO THÁO)
    {
        "id": "meta_tam_the_hoang_cai_truong_giac",
        "name": "Tam Thế Hoả Thiêu (Hoàng Cái - Trương Giác - Tào Tháo)",
        "tier": "T0.5",
        "season": "PK",
        "faction": "Tam Thế",
        "troop": "Thương",
        "description": "Bộ ba liên phe tận dụng Tam Thế Trận. Hoàng Cái kích hoạt thiêu đốt Khổ Nhục Kế, Trương Giác sấm sét chấn nhiếp, Tào Tháo buff sát thương và hồi phục đội. Đội hình liên phe linh hoạt hàng đầu.",
        "strengths": ["Tam Thế Trận tăng hiệu quả các chiến pháp chủ động", "Thiêu đốt + sét phối hợp ép liên tục", "Rất linh hoạt không bị trói buộc phe phái"],
        "weaknesses": ["Các tướng đơn lẻ không đủ mạnh nếu thiếu Tam Thế Trận"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_hoang_cai",
                "name": "Hoàng Cái",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật"],
                "sub_tactics": ["Hỏa Sí Nguyên Liêu", "Cốc Sát Nghiêm Túc", "Bạch Mi"],
                "alt_generals": ["ngo_luc_ton"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "quan_truong_giac",
                "name": "Trương Giác",
                "bis_tactics": ["Lâm Điện Phong Âm", "Đoạt Hồn Hiếp Phách"],
                "sub_tactics": ["Phản Kế Nguyên Mưu", "Trí Lực Phản Kế", "Cốc Sát Nghiêm Túc"],
                "alt_generals": ["quan_vu_cat"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_tao_thao",
                "name": "Tào Tháo",
                "bis_tactics": ["Tam Thế Trận", "An Ủi Quân Dân"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Thảo Thuyền Mượn Tên", "Tạm Thời Tránh Mũi Nhọn"],
                "alt_generals": ["thuc_luu_bi"]
            }
        ]
    },

    # 25. ĐẶNG NGẢI KỲ TẬP (ĐẶNG NGẢI - TRƯƠNG LIÊU - TÀO THÁO)
    {
        "id": "meta_nguy_dac_biet_dang_ngai",
        "name": "Ngụy Kỵ Kỳ Tập (Đặng Ngải - Trương Liêu - Tào Tháo)",
        "tier": "T0.5",
        "season": "S3",
        "faction": "Ngụy",
        "troop": "Kỵ",
        "description": "Đội hình tập kích đột phá của Ngụy thời S3. Đặng Ngải với kỹ năng Đảm Trí Dũng Kiêm tập kích hiểm hóc, Trương Liêu trảm chủ tướng, Tào Tháo buff sát thương và tăng tốc.",
        "strengths": ["Cơ chế tập kích bất ngờ độc đáo", "Tốc độ và sát thương cân bằng"],
        "weaknesses": ["Meta hiện tại ở mùa PK có đối thủ mạnh hơn"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_duc_luong",
                "name": "Đặng Ngải",
                "bis_tactics": ["Nhất Đao Đương Thiên", "Quỷ Thần Đình Uy"],
                "sub_tactics": ["Bách Lăng Kỵ Tiệp", "Dũng Giả Đắc Tiền", "Trảm Tướng Đoạt Kỳ"],
                "alt_generals": ["nguy_truong_lieu"]
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_truong_lieu",
                "name": "Trương Liêu",
                "bis_tactics": ["Hổ Báo Kỵ", "Tây Lương Thiết Kỵ"],
                "sub_tactics": ["Bách Lăng Kỵ Tiệp", "Trảm Tướng Đoạt Kỳ", "Cường Cung Bạo Thỉ"],
                "alt_generals": ["nguy_ha_hau_uyen"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_tao_thao",
                "name": "Tào Tháo",
                "bis_tactics": ["Phong Thỉ Trận", "An Ủi Quân Dân"],
                "sub_tactics": ["Ngự Địch Bối Hợp", "Tạm Thời Tránh Mũi Nhọn", "Thảo Thuyền Mượn Tên"],
                "alt_generals": ["nguy_quach_gia"]
            }
        ]
    },

    # ================================================================
    # ĐỘI HÌNH META MỚI - TRÍCH XUẤT TỪ 98 ẢNH QUÉT
    # ================================================================

    # 26. TRƯƠNG PHI HẠCH ĐẠN CUNG
    {
        "id": "meta_truong_phi_hach_dan_cung",
        "name": "Trương Phi Hạch Đạn Cung (Chu Thái - Trương Phi SP - SP Chu Tuấn)",
        "tier": "T1",
        "season": "PK",
        "faction": "Thục",
        "troop": "Cung",
        "description": "Đội hình Cung ăn vạ nổi tiếng. Trương Phi SP mang Tiêm Long Trận + Thịnh Khí Linh Địch + Vô Địch Can Trường làm core. Phối hợp [Kiêm Tu] + [Mùi Định] + [Phá Quân] + [Trí Tuyệt] là combo sát thương đỉnh cao.",
        "strengths": ["Ăn vạ xuyên phòng ngự địch", "Kết hợp [Phá Quân] bỏ qua % phòng thủ", "Đội hình bùng nổ kinh điển"],
        "weaknesses": ["Cần bộ chiến pháp ăn vạ đặc biệt", "Sợ đội khống chế sớm"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_chu_thai",
                "name": "Chu Thái",
                "bis_tactics": ["Tiêm Long Trận", "Thịnh Khí Linh Địch"],
                "sub_tactics": ["Thống Soái - Biết Cách Phòng Thủ", "Thể Phòng Thủ - Khép Hờ", "Phòng Bị - Khích Lệ Lòng Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_truong_phi",
                "name": "Trương Phi (Chính Lệnh - Cung S)",
                "bis_tactics": ["Gió Táp Mưa Sa", "Vô Địch Can Trường"],
                "sub_tactics": ["Võ Lực - Lấy Lùi Làm Tiến", "Tinh Chuẩn", "Trì Trọng"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "quan_sp_chu_tuan",
                "name": "SP Chu Tuấn",
                "bis_tactics": ["Tinh Vô Đương - Bạch Mã Nghĩa Tùng", "Thái Bình Đạo Pháp", "Thiêu Đốt Doanh Lũy"],
                "sub_tactics": ["Trí Lực - Lấy Lùi Làm Tiến", "Tinh Chuẩn", "Trì Trọng"],
                "alt_generals": []
            }
        ]
    },

    # 27. LỮ QUÁCH KIỀU (LỮ BỐ 40TH - QUÁCH GIA - VÔ SONG TIỂU KIỀU)
    {
        "id": "meta_lu_quach_kieu",
        "name": "Lữ Quách Kiều (Lữ Bố 40th - Quách Gia - Vô Song Tiểu Kiều)",
        "tier": "T0",
        "season": "PK",
        "faction": "Quần",
        "troop": "Cung",
        "description": "Đội hình nổ dame cực mạnh. Vô Song Tiểu Kiều mang [Tinh Bạch Mã Nghĩa Tùng] gây hỗn loạn diện rộng, Quách Gia Tam Thế Trận + Lửa Lan Khắp Chốn tăng kích hoạt, Lữ Bố 40th cung cấp đầu ra sát thương. Combo [Tật Trì] + [Tập Võ] + [Linh Quang] + [Cứu Chiến] bùng nổ cực mạnh.",
        "strengths": ["Hỗn loạn diện rộng tê liệt địch", "Combo Cứu Chiến hủy giới hạn Tiến Công Trước", "Sát thương bùng nổ cực nhanh"],
        "weaknesses": ["Cần vô song Kiều mới đạt T0", "Sợ đội phòng thủ chắc"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "quan_lu_bo_40",
                "name": "Lữ Bố 40th (Quân Sư)",
                "bis_tactics": ["Loan Cung Âm Vũ", "Phá Giáp"],
                "sub_tactics": ["Võ Lực", "Đánh Bất Ngờ Thắng", "Trì Trọng", "Tinh Chuẩn"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_quach_gia",
                "name": "Quách Gia",
                "bis_tactics": ["Tam Thế Trận", "Lửa Lan Khắp Chốn"],
                "sub_tactics": ["Nửa Trí Nửa Thống", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_vo_song_tieu_kieu",
                "name": "Vô Song Tiểu Kiều",
                "bis_tactics": ["Tinh Bạch Mã Nghĩa Tùng", "Văn Võ Song Toàn"],
                "sub_tactics": ["Võ Lực", "Lấy Lùi Làm Tiến", "Tinh Chuẩn", "Trì Trọng"],
                "alt_generals": []
            }
        ]
    },

    # 28. ĐÔ ĐỐC CUNG CHU DU LỤC TỐN
    {
        "id": "meta_do_doc_cung_chu_du_luc_ton",
        "name": "Đô Đốc Cung - Chuyển Bạch Nhị Binh (Chu Du - Lục Tốn - SP Lữ Mông)",
        "tier": "T1",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Cung",
        "description": "Đội hình Cung pháp sư Ngô. Chu Du Đoạt Hồn Hiệp Phách cướp chỉ số địch, Lục Tốn Đồng Lòng Hợp Sức + Tinh Nhanh Trí Động Não nâng phép, SP Lữ Mông Nhạn Hình Trận + Thuyền Cò Mượn Tên hỗ trợ. Chuyển Bạch Nhị Binh cộng thêm đòn phép mỗi đánh thường.",
        "strengths": ["Đòn phép liên tục mỗi đánh thường", "Cướp chỉ số địch liên tục", "Duyên phận Ngô Cung rất mạnh"],
        "weaknesses": ["Cần SP Lữ Mông để tối ưu", "Sợ đội vật lý áp đảo nhanh"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_chu_du",
                "name": "Chu Du",
                "bis_tactics": ["Đoạt Hồn Hiệp Phách", "Thiêu Đốt Doanh Lũy"],
                "sub_tactics": ["Trí Lực", "Tam Quân Chi Chúng", "Mưu Kế Sâu Xa", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_luc_ton",
                "name": "Lục Tốn",
                "bis_tactics": ["Đồng Lòng Hợp Sức", "Chuyển Bạch Nhị Binh"],
                "sub_tactics": ["Trí Lực", "Đánh Sau Trúng Trước", "Tinh Chuẩn", "Khai Hạp"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_sp_lu_mong",
                "name": "SP Lữ Mông",
                "bis_tactics": ["Nhạn Hình Trận", "Thuyền Cò Mượn Tên"],
                "sub_tactics": ["Thống Soái", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            }
        ]
    },

    # 29. NGÔ NỮ HỔ BÁO KỴ (VÔ SONG ĐẠI KIỀU - TÔN THƯỢNG HƯƠNG - VÔ SONG TIỂU KIỀU)
    {
        "id": "meta_ngo_nu_ho_bao_ky",
        "name": "Ngô Nữ Hổ Báo Kỵ (Vô Song Đại Kiều - Tôn Thượng Hương - Vô Song Tiểu Kiều)",
        "tier": "T0",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Cung",
        "description": "Đội hình Ngô Nữ Cung kết hợp Hổ Báo Kỵ tinh. Đại Kiều Mê Hoặc + Thuyền Cò Mượn Tên Thống soái cao, Tôn Thượng Hương Đường Phong Thôi Quyết + Mau Giành Lợi Thế tấn công tốc chiến, Tiểu Kiều Tinh Hổ Báo Kỵ + Lâm Nguy Cứu Chủ hỗ trợ. Combo [Thần Hành] + [Thao Luyện] + [Diên Ích] + [Trọng Thương].",
        "strengths": ["Hỗn loạn + Kinh Hồng combo cực mạnh", "Tinh Hổ Báo Kỵ bạo kích liên tục", "Đội hình duyên phận Ngô Nữ"],
        "weaknesses": ["Cần vô song Kiều", "Sợ đội khống chế sớm Tước Khí"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_vo_song_dai_kieu",
                "name": "Vô Song Đại Kiều",
                "bis_tactics": ["Mê Hoặc", "Thuyền Cò Mượn Tên"],
                "sub_tactics": ["Thống Soái - Nhìn Rõ Mòn Một", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_ton_thuong_huong",
                "name": "Tôn Thượng Hương",
                "bis_tactics": ["Đường Phong Thôi Quyết", "Mau Giành Lợi Thế"],
                "sub_tactics": ["Võ Lực - Kinh Hồng - Lấy Võ Đẹp Loan", "Thắng Trận", "Thần Cơ", "Tướng Uy"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_vo_song_tieu_kieu",
                "name": "Vô Song Tiểu Kiều",
                "bis_tactics": ["Tinh Hổ Báo Kỵ", "Lâm Nguy Cứu Chủ"],
                "sub_tactics": ["Võ Lực / Thống Soái - Chẩm Qua Tọa Giáp", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            }
        ]
    },

    # 30. THỤC TRÍ PHI HÙNG CUNG (BÀNG THỐNG - GIA CÁT LƯỢNG - SP PHÁP CHÍNH)
    {
        "id": "meta_thuc_tri_phi_hung_cung",
        "name": "Thục Trí Phi Hùng Cung (Bàng Thống - Gia Cát Lượng - SP Pháp Chính)",
        "tier": "T0",
        "season": "PK",
        "faction": "Thục",
        "troop": "Cung",
        "description": "Đội hình pháp sư tốc độ cực cao meta PK. SP Pháp Chính Tinh Phi Hùng Quân kích hoạt chiêu gần như mỗi hiệp, Gia Cát Lượng Thần Cơ Diệu Toán ngắt chiêu, Bàng Thống Liên Hoàn Kế nối xích pháp sư. Binh chủng cải tạo Cung Cong + Phá Địch + Phò Thương + Trút Xuống.",
        "strengths": ["Kích hoạt chiêu cực nhanh", "Combo pháp sư Thục vô đối", "Ngắt chiêu địch đồng thời tung chiêu bản thân"],
        "weaknesses": ["Cần SP Pháp Chính + bộ chiến pháp đắt tiền", "Sợ đội vật lý bộc phát nhanh"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_bang_thong",
                "name": "Bàng Thống",
                "bis_tactics": ["Thái Bình Đạo Pháp", "Thiêu Đốt Doanh Lũy"],
                "sub_tactics": ["Tam Quân Chi Chúng", "Quy Thuận", "Mưu Kế Sâu Xa", "Văn Thao"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_gia_cat_luong",
                "name": "Gia Cát Lượng",
                "bis_tactics": ["Đường Phong Thôi Quyết", "Đồng Lòng Hợp Sức"],
                "sub_tactics": ["Kỳ Chính Tương Sinh", "Giấu Đao", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_sp_phap_chinh",
                "name": "SP Pháp Chính",
                "bis_tactics": ["Tinh Phi Hùng Quân", "Tinh Nhanh Trí Động Não"],
                "sub_tactics": ["Tam Quân Chi Chúng", "Dẫn Quân", "Rèn Luyện"],
                "alt_generals": []
            }
        ]
    },

    # 31. HOÀNG MÃ GIẢI PHIỀN VỆ (SP MÃ SIÊU - SP HOÀNG PHỦ TUNG - HỨA DU)
    {
        "id": "meta_hoang_ma_giai_phien_ve",
        "name": "Hoàng Mã Giải Phiền Vệ (SP Mã Siêu - SP Hoàng Phủ Tung - Hứa Du)",
        "tier": "T0+",
        "season": "PK",
        "faction": "Thục",
        "troop": "Kỵ",
        "description": "Đội hình T0 mạnh nhất meta PK. SP Mã Siêu Đường Phong Thôi Quyết + Thôi Phong Đoạn Nhẫn gây sát thương Võ Lực kép, SP Hoàng Phủ Tung Thuyền Cò Mượn Tên + Vạn Quân Đoạt Sư Thống Soái cực cao, Hứa Du Lâm Nguy Cứu Chủ + Tinh Giải Phiền Vệ. Cải tạo [Tinh Nghiên] + [Võ Khôi] + [Cứu Viện] + [Quân Tâm].",
        "strengths": ["Sát thương vật lý cực khủng từ Võ Lực", "Hứa Du giải trừ debuff và hồi máu", "Đội hình đắt nhất và mạnh nhất PK"],
        "weaknesses": ["Cần SP Mã Siêu + SP Hoàng Phủ Tung mới T0", "Tốn kém nhất game"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_sp_ma_sieu",
                "name": "SP Mã Siêu",
                "bis_tactics": ["Đường Phong Thôi Quyết", "Thôi Phong Đoạn Nhẫn"],
                "sub_tactics": ["Tấn Công Điểm Yếu", "Tốc Chiến", "Khép Hờ"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_sp_hoang_phu_tung",
                "name": "SP Hoàng Phủ Tung",
                "bis_tactics": ["Thuyền Cò Mượn Tên", "Vạn Quân Đoạt Sư"],
                "sub_tactics": ["Đánh Giá Tình Hình", "Khai Hạp", "Chia Lời"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "quan_hua_du",
                "name": "Hứa Du (Thưởng S)",
                "bis_tactics": ["Lâm Nguy Cứu Chủ", "Tinh Giải Phiền Vệ"],
                "sub_tactics": ["Tam Quân Chi Chúng", "Dẫn Quân", "Rèn Luyện"],
                "alt_generals": []
            }
        ]
    },

    # 32. PHÁP QUAN KHIÊN - TINH LĨNH GIÁP MÂY
    {
        "id": "meta_phap_quan_khien",
        "name": "Pháp Quan Khiên - Tinh Lĩnh Giáp Mây (SP Quan Vũ - Mã Đại CO Tinh Thái - SP Pháp Chính)",
        "tier": "T0",
        "season": "PK",
        "faction": "Thục",
        "troop": "Khiên",
        "description": "Đội hình phòng thủ kiên cố nhất Thục. Mã Đại/CO Tinh Thái Tinh Lĩnh Giáp Mây tăng giảm sát thương cực cao, SP Quan Vũ Lấy Ít Đánh Nhiều + Gió Táp Mưa Sa gây sát thương, SP Pháp Chính Không Đánh Mà Thắng bảo vệ. Combo [Nhẫn Nại] + [Giáp Mây] + [Miễn Dịch] + [Rắn Chắc].",
        "strengths": ["Giảm sát thương Binh dao cực mạnh", "Chống đốt cháy hiệu quả", "Phòng thủ bền vững nhất Thục"],
        "weaknesses": ["Cần CO Tinh Thái hoặc Mã Đại", "Sát thương đầu ra thấp hơn các đội T0 khác"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_sp_quan_vu",
                "name": "SP Quan Vũ",
                "bis_tactics": ["Lấy Ít Đánh Nhiều", "Gió Táp Mưa Sa"],
                "sub_tactics": ["Võ Lực", "Chia Nhỏ Đánh Nhanh", "Trăm Trận", "Khép Hờ"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_co_tinh_thai",
                "name": "Mã Đại/CO Tinh Thái",
                "bis_tactics": ["Ngư Lân Trận", "Tinh Lĩnh Giáp Mây"],
                "sub_tactics": ["Thống Soái", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_sp_phap_chinh",
                "name": "SP Pháp Chính",
                "bis_tactics": ["Không Đánh Mà Thắng", "Dưỡng Sức Đợi Chiến"],
                "sub_tactics": ["Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            }
        ]
    },

    # 33. THÁI SƯ CUNG (SP ĐỔNG TRÁC - SP LÔ TRỰC - SP ĐIÊU THUYỀN)
    {
        "id": "meta_thai_su_cung",
        "name": "Thái Sư Cung - Chuyển Phi Hùng Cung (SP Đổng Trác - SP Lô Trực - SP Điêu Thuyền)",
        "tier": "T0",
        "season": "PK",
        "faction": "Quần",
        "troop": "Cung",
        "description": "Đội hình Cung Quần Hùng với SP Đổng Trác Chuyển Phi Hùng Quân + Thưởng Binh Phạt Mưu Thống Soái cực cao, SP Lô Trực Nhạn Hình Trận + Cường Nhu Kết Hợp bảo vệ, SP Điêu Thuyền Thâm Tàng Nhược Hư + Đồng Lòng Hợp Sức Trí Lực. Combo [Chuyển Cung] + [Phá Địch] + [Phò Thương] + [Quân Lực].",
        "strengths": ["Thống Soái cao nhất game", "Trị liệu và phòng thủ tốt", "Lượng trị liệu và sinh tồn đỉnh"],
        "weaknesses": ["Cần 3 SP quý hiếm", "Khó lắp ráp cho người mới"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_sp_dong_trac",
                "name": "SP Đổng Trác",
                "bis_tactics": ["Chuyển Phi Hùng Quân", "Thưởng Binh Phạt Mưu"],
                "sub_tactics": ["Thống Soái", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_sp_lo_truc",
                "name": "SP Lô Trực",
                "bis_tactics": ["Nhạn Hình Trận", "Cường Nhu Kết Hợp"],
                "sub_tactics": ["Thống Soái", "Tam Quân Chi Chúng", "Cứu Chiến", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_sp_dieu_thuyen",
                "name": "SP Điêu Thuyền",
                "bis_tactics": ["Thâm Tàng Nhược Hư", "Đồng Lòng Hợp Sức"],
                "sub_tactics": ["Trí Lực", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            }
        ]
    },

    # 34. LỮ BỐ 40TH QUẦN CUNG - TINH QUÂN CẨM PHÀM
    {
        "id": "meta_lu_bo_40_quan_cung",
        "name": "Lữ Bố 40th Quần Cung - Tinh Quân Cẩm Phàm (Cam Ninh - Lữ Bố 40th - Hứa Du)",
        "tier": "T1",
        "season": "PK",
        "faction": "Quần",
        "troop": "Cung",
        "description": "Cam Ninh Tinh Quân Cẩm Phàm + Thuyền Cò Mượn Tên Lệnh Đăng Ung chuyển Phê Quản, Lữ Bố 40th Dẫn Huyền Lực Chiến + Huyết Đao Tranh Giành sát thương thường, Hứa Du Lâm Nguy Cứu Chủ + Nhạn Hình Trận hỗ trợ. Combo [Thần Xạ] + [Dũng Võ] + [Ngăn Chặn] + [Doanh Khiếu].",
        "strengths": ["Cẩm Phàm Quân hồi máu khi đánh thường", "Sát thương tần suất cao", "Tốt cho khai hoang"],
        "weaknesses": ["Sức bùng nổ thấp hơn T0", "Phụ thuộc vào Cam Ninh Lệnh Đăng Ung"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_cam_ninh",
                "name": "Cam Ninh (Lệnh Đăng Ung Chuyển Quản)",
                "bis_tactics": ["Thuyền Cò Mượn Tên", "Tinh Quân Cẩm Phàm"],
                "sub_tactics": ["Võ Lực / Thống Soái", "Thích Làm Việc Thiện", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "quan_lu_bo_40",
                "name": "Lữ Bố 40th",
                "bis_tactics": ["Dẫn Huyền Lực Chiến", "Huyết Đao Tranh Giành"],
                "sub_tactics": ["Võ Lực", "Thắng Càng Mạnh", "Võ Lược", "Cầm Binh Khí"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "quan_hua_du",
                "name": "Hứa Du",
                "bis_tactics": ["Lâm Nguy Cứu Chủ", "Nhạn Hình Trận"],
                "sub_tactics": ["Trí Lực", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            }
        ]
    },

    # 35. HUY QUÂN KẾT TRẬN (LƯU BỊ - QUAN VŨ - TRƯƠNG PHI)
    {
        "id": "meta_huy_quan_ket_tran",
        "name": "Huy Quân Kết Trận Thục Tam Anh (Lưu Bị - Quan Vũ - Trương Phi)",
        "tier": "T1",
        "season": "S1",
        "faction": "Thục",
        "troop": "Khiên",
        "description": "Đội hình Thục Tam Anh cổ điển. Quan Vũ mang Huy Quân Kết Trận tăng 16% kích hoạt chiêu chủ động dựa vào Võ Lực cao, Trương Phi Vô Địch Can Trường + Kích Kỳ Nọa Quy tăng sát thương, Lưu Bị Hãm Trận Doanh + Cắt Xương Trị Độc trị liệu và giải khống. Phù hợp người mới.",
        "strengths": ["Dễ xây dựng", "Tự hỗ trợ toàn diện", "Ổn định qua nhiều giai đoạn"],
        "weaknesses": ["Đã lỗi thời ở meta PK", "Sức bùng nổ không đủ đánh T0"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_luu_bi",
                "name": "Lưu Bị",
                "bis_tactics": ["Hãm Trận Doanh", "Cắt Xương Trị Độc"],
                "sub_tactics": ["Trí Lực", "Tấn Công Điểm Yếu", "Khép Hờ", "Khích Lệ Lòng Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_quan_vu",
                "name": "Quan Vũ (Kỳ Năng Quân Sư)",
                "bis_tactics": ["Uy Mưu Võ Địch", "Huy Quân Kết Trận"],
                "sub_tactics": ["Võ Lực", "Đánh Sau Trúng Trước", "Quỷ Mưu", "Tướng Uy"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_truong_phi",
                "name": "Trương Phi",
                "bis_tactics": ["Vô Địch Can Trường", "Kích Kỳ Nọa Quy/Gió Táp Mưa Sa"],
                "sub_tactics": ["Võ Lực", "Dị Trực Báo Oán", "Tinh Chuẩn", "Thiện Chiến"],
                "alt_generals": []
            }
        ]
    },

    # 36. BẮC PHẠT KHIÊN (SP GIA CÁT LƯỢNG - QUAN HƯNG/QUAN VŨ - TRƯƠNG BẢO)
    {
        "id": "meta_bac_phat_khien",
        "name": "Bắc Phạt Khiên - Tinh Quân Hổ Vệ (SP Gia Cát Lượng - Quan Hưng - Trương Bảo)",
        "tier": "T1",
        "season": "PK",
        "faction": "Thục",
        "troop": "Khiên",
        "description": "Đội hình Bắc Phạt kiên cố. SP Gia Cát Lượng Tinh Quân Hổ Vệ + Dưỡng Sức Đợi Chiến Thống Soái cao, Quan Hưng/Quan Vũ Cuỡi Ngựa Nghìn Dặm + Văn Võ Song Toàn/Gió Táp Mưa Sa Võ Lực, Trương Bảo Xông Pha Khói Lửa + Không Đánh Mà Thắng phòng thủ. Combo [Đồng Lòng] + [Thiện Chiến] + [Làm Phản] + [Võ Khôi].",
        "strengths": ["Hỗ trợ cả tấn công lẫn phòng thủ", "Mở rộng phạm vi kích hoạt", "Toàn diện cho mọi giai đoạn"],
        "weaknesses": ["Sức bùng nổ thấp hơn Kỵ binh T0", "Cần SP Gia Cát Lượng"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "thuc_sp_gia_cat_luong",
                "name": "SP Gia Cát Lượng (Chính Lệnh Khiên S)",
                "bis_tactics": ["Tinh Quân Hổ Vệ", "Dưỡng Sức Đợi Chiến"],
                "sub_tactics": ["Thống Soái", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "thuc_quan_hung",
                "name": "Quan Hưng/Quan Vũ",
                "bis_tactics": ["Cuỡi Ngựa Nghìn Dặm", "Văn Võ Song Toàn/Gió Táp Mưa Sa"],
                "sub_tactics": ["Võ Lực", "Đánh Sau Trúng Trước", "Quỷ Mưu", "Tướng Uy"],
                "alt_generals": ["thuc_quan_vu"]
            },
            {
                "position": "Phó tướng 2",
                "general_id": "thuc_truong_bao",
                "name": "Trương Bảo",
                "bis_tactics": ["Xông Pha Khói Lửa", "Không Đánh Mà Thắng"],
                "sub_tactics": ["Thống Soái", "Chẩm Qua Tọa Giáp", "Dẫn Quân", "Rèn Luyện"],
                "alt_generals": []
            }
        ]
    },

    # 37. NGŨ MƯU THẦN BẠCH NHĨ CUNG (SP TUÂN ÚC - SP QUÁCH GIA - GIẢ HỦ)
    {
        "id": "meta_ngu_muu_than_bach_nhi_cung",
        "name": "Ngũ Mưu Thần Bạch Nhị Cung (SP Tuân Úc - SP Quách Gia - Giả Hủ)",
        "tier": "T0",
        "season": "PK",
        "faction": "Ngụy",
        "troop": "Cung",
        "description": "Đội hình mưu sĩ Ngụy T0 siêu mạnh. SP Tuân Úc Chuyển Bạch Nhĩ Binh + Cắt Xương Trị Độc, SP Quách Gia Đoạt Hồn Hiệp Phách + Đường Phong Thôi Quyết tăng Trí, Giả Hủ Nhanh Trí Động Não + Thưởng Binh Phạt Mưu. Combo [Chuyển Cung] + [Thành Thạo] + [Lưỡng Nghi] + [Bút Đao].",
        "strengths": ["Đòn phép liên tục từ Bạch Nhĩ Binh", "Trí lực 3 tướng cực cao", "Combo mưu sĩ Ngụy vô đối"],
        "weaknesses": ["Cần SP Tuân Úc + SP Quách Gia", "Sợ đội vật lý tốc chiến"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "nguy_sp_tuan_uc",
                "name": "SP Tuân Úc (Chính Lệnh Toàn S)",
                "bis_tactics": ["Chuyển Bạch Nhĩ Binh", "Cắt Xương Trị Độc"],
                "sub_tactics": ["Trí Lực", "Tam Quân Chi Chúng", "Dẫn Quân", "Rèn Luyện"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "nguy_sp_quach_gia",
                "name": "SP Quách Gia (Cung S)",
                "bis_tactics": ["Đoạt Hồn Hiệp Phách", "Đường Phong Thôi Quyết"],
                "sub_tactics": ["Kỳ Chính Tương Sinh", "Giấu Đao", "Văn Thao"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "nguy_gia_hu",
                "name": "Giả Hủ",
                "bis_tactics": ["Nhanh Trí Động Não", "Thưởng Binh Phạt Mưu"],
                "sub_tactics": ["Trí Lực", "Tam Quân Chi Chúng", "Dẫn Quân", "Rèn Luyện"],
                "alt_generals": []
            }
        ]
    },

    # 38. KHẢNG KHÁI CUNG - TINH QUÂN CẨM PHÀM (CAM NINH - THÁI SỬ TỪ - SP LỮ MÔNG)
    {
        "id": "meta_khang_khai_cung",
        "name": "Khảng Khái Cung - Tinh Quân Cẩm Phàm (Cam Ninh - Thái Sử Từ - SP Lữ Mông)",
        "tier": "T1",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Cung",
        "description": "Đội hình Cung Ngô sát thương thường mạnh. Cam Ninh Tinh Quân Cẩm Phàm Chuyển Phê Quản, Thái Sử Từ Đường Phong Thôi Quyết + Thôi Phong Đoạn Nhẫn Võ Lực, SP Lữ Mông Lâm Nguy Cứu Chủ + Nhạn Hình Trận. Combo [Thần Xạ] + [Dũng Võ] + [Ngăn Chặn] + [Doanh Khiếu].",
        "strengths": ["Sát thương thường liên tục cao", "Tần suất đánh nhanh", "Hồi phục thông qua Cẩm Phàm"],
        "weaknesses": ["Đòn bùng nổ thấp hơn T0", "Phụ thuộc Cam Ninh Lệnh Đăng Ung"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_cam_ninh",
                "name": "Cam Ninh",
                "bis_tactics": ["Thuyền Cò Mượn Tên", "Tinh Quân Cẩm Phàm"],
                "sub_tactics": ["Võ Lực / Thống Soái", "Thích Làm Việc Thiện", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_thai_su_tu",
                "name": "Thái Sử Từ",
                "bis_tactics": ["Đường Phong Thôi Quyết", "Thôi Phong Đoạn Nhẫn"],
                "sub_tactics": ["Võ Lực", "Thắng Càng Mạnh", "Võ Lược", "Cầm Binh Khí"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_sp_lu_mong",
                "name": "SP Lữ Mông",
                "bis_tactics": ["Lâm Nguy Cứu Chủ", "Nhạn Hình Trận"],
                "sub_tactics": ["Thống Soái", "Tam Quân Chi Chúng", "Rèn Luyện", "Dẫn Quân"],
                "alt_generals": []
            }
        ]
    },

    # 39. QUYỀN KỴ - TINH HỔ BÁO KỴ (TÔN QUYỀN - LĂNG THỐNG - CHU THÁI)
    {
        "id": "meta_quyen_ky_ho_bao",
        "name": "Quyền Kỵ - Tinh Hổ Báo Kỵ (Tôn Quyền - Lăng Thống - Chu Thái)",
        "tier": "T1",
        "season": "PK",
        "faction": "Ngô",
        "troop": "Kỵ",
        "description": "Tôn Quyền Nhất Ký Đường Thiên + Bách Ký Kiếp Doanh Võ Lực, Lăng Thống Lõa Y Huyết Chiến + Đường Phong Thôi Quyết/Mau Giành Lợi Thế sát thương cao, Chu Thái Tinh Hổ Báo Kỵ + Phong Thi Trận. Combo [Thần Hành] + [Xung Phong] + [Diên Ích] + [Trọng Thương].",
        "strengths": ["Tinh Hổ Báo Kỵ bạo kích sát thương vật lý cao", "Kỵ binh tốc chiến Ngô", "Tốt cho khai hoang"],
        "weaknesses": ["Sợ Tước Khí đầu trận", "Ít trị liệu"],
        "generals": [
            {
                "position": "Chủ tướng",
                "general_id": "ngo_ton_quan",
                "name": "Tôn Quyền",
                "bis_tactics": ["Nhất Ký Đường Thiên", "Bách Ký Kiếp Doanh"],
                "sub_tactics": ["Võ Lực", "Liên Mạch Một Hơi", "Võ Lược", "Cầm Binh Khí"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 1",
                "general_id": "ngo_lang_thong",
                "name": "Lăng Thống",
                "bis_tactics": ["Lõa Y Huyết Chiến", "Đường Phong Thôi Quyết/Mau Giành Lợi Thế"],
                "sub_tactics": ["Võ Lực / Tốc Độ", "Không Chiến Sẽ Chết", "Thắng Trận", "Phân Hiểm"],
                "alt_generals": []
            },
            {
                "position": "Phó tướng 2",
                "general_id": "ngo_chu_thai",
                "name": "Chu Thái",
                "bis_tactics": ["Tinh Hổ Báo Kỵ", "Phong Thi Trận"],
                "sub_tactics": ["Thống Soái", "Biết Cách Phòng Thủ - Thể Phòng Thủ", "Tinh Tâm"],
                "alt_generals": []
            }
        ]
    }
]


def main():
    db_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(db_dir, "generals.json"), "w", encoding="utf-8") as f:
        json.dump(generals_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(generals_data)} generals to generals.json")

    with open(os.path.join(db_dir, "tactics.json"), "w", encoding="utf-8") as f:
        json.dump(tactics_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(tactics_data)} tactics to tactics.json")

    with open(os.path.join(db_dir, "meta_teams.json"), "w", encoding="utf-8") as f:
        json.dump(meta_teams, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(meta_teams)} meta teams to meta_teams.json")


if __name__ == "__main__":
    main()
