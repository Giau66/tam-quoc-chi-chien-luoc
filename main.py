# -*- coding: utf-8 -*-
"""
Main launcher for Tam Quoc Chi - Chien Luoc Web Application.
Run with: py main.py
"""
import uvicorn
import webbrowser
import threading
import time

import socket

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass

if __name__ == "__main__":
    lan_ip = get_lan_ip()
    print("==================================================================")
    print("  TAM QUỐC CHÍ - CHIẾN LƯỢC: TRỢ LÝ ĐỘI HÌNH META & NHẬN DIỆN ẢNH")
    print("  Khởi động máy chủ Web thành công!")
    print(f"  * Truy cập trên máy tính:  http://127.0.0.1:8000")
    print(f"  * Truy cập trên điện thoại: http://{lan_ip}:8000 (cùng WiFi)")
    print("==================================================================")
    # Open browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
