# -*- coding: utf-8 -*-
"""
Full extraction script v2:
Reads ALL 12 sheets from Excel and creates complete, rich database.
Fixes Binh Thư extraction for all sheets (including 'Meta mỗi phe (cũ)').
Extracts:
  - generals.json (all generals with inherent skill, inherit tactic, usage, season)
  - tactics.json (all tactics with type, desc, food, suitable gens, season)
  - meta_teams.json (200+ unique meta teams with full Binh Thư 1, 2, 3, Chạm/Tránh notes, season)
  - starter_teams.json (15 real starter teams from Khai hoang + Mỏ 4-8 defense difficulty + touch scouts)
  - team_do_uy.json (12 Do Uy teams with Binh Thư & notes)
  - cai_tao_binh_chung.json (15 special Troop Remodel & Lệnh Đăng Ung teams with Binh Thư)
  - coexisting_portfolios.json (5 Coexisting Portfolios with Starter recommendations, stats, and Binh Thư + Multi-team sets)
"""
import sys
import openpyxl
import re
import os
import json
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")

# Locate Excel file
EXCEL_PATH = None
for fname in os.listdir(BASE_DIR):
    if fname.startswith("Meta Team") and fname.endswith(".xlsx"):
        EXCEL_PATH = os.path.join(BASE_DIR, fname)
        break

if not EXCEL_PATH or not os.path.exists(EXCEL_PATH):
    raise FileNotFoundError(f"Excel file not found in {BASE_DIR}")

print(f"Loading Excel from: {EXCEL_PATH}")
wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
print(f"Workbook sheet names: {wb.sheetnames}")

def slugify(text):
    text = unicodedata.normalize('NFD', str(text))
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().replace('đ', 'd').replace('Đ', 'd')
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text

GEN_NORM = {
    'gia hu': 'Gia Hủ', 'tha tho': 'Tào Tháo', 'lam thong': 'Lăng Thống',
    'giả hư': 'Giả Hủ', 'thào tháo': 'Tào Tháo', 'lăm thống': 'Lăng Thống',
    'sp quãn vũ': 'SP Quan Vũ', 'sp quan vu': 'SP Quan Vũ',
    'spđồng trác': 'SP Đổng Trác', 'lục tốṇ': 'Lục Tốn', 'lục tốṇ': 'Lục Tốn',
    'bái sư hứa du': 'Hứa Du', 'bái sư lỗ túc': 'Lỗ Túc',
    'bái sư pháp chính': 'Pháp Chính', 'bái sư sp tuân úc': 'SP Tuân Úc',
    'lữ bố 40th': 'Lữ Bố', 'co tinh thái': 'Trương Tinh Thái',
    'co đại kiều': 'Đại Kiều', 'co tiểu kiều': 'Tiểu Kiều',
    'vô song đại kiều': 'Đại Kiều', 'vô song tiểu kiều': 'Tiểu Kiều',
    'tinh thái': 'Trương Tinh Thái', 'tư mã ý': 'Tư Mã Ý',
    'mãn sủng': 'Mãn Sủng', 'triệu vân': 'Triệu Vân',
    'khương duy': 'Khương Duy', 'bàng thống': 'Bàng Thống',
    'gia cát lượng': 'Gia Cát Lượng', 'tào tháo': 'Tào Tháo',
    'chu thái': 'Chu Thái', 'lăng thống': 'Lăng Thống',
    'lưu bị': 'Lưu Bị', 'trương phi': 'Trương Phi',
    'quan vũ': 'Quan Vũ', 'ngụy diên': 'Ngụy Diên',
    'quan ngân bình': 'Quan Ngân Bình', 'pháp chính': 'Pháp Chính',
    'sp mã siêu': 'SP Mã Siêu', 'sp hoàng phổ tung': 'SP Hoàng Phổ Tung',
    'sp tuân úc': 'SP Tuân Úc', 'sp quách gia': 'SP Quách Gia',
    'sp quan vũ': 'SP Quan Vũ', 'sp chu du': 'SP Chu Du',
    'sp lữ mông': 'SP Lữ Mông', 'sp viên thiệu': 'SP Viên Thiệu',
    'sp chu tuấn': 'SP Chu Tuấn', 'sp đổng trác': 'SP Đổng Trác',
    'sp điêu thuyền': 'SP Điêu Thuyền', 'sp lô trực': 'SP Lô Trực',
    'sp tôn kiên': 'SP Tôn Kiên', 'sp hoàng nguyệt anh': 'SP Hoàng Nguyệt Anh',
    'mã quân': 'Mã Quân', 'sp hứa chử': 'SP Hứa Chử',
    'sp tào chân': 'SP Tào Chân', 'dương dị': 'Dương Dị',
    'sp trương bảo': 'SP Trương Bảo', 'sp trương lương': 'SP Trương Lương',
    'sp bàng đức': 'SP Bàng Đức', 'sp lưu diệp': 'SP Lưu Diệp',
    'gia cát khác': 'Gia Cát Khác', 'mã đại': 'Mã Đại',
    'sp pháp chính': 'SP Pháp Chính', 'hạ hầu uyên': 'Hạ Hầu Uyên',
    'thái sử từ': 'Thái Sử Từ', 'trương xuân hoa': 'Trương Xuân Hoa',
    'thái văn cơ': 'Thái Văn Cơ', 'nhạc tiến': 'Nhạc Tiến',
    'lục tốn': 'Lục Tốn', 'tả từ': 'Tả Từ', 'tôn thượng hương': 'Tôn Thượng Hương',
    'trần cung': 'Trần Cung', 'chu thiệu': 'Chu Thiệu', 'dương kỳ': 'Dương Kỳ'
}

