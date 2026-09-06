# -*- coding: utf-8 -*-
"""
FastAPI Server for Tam Quoc Chi - Chien Luoc Team Builder Web App.
v2.0 - Full website with Auth, Cloud Save, Seasons, and Tools API.
"""
import os
import json
import shutil
import uuid
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from recommender.engine import TeamRecommender, TACTIC_SUBSTITUTE_GUIDE
from recognition.vision_service import VisionService
from database.auth import (
    create_user, authenticate_user, get_user_safe,
    get_inventory, save_inventory,
    create_access_token, decode_token
)

# ─────────────────────────────────────────────
app = FastAPI(title="Tam Quốc Chí - Chiến Lược API v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
HINH_DIR   = os.path.join(BASE_DIR, "hinh")
DB_DIR     = os.path.join(BASE_DIR, "database")
ANH_DIR    = os.path.join(BASE_DIR, "anh")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize engines
recommender    = TeamRecommender()
vision_service = VisionService()

# Bearer auth helper
security = HTTPBearer(auto_error=False)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[int]:
    if not credentials:
        return None
    payload = decode_token(credentials.credentials)
    if not payload:
        return None
    return payload.get("user_id")

def require_user(user_id: Optional[int] = Depends(get_current_user_id)) -> int:
    if not user_id:
        raise HTTPException(status_code=401, detail="Vui lòng đăng nhập để tiếp tục.")
    return user_id

# ─────────────────────────────────────────────
# AUTH ENDPOINTS
# ─────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    display_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Mật khẩu phải có ít nhất 6 ký tự.")
    if len(req.username) < 3:
        raise HTTPException(status_code=400, detail="Tên đăng nhập phải có ít nhất 3 ký tự.")
    try:
        user = create_user(req.username, req.email, req.password, req.display_name)
        token = create_access_token({"user_id": user["id"]})
        return {
            "success": True,
            "token": token,
            "user": {k: v for k, v in user.items() if k != "password"}
        }
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.post("/api/auth/login")
def login(req: LoginRequest):
    user = authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng.")
    token = create_access_token({"user_id": user["id"]})
    safe = {k: v for k, v in user.items() if k != "password"}
    return {"success": True, "token": token, "user": safe}

@app.get("/api/auth/me")
def me(user_id: int = Depends(require_user)):
    user = get_user_safe(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")
    return user

# ─────────────────────────────────────────────
# INVENTORY (CLOUD SAVE)
# ─────────────────────────────────────────────

class InventoryRequest(BaseModel):
    owned_generals: List[str]
    owned_tactics: List[str]

@app.get("/api/user/inventory")
def get_user_inventory(user_id: int = Depends(require_user)):
    return get_inventory(user_id)

@app.post("/api/user/inventory")
def save_user_inventory(req: InventoryRequest, user_id: int = Depends(require_user)):
    return save_inventory(user_id, req.owned_generals, req.owned_tactics)

# ─────────────────────────────────────────────
# SEASONS
# ─────────────────────────────────────────────

def load_seasons():
    path = os.path.join(DB_DIR, "seasons.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/api/seasons")
def get_seasons():
    seasons = load_seasons()
    # Return lightweight version (without full image list)
    result = []
    for s in seasons:
        item = {k: v for k, v in s.items() if k not in ("images",)}
        item["image_count"] = len(s.get("images", []))
        result.append(item)
    return result

@app.get("/api/seasons/{season_id}")
def get_season_detail(season_id: str):
    seasons = load_seasons()
    for s in seasons:
        if s["id"] == season_id:
            return s
    raise HTTPException(status_code=404, detail="Không tìm thấy mùa giải.")

@app.get("/api/seasons/{season_id}/images")
def get_season_images(season_id: str):
    seasons = load_seasons()
    for s in seasons:
        if s["id"] == season_id:
            return {"images": s.get("images", []), "count": len(s.get("images", []))}
    raise HTTPException(status_code=404, detail="Không tìm thấy mùa giải.")

# ─────────────────────────────────────────────
# EXISTING DATABASE API
# ─────────────────────────────────────────────

@app.get("/api/database")
def get_database():
    return {
        "generals": recommender.generals,
        "tactics": recommender.tactics,
        "meta_teams": recommender.meta_teams,
        "coexisting_portfolios": getattr(recommender, "coexisting_portfolios", []),
        "tactic_substitutes": TACTIC_SUBSTITUTE_GUIDE
    }

@app.get("/api/coexisting-portfolios")
def get_coexisting_portfolios():
    return getattr(recommender, "coexisting_portfolios", [])

@app.get("/api/starter-teams")
def get_starter_teams():
    return recommender.starter_data

# ─────────────────────────────────────────────
# IMAGE UPLOAD & OCR
# ─────────────────────────────────────────────

@app.post("/api/upload-images")
async def upload_images(
    files: List[UploadFile] = File(...),
    gemini_api_key: Optional[str] = Form(None)
):
    detected_generals = set()
    detected_tactics  = set()
    file_results = []

    for file in files:
        file_id  = str(uuid.uuid4())[:8]
        filename = f"{file_id}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        res = vision_service.recognize_image(filepath, gemini_api_key)
        for g in res.get("generals", []):
            detected_generals.add(g)
        for t in res.get("tactics", []):
            detected_tactics.add(t)

        file_results.append({
            "filename": file.filename,
            "detected_generals": res.get("generals", []),
            "detected_tactics": res.get("tactics", []),
            "source": res.get("source", "unknown"),
            "success": res.get("success", True),
            "error": res.get("error")
        })

    return {
        "success": True,
        "total_generals": len(detected_generals),
        "total_tactics": len(detected_tactics),
        "generals": sorted(list(detected_generals)),
        "tactics": sorted(list(detected_tactics)),
        "details": file_results
    }

# ─────────────────────────────────────────────
# RECOMMENDER
# ─────────────────────────────────────────────

class RecommendRequest(BaseModel):
    owned_generals: List[str]
    owned_tactics: List[str]
    season: Optional[str] = "All"
    faction: Optional[str] = "All"
    troop: Optional[str] = "All"
    min_score: Optional[int] = 30
    mode: Optional[str] = "ranked"
    max_teams: Optional[int] = 4

@app.post("/api/recommend")
def recommend_teams(req: RecommendRequest):
    if req.mode == "portfolio":
        portfolio = recommender.build_multi_team_portfolio(
            owned_generals=req.owned_generals,
            owned_tactics=req.owned_tactics,
            max_teams=req.max_teams or 4
        )
        return {"mode": "portfolio", "count": len(portfolio), "results": portfolio}
    else:
        ranked = recommender.recommend(
            owned_generals=req.owned_generals,
            owned_tactics=req.owned_tactics,
            season_filter=req.season or "All",
            faction_filter=req.faction or "All",
            troop_filter=req.troop or "All",
            min_score=req.min_score or 30
        )
        return {"mode": "ranked", "count": len(ranked), "results": ranked}

class StarterRecommendRequest(BaseModel):
    owned_generals: List[str]
    owned_tactics: List[str]

@app.post("/api/recommend-starter")
def recommend_starter(req: StarterRecommendRequest):
    return recommender.recommend_starter_teams(req.owned_generals, req.owned_tactics)

# ─────────────────────────────────────────────
# AI FEATURES (Gemini-powered)
# ─────────────────────────────────────────────

class AIChatRequest(BaseModel):
    question: str
    owned_generals: List[str] = []
    owned_tactics: List[str] = []
    gemini_api_key: str

class AnalyzeTeamRequest(BaseModel):
    team_id: str
    team_name: str
    generals: List[str]
    tactics: List[str]
    owned_generals: List[str] = []
    owned_tactics: List[str] = []
    score: Optional[int] = None
    tier: Optional[str] = None
    faction: Optional[str] = None
    troop: Optional[str] = None
    gemini_api_key: str

def call_gemini_text(prompt: str, api_key: str, temperature: float = 0.7) -> str:
    """Shared Gemini text API caller."""
    import requests as req_lib
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": 1024}
    }
    resp = req_lib.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=25)
    if resp.status_code == 200:
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    raise Exception(f"Gemini API lỗi: {resp.status_code} — {resp.text[:200]}")

