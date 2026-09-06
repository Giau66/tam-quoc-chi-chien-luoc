# -*- coding: utf-8 -*-
import json

with open("database/meta_teams.json", "r", encoding="utf-8") as f:
    meta_teams = json.load(f)
with open("database/generals.json", "r", encoding="utf-8") as f:
    generals = json.load(f)
with open("database/tactics.json", "r", encoding="utf-8") as f:
    tactics = json.load(f)

user_gens = [
    "Khương Duy", "SP Quan Vũ", "Quan Vũ", "Triệu Vân", "Trương Phi", "Hoàng Trung",
    "Bàng Thống", "Mã Siêu", "Quan Hưng", "Mã Đại", "Trương Bào", "Nghiêm Nhan", "Y Tịch",
    "Tôn Kiên", "SP Tôn Kiên", "Tôn Thượng Hương", "Lục Tốn", "Chu Thái", "Thái Sử Từ",
    "Cam Ninh", "Đại Kiều", "Lục Kháng", "Tư Mã Ý", "Giả Hủ", "SP Bàng Đức", "Hạ Hầu Đôn",
    "Từ Hoảng", "Chân Cơ", "Vương Song", "Lữ Bố", "Trương Giác", "SP Chu Tuấn", "SP Trương Bảo",
    "Điêu Thuyền", "Điền Phong", "Lữ Linh Ỷ", "Chúc Dung", "Viên Thiệu", "Mạnh Hoạch", "Mã Quân"
]

user_tacs = [
    "Mưu Lược Tung Hoành", "Lư Giang Thượng Giáp", "Thi Chí Bất Di", "Thần Thượng Sứ",
    "Tự Lành", "Kiêu Kiện Thần Hành", "Tị Thực Kích Hư", "Tài Khí Quá Nhân", "Phấn Đột",
    "Loạn Cung Ẩm Vũ", "Yêu Thuật", "Nhất Cử Tiệm Diệt", "Bất Nhục Sứ Mệnh", "Ám Tàng Huyền Cơ",
    "Trá Hàng", "Tịnh Hóa", "Xua Đuổi", "Ỷ Thế Cầm Quyền", "Chờ Đợi Xuất Phát", "Đánh Vào Chỗ Đau",
    "Đánh Vào Chỗ Hiểm", "Ngự Địch Bình Chướng"
]

# Find teams where user has 3/3 generals!
teams_with_all_3_gens = []
teams_with_2_gens = []

gen_set = set(user_gens)

for t in meta_teams:
    team_gens = t['generals']
    owned_count = 0
    gens_status = []
    for g in team_gens:
        gname = g['name']
        alts = g.get('alt_generals', [])
        if gname in gen_set:
            owned_count += 1
            gens_status.append((gname, "Chính thức"))
        elif any(a in gen_set for a in alts):
            alt_found = [a for a in alts if a in gen_set][0]
            owned_count += 0.8
            gens_status.append((alt_found, "Thay thế"))
        else:
            gens_status.append((gname, "Thiếu"))
            
    if owned_count >= 2.8:
        teams_with_all_3_gens.append((t, gens_status))
    elif owned_count >= 1.8:
        teams_with_2_gens.append((t, gens_status))

print(f"=== TEAMS WITH FULL 3/3 GENERALS OWNED: {len(teams_with_all_3_gens)} ===")
for t, status in teams_with_all_3_gens[:10]:
    print(f"  * [{t['tier']}] {t['name']}")
    for g, st in status:
        print(f"      {g} ({st})")

print(f"\n=== TEAMS WITH 2/3 GENERALS OWNED: {len(teams_with_2_gens)} ===")
for t, status in teams_with_2_gens[:5]:
    print(f"  * [{t['tier']}] {t['name']}")
