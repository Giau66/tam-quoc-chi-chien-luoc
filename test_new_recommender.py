# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from recommender.engine import TeamRecommender

rec = TeamRecommender("database")

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

print("=== RECOMMENDED TEAMS ===")
teams = rec.recommend(user_gens, user_tacs, min_score=30)
print(f"Total recommended teams: {len(teams)}")

for i, t in enumerate(teams[:10]):
    mt = t["meta_team"]
    gens_info = []
    for g in t["generals_eval"]:
        status = "✓ Có" if (g["is_main"] or g["is_sub"]) else "❌ Thiếu"
        gens_info.append(f"{g['target_name']} ({status})")
    
    tactics_info = []
    for g in t["generals_eval"]:
        for tc in g["tactics"]:
            tactics_info.append(f"{tc['name']} [{tc['status_label']}]")

    print(f"\n{i+1}. [{mt['tier']}] {mt['name']}")
    print(f"   Score: {t['overall_score']}% | Tướng: {t['owned_gen_count']}/3 ({t['rating_label']})")
    print(f"   Tướng: {' | '.join(gens_info)}")
    print(f"   Chiến pháp: {' | '.join(tactics_info[:4])}...")

print("\n=== STARTER TEAMS (KHAI HOANG) ===")
starter_res = rec.recommend_starter_teams(user_gens, user_tacs)
starters = starter_res["starter_teams"]
for s in starters[:5]:
    gens_str = " - ".join([f"{g['active_name']} ({'Có' if g['is_owned'] else 'Thiếu'})" for g in s["generals"]])
    print(f"  [{s['owned_generals_count']}/{s['total_generals']} tướng - {s['gen_percentage']}%] {s['troop']}: {gens_str}")