FACTION_MAP = {
    'Lưu Bị': 'Thục', 'Quan Vũ': 'Thục', 'Trương Phi': 'Thục', 'Triệu Vân': 'Thục',
    'Gia Cát Lượng': 'Thục', 'Bàng Thống': 'Thục', 'Khương Duy': 'Thục', 'Ngụy Diên': 'Thục',
    'Hoàng Trung': 'Thục', 'Mã Siêu': 'Thục', 'Pháp Chính': 'Thục', 'Quan Ngân Bình': 'Thục',
    'Trương Tinh Thái': 'Thục', 'Hoàng Nguyệt Anh': 'Thục', 'Nghiêm Nhan': 'Thục',
    'Mã Vân Lộc': 'Thục', 'Vương Bình': 'Thục', 'Từ Thứ': 'Thục', 'SP Quan Vũ': 'Thục',
    'SP Gia Cát Lượng': 'Thục', 'SP Hoàng Nguyệt Anh': 'Thục', 'SP Mã Siêu': 'Thục',
    'Mã Đại': 'Thục', 'SP Pháp Chính': 'Thục', 'Liêu Hóa': 'Thục', 'Quan Hưng': 'Thục',
    'Trương Bào': 'Thục', 'Trần Đáo': 'Thục',
    'Tào Tháo': 'Ngụy', 'Tư Mã Ý': 'Ngụy', 'Quách Gia': 'Ngụy', 'Giả Hủ': 'Ngụy',
    'Trình Dục': 'Ngụy', 'Hạ Hầu Uyên': 'Ngụy', 'Hạ Hầu Đôn': 'Ngụy', 'Trương Liêu': 'Ngụy',
    'Hác Chiêu': 'Ngụy', 'Mãn Sủng': 'Ngụy', 'Tuân Úc': 'Ngụy', 'Tuân Du': 'Ngụy',
    'Vương Nguyên Cơ': 'Ngụy', 'Chung Hội': 'Ngụy', 'Đặng Ngải': 'Ngụy', 'Hứa Chử': 'Ngụy',
    'Điển Vi': 'Ngụy', 'Tào Nhân': 'Ngụy', 'Tào Phi': 'Ngụy', 'Tào Thuần': 'Ngụy',
    'Bàng Đức': 'Ngụy', 'Chân Cơ': 'Ngụy', 'SP Tuân Úc': 'Ngụy', 'SP Quách Gia': 'Ngụy',
    'SP Hứa Chử': 'Ngụy', 'SP Tào Chân': 'Ngụy', 'SP Bàng Đức': 'Ngụy', 'SP Lưu Diệp': 'Ngụy',
    'Tào Chương': 'Ngụy', 'Quách Hoài': 'Ngụy', 'Giả Quỳ': 'Ngụy', 'Văn Sính': 'Ngụy',
    'Tào Chân': 'Ngụy', 'Lý Điển': 'Ngụy',
    'Tôn Quyền': 'Ngô', 'Tôn Sách': 'Ngô', 'Tôn Kiên': 'Ngô', 'Tôn Thượng Hương': 'Ngô',
    'Chu Du': 'Ngô', 'Lục Tốn': 'Ngô', 'Lỗ Túc': 'Ngô', 'Lữ Mông': 'Ngô',
    'Thái Sử Từ': 'Ngô', 'Cam Ninh': 'Ngô', 'Trình Phổ': 'Ngô', 'Hoàng Cái': 'Ngô',
    'Chu Thái': 'Ngô', 'Lăng Thống': 'Ngô', 'Đại Kiều': 'Ngô', 'Tiểu Kiều': 'Ngô',
    'Lục Kháng': 'Ngô', 'Đinh Phụng': 'Ngô', 'Hàn Đương': 'Ngô', 'Tưởng Khâm': 'Ngô',
    'SP Chu Du': 'Ngô', 'SP Lữ Mông': 'Ngô', 'SP Tôn Kiên': 'Ngô', 'Gia Cát Khác': 'Ngô',
    'Chu Trị': 'Ngô',
    'Lữ Bố': 'Quần', 'Điêu Thuyền': 'Quần', 'Đổng Trác': 'Quần', 'Hoa Đà': 'Quần',
    'Tả Từ': 'Quần', 'Vu Cát': 'Quần', 'Trương Giác': 'Quần', 'Viên Thiệu': 'Quần',
    'Chu Tuấn': 'Quần', 'Thư Thụ': 'Quần', 'Hoa Hùng': 'Quần', 'Nhan Lương': 'Quần',
    'Văn Xú': 'Quần', 'Chúc Dung': 'Quần', 'Mạnh Hoạch': 'Quần', 'Trần Cung': 'Quần',
    'Điền Phong': 'Quần', 'Lý Nho': 'Quần', 'Hứa Du': 'Quần', 'Dương Dị': 'Quần',
    'Mã Quân': 'Quần', 'SP Viên Thiệu': 'Quần', 'SP Chu Tuấn': 'Quần', 'SP Đổng Trác': 'Quần',
    'SP Điêu Thuyền': 'Quần', 'SP Lô Trực': 'Quần', 'SP Hoàng Phổ Tung': 'Quần',
    'SP Trương Bảo': 'Quần', 'SP Trương Lương': 'Quần', 'Khúc Nghĩa': 'Quần',
    'Cao Lãm': 'Quần', 'Chu Thiệu': 'Quần', 'Viên Thuật': 'Quần', 'Thái Văn Cơ': 'Quần',
    'Trương Xuân Hoa': 'Ngụy', 'Dương Kỳ': 'Quần'
}

def clean_gen_name(name):
    if not name:
        return ""
    name = str(name).strip()
    name = re.sub(r'[\r\n]+', ' ', name)
    name = re.sub(r'\([^\)]*\)', '', name)
    name = re.sub(r'\b(40th|CO|Chủ Tướng|Phó Tướng)\b', '', name, flags=re.I)
    name = name.strip()
    name = re.sub(r'\s+', ' ', name)
    n_lower = name.lower()
    return GEN_NORM.get(n_lower, name)

def clean_tac_name(name):
    if not name:
        return ""
    name = str(name).strip()
    name = re.sub(r'[\r\n]+', ' ', name)
    name = re.sub(r'^(Tinh|Chuyển|Thác)[·\.\s]', '', name)
    name = re.sub(r'\([^\)]*\)', '', name)
    name = name.strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def infer_faction(name):
    clean = clean_gen_name(name)
    if clean in FACTION_MAP:
        return FACTION_MAP[clean]
    for k, v in FACTION_MAP.items():
        if clean == k or clean in k:
            return v
    return "Quần"

