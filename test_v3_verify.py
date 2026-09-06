import requests, sys

BASE = "http://127.0.0.1:8000"
ok = True

# Test recommend API with smart scoring
r = requests.post(BASE + "/api/recommend", json={
    "owned_generals": ["Tao Thao", "Tu Ma Y", "Trieu Van"],
    "owned_tactics": ["Hoanh Tao Thien Quan", "Si Biet Tam Nhat", "Quan Dan Khich Le"],
    "season": "All", "faction": "All", "troop": "All", "min_score": 30
})
data = r.json()
results = data.get("results", [])
print("Recommend API:", r.status_code, "-", len(results), "teams")
if results:
    top = results[0]
    score = top["overall_score"]
    syn = top.get("synergy_bonus", "N/A")
    farm_count = len(top.get("farm_suggestions", []))
    cov = top.get("role_coverage", {}).get("coverage_score", "N/A")
    print("  Score:", score, "% | Synergy:", syn, "| Farm:", farm_count, "| Coverage:", cov, "/4")
    if "synergy_bonus" not in top:
        print("  ERROR: synergy_bonus missing!")
        ok = False

# Test static serving
r2 = requests.get(BASE + "/tools.html")
has_tab = "tab-ai-chat" in r2.text
has_css = "ai-chat.css" in r2.text
has_js = "ai-chat.js" in r2.text
has_modal = "ai-analyze-overlay" in r2.text
print("tools.html:", r2.status_code)
print("  AI tab:", has_tab, "| CSS:", has_css, "| JS:", has_js, "| Modal:", has_modal)

r3 = requests.get(BASE + "/js/ai-chat.js")
has_fn = "sendAIMessage" in r3.text
has_analyze = "openAnalyzeModal" in r3.text
print("ai-chat.js:", r3.status_code, "| sendAI:", has_fn, "| analyze:", has_analyze)

r4 = requests.get(BASE + "/css/ai-chat.css")
has_chat = "ai-chat-wrap" in r4.text
print("ai-chat.css:", r4.status_code, "| styles:", has_chat)

if ok and has_tab and has_css and has_js and has_modal and has_fn and has_analyze and has_chat:
    print()
    print("=== ALL CHECKS PASSED ===")
else:
    print()
    print("=== SOME CHECKS FAILED ===")
    sys.exit(1)
