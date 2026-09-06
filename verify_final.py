# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import json

payload = {
    'owned_generals': [
        'Khương Duy', 'SP Quan Vũ', 'Quan Vũ', 'Triệu Vân', 'Trương Phi', 'Hoàng Trung',
        'Bàng Thống', 'Mã Siêu', 'Quan Hưng', 'Mã Đại', 'Trương Bào', 'Nghiêm Nhan', 'Y Tịch',
        'Tôn Kiên', 'SP Tôn Kiên', 'Tôn Thượng Hương', 'Lục Tốn', 'Chu Thái', 'Thái Sử Từ',
        'Cam Ninh', 'Đại Kiều', 'Lục Kháng', 'Tư Mã Ý', 'Giả Hủ', 'SP Bàng Đức', 'Hạ Hầu Đôn',
        'Từ Hoảng', 'Chân Cơ', 'Vương Song', 'Lữ Bố', 'Trương Giác', 'SP Chu Tuấn', 'SP Trương Bảo',
        'Điêu Thuyền', 'Điền Phong', 'Lữ Linh Ỷ', 'Chúc Dung', 'Viên Thiệu', 'Mạnh Hoạch', 'Mã Quân'
    ],
    'owned_tactics': [
        'Mưu Lược Tung Hoành', 'Lư Giang Thượng Giáp', 'Thi Chí Bất Di', 'Thần Thượng Sứ',
        'Tự Lành', 'Kiêu Kiện Thần Hành', 'Tị Thực Kích Hư', 'Tài Khí Quá Nhân', 'Phấn Đột',
        'Loạn Cung Ẩm Vũ', 'Yêu Thuật', 'Nhất Cử Tiệm Diệt', 'Bất Nhục Sứ Mệnh', 'Ám Tàng Huyền Cơ',
        'Trá Hàng', 'Tịnh Hóa', 'Xua Đuổi', 'Ỷ Thế Cầm Quyền', 'Chờ Đợi Xuất Phát', 'Đánh Vào Chỗ Đau',
        'Đánh Vào Chỗ Hiểm', 'Ngự Địch Bình Chướng'
    ],
    'min_score': 30
}

req = urllib.request.Request('http://127.0.0.1:8000/api/recommend', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))

print(f"=== KẾT QUẢ ĐỀ XUẤT META CHO KHO CỦA USER ({len(data['results'])} đội) ===")
for i, t in enumerate(data['results'][:5]):
    mt = t['meta_team']
    gens_str = " - ".join([f"{g['target_name']} ({'Có' if g['is_main'] else 'Thiếu'})" for g in t['generals_eval']])
    subs = []
    for g in t['generals_eval']:
        for tc in g['tactics']:
            if tc.get('is_substitute'):
                subs.append(f"{tc['name']} -> {tc.get('original_bis')}")
    print(f"\n{i+1}. [{mt['tier']}] {mt['name']}")
    print(f"   Tướng: {gens_str} [Sở hữu: {t['owned_gen_count']}/3]")
    print(f"   Độ hoàn thiện: {t['overall_score']}% ({t['rating_label']})")
    if subs:
        print(f"   Thay thế chiến pháp: {', '.join(subs[:3])}")

# Test Starter
req_st = urllib.request.Request('http://127.0.0.1:8000/api/recommend-starter', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
resp_st = urllib.request.urlopen(req_st)
data_st = json.loads(resp_st.read().decode('utf-8'))

print(f"\n=== ĐỘI HÌNH KHAI HOANG (MỞ ĐẤT) ===")
for i, st in enumerate(data_st['starter_teams'][:4]):
    gens_str = " - ".join([f"{g['active_name']} ({'Có' if g['is_owned'] else 'Thiếu'})" for g in st['generals']])
    print(f"{i+1}. [{st['troop']}] {gens_str} | Tướng: {st['owned_generals_count']}/{st['total_generals']} ({st['starter_rating']})")