def infer_tactic_type(name):
    n = name.lower()
    if 'trận' in n:
        return 'Trận pháp'
    if any(k in n for k in ['kỵ', 'khiên', 'cung', 'thương', 'binh', 'doanh', 'vệ', 'sĩ']):
        return 'Binh chủng'
    if any(k in n for k in ['thái bình', 'sĩ biệt', 'dụng võ', 'tuyệt địa', 'hổ cứ', 'lõa y', 'binh vô', 'văn thao']):
        return 'Bị động'
    if any(k in n for k in ['bát môn', 'quân dân', 'thảo thuyền', 'thuyền cỏ', 'tạm lánh', 'thịnh khí', 'tiềm long', 'cơ hình', 'giải phiền']):
        return 'Chỉ huy'
    if any(k in n for k in ['nhất kỵ', 'quỷ thần', 'bách kỵ', 'bạo lệ', 'đương phong', 'mau giành', 'thôi phong']):
        return 'Đột kích'
    return 'Chủ động'

generals_data = {}
tactics_data = {}

def reg_gen(name, season="PK", inherent="", inherit="", role="", notes=""):
    if not name:
        return
    f = infer_faction(name)
    gid = f"{slugify(f)}_{slugify(name)}"
    if name not in generals_data:
        generals_data[name] = {
            "id": gid,
            "name": name,
            "faction": f,
            "cost": 7 if 'SP' in name else 6,
            "troop": {"Ky": "S" if 'Kỵ' in role else "A", "Khien": "A", "Cung": "A", "Thuong": "A", "Khi": "B"},
            "inherent_skill": inherent or f"Kỹ năng tự mang của {name}",
            "inherit_tactic": inherit or "",
            "role": [role] if role and role != '-' else ["Tướng chủ lực / Hỗ trợ trong Meta"],
            "season": season,
            "note": notes
        }
    else:
        if inherent and not generals_data[name].get("inherent_skill"):
            generals_data[name]["inherent_skill"] = inherent
        if inherit and not generals_data[name].get("inherit_tactic"):
            generals_data[name]["inherit_tactic"] = inherit
        if role and role != '-':
            if role not in generals_data[name]["role"]:
                generals_data[name]["role"].append(role)

def reg_tac(name, desc="", suitable="", food="", season="PK"):
    if not name:
        return
    t_clean = clean_tac_name(name)
    if not t_clean:
        return
    if t_clean not in tactics_data:
        tactics_data[t_clean] = {
            "id": slugify(t_clean),
            "name": t_clean,
            "type": infer_tactic_type(t_clean),
            "quality": "S",
            "description": desc or f"Chiến pháp mạnh trong meta {season}",
            "suitable_generals": suitable or "",
            "food_required": food or "",
            "season": season
        }
    else:
        if desc and ("Chiến pháp mạnh" in tactics_data[t_clean]["description"] or not tactics_data[t_clean]["description"]):
            tactics_data[t_clean]["description"] = desc
        if suitable and not tactics_data[t_clean]["suitable_generals"]:
            tactics_data[t_clean]["suitable_generals"] = suitable
        if food and not tactics_data[t_clean]["food_required"]:
            tactics_data[t_clean]["food_required"] = food

# ==========================================================
# 1. Tướng & CP (All Seasons)
# ==========================================================
print("\n--- 1. Parsing Tướng&CP ---")
s_cp = wb['Tướng&CP']
cur_season = "PK"
mode = None
for r in range(1, s_cp.max_row + 1):
    c1 = str(s_cp.cell(r, 1).value or '').strip()
    c2 = str(s_cp.cell(r, 2).value or '').strip()
    c3 = str(s_cp.cell(r, 3).value or '').strip()
    c4 = str(s_cp.cell(r, 4).value or '').strip()
    c5 = str(s_cp.cell(r, 5).value or '').strip()

    if 'PK' in c1 or 'mùa' in c1.lower() or 'Mùa' in c1:
        cur_season = c1
    if 'Tướng Mới' in c1 or 'Tướng Mới' in c2:
        mode = 'GEN'
        continue
    elif 'Chiến Pháp' in c1 or 'Chiến Pháp' in c2:
        mode = 'TAC'
        continue

    if c1 in ['STT', ''] and c2 in ['Tên Tướng', 'Tên Chiến Pháp']:
        continue

    if mode == 'GEN' and c2:
        g_name = clean_gen_name(c2)
        if g_name:
            reg_gen(g_name, season=cur_season, inherent=c3, inherit=clean_tac_name(c4) if c4 != '-' else '', role=c5)
            if c4 and c4 != '-':
                t_inherit = clean_tac_name(c4)
                reg_tac(t_inherit, desc=f"Chiến pháp kế thừa từ {g_name}", season=cur_season)
    elif mode == 'TAC' and c2:
        t_name = clean_tac_name(c2)
        if t_name:
            reg_tac(t_name, desc=c3, suitable=c4, food=c5, season=cur_season)

print(f"  Extracted {len(generals_data)} Generals, {len(tactics_data)} Tactics from Tướng&CP")

# ==========================================================
# 2. Khai hoang (15 Starter teams + Mines guide)
# ==========================================================
print("\n--- 2. Parsing Khai hoang ---")
s_kh = wb['Khai hoang']
starter_teams_list = []
mines_guide = {
    "Mỏ 4": [],
    "Mỏ 5": [],
    "Mỏ 6": [],
    "Mỏ 7": [],
    "Mỏ 8": []
}

# Parse Mines difficulty rows
for r in range(4, 15):
    header = str(s_kh.cell(r, 1).value or '').strip()
    for m in ["Mỏ 4", "Mỏ 5", "Mỏ 6", "Mỏ 7", "Mỏ 8"]:
        if header == m:
            defenders = [str(s_kh.cell(r+1, c).value or '').strip() for c in range(1, 15)]
            mines_guide[m] = [d for d in defenders if d]

