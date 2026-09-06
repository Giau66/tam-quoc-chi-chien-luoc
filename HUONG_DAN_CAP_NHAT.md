# 📘 HƯỚNG DẪN CẬP NHẬT & VẬN HÀNH WEBSITE TAM QUỐC CHÍ CHIẾN LƯỢC

Tài liệu này hướng dẫn chi tiết quy trình cập nhật web từ máy tính cá nhân lên **GitHub** và triển khai lên máy chủ online **Render.com**.

---

## 📌 THÔNG TIN ĐƯỜNG LINK HỆ THỐNG

| Mục đích | Đường dẫn (URL) | Ghi chú |
| :--- | :--- | :--- |
| **Web Online (Mọi nơi)** | 🌐 [https://tam-quoc-chi-chien-luoc.onrender.com](https://tam-quoc-chi-chien-luoc.onrender.com) | Chia sẻ cho bạn bè / điện thoại |
| **Web Trực tiếp (Local)** | 💻 [http://127.0.0.1:8000](http://127.0.0.1:8000) | Mở ngay tức thì trên máy tính |
| **Web qua WiFi LAN** | 📱 `http://192.168.1.52:8000` | Điện thoại kết nối cùng WiFi |
| **Mã nguồn GitHub** | 📂 [https://github.com/Giau66/tam-quoc-chi-chien-luoc](https://github.com/Giau66/tam-quoc-chi-chien-luoc) | Kho lưu trữ code |
| **Quản lý Render** | ⚙️ [https://dashboard.render.com](https://dashboard.render.com) | Bảng điều khiển máy chủ |

---

## PHẦN 1: CẬP NHẬT WEB ONLINE TRÊN RENDER.COM

Khi bạn đã sửa code trên máy hoặc đã push lên GitHub, thực hiện các bước sau để web online nhận bản mới nhất:

### Cách 1: Cập nhật ngay lập tức bằng tay (Manual Deploy)
1. Truy cập vào trang quản lý: **[https://dashboard.render.com](https://dashboard.render.com)**
2. Đăng nhập bằng tài khoản **GitHub** của bạn.
3. Nhấp chọn Web Service có tên **`tam-quoc-chi-chien-luoc`**.
4. Ở góc trên bên phải màn hình, nhấp nút **`Manual Deploy`**.
5. Chọn một trong hai lựa chọn:
   * **`Deploy latest commit`**: Cập nhật bản mới nhất từ nhánh `main` (nhanh nhất).
   * **`Clear build cache & deploy`**: Xóa bộ nhớ đệm và build lại từ đầu (dùng khi bạn thêm thư viện mới hoặc sửa Dockerfile).
6. Đợi khoảng **2 - 4 phút**. Khi nào trạng thái đổi sang chữ **`Live` màu xanh lá**, hãy vào lại trang web để kiểm tra.

### Cách 2: Cấu hình tự động cập nhật (Auto-Deploy) - Nên bật
Để mỗi lần bạn đẩy code lên GitHub (`git push`), Render sẽ tự động cập nhật mà không cần bấm tay:
1. Trong trang Web Service trên Render, bấm vào thẻ **`Settings`** ở menu bên trái.
2. Cuộn chuột xuống tìm mục **`Auto-Deploy`**.
3. Chuyển tùy chọn sang **`Yes`**.
4. Bấm nút **`Save Changes`** bên dưới.

---

## PHẦN 2: QUY TRÌNH ĐẨY CODE TỪ MÁY LÊN GITHUB

Khi bạn chỉnh sửa file trong thư mục dự án (`d:\TamQuocChiChienLuoc`), mở terminal **PowerShell** tại thư mục dự án và chạy 3 lệnh sau:

```bash
# 1. Thêm tất cả các file đã thay đổi vào danh sách chuẩn bị lưu
git add .

# 2. Tạo bản ghi nhận thay đổi (ghi chú ngắn gọn nội dung cập nhật)
git commit -m "feat: cap nhat du lieu va giao dien moi"

# 3. Đẩy code lên GitHub
git push origin main
```

> **Mẹo:** Nếu bạn đã bật tính năng **Auto-Deploy** ở Phần 1, ngay sau khi gõ lệnh `git push origin main`, Render sẽ tự động cập nhật web cho bạn!

---

## PHẦN 3: CẬP NHẬT DỮ LIỆU TỪ FILE EXCEL

Mỗi khi bạn có file Excel mới (`Meta Team Gioi Thieu Mua PK.xlsx`):
1. Chép đè file Excel mới vào thư mục gốc `d:\TamQuocChiChienLuoc`.
2. Mở terminal gõ lệnh để trích xuất lại toàn bộ 12 sheet vào hệ cơ sở dữ liệu:
   ```bash
   py database/full_extract_v2.py
   ```
3. Sau khi file chạy xong (khoảng 5-10 giây), dữ liệu trong thư mục `database/` sẽ tự động cập nhật.
4. Tiếp tục thực hiện **Phần 2 (Git Push)** và **Phần 1 (Render Deploy)**.

---

## PHẦN 4: KHỞI ĐỘNG CHẠY WEB TRÊN MÁY TÍNH CÁ NHÂN (LOCAL)

Để trải nghiệm tốc độ nhanh nhất hoặc kiểm tra trước khi đưa lên mạng:

1. Mở PowerShell trong thư mục `d:\TamQuocChiChienLuoc`.
2. Chạy lệnh:
   ```bash
   py main.py
   ```
3. Hệ thống sẽ tự động bật trình duyệt web tại địa chỉ `http://127.0.0.1:8000`.
4. Muốn tắt server: Trở lại cửa sổ PowerShell và nhấn tổ hợp phím **`Ctrl + C`**.

---

## ⚠️ XỬ LÝ SỰ CỐ THƯỜNG GẶP

### 1. Web đã báo "Live" trên Render nhưng mở lên vẫn thấy giao diện cũ?
* **Nguyên nhân:** Trình duyệt web (Chrome, Edge, Cốc Cốc) lưu bản cache cũ của trang HTML/CSS.
* **Cách khắc phục:** 
  * Trên máy tính: Bấm tổ hợp phím **`Ctrl + F5`** (hoặc `Ctrl + Shift + R`) để ép trình duyệt tải mới hoàn toàn.
  * Trên điện thoại: Xóa lịch sử duyệt web gần nhất hoặc mở tab ẩn danh.

### 2. Bấm vào link Render bị quay vòng vòng lâu (30 - 50 giây)?
* **Nguyên nhân:** Do sử dụng gói miễn phí của Render, sau 15 phút không có người truy cập, máy chủ sẽ chuyển sang trạng thái "ngủ" để tiết kiệm tài nguyên.
* **Cách khắc phục:** Đây là cơ chế hoàn toàn bình thường của Render Free. Bạn chỉ cần đợi khoảng 40 giây cho máy chủ khởi động lại lần đầu tiên, những lượt truy cập sau đó sẽ rất nhanh.