@app.post("/api/ai-chat")
def ai_chat(req: AIChatRequest):
    """AI Assistant: Trả lời câu hỏi chiến thuật dựa vào kho đồ của người dùng."""
    if not req.gemini_api_key or len(req.gemini_api_key.strip()) < 10:
        raise HTTPException(status_code=400, detail="Vui lòng nhập Gemini API Key hợp lệ.")
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống.")

    # Build context from user's inventory
    gen_list = ", ".join(req.owned_generals[:50]) if req.owned_generals else "Chưa có tướng nào"
    tac_list = ", ".join(req.owned_tactics[:50]) if req.owned_tactics else "Chưa có chiến pháp nào"

    prompt = f"""Bạn là chuyên gia chiến thuật game Tam Quốc Chí - Chiến Lược (Three Kingdoms Strategy).
Nhiệm vụ: Trả lời câu hỏi chiến thuật của người chơi một cách chính xác, ngắn gọn và hữu ích.

THÔNG TIN KHO ĐỒ NGƯỜI CHƠI:
- Tướng sở hữu: {gen_list}
- Chiến pháp sở hữu: {tac_list}

CÂU HỎI: {req.question}

Hướng dẫn trả lời:
1. Trả lời trực tiếp câu hỏi, ưu tiên đề xuất dựa trên kho đồ thực tế của người chơi.
2. Nếu họ hỏi về đội hình, gợi ý cụ thể: [Tướng 1] + [Tướng 2] + [Tướng 3], kèm chiến pháp BIS.
3. Nếu thiếu tướng/chiến pháp để hoàn thiện đội, gợi ý nên farm gì tiếp theo.
4. Dùng tiếng Việt, ngắn gọn, dễ hiểu. Tối đa 300 từ.
5. Dùng emoji để làm rõ (⚔️ cho tướng, 📜 cho chiến pháp, 🏆 cho tier, 💡 cho gợi ý).
"""

    try:
        answer = call_gemini_text(prompt, req.gemini_api_key.strip(), temperature=0.5)
        return {"success": True, "answer": answer, "question": req.question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi AI: {str(e)}")

@app.post("/api/analyze-team")
def analyze_team(req: AnalyzeTeamRequest):
    """AI Team Analyzer: Phân tích sâu một đội hình cụ thể."""
    if not req.gemini_api_key or len(req.gemini_api_key.strip()) < 10:
        raise HTTPException(status_code=400, detail="Vui lòng nhập Gemini API Key hợp lệ.")

    gen_display = " + ".join(req.generals) if req.generals else "?"
    tac_display = ", ".join(req.tactics) if req.tactics else "?"
    owned_display = ", ".join(req.owned_generals[:30]) if req.owned_generals else "Chưa có"
    owned_tac_display = ", ".join(req.owned_tactics[:30]) if req.owned_tactics else "Chưa có"

    prompt = f"""Bạn là chuyên gia chiến thuật game Tam Quốc Chí - Chiến Lược.
Phân tích chi tiết đội hình sau:

ĐỘI HÌNH: {req.team_name}
- Tướng: {gen_display}
- Chiến pháp BIS: {tac_display}
- Phe: {req.faction or '?'} | Binh chủng: {req.troop or '?'} | Tier: {req.tier or '?'}
- Điểm tương thích kho đồ: {req.score or '?'}%

KHO ĐỒ NGƯỜI CHƠI:
- Tướng có: {owned_display}
- Chiến pháp có: {owned_tac_display}

Phân tích theo 4 mục sau (dùng emoji đầu mục):
⚡ ĐIỂM MẠNH: Điểm mạnh nổi bật của đội hình này (2-3 điểm)
⚠️ ĐIỂM YẾU / KHẮC CHẾT: Đội hình nào/chiến pháp nào khắc chế đội này
🎯 CHIẾN THUẬT TRIỂN KHAI: Cách dùng đội hiệu quả nhất (binh chủng, skill order)
🔧 GỢI Ý HOÀN THIỆN: Nếu thiếu tướng/chiến pháp, nên farm gì để hoàn thiện đội

Trả lời bằng tiếng Việt, ngắn gọn súc tích, tổng cộng không quá 350 từ.
"""

    try:
        analysis = call_gemini_text(prompt, req.gemini_api_key.strip(), temperature=0.4)
        return {"success": True, "analysis": analysis, "team_name": req.team_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi AI: {str(e)}")

@app.get("/favicon.ico")
def favicon():
    fav_path = os.path.join(BASE_DIR, "anh", "tamquocchi.jpg")
    if os.path.exists(fav_path):
        return FileResponse(fav_path, media_type="image/jpeg")
    return JSONResponse(status_code=404, content={"detail": "Not found"})

# ─────────────────────────────────────────────
# STATIC FILES
# ─────────────────────────────────────────────

# Serve season images from hinh/ folder at /hinh/
if os.path.isdir(HINH_DIR):
    app.mount("/hinh", StaticFiles(directory=HINH_DIR), name="hinh")

# Serve assets from anh/ folder at /anh/
if os.path.isdir(ANH_DIR):
    app.mount("/anh", StaticFiles(directory=ANH_DIR), name="anh")

# Serve main static app
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)

