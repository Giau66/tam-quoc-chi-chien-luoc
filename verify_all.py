import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("========================================")
    print("1. KIỂM TRA API DATABASE")
    print("========================================")
    with urllib.request.urlopen(f"{BASE_URL}/api/database") as res:
        assert res.status == 200
        data = json.loads(res.read().decode('utf-8'))
        print(f"  * Generals: {len(data['generals'])}")
        print(f"  * Tactics: {len(data['tactics'])}")
        print(f"  * Meta Teams: {len(data['meta_teams'])}")
        print(f"  * Coexisting Portfolios: {len(data.get('coexisting_portfolios', []))}")
        print(f"  * Tactic Substitutes: {len(data.get('tactic_substitutes', {}))} chiến pháp có phương án thay thế")
        assert len(data['generals']) > 0
        assert len(data['tactics']) > 0
        assert len(data['meta_teams']) > 0
        assert len(data['tactic_substitutes']) > 0

    print("\n========================================")
    print("2. KIỂM TRA API MÙA GIẢI")
    print("========================================")
    with urllib.request.urlopen(f"{BASE_URL}/api/seasons") as res:
        assert res.status == 200
        seasons = json.loads(res.read().decode('utf-8'))
        print(f"  * Số mùa giải: {len(seasons)}")
        for s in seasons:
            print(f"    - [{s['id']}] {s['name']} (Ảnh: {s.get('image_count', 0)})")

    with urllib.request.urlopen(f"{BASE_URL}/api/seasons/pk20") as res:
        assert res.status == 200
        pk20 = json.loads(res.read().decode('utf-8'))
        print(f"  * Chi tiết PK20:")
        print(f"    - Tướng mới: {len(pk20.get('new_generals', []))}")
        print(f"    - Ảnh đội hình: {len(pk20.get('images', []))}")
        print(f"    - Team giới thiệu: {len(pk20.get('intro_teams', []))}")
        print(f"    - Team Đô Úy: {len(pk20.get('douy_teams', []))}")
        assert len(pk20.get('images', [])) > 0
        assert len(pk20.get('intro_teams', [])) > 0

    print("\n========================================")
    print("3. KIỂM TRA ĐỀ XUẤT META (RANKED & PORTFOLIO)")
    print("========================================")
    payload = {
        'owned_generals': ['Khương Duy', 'Bàng Thống', 'Gia Cát Lượng', 'Tư Mã Ý', 'Tào Tháo', 'Mãn Sủng'],
        'owned_tactics': ['Quân Dân Khích Lệ', 'Thảo Thuyền Mượn Tên', 'Sĩ Biệt Ba Ngày'],
        'min_score': 30
    }
    req = urllib.request.Request(f"{BASE_URL}/api/recommend", data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        rec = json.loads(res.read().decode('utf-8'))
        print(f"  * Ranked results: {len(rec['results'])} đội hình")
        top = rec['results'][0]
        print(f"    - Top 1: [{top['meta_team']['tier']}] {top['meta_team']['name']} ({top['overall_score']}%)")

    payload['mode'] = 'portfolio'
    payload['max_teams'] = 3
    req = urllib.request.Request(f"{BASE_URL}/api/recommend", data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        port = json.loads(res.read().decode('utf-8'))
        print(f"  * Portfolio results: {len(port['results'])} đội hình độc lập không trùng")

    print("\n========================================")
    print("4. KIỂM TRA ĐỘI HÌNH KHAI HOANG & MỎ & THÁM THÍNH")
    print("========================================")
    req = urllib.request.Request(f"{BASE_URL}/api/recommend-starter", data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        starter = json.loads(res.read().decode('utf-8'))
        print(f"  * Starter teams: {len(starter.get('starter_teams', []))}")
        print(f"  * Mines guide tiers: {list(starter.get('mines_guide', {}).keys())}")
        print(f"  * Touch scouts: {len(starter.get('touch_scout_teams', []))}")
        assert len(starter.get('mines_guide', {})) > 0
        assert len(starter.get('touch_scout_teams', [])) > 0

    print("\n========================================")
    print("5. KIỂM TRA CÁC TRANG & STATIC ASSETS")
    print("========================================")
    pages = [
        "/",
        "/tools.html",
        "/seasons.html",
        "/js/app.js",
        "/js/seasons.js",
        "/js/auth.js",
        "/js/ai-chat.js",
        "/css/style.css",
        "/css/seasons.css",
        "/css/navbar.css",
        "/css/auth.css",
        "/css/landing.css"
    ]
    for p in pages:
        with urllib.request.urlopen(f"{BASE_URL}{p}") as res:
            assert res.status == 200
            print(f"  ✓ {p} : OK (200, {len(res.read())} bytes)")

    print("\n========================================")
    print("✅ TẤT CẢ CÁC BƯỚC KIỂM TRA ĐỀU THÀNH CÔNG RỰC RỠ!")
    print("========================================")

if __name__ == '__main__':
    test_api()