# Parse Starter teams from row 21 onwards
cur_st = None
for r in range(21, s_kh.max_row + 1):
    c1 = str(s_kh.cell(r, 1).value or '').strip()
    c2 = str(s_kh.cell(r, 2).value or '').strip()
    c3 = str(s_kh.cell(r, 3).value or '').strip()
    c4 = str(s_kh.cell(r, 4).value or '').strip()
    c5 = str(s_kh.cell(r, 5).value or '').strip()
    c6 = str(s_kh.cell(r, 6).value or '').strip()

    if c1 and any(t in c1 for t in ['Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí']):
        if cur_st and len(cur_st['generals']) >= 2:
            starter_teams_list.append(cur_st)
        cur_st = {
            "id": f"starter_team_{len(starter_teams_list)+1:02d}",
            "troop": c1,
            "troop_lv20": c4 if c4 else c1,
            "generals": [],
            "note": "Đội hình khai hoang chuẩn mở đất mùa PK."
        }
    if cur_st and c2:
        reg_gen(clean_gen_name(c2))
        for cp in [c3, c5, c6]:
            if cp:
                for part in re.split(r'[/,\n]+', cp):
                    clean_p = clean_tac_name(part)
                    if clean_p:
                        reg_tac(clean_p)
        cur_st['generals'].append({
            "name": c2,
            "cp_early": c3,
            "cp_lv20": [clean_tac_name(p) for p in [c5, c6] if clean_tac_name(p)]
        })

if cur_st and len(cur_st['generals']) >= 2:
    starter_teams_list.append(cur_st)

touch_scout_teams = [
    {"name": "Lữ Mông & Giả Hủ", "tactics": "Bạch Mã Nghĩa Tòng / Ngụy Báo Uyên Cương", "note": "Hỗ trợ làm suy yếu vệ quân mỏ trước khi đội chính vào"},
    {"name": "Mã Siêu & Hoàng Nguyệt Anh", "tactics": "Bách Kỵ Kiếp Doanh / Lõa Y Huyết Chiến", "note": "Gây sát thương vòng đầu cực mạnh với 1 lính"},
    {"name": "Trương Nhượng & Hoàng Nguyệt Anh", "tactics": "Văn Võ Song Toàn", "note": "Tỉa máu vệ quân mỏ cấp cao"},
    {"name": "Tôn Thượng Hương & Lăng Thống", "tactics": "Lõa Y Huyết Chiến / Bách Kỵ", "note": "Tận dụng tiên phong + tất trúng để quấy rối"},
    {"name": "Thái Sử Từ & Lăng Thống", "tactics": "Bạo Lệ Vô Nhân / Đánh Bại Quân Địch", "note": "Đánh liên kích 2 lần hạ lính đối phương"},
    {"name": "Hạ Hầu Uyên & Tào Thuần", "tactics": "Lõa Y Huyết Chiến / Bách Kỵ", "note": "Khóa tướng địch và làm tiêu hao binh lực mỏ"},
    {"name": "Cam Ninh & Lăng Thống", "tactics": "Phá Quân Uy Thắng / Bất Nhục Sứ Mệnh", "note": "Bạo kích sốc sát thương 1 lính"}
]

starter_database = {
    "mines_guide": mines_guide,
    "touch_scout_teams": touch_scout_teams,
    "starter_teams": starter_teams_list
}
print(f"  Extracted {len(starter_teams_list)} starter teams")

# ==========================================================
# 3. Team giới thiệu(mới) (PK Meta Teams with Binh Thư)
# ==========================================================
print("\n--- 3. Parsing Team giới thiệu(mới) ---")
s_new = wb['Team giới thiệu(mới)']
raw_pk_new_teams = []
cur_t = None
for r in range(5, s_new.max_row + 1):
    type_val = str(s_new.cell(r, 1).value or '').strip()
    gen_val  = str(s_new.cell(r, 2).value or '').strip()
    cp1_val  = str(s_new.cell(r, 3).value or '').strip()
    cp2_val  = str(s_new.cell(r, 4).value or '').strip()
    bt1 = str(s_new.cell(r, 5).value or '').strip()
    bt2 = str(s_new.cell(r, 6).value or '').strip()
    bt3 = str(s_new.cell(r, 7).value or '').strip()
    note = str(s_new.cell(r, 8).value or '').strip()

    if type_val and any(t in type_val for t in ['Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí', 'Thuong', 'Khien', 'Ky']):
        if cur_t and len(cur_t['generals']) >= 2:
            raw_pk_new_teams.append(cur_t)
        troop = "Kỵ"
        for t in ["Thương", "Khiên", "Cung", "Kỵ", "Khí"]:
            if t in type_val:
                troop = t
                break
        tier = "T0"
        if "⭐" in type_val:
            star_count = type_val.count("⭐")
            if star_count >= 5: tier = "T0"
            elif star_count == 4: tier = "T0.5"
            else: tier = "T1"
        cur_t = {
            "source": "Team giới thiệu(mới)",
            "troop": troop,
            "tier": tier,
            "note": note,
            "season": "PK",
            "generals": []
        }
    if cur_t and gen_val:
        cur_t['generals'].append({
            "raw_name": gen_val,
            "cp1_raw": cp1_val,
            "cp2_raw": cp2_val,
            "binh_thu": [b for b in [bt1, bt2, bt3] if b]
        })
        if note and not cur_t['note']:
            cur_t['note'] = note

if cur_t and len(cur_t['generals']) >= 2:
    raw_pk_new_teams.append(cur_t)

print(f"  Extracted {len(raw_pk_new_teams)} teams from Team giới thiệu(mới)")

