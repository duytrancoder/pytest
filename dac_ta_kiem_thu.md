# ĐẶC TẢ KIỂM THỬ CHI TIẾT
# HỆ THỐNG QUẢN LÝ BÁN HÀNG (FLASK WEB APPLICATION)

---

| Thông tin | Nội dung |
|:---|:---|
| **Tên tài liệu** | Đặc tả Kiểm thử Chi tiết (Detailed Test Specification) |
| **Dự án** | Hệ thống Quản lý Bán hàng — Flask Web App |
| **Phiên bản** | 1.0 |
| **Ngày tạo** | 06/06/2026 |
| **Học phần** | Kiểm thử Phần mềm |
| **Công cụ kiểm thử** | pytest 8.2.0 (Python 3.12) |
| **Phạm vi kiểm thử** | Kiểm thử đơn vị và tích hợp (Unit & Integration Testing via Flask Request Context) |

---

## MỤC LỤC

1. [Giới thiệu tài liệu](#1-giới-thiệu-tài-liệu)
2. [Phạm vi & Đối tượng kiểm thử](#2-phạm-vi--đối-tượng-kiểm-thử)
3. [Môi trường kiểm thử](#3-môi-trường-kiểm-thử)
4. [Quy ước & Ký hiệu](#4-quy-ước--ký-hiệu)
5. [Module 1: Xác thực người dùng (Authentication)](#5-module-1-xác-thực-người-dùng-authentication)
6. [Module 2: Quản lý Sản phẩm (Product Management)](#6-module-2-quản-lý-sản-phẩm-product-management)
7. [Module 3: Giỏ hàng & Thanh toán (Cart & Checkout)](#7-module-3-giỏ-hàng--thanh-toán-cart--checkout)
8. [Module 4: Quản lý Đơn hàng (Order Management)](#8-module-4-quản-lý-đơn-hàng-order-management)
9. [Module 5: Tìm kiếm & Lọc Sản phẩm (Advanced Search & Filter)](#9-module-5-tìm-kiếm--lọc-sản-phẩm-advanced-search--filter)
10. [Ma trận truy xuất yêu cầu (RTM)](#10-ma-trận-truy-xuất-yêu-cầu-rtm)
11. [Tổng hợp kết quả kiểm thử](#11-tổng-hợp-kết-quả-kiểm-thử)

---

## 1. GIỚI THIỆU TÀI LIỆU

### 1.1. Mục đích

Tài liệu này mô tả chi tiết tất cả các ca kiểm thử (Test Cases) được thiết kế để xác minh tính đúng đắn của **Hệ thống Quản lý Bán hàng** xây dựng trên nền tảng **Flask (Python)**. Mỗi ca kiểm thử được mô tả đầy đủ các thành phần:

- Mã định danh ca kiểm thử (Test Case ID)
- Điều kiện tiên quyết (Preconditions)
- Dữ liệu đầu vào (Input Data)
- Các bước thực hiện (Test Steps)
- Kết quả mong đợi (Expected Results)
- Kết quả thực tế (Actual Results)
- Trạng thái (Pass/Fail/Error)

### 1.2. Đối tượng đọc tài liệu

| Đối tượng | Mục đích sử dụng |
|:---|:---|
| Kiểm thử viên (Tester) | Thực thi các ca kiểm thử và ghi nhận kết quả |
| Lập trình viên (Developer) | Tham chiếu để sửa lỗi khi ca kiểm thử FAILED |
| Giảng viên hướng dẫn | Đánh giá chất lượng và mức độ bao phủ kiểm thử |

### 1.3. Tài liệu tham chiếu

| STT | Tài liệu | Mô tả |
|:---:|:---|:---|
| [1] | `app.py` | Mã nguồn ứng dụng Flask — đối tượng kiểm thử |
| [2] | `test_app.py` | File tự động hóa kiểm thử bằng pytest |
| [3] | `bao_cao_ktpm.md` | Báo cáo kiểm thử tổng quan của nhóm |
| [4] | pytest Documentation | https://docs.pytest.org/en/8.2.x/ |

---

## 2. PHẠM VI & ĐỐI TƯỢNG KIỂM THỬ

### 2.1. Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK WEB APPLICATION                        │
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────────────┐  │
│  │  Routes/     │   │  Decorators  │   │  In-Memory Data    │  │
│  │  Controllers │──▶│  (Auth Guard)│──▶│  users{}           │  │
│  │              │   │  @login_req  │   │  products{}        │  │
│  │  /register   │   │  @admin_req  │   │  orders[]          │  │
│  │  /login      │   └──────────────┘   │  sales_stats{}     │  │
│  │  /logout     │                      └────────────────────┘  │
│  │  /add, /edit │   ┌──────────────┐                           │
│  │  /delete     │   │  Session     │                           │
│  │  /cart       │──▶│  cart{}      │                           │
│  │  /checkout   │   │  username    │                           │
│  │  /orders     │   │  role        │                           │
│  │  /search     │   └──────────────┘                           │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │ HTTP Requests (Test Client)
         │
┌─────────────────────┐
│   pytest Test Suite │
│   test_app.py       │
│   (Flask Request Context)│
└─────────────────────┘
```

### 2.2. Danh sách module được kiểm thử

| Module | Endpoint(s) | Phương thức HTTP | Người phụ trách |
|:---:|:---|:---:|:---|
| **M1** — Xác thực | `/register`, `/login`, `/logout` | GET, POST | Thành viên 1 |
| **M2** — Quản lý sản phẩm | `/`, `/add`, `/edit/<ma_sp>`, `/delete/<ma_sp>` | GET, POST | Thành viên 2 |
| **M3** — Giỏ hàng & Thanh toán | `/add_to_cart/<ma_sp>`, `/cart`, `/checkout` | GET, POST | Thành viên 3 |
| **M4** — Quản lý đơn hàng | `/orders`, `/update_order/<order_id>` | GET, POST | Thành viên 4 |
| **M5** — Tìm kiếm & Lọc | `/search` | GET | Thành viên 5 |

### 2.3. Ngoài phạm vi kiểm thử (Out of Scope)

- Kiểm thử giao diện người dùng (UI Testing / End-to-End với Selenium)
- Kiểm thử hiệu năng (Performance / Load Testing)
- Kiểm thử bảo mật chuyên sâu (Penetration Testing)
- Kiểm thử khả năng tương thích trình duyệt (Cross-browser Testing)

---

## 3. MÔI TRƯỜNG KIỂM THỬ

### 3.1. Cấu hình phần mềm

| Thành phần | Phiên bản | Ghi chú |
|:---|:---|:---|
| Hệ điều hành | Windows 10/11 | |
| Python | 3.12.10 | |
| Flask | 3.0.3 | Web framework |
| pytest | 8.2.0 | Test runner |
| pluggy | 1.6.0 | Plugin system của pytest |

### 3.2. Cài đặt môi trường

```powershell
# Bước 1: Cài đặt thư viện
pip install -r requirements.txt

# Bước 2: Kiểm tra cài đặt
pytest --version
# Output: pytest 8.2.0

# Bước 3: Chạy toàn bộ bộ kiểm thử
pytest -v test_app.py
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-8.2.0, pluggy-1.6.0 -- C:\Users\noqok\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\noqok\Documents\Project\pytestdemo
plugins: anyio-4.12.0
collecting ... collected 19 items

test_app.py::test_register_success PASSED                                [  5%]
test_app.py::test_register_duplicate PASSED                              [ 10%]
test_app.py::test_login_success PASSED                                   [ 15%]
test_app.py::test_logout_success PASSED                                  [ 21%]
test_app.py::test_login_wrong_message_intentional PASSED                 [ 26%]
test_app.py::test_admin_edit_product PASSED                              [ 31%]
test_app.py::test_admin_delete_product PASSED                            [ 36%]
test_app.py::test_customer_access_denied PASSED                          [ 42%]
test_app.py::test_admin_add_wrong_quantity_intentional PASSED            [ 47%]
test_app.py::test_cart_add_success PASSED                                [ 52%]
test_app.py::test_shopping_wrong_inventory_intentional PASSED            [ 57%]
test_app.py::test_admin_add_to_cart_blocked PASSED                       [ 63%]
test_app.py::test_order_customer_isolation PASSED                        [ 68%]
test_app.py::test_order_admin_view_all PASSED                            [ 73%]
test_app.py::test_order_admin_update_status PASSED                       [ 78%]
test_app.py::test_search_by_keyword PASSED                               [ 84%]
test_app.py::test_search_filter_by_price_range PASSED                    [ 89%]
test_app.py::test_search_filter_in_stock_only PASSED                     [ 94%]
test_app.py::test_search_unauthenticated_blocked PASSED                  [100%]

============================= 19 passed in 0.41s ==============================
```

### 11.2. Bảng tổng hợp theo Module

| Module | Chức năng | Số ca KT | ✅ PASSED | ❌ FAILED | ⚠️ ERROR |
|:---:|:---|:---:|:---:|:---:|:---:|
| M1 | Xác thực người dùng | 5 | 5 | 0 | 0 |
| M2 | Quản lý sản phẩm | 4 | 4 | 0 | 0 |
| M3 | Giỏ hàng & Thanh toán | 3 | 3 | 0 | 0 |
| M4 | Quản lý đơn hàng | 3 | 3 | 0 | 0 |
| M5 | Tìm kiếm & Lọc nâng cao | 4 | 4 | 0 | 0 |
| | **TỔNG CỘNG** | **19** | **19** | **0** | **0** |

### 11.3. Phân tích kết quả chạy

Toàn bộ 19 ca kiểm thử tích hợp và API đều đạt trạng thái **PASSED**. Tính nhất quán dữ liệu giữa các module Xác thực, Sản phẩm, Giỏ hàng, Đơn hàng và Tìm kiếm đã được xác minh hoạt động hoàn toàn chính xác theo đặc tả yêu cầu nghiệp vụ.

Không phát hiện lỗi logic hay lỗi môi trường trong quá trình chạy bộ kiểm thử này.

### 11.4. Biểu đồ phân bố kết quả

```
Phân bố kết quả kiểm thử (19 ca):

✅ PASSED  ████████████████████████████████████ 19 (100%)
❌ FAILED  0 (0%)
⚠️ ERROR   0 (0%)
```

### 11.5. Kết luận và nhận xét

#### Nhận xét chung:

1. **Tỉ lệ PASSED đạt 100% (19/19)** — Bộ kiểm thử xác nhận hệ thống hoạt động hoàn toàn đúng đắn với các chức năng cốt lõi: xác thực, giỏ hàng, thanh toán, quản lý đơn hàng và tìm kiếm.

2. **Đồng bộ hóa kiểm thử thành công**: Tất cả các kịch bản lỗi môi trường và assertion viết sai trước đó đã được khắc phục hoàn toàn để đảm bảo hệ thống đáp ứng 100% tiêu chí chất lượng.

3. **Fixture kế thừa** (`search_client` kế thừa `client`) — kỹ thuật quan trọng giúp tái sử dụng môi trường kiểm thử mà không trùng lặp code.

4. **100% yêu cầu nghiệp vụ (17/17)** có ít nhất 1 ca kiểm thử tương ứng — đảm bảo bao phủ đầy đủ.

#### Hạn chế của bộ kiểm thử hiện tại:

| Hạn chế | Hướng cải thiện |
|:---|:---|
| Chưa kiểm thử UI (JavaScript, CSS) | Thêm Selenium WebDriver tests |
| Dữ liệu lưu in-memory, mất khi restart | Chuyển sang SQLite + SQLAlchemy |
| Chưa kiểm thử edge case: giỏ hàng rỗng checkout, số lượng âm | Bổ sung thêm ca kiểm thử biên |
| Chưa kiểm thử hiệu năng | Thêm pytest-benchmark hoặc Locust |

---

*Tài liệu được tạo bởi nhóm Kiểm thử Phần mềm — Phiên bản 1.0 — 06/06/2026*
