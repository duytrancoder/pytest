
## 📂 Cấu Trúc Thư Mục Dự Án

```text
pytestdemo/
├── app.py                      # Mã nguồn chính của ứng dụng Flask
├── test_app.py                 # Bộ kiểm thử tự động gồm 19 ca test viết bằng Pytest
├── requirements.txt            # Danh sách thư viện và dependencies
├── Dockerfile                  # Cấu hình đóng gói Docker container cho ứng dụng
├── docker-compose.yml          # Thiết lập chạy ứng dụng Flask và database MySQL song song
├── static/                     # Các file tĩnh (CSS, JS, Images nếu có)
├── templates/                  # Giao diện HTML (Jinja2)
│   ├── base.html               # Layout cơ sở
│   ├── auth.html               # Giao diện Đăng nhập / Đăng ký
│   ├── products.html           # Quản lý & hiển thị sản phẩm
│   └── transactions.html       # Giỏ hàng, thanh toán & lịch sử đơn hàng
├── bao_cao_ktpm.md             # Báo cáo tổng quan bài tập lớn môn Kiểm thử phần mềm
├── dac_ta_kiem_thu.md          # Tài liệu đặc tả 19 ca kiểm thử chi tiết
├── dac_ta_kiem_thu_toan_dien.md# Đặc tả kiểm thử toàn diện
└── testing_report.md           # Báo cáo kết quả thực thi kiểm thử
```

---

## ⚙️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

Bạn có thể chạy ứng dụng theo 2 cách: Chạy trực tiếp trên máy local hoặc sử dụng Docker Compose.

### Cách 1: Chạy trực tiếp trên máy (Chế độ In-Memory Mock Database)
*Chế độ này không yêu cầu cài đặt MySQL. Dữ liệu sẽ được lưu trong RAM.*

1. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Khởi chạy ứng dụng**:
   ```bash
   python app.py
   ```
   Ứng dụng sẽ chạy tại địa chỉ: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Cách 2: Chạy với Docker Compose (Có kết nối CSDL MySQL thực tế)
*Yêu cầu đã cài đặt Docker và Docker Desktop trên máy.*

1. **Khởi động các dịch vụ (Web + MySQL)**:
   ```bash
   docker-compose up --build -d
   ```
2. **Thông tin kết nối cơ sở dữ liệu mặc định**:
   - **Host CSDL**: `localhost` (Port: `3306`)
   - **Tài khoản**: Root (Password: `rootpassword`) hoặc App User (`appuser` / `apppassword`)
   - **Tên CSDL**: `pytestdemodb`
   - *Hệ thống sẽ tự động khởi tạo các bảng `users`, `products`, `orders`, `order_items` và thêm dữ liệu mẫu (Seeding) khi khởi động thành công.*

3. **Dừng hệ thống**:
   ```bash
   docker-compose down -v
   ```

---

## 🧪 Hướng Dẫn Thực Thi Kiểm Thử (Pytest)

Dự án tích hợp bộ kiểm thử tự động sử dụng **pytest 8.2.0**. Môi trường kiểm thử được cô lập hoàn toàn nhờ cơ chế Fixture của pytest và Flask `test_request_context`.

### 1. Lệnh thực thi kiểm thử:

* Chạy toàn bộ bộ kiểm thử với thông báo chi tiết:
  ```bash
  pytest -v test_app.py
  ```
* Chạy riêng các ca kiểm thử theo từ khóa (ví dụ: chỉ chạy các ca liên quan đến `login`):
  ```bash
  pytest -k "login" -v test_app.py
  ```

### 2. Thống kê bộ kiểm thử (19/19 ca Test PASSED):

| Module | Chức năng kiểm thử | Số ca kiểm thử | ✅ Passed | ❌ Failed | ⚠️ Error |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **M1** | Xác thực người dùng (`/register`, `/login`, `/logout`) | 5 | 5 | 0 | 0 |
| **M2** | Quản lý sản phẩm (`/add`, `/edit`, `/delete`) | 4 | 4 | 0 | 0 |
| **M3** | Giỏ hàng & Thanh toán (`/add_to_cart`, `/checkout`) | 3 | 3 | 0 | 0 |
| **M4** | Quản lý đơn hàng (`/orders`, `/update_order`) | 3 | 3 | 0 | 0 |
| **M5** | Tìm kiếm & Lọc nâng cao (`/search`) | 4 | 4 | 0 | 0 |
| **Tổng** | **Hệ thống Quản lý Bán hàng** | **19** | **19** | **0** | **0** |

---