# ==========================================================
# 4. Meta mỗi phe (cũ) (WITH BINH THƯ 1, 2, 3!)
# ==========================================================
print("\n--- 4. Parsing Meta mỗi phe (cũ) with Binh Thư ---")
s_phe = wb['Meta mỗi phe (cũ)']
raw_phe_teams = []
cur_t = None
for r in range(4, s_phe.max_row + 1):
    type_val = str(s_phe.cell(r, 1).value or '').strip()
    gen_val  = str(s_phe.cell(r, 2).value or '').strip()
    cp1_val  = str(s_phe.cell(r, 3).value or '').strip()
    cp2_val  = str(s_phe.cell(r, 4).value or '').strip()
    bt1 = str(s_phe.cell(r, 5).value or '').strip()
    bt2 = str(s_phe.cell(r, 6).value or '').strip()
    bt3 = str(s_phe.cell(r, 7).value or '').strip()
    note = str(s_phe.cell(r, 8).value or '').strip() if s_phe.max_column >= 8 else ''

    if type_val and any(t in type_val for t in ["Thương", "Khiên", "Cung", "Kỵ", "Khí"]):
        if cur_t and len(cur_t['generals']) >= 2:
            raw_phe_teams.append(cur_t)
        troop = "Kỵ"
        for t in ["Thương", "Khiên", "Cung", "Kỵ", "Khí"]:
            if t in type_val:
                troop = t
                break
        cur_t = {
            "source": "Meta mỗi phe (cũ)",
            "troop": troop,
            "tier": "T1",
            "note": note,
            "season": "PK",
            "generals": []
        }
    if cur_t and gen_val:
        cur_t['generals'].append({
            "raw_name": gen_val,
            "cp1_raw": cp1_val,
            "cp2_raw": cp2_val,
            "binh_thu": [b for b in [bt1, bt2, bt3] if b]
        })
        if note and not cur_t['note']:
            cur_t['note'] = note

if cur_t and len(cur_t['generals']) >= 2:
    raw_phe_teams.append(cur_t)

print(f"  Extracted {len(raw_phe_teams)} teams from Meta mỗi phe (cũ) (all with Binh Thư!)")

# ==========================================================
# 5. Meta Team (official) - Tiers and In-depth tactical notes
# ==========================================================
print("\n--- 5. Parsing Meta Team (official) ---")
s_meta = wb['Meta Team']
raw_official_teams = []
cur_t = None
for r in range(3, s_meta.max_row + 1):
    stt      = str(s_meta.cell(r, 1).value or '').strip()
    type_val = str(s_meta.cell(r, 2).value or '').strip()
    power    = str(s_meta.cell(r, 3).value or '').strip()
    gen_val  = str(s_meta.cell(r, 4).value or '').strip()
    cp1_val  = str(s_meta.cell(r, 5).value or '').strip()
    cp2_val  = str(s_meta.cell(r, 6).value or '').strip()
    note     = str(s_meta.cell(r, 10).value or '').strip() if s_meta.max_column >= 10 else ''

    if stt or type_val:
        if cur_t and len(cur_t['generals']) >= 2:
            raw_official_teams.append(cur_t)
        troop = "Kỵ"
        for t in ["Thương", "Khiên", "Cung", "Kỵ", "Khí"]:
            if t in type_val:
                troop = t
                break
        cur_t = {
            "source": "Meta Team",
            "troop": troop,
            "tier": power if power in ["T0", "T0.5", "T1", "T2"] else "T1",
            "note": note,
            "season": "PK",
            "generals": []
        }
    if cur_t and gen_val:
        cur_t['generals'].append({
            "raw_name": gen_val,
            "cp1_raw": cp1_val,
            "cp2_raw": cp2_val,
            "binh_thu": []
        })
        if note and not cur_t['note']:
            cur_t['note'] = note

if cur_t and len(cur_t['generals']) >= 2:
    raw_official_teams.append(cur_t)

print(f"  Extracted {len(raw_official_teams)} teams from Meta Team")

# ==========================================================
# 6. Meta team mùa 4 & Meta team mùa 5 (with Binh Thư)
# ==========================================================
print("\n--- 6. Parsing Meta team mùa 4 & mùa 5 ---")
s_m4 = wb['Meta team mùa 4']
raw_m4_teams = []
cur_t = None
for r in range(3, s_m4.max_row + 1):
    type_val = str(s_m4.cell(r, 1).value or '').strip()
    gen_val  = str(s_m4.cell(r, 2).value or '').strip()
    cp1_val  = str(s_m4.cell(r, 3).value or '').strip()
    cp2_val  = str(s_m4.cell(r, 4).value or '').strip()
    bt1      = str(s_m4.cell(r, 5).value or '').strip()
    if type_val and any(t in type_val for t in ['Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí']):
        if cur_t and len(cur_t['generals']) >= 2:
            raw_m4_teams.append(cur_t)
        troop = "Kỵ"
        for t in ["Thương", "Khiên", "Cung", "Kỵ", "Khí"]:
            if t in type_val:
                troop = t
                break
        cur_t = {
            "source": "Meta team mùa 4",
            "troop": troop,
            "tier": "T1",
            "note": "Đội hình tiêu biểu mùa 4",
            "season": "Mùa 4",
            "generals": []
        }
    if cur_t and gen_val:
        cur_t['generals'].append({
            "raw_name": gen_val, "cp1_raw": cp1_val, "cp2_raw": cp2_val, "binh_thu": [bt1] if bt1 else []
        })
if cur_t and len(cur_t['generals']) >= 2:
    raw_m4_teams.append(cur_t)

s_m5 = wb['Meta team mùa 5']
raw_m5_teams = []
cur_t = None
for r in range(3, s_m5.max_row + 1):
    type_val = str(s_m5.cell(r, 1).value or '').strip()
    gen_val  = str(s_m5.cell(r, 2).value or '').strip()
    cp1_val  = str(s_m5.cell(r, 3).value or '').strip()
    cp2_val  = str(s_m5.cell(r, 4).value or '').strip()
    bt1      = str(s_m5.cell(r, 5).value or '').strip()
    bt2      = str(s_m5.cell(r, 6).value or '').strip()
    if type_val and any(t in type_val for t in ['Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí']):
        if cur_t and len(cur_t['generals']) >= 2:
            raw_m5_teams.append(cur_t)
        troop = "Kỵ"
        for t in ["Thương", "Khiên", "Cung", "Kỵ", "Khí"]:
            if t in type_val:
                troop = t
                break
        cur_t = {
            "source": "Meta team mùa 5",
            "troop": troop,
            "tier": "T1",
            "note": "Đội hình tiêu biểu mùa 5",
            "season": "Mùa 5",
            "generals": []
        }
    if cur_t and gen_val:
        cur_t['generals'].append({
            "raw_name": gen_val, "cp1_raw": cp1_val, "cp2_raw": cp2_val, "binh_thu": [b for b in [bt1, bt2] if b]
        })
