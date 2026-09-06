# -*- coding: utf-8 -*-
import openpyxl
import json
import re

wb = openpyxl.load_workbook('Meta Team Giới Thiệu Mùa PK.xlsx', data_only=True)
s = wb['Khai hoang']

# 1. Extract mine difficulty
mines_guide = {}
for r in [4, 6, 8, 10, 12]:
    mo_title = str(s.cell(r, 1).value or '').strip()
    guards = []
    for c in range(1, 15):
        v = str(s.cell(r+1, c).value or '').strip()
        if v:
            guards.append(v)
    if mo_title and guards:
        mines_guide[mo_title] = guards

# 2. Extract touch scout teams (Team Chạm Sứ - mang 1 lính)
touch_scouts = [
    {"name": "Lữ Mông & Giả Hủ", "tactics": "Bạch Mã Nghĩa Tòng / Ngụy Báo Uyên Cương", "note": "Hỗ trợ làm suy yếu vệ quân mỏ trước khi đội chính vào"},
    {"name": "Mã Siêu & Hoàng Nguyệt Anh", "tactics": "Bách Kỵ Kiếp Doanh / Lõa Y Huyết Chiến", "note": "Gây sát thương vòng đầu cực mạnh với 1 lính"},
    {"name": "Trương Nhượng & Hoàng Nguyệt Anh", "tactics": "Văn Võ Song Toàn", "note": "Tỉa máu vệ quân mỏ cấp cao"},
    {"name": "Tôn Thượng Hương & Lăng Thống", "tactics": "Lõa Y Huyết Chiến / Bách Kỵ", "note": "Tận dụng tiên phong + tất trúng để quấy rối"},
    {"name": "Thái Sử Từ & Lăng Thống", "tactics": "Bạo Lệ Vô Nhân / Đánh Bại Quân Địch", "note": "Đánh liên kích 2 lần hạ lính đối phương"},
    {"name": "Hạ Hầu Uyên & Tào Thuận", "tactics": "Lõa Y Huyết Chiến / Bách Kỵ", "note": "Khóa tướng địch và làm tiêu hao binh lực mỏ"},
    {"name": "Cam Ninh & Lăng Thống", "tactics": "Phá Quân Uy Thắng / Bất Nhục Sứ Mệnh", "note": "Bạo kích sốc sát thương 1 lính"}
]

# 3. Extract starter teams
starter_teams = []
cur_t = None
for r in range(20, 66):
    type_val = str(s.cell(r, 1).value or '').strip()
    gen_val = str(s.cell(r, 2).value or '').strip()
    cp1_val = str(s.cell(r, 3).value or '').strip()
    type20_val = str(s.cell(r, 4).value or '').strip()
    cp20_1 = str(s.cell(r, 5).value or '').strip()
    cp20_2 = str(s.cell(r, 6).value or '').strip()
    note = str(s.cell(r, 7).value or s.cell(r, 8).value or '').strip()
    
    if any(t in type_val for t in ['Cung', 'Thương', 'Khiên', 'Kỵ']):
        if cur_t and len(cur_t['generals']) >= 2:
            starter_teams.append(cur_t)
        cur_t = {
            'id': f"starter_team_{len(starter_teams)+1:02d}",
            'troop': type_val,
            'troop_lv20': type20_val or type_val,
            'generals': [],
            'note': note
        }
    if cur_t and gen_val and gen_val not in ['Tướng', 'Võ Tướng', 'Type']:
        cur_t['generals'].append({
            'name': gen_val,
            'cp_early': cp1_val,
            'cp_lv20': [c for c in [cp20_1, cp20_2] if c]
        })
        if note and not cur_t['note']:
            cur_t['note'] = note

if cur_t and len(cur_t['generals']) >= 2:
    starter_teams.append(cur_t)

output_data = {
    "mines_guide": mines_guide,
    "touch_scout_teams": touch_scouts,
    "starter_teams": starter_teams
}

with open("database/starter_teams.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(starter_teams)} starter teams, {len(touch_scouts)} touch scouts, and {len(mines_guide)} mine tiers.")
