@echo off
chcp 65001 > nul
title Tam Quốc Chí: Chiến Lược - Trợ Lý Đội Hình Web
echo ====================================================================
echo   TAM QUỐC CHÍ: CHIẾN LƯỢC - KHỞI ĐỘNG WEBSITE TRỢ LÝ ĐỘI HÌNH
echo ====================================================================
echo.
echo Đang khởi chạy máy chủ web và tự động mở trình duyệt...
echo Địa chỉ truy cập: http://127.0.0.1:8000
echo.
python main.py
if errorlevel 1 (
    echo.
    echo [LỖI] Không thể chạy với 'python'. Đang thử lệnh 'py'...
    py main.py
)
pause