if cur_t and len(cur_t['generals']) >= 2:
    raw_m5_teams.append(cur_t)

print(f"  Extracted {len(raw_m4_teams)} Mùa 4 teams, {len(raw_m5_teams)} Mùa 5 teams")

# ==========================================================
# 7. Team Đô Úy (12 Teams with Binh Thư)
# ==========================================================
print("\n--- 7. Parsing Team Đô Úy ---")
s_du = wb['Team Đô Úy']
team_do_uy_list = []
cur_t = None
for r in range(6, s_du.max_row + 1):
    type_val = str(s_du.cell(r, 1).value or '').strip()
    gen_val  = str(s_du.cell(r, 2).value or '').strip()
    cp1_val  = str(s_du.cell(r, 3).value or '').strip()
    cp2_val  = str(s_du.cell(r, 4).value or '').strip()
    bt1 = str(s_du.cell(r, 5).value or '').strip()
    bt2 = str(s_du.cell(r, 6).value or '').strip()
    bt3 = str(s_du.cell(r, 7).value or '').strip()
    note = str(s_du.cell(r, 8).value or '').strip() if s_du.max_column >= 8 else ''

    if type_val and any(t in type_val for t in ['Đại Khích', 'Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí']):
        if cur_t and len(cur_t['generals']) >= 2:
            team_do_uy_list.append(cur_t)
        cur_t = {
            "id": f"team_do_uy_{len(team_do_uy_list)+1:02d}",
            "troop": type_val,
            "tier": "T1",
            "note": note,
            "season": "PK",
            "generals": []
        }
    if cur_t and gen_val:
        g_clean = clean_gen_name(gen_val)
        if g_clean and g_clean not in ['Type', 'Tướng', 'Võ Tướng']:
            reg_gen(g_clean)
            for cp in [cp1_val, cp2_val]:
                for part in re.split(r'[/,\n]+', cp):
                    clean_p = clean_tac_name(part)
                    if clean_p:
                        reg_tac(clean_p)
            cur_t['generals'].append({
                "name": g_clean,
                "raw_name": gen_val,
                "cp1": cp1_val,
                "cp2": cp2_val,
                "binh_thu": [b for b in [bt1, bt2, bt3] if b]
            })
            if note and not cur_t['note']:
                cur_t['note'] = note

if cur_t and len(cur_t['generals']) >= 2:
    team_do_uy_list.append(cur_t)

print(f"  Extracted {len(team_do_uy_list)} Team Đô Úy")

# ==========================================================
# 8. Cải Tạo Binh Chủng & Lệnh Đăng Ung (15 Teams)
# ==========================================================
print("\n--- 8. Parsing Cải Tạo Binh Chủng & Lệnh Đăng Un ---")
s_ct = wb['Cải Tạo Binh Chủng&Lệnh Đăng Un']
cai_tao_teams = []
cur_t = None
current_section = "Cải Tạo Binh Chủng"
for r in range(4, s_ct.max_row + 1):
    c1 = str(s_ct.cell(r, 1).value or '').strip()
    c2 = str(s_ct.cell(r, 2).value or '').strip()
    c3 = str(s_ct.cell(r, 3).value or '').strip()
    c4 = str(s_ct.cell(r, 4).value or '').strip()
    bt1 = str(s_ct.cell(r, 5).value or '').strip()
    bt2 = str(s_ct.cell(r, 6).value or '').strip()
    bt3 = str(s_ct.cell(r, 7).value or '').strip()
    note = str(s_ct.cell(r, 8).value or '').strip() if s_ct.max_column >= 8 else ''

    if 'Lệnh Đăng Ung' in c1:
        current_section = "Lệnh Đăng Ung"
        continue
    if c1 in ['Type', 'Tiến Cử Đội Hình Cải Tạo Binh Chủng', 'Tiến Cử Đội Hình Lệnh Đăng Ung']:
        continue

    if c1 and any(t in c1 for t in ['Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí']):
        if cur_t and len(cur_t['generals']) >= 2:
            cai_tao_teams.append(cur_t)
        cur_t = {
            "id": f"cai_tao_{len(cai_tao_teams)+1:02d}",
            "section": current_section,
            "troop": c1,
            "tier": "T0.5" if current_section == "Lệnh Đăng Ung" else "T1",
            "note": note,
            "season": "PK",
            "generals": []
        }
    if cur_t and c2:
        g_clean = clean_gen_name(c2)
        if g_clean:
            reg_gen(g_clean)
            for cp in [c3, c4]:
                for part in re.split(r'[/,\n]+', cp):
                    clean_p = clean_tac_name(part)
                    if clean_p:
                        reg_tac(clean_p)
            cur_t['generals'].append({
                "name": g_clean,
                "raw_name": c2,
                "cp1": c3,
                "cp2": c4,
                "binh_thu": [b for b in [bt1, bt2, bt3] if b]
            })
            if note and not cur_t['note']:
                cur_t['note'] = note

if cur_t and len(cur_t['generals']) >= 2:
    cai_tao_teams.append(cur_t)

print(f"  Extracted {len(cai_tao_teams)} Cải Tạo Binh Chủng & Lệnh Đăng Ung teams")

# ==========================================================
# 9. Team Cùng Tồn (5 Coexisting Portfolios)
# ==========================================================
print("\n--- 9. Parsing Team Cùng Tồn (5 Sets) ---")
s_tc = wb['Team Cùng Tồn']
coexisting_portfolios = []
cur_set = None
cur_sub_team = None

