# -*- coding: utf-8 -*-
import urllib.request
import json

def test():
    # 1. Test database
    with urllib.request.urlopen("http://127.0.0.1:8000/api/database") as res:
        db = json.loads(res.read().decode('utf-8'))
        print(f"Database: {len(db['generals'])} generals, {len(db['tactics'])} tactics, {len(db['meta_teams'])} meta teams")

    # 2. Test recommend ranked
    payload = {
        "owned_generals": ["Khương Duy", "Bàng Thống", "Gia Cát Lượng", "Tào Tháo", "Tư Mã Ý", "Mãn Sủng"],
        "owned_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật", "Bát Môn Kim Tỏa", "Quân Dân Khích Lệ"],
        "mode": "ranked",
        "min_score": 20
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/recommend",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        print(f"Ranked mode: {data['count']} teams found")
        for item in data['results'][:3]:
            print(f"  * {item['meta_team']['name']} - Điểm: {item['overall_score']}% ({item['rating_label']})")

    # 3. Test portfolio mode
    payload_portfolio = {
        "owned_generals": ["Khương Duy", "Bàng Thống", "Gia Cát Lượng", "Tào Tháo", "Tư Mã Ý", "Mãn Sủng", "Lưu Bị", "Trương Phi", "Quan Vũ"],
        "owned_tactics": ["Thái Bình Đạo Pháp", "Sĩ Biệt Tam Nhật", "Bát Môn Kim Tỏa", "Quân Dân Khích Lệ", "Thảo Thuyền Mượn Tên", "Tạm Thời Tránh Mũi Nhọn"],
        "mode": "portfolio",
        "max_teams": 3
    }
    req2 = urllib.request.Request(
        "http://127.0.0.1:8000/api/recommend",
        data=json.dumps(payload_portfolio).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req2) as res:
        data2 = json.loads(res.read().decode('utf-8'))
        print(f"Portfolio mode: {data2['count']} multi-team options found")

    # 4. Test starter teams recommendation
    payload_starter = {
        "owned_generals": [
            "Khương Duy", "SP Quan Vũ", "Quan Vũ", "Triệu Vân", "Trương Phi", "Hoàng Trung",
            "Bàng Thống", "Mã Siêu", "Quan Hưng", "Mã Đại", "Trương Bào", "Nghiêm Nhan", "Y Tịch",
            "Tôn Kiên", "SP Tôn Kiên", "Tôn Thượng Hương", "Lục Tốn", "Chu Thái", "Thái Sử Từ",
            "Cam Ninh", "Đại Kiều", "Lục Kháng", "Tư Mã Ý", "Giả Hủ", "SP Bàng Đức", "Hạ Hầu Đôn",
            "Từ Hoảng", "Chân Cơ", "Vương Song", "Lữ Bố", "Trương Giác", "SP Chu Tuấn", "SP Trương Bảo",
            "Điêu Thuyền", "Điền Phong", "Lữ Linh Ỷ", "Chúc Dung", "Viên Thiệu", "Mạnh Hoạch", "Mã Quân"
        ],
        "owned_tactics": [
            "Mưu Lược Tung Hoành", "Lư Giang Thượng Giáp", "Thi Chí Bất Di", "Thần Thượng Sứ",
            "Tự Lành", "Kiêu Kiện Thần Hành", "Tị Thực Kích Hư", "Tài Khí Quá Nhân", "Phấn Đột",
            "Loạn Cung Ẩm Vũ", "Yêu Thuật", "Nhất Cử Tiệm Diệt", "Bất Nhục Sứ Mệnh", "Ám Tàng Huyền Cơ",
            "Trá Hàng", "Tịnh Hóa", "Xua Đuổi", "Ỷ Thế Cầm Quyền", "Chờ Đợi Xuất Phát", "Đánh Vào Chỗ Đau",
            "Đánh Vào Chỗ Hiểm", "Ngự Địch Bình Chướng"
        ]
    }
    req_starter = urllib.request.Request(
        "http://127.0.0.1:8000/api/recommend-starter",
        data=json.dumps(payload_starter).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_starter) as res:
        starter_res = json.loads(res.read().decode('utf-8'))
        print(f"Starter teams evaluated: {len(starter_res['starter_teams'])}")
        for st in starter_res['starter_teams'][:3]:
            gens = [f"{g['active_name']} ({'Có' if g['is_owned'] else 'Thiếu'})" for g in st['generals']]
            print(f"  * [{st['troop']}] {' - '.join(gens)} | Tướng: {st['owned_generals_count']}/{st['total_generals']} ({st['starter_rating']})")

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    test()