for r in range(4, s_tc.max_row + 1):
    c1 = str(s_tc.cell(r, 1).value or '').strip()
    c2 = str(s_tc.cell(r, 2).value or '').strip()
    c3 = str(s_tc.cell(r, 3).value or '').strip()
    c4 = str(s_tc.cell(r, 4).value or '').strip()
    c5 = str(s_tc.cell(r, 5).value or '').strip()
    c6 = str(s_tc.cell(r, 6).value or '').strip()
    c7 = str(s_tc.cell(r, 7).value or '').strip()

    if 'Cùng tồn' in c1 or 'cung ton' in c1.lower():
        if cur_set:
            coexisting_portfolios.append(cur_set)
        cur_set = {
            "set_id": slugify(c1),
            "set_name": c1,
            "description": c2,
            "starter_recommendation": "",
            "teams": []
        }
        cur_sub_team = None
        continue

    # Starter recommendations in column 1
    if cur_set and c1 and 'Tiến cử khai hoang' not in c1:
        if not cur_set["starter_recommendation"]:
            cur_set["starter_recommendation"] = c1

    # Team header in column 2
    if c2 and any(t in c2 for t in ['Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí', '19C', '20C', '18C', '16C', 'Lữ', 'Mã', 'Ngũ']):
        cur_sub_team = {
            "team_name": c2.replace('\n', ' - '),
            "cost": "19C" if "19C" in c2 else ("20C" if "20C" in c2 else "18C"),
            "generals": []
        }
        if cur_set:
            cur_set["teams"].append(cur_sub_team)

    if cur_sub_team and c3:
        g_clean = clean_gen_name(c3)
        if g_clean and g_clean not in ['Võ Tướng', 'Tướng']:
            reg_gen(g_clean)
            for cp in [c4, c5]:
                for part in re.split(r'[/,\n]+', cp):
                    clean_p = clean_tac_name(part)
                    if clean_p:
                        reg_tac(clean_p)
            cur_sub_team["generals"].append({
                "name": g_clean,
                "raw_name": c3.replace('\n', ' '),
                "tactic1": clean_tac_name(c4),
                "tactic2": clean_tac_name(c5),
                "stat_point": c6,
                "binh_thu": [c7] if c7 else []
            })

if cur_set:
    coexisting_portfolios.append(cur_set)

# Also parse "nhiều Team cùng tồn tại" for extra sets
s_nt = wb['nhiều Team cùng tồn tại']
cur_multi_set = None
cur_multi_team = None
for r in range(3, s_nt.max_row + 1):
    c1 = str(s_nt.cell(r, 1).value or '').strip()
    c2 = str(s_nt.cell(r, 2).value or '').strip()
    c3 = str(s_nt.cell(r, 3).value or '').strip()
    c4 = str(s_nt.cell(r, 4).value or '').strip()
    bt1 = str(s_nt.cell(r, 5).value or '').strip()
    bt2 = str(s_nt.cell(r, 6).value or '').strip()
    bt3 = str(s_nt.cell(r, 7).value or '').strip()

    if 'team' in c1.lower() and ('8' in c1 or '7' in c1 or '6' in c1):
        if cur_multi_set:
            coexisting_portfolios.append(cur_multi_set)
        cur_multi_set = {
            "set_id": slugify(c1),
            "set_name": f"Bộ {c1.upper()}",
            "description": f"Phương án xuất chiến cùng tồn tại gồm {c1}",
            "starter_recommendation": "",
            "teams": []
        }
        cur_multi_team = None
        continue

    if c1 and any(t in c1 for t in ['Thương', 'Khiên', 'Cung', 'Kỵ', 'Khí', 'Team']):
        cur_multi_team = {
            "team_name": f"Team {c1}",
            "cost": "19C",
            "generals": []
        }
        if cur_multi_set:
            cur_multi_set["teams"].append(cur_multi_team)

    if cur_multi_team and c2:
        g_clean = clean_gen_name(c2)
        if g_clean and g_clean not in ['Tướng', 'Võ Tướng']:
            reg_gen(g_clean)
            cur_multi_team["generals"].append({
                "name": g_clean,
                "raw_name": c2,
                "tactic1": clean_tac_name(c3),
                "tactic2": clean_tac_name(c4),
                "stat_point": "",
                "binh_thu": [b for b in [bt1, bt2, bt3] if b]
            })

if cur_multi_set:
    coexisting_portfolios.append(cur_multi_set)

print(f"  Extracted {len(coexisting_portfolios)} coexisting sets")

# ==========================================================
# 10. MERGE, DEDUPLICATE & ENRICH META TEAMS
# ==========================================================
print("\n--- 10. Processing & Merging All Meta Teams ---")
# Priority order:
# 1. Team giới thiệu(mới) (PK latest with stars, Binh Thư, Chạm/Tránh)
# 2. Meta mỗi phe (cũ) (Faction teams with full Binh Thư)
# 3. Meta Team (Official T0/T1/T2 tags & descriptions)
# 4. Meta team mùa 4 & mùa 5

all_raw_meta = raw_pk_new_teams + raw_phe_teams + raw_official_teams + raw_m4_teams + raw_m5_teams
processed_meta_teams = []
seen_signatures = {}
positions = ["Chủ tướng", "Phó tướng 1", "Phó tướng 2"]

for raw_t in all_raw_meta:
    gens = raw_t.get('generals', [])
    if len(gens) < 2:
        continue

    team_gens = []
    main_names = []
    has_bt = False

    for idx, g_obj in enumerate(gens[:3]):
        raw_name = g_obj['raw_name']
        alts = [clean_gen_name(p) for p in raw_name.split('/') if clean_gen_name(p)]
        if not alts:
            continue
        mn = alts[0]
        main_names.append(mn)
        reg_gen(mn, raw_t.get('season', 'PK'))

        bis = []
        sub = []
        for cp_raw in [g_obj.get('cp1_raw', ''), g_obj.get('cp2_raw', '')]:
            if not cp_raw:
                continue
            parts = [clean_tac_name(p) for p in re.split(r'[/,\n]+', cp_raw) if clean_tac_name(p)]
            if parts:
                bis.append(parts[0])
                reg_tac(parts[0], season=raw_t.get('season', 'PK'))
                for alt_t in parts[1:]:
                    sub.append(alt_t)
                    reg_tac(alt_t, season=raw_t.get('season', 'PK'))

        bt = g_obj.get('binh_thu', [])
        if bt:
            has_bt = True

        gid = generals_data[mn]["id"] if mn in generals_data else f"{slugify(infer_faction(mn))}_{slugify(mn)}"
        team_gens.append({
            "position": positions[idx] if idx < len(positions) else f"Phó tướng {idx}",
            "general_id": gid,
            "name": mn,
            "raw_name": raw_name,
            "bis_tactics": bis,
            "sub_tactics": sub,
            "binh_thu": bt,
            "alt_generals": alts[1:]
        })

    if len(team_gens) < 2:
        continue

    sig = f"{raw_t.get('season', 'PK')}_" + "_".join(sorted(main_names)) + f"_{raw_t['troop']}"

    # If this signature already seen, enrich it if current has better Binh Thư or better note/tier!
    if sig in seen_signatures:
        existing = seen_signatures[sig]
        # Enrich Binh Thư if existing was empty but current has it
        for ex_g, cur_g in zip(existing['generals'], team_gens):
            if not ex_g.get('binh_thu') and cur_g.get('binh_thu'):
                ex_g['binh_thu'] = cur_g['binh_thu']
        # Enrich note if existing was default and current has rich note
        if ("Chạm:" in raw_t.get('note', '') or "Tránh:" in raw_t.get('note', '')) and "Chạm:" not in existing['description']:
            existing['description'] = raw_t.get('note', '')
        # Enrich tier if current is official T0/T0.5
        if raw_t.get('tier') in ["T0", "T0.5"] and existing.get('tier') not in ["T0", "T0.5"]:
            existing['tier'] = raw_t.get('tier')
        continue

    factions = [infer_faction(g['name']) for g in team_gens]
    team_faction = factions[0] if len(set(factions)) == 1 else "Tam Thế"

    notes_str = raw_t.get('note', '')
    strengths = []
    weaknesses = []
    if "Chạm:" in notes_str or "Cham:" in notes_str:
        key_str = "Chạm:" if "Chạm:" in notes_str else "Cham:"
        match_part = notes_str.split(key_str)[1]
        avoid_key = "Tránh:" if "Tránh:" in match_part else "Tranh:"
        if avoid_key in match_part:
            cham_val = match_part.split(avoid_key)[0].strip()
            tranh_val = match_part.split(avoid_key)[1].strip()
            strengths.append(f"Khắc chế tốt: {cham_val}")
            weaknesses.append(f"Cần né tránh: {tranh_val}")
        else:
            strengths.append(f"Khắc chế tốt: {match_part.strip()}")
    if not strengths:
        strengths.append(f"Đội hình {raw_t['troop']} {raw_t.get('tier', 'T1')} chuẩn meta {raw_t.get('season', 'PK')}")
    if not weaknesses:
        weaknesses.append("Cần căn cứ theo binh chủng và chiến pháp đối phương để linh hoạt khắc chế")

    team_name_str = f"{raw_t['troop']} {team_faction} ({' - '.join(main_names)})"
    team_id = f"meta_{len(processed_meta_teams)+1:03d}_{slugify(team_name_str[:35])}"

    meta_obj = {
        "id": team_id,
        "name": team_name_str,
        "tier": raw_t.get('tier', 'T1'),
        "season": raw_t.get('season', 'PK'),
        "source": raw_t.get('source', ''),
        "faction": team_faction,
        "troop": raw_t['troop'],
        "description": notes_str if notes_str else f"Đội hình {team_name_str} xếp hạng {raw_t.get('tier', 'T1')}.",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "generals": team_gens
    }
    processed_meta_teams.append(meta_obj)
    seen_signatures[sig] = meta_obj

# Second pass: cross-enrich Binh Thư for any team that still has empty Binh Thư
# by checking if any other team uses the exact same general with similar role/tactics!
gen_bt_catalog = {}
for t in processed_meta_teams:
    for g in t['generals']:
        if g.get('binh_thu') and len(g['binh_thu']) >= 2:
            if g['name'] not in gen_bt_catalog:
                gen_bt_catalog[g['name']] = g['binh_thu']

for t in processed_meta_teams:
    for g in t['generals']:
        if not g.get('binh_thu') and g['name'] in gen_bt_catalog:
            g['binh_thu'] = gen_bt_catalog[g['name']]

# Sort teams: PK first (T0 -> T0.5 -> T1 -> T2), then Mùa 4, then Mùa 5
tier_rank = {"T0": 0, "T0.5": 1, "T1": 2, "T2": 3}
season_rank = {"PK": 0, "Mùa 4": 1, "Mùa 5": 2}
processed_meta_teams.sort(key=lambda t: (season_rank.get(t['season'], 99), tier_rank.get(t['tier'], 99)))

generals_list = sorted(generals_data.values(), key=lambda g: (g['faction'], g['name']))
tactics_list = sorted(tactics_data.values(), key=lambda t: (t['type'], t['name']))

# Summary counts
teams_with_bt = sum(1 for t in processed_meta_teams if all(g.get('binh_thu') for g in t['generals']))
gens_with_bt = sum(1 for t in processed_meta_teams for g in t['generals'] if g.get('binh_thu'))

print("\n" + "=" * 60)
print("FINAL SUMMARY REPORT:")
print(f"  Total Generals:                   {len(generals_list)}")
print(f"  Total Tactics:                    {len(tactics_list)}")
print(f"  Total Meta Teams:                 {len(processed_meta_teams)}")
print(f"    - Teams with 100% Binh Thư:     {teams_with_bt}/{len(processed_meta_teams)}")
print(f"    - Generals with Binh Thư:       {gens_with_bt}/{len(processed_meta_teams)*3}")
print(f"  Total Starter Teams:              {len(starter_teams_list)}")
print(f"  Total Team Đô Úy:                 {len(team_do_uy_list)}")
print(f"  Total Cải Tạo Binh Chủng Teams:   {len(cai_tao_teams)}")
print(f"  Total Coexisting Portfolios:      {len(coexisting_portfolios)}")
print("=" * 60)

def save_json(fname, data):
    path = os.path.join(DB_DIR, fname)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    sz = os.path.getsize(path)
    print(f"  Saved {fname} ({sz // 1024} KB)")

save_json("generals.json", generals_list)
save_json("tactics.json", tactics_list)
save_json("meta_teams.json", processed_meta_teams)
save_json("starter_teams.json", starter_database)
save_json("team_do_uy.json", team_do_uy_list)
save_json("cai_tao_binh_chung.json", cai_tao_teams)
save_json("coexisting_portfolios.json", coexisting_portfolios)

print("\nAll database files extracted and updated successfully!")
