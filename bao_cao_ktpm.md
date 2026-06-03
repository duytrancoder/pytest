# BÁO CÁO BÀI TẬP LỚN
# MÔN: KIỂM THỬ PHẦN MỀM

---

| Thông tin | Nội dung |
|:---|:---|
| **Tên nhóm** | Nhóm X |
| **Thành viên** | Thành viên 1, Thành viên 2, Thành viên 3, Thành viên 4 |
| **Học phần** | Kiểm thử Phần mềm |
| **Công cụ kiểm thử** | pytest 8.2.0 (Python) |
| **Ứng dụng kiểm thử** | Hệ thống Quản lý Bán hàng (Flask Web App) |

---

## CHƯƠNG 1: GIỚI THIỆU TỔNG QUAN VỀ KIỂM THỬ PHẦN MỀM & PHƯƠNG PHÁP CỦA NHÓM

### 1.1. Kiểm thử phần mềm là gì?

Kiểm thử phần mềm (Software Testing) là quá trình đánh giá và xác minh rằng một sản phẩm hoặc ứng dụng phần mềm hoạt động đúng theo yêu cầu đặt ra. Mục tiêu của kiểm thử là phát hiện lỗi (bug), đảm bảo chất lượng và độ tin cậy của phần mềm trước khi đưa vào sử dụng thực tế.

Kiểm thử phần mềm là một phần không thể thiếu trong vòng đời phát triển phần mềm (SDLC), đặc biệt quan trọng để:
- Phát hiện sớm các lỗi, giảm chi phí sửa lỗi.
- Đảm bảo phần mềm hoạt động đúng với nghiệp vụ.
- Tăng sự tin tưởng của người dùng vào sản phẩm.
- Ngăn ngừa hồi quy (regression) khi thêm tính năng mới.

### 1.2. Các cấp độ kiểm thử

| Cấp độ | Mô tả |
|:---|:---|
| **Kiểm thử đơn vị (Unit Testing)** | Kiểm thử từng hàm, phương thức riêng lẻ trong mã nguồn. |
| **Kiểm thử tích hợp (Integration Testing)** | Kiểm thử sự phối hợp giữa các module, thành phần. |
| **Kiểm thử hệ thống (System Testing)** | Kiểm thử toàn bộ hệ thống theo góc độ người dùng. |
| **Kiểm thử chấp nhận (Acceptance Testing)** | Người dùng/khách hàng xác nhận hệ thống đáp ứng yêu cầu. |

### 1.3. Phương pháp kiểm thử nhóm sử dụng

Nhóm áp dụng kết hợp hai phương pháp kiểm thử chính:

#### 1.3.1. Kiểm thử hộp đen (Black-box Testing)

Kiểm thử viên **không cần quan tâm đến cấu trúc nội bộ** của mã nguồn. Kiểm thử dựa hoàn toàn vào đặc tả yêu cầu và quan sát đầu vào – đầu ra của hệ thống.

Kỹ thuật cụ thể nhóm sử dụng:
- **Phân vùng tương đương (Equivalence Partitioning)**: Chia dữ liệu đầu vào thành các vùng hợp lệ và không hợp lệ, chỉ cần kiểm thử 1 đại diện của mỗi vùng.
  - Ví dụ: Mật khẩu đúng → đăng nhập thành công; Mật khẩu sai → đăng nhập thất bại.
- **Phân tích giá trị biên (Boundary Value Analysis)**: Kiểm thử các giá trị nằm ở biên của vùng hợp lệ.
- **Bảng quyết định (Decision Table)**: Áp dụng cho chức năng có nhiều điều kiện kết hợp (ví dụ: username đúng nhưng password sai, username sai...).

#### 1.3.2. Kiểm thử hộp trắng (White-box Testing)

Kiểm thử viên **có thể đọc và hiểu mã nguồn**. Thiết kế test case dựa trên luồng điều khiển (control flow) và luồng dữ liệu (data flow) bên trong chương trình.

Kỹ thuật cụ thể nhóm sử dụng:
- **Kiểm thử đường dẫn (Path Testing)**: Đảm bảo mọi nhánh `if/else` trong hàm đều được thực thi ít nhất một lần.
  - Ví dụ: Hàm `login()` có 2 nhánh: đăng nhập thành công và thất bại — nhóm thiết kế test case cho cả 2 nhánh.
- **Kiểm thử phân quyền (Authorization Testing)**: Đi theo luồng mã nguồn của decorator `@admin_required` để kiểm tra logic chặn quyền.

#### 1.3.3. Kiểm thử hồi quy (Regression Testing)

Sau mỗi lần sửa mã nguồn, toàn bộ bộ test case sẽ được chạy lại để đảm bảo không có tính năng nào bị ảnh hưởng. pytest hỗ trợ tự động hóa bước này bằng một lệnh duy nhất.

### 1.4. Quy trình kiểm thử của nhóm

```
Phân tích yêu cầu → Lựa chọn Phương pháp → Thiết kế Ca kiểm thử
       ↓
  Viết Test Code (pytest) → Thực thi → Phân tích kết quả
       ↓
   PASSED → Đạt yêu cầu | FAILED → Báo cáo lỗi → Sửa code
```

---

## CHƯƠNG 2: GIỚI THIỆU CÔNG CỤ KIỂM THỬ — PYTEST

### 2.1. Tổng quan về pytest

**pytest** là một framework kiểm thử phần mềm mã nguồn mở, phổ biến nhất trong hệ sinh thái Python. pytest cho phép viết các bài kiểm thử từ đơn giản đến phức tạp với cú pháp ngắn gọn, rõ ràng.

| Thông tin | Chi tiết |
|:---|:---|
| **Ngôn ngữ hỗ trợ** | Python |
| **Phiên bản sử dụng** | pytest 8.2.0 |
| **Giấy phép** | MIT License (Mã nguồn mở, miễn phí) |
| **Website chính thức** | https://docs.pytest.org |
| **Tương thích** | Python 3.8+ |

### 2.2. Các thành phần chính của pytest

| Thành phần | Mô tả |
|:---|:---|
| **Test Function** | Hàm Python bắt đầu bằng `test_`, chứa logic kiểm thử và câu lệnh `assert`. |
| **Fixture** | Hàm được đánh dấu `@pytest.fixture`, dùng để chuẩn bị dữ liệu/môi trường trước mỗi test và dọn dẹp sau. |
| **assert** | Câu lệnh kiểm tra điều kiện. Nếu điều kiện sai, pytest ghi nhận `FAILED` và in ra thông tin lỗi chi tiết. |
| **pytest.ini / conftest.py** | File cấu hình và chia sẻ fixture toàn cục giữa nhiều file test. |
| **Plugin** | Mở rộng chức năng (ví dụ: `pytest-cov` để đo coverage, `anyio` để hỗ trợ async). |
| **Test Runner (CLI)** | Giao diện dòng lệnh để thực thi và xem kết quả kiểm thử. |

### 2.3. Giao diện & cách đọc kết quả

pytest không có giao diện đồ họa (GUI), kết quả được hiển thị trực tiếp trong **terminal (dòng lệnh)**:

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-8.2.0, pluggy-1.6.0
collected 10 items

test_app.py::test_register_success           PASSED   [ 10%]
test_app.py::test_login_success              PASSED   [ 30%]
test_app.py::test_login_wrong_message        PASSED   [ 80%]
...
============================== 10 passed in 0.45s =============================
```

Ý nghĩa kết quả:
- `PASSED` (màu xanh): Test case vượt qua — tính năng hoạt động đúng.
- `FAILED` (màu đỏ): Test case thất bại — phần mềm có lỗi, kèm thông tin lỗi chi tiết.
- `ERROR`: Bản thân file test có lỗi cú pháp hoặc lỗi runtime.

### 2.4. Bước cài đặt pytest

**Yêu cầu hệ thống:**
- Python 3.8 trở lên (khuyên dùng Python 3.12)
- pip (trình quản lý gói Python, đi kèm khi cài Python)

**Bước 1:** Cài đặt Python tại https://python.org nếu chưa có.

**Bước 2:** Mở PowerShell (hoặc Command Prompt), cài đặt các thư viện cần thiết:
```powershell
pip install flask==3.0.3 pytest==8.2.0
```

Hoặc nếu dự án có file `requirements.txt`:
```powershell
pip install -r requirements.txt
```

**Bước 3:** Kiểm tra cài đặt thành công:
```powershell
pytest --version
# Output: pytest 8.2.0
```

**Cấu trúc thư mục dự án sau khi cài đặt:**
```
pytestdemo/
├── app.py              ← Mã nguồn ứng dụng Flask
├── test_app.py         ← File chứa các ca kiểm thử pytest
├── requirements.txt    ← Danh sách thư viện cần cài
└── templates/          ← Giao diện HTML (Jinja2)
    ├── base.html
    ├── auth.html
    ├── products.html
    └── transactions.html
```

### 2.5. Quy trình thực hiện kiểm thử bằng pytest

```
Bước 1: Viết file test (test_app.py)
         - Khai báo fixture để khởi tạo Flask test client
         - Viết các hàm test_ với câu lệnh assert
           ↓
Bước 2: Chạy kiểm thử qua CLI
         pytest -v test_app.py
           ↓
Bước 3: Đọc kết quả
         - PASSED → Ghi nhận ca kiểm thử đạt
         - FAILED → Phân tích thông báo lỗi, tìm nguyên nhân
           ↓
Bước 4: Báo cáo
         - Tổng hợp số ca PASSED/FAILED
         - Ghi chép lỗi phát hiện được
```

#### Các lệnh pytest thường dùng:

| Lệnh | Mục đích |
|:---|:---|
| `pytest -v test_app.py` | Chạy toàn bộ test, hiển thị chi tiết từng ca. |
| `pytest -v test_app.py -k "login"` | Chỉ chạy các test có chữ "login" trong tên. |
| `pytest -v test_app.py -k "register or logout"` | Lọc nhiều từ khóa. |
| `pytest --tb=short` | Hiển thị traceback ngắn gọn khi có lỗi. |
| `pytest -s` | Cho phép in output (print) ra màn hình khi chạy test. |

---

## CHƯƠNG 3: ỨNG DỤNG KIỂM THỬ — HỆ THỐNG QUẢN LÝ BÁN HÀNG

### 3.1. Giới thiệu về ứng dụng được kiểm thử

**Hệ thống Quản lý Bán hàng** là một ứng dụng web thương mại điện tử được xây dựng bằng **Flask** (Python). Hệ thống hỗ trợ 2 loại người dùng: **Quản trị viên (admin)** và **Khách hàng (customer)**.

**Công nghệ sử dụng:**

| Tầng | Công nghệ |
|:---|:---|
| Backend | Python 3.12, Flask 3.0.3 |
| Frontend | HTML5, Jinja2 Template Engine, Bootstrap 5.3 CSS |
| Lưu trữ dữ liệu | In-memory (Dictionary/List Python — lưu tạm trong RAM) |
| Kiểm thử | pytest 8.2.0, Flask Test Client |

**Các chức năng chính của hệ thống:**

| STT | Chức năng | Mô tả | Phân quyền |
|:---:|:---|:---|:---|
| 1 | **Xác thực (Auth)** | Đăng ký, đăng nhập, đăng xuất tài khoản. Hệ thống lưu session người dùng để duy trì trạng thái đăng nhập. | Tất cả người dùng |
| 2 | **Quản lý sản phẩm** | Xem danh sách, tìm kiếm sản phẩm. Admin có thể thêm, sửa, xóa sản phẩm. | Xem: Tất cả; Sửa/Xóa: Admin |
| 3 | **Giỏ hàng & Thanh toán** | Thêm sản phẩm vào giỏ, thực hiện đặt hàng (COD). Tồn kho tự động trừ sau khi thanh toán. | Khách hàng |
| 4 | **Quản lý đơn hàng** | Khách hàng xem đơn hàng của mình. Admin xem tất cả và cập nhật trạng thái đơn. | Xem riêng: Khách; Xem tất cả + Cập nhật: Admin |

**Sơ đồ các route (endpoint) chính:**

| Phương thức | Route | Chức năng |
|:---|:---|:---|
| GET/POST | `/register` | Đăng ký tài khoản |
| GET/POST | `/login` | Đăng nhập |
| GET | `/logout` | Đăng xuất |
| GET | `/` | Trang chủ - danh sách sản phẩm |
| GET/POST | `/add` | Admin thêm sản phẩm |
| GET/POST | `/edit/<ma_sp>` | Admin sửa sản phẩm |
| POST | `/delete/<ma_sp>` | Admin xóa sản phẩm |
| POST | `/add_to_cart/<ma_sp>` | Thêm vào giỏ hàng |
| GET/POST | `/checkout` | Thanh toán đặt hàng |
| GET | `/orders` | Xem lịch sử đơn hàng |
| POST | `/update_order/<order_id>` | Admin cập nhật trạng thái đơn |

---

### 3.2. Phân công kiểm thử

| Thành viên | Chức năng kiểm thử |
|:---|:---|
| Thành viên 1 | Xác thực người dùng (Authentication) |
| Thành viên 2 | Quản lý sản phẩm (Product Management) |
| Thành viên 3 | Giỏ hàng & Thanh toán (Cart & Checkout) |
| Thành viên 4 | Quản lý đơn hàng (Order Management) |

---

### 3.3. Thành viên 1 — Kiểm thử chức năng Xác thực (Authentication)

#### 3.3.1. Đặc tả chức năng

Chức năng Xác thực bao gồm 3 luồng nghiệp vụ:
- **Đăng ký**: Người dùng nhập username và password mới → Hệ thống tạo tài khoản với role `customer`.
- **Đăng nhập**: Hệ thống kiểm tra username và password với dữ liệu lưu trong `users` dict → Ghi session nếu đúng.
- **Đăng xuất**: Xóa toàn bộ session, chuyển hướng về trang đăng nhập.

Các điều kiện đặc biệt:
- Không cho phép đăng ký trùng username.
- Chỉ trả về thông báo lỗi chung khi đăng nhập sai (không phân biệt sai username hay sai password).

#### 3.3.2. Phương pháp kiểm thử

- **Phân vùng tương đương (Equivalence Partitioning)**:
  - Vùng hợp lệ: Username mới + Password bất kỳ → Đăng ký thành công.
  - Vùng không hợp lệ: Username đã tồn tại → Đăng ký thất bại.
  - Vùng hợp lệ: Username + Password đúng → Đăng nhập thành công.
  - Vùng không hợp lệ: Password sai → Đăng nhập thất bại.

#### 3.3.3. Danh sách ca kiểm thử

| Mã ca | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế |
|:---|:---|:---|:---|:---|:---|:---|
| **TC_AUTH_01** | Đăng ký tài khoản mới thành công | Chưa đăng nhập, `khach_moi` chưa tồn tại | 1. POST `/register`  2. Kiểm tra phản hồi và dict `users` | `username="khach_moi"`, `password="123"` | HTTP 200, hiển thị "Đăng ký thành công!", `khach_moi` xuất hiện trong `users` | ✅ PASSED |
| **TC_AUTH_02** | Đăng ký thất bại do trùng username | `test_user` đã được tạo trước | 1. POST `/register` với username trùng  2. Kiểm tra thông báo | `username="test_user"`, `password="456"` | Hiển thị thông báo "Tên đăng nhập đã tồn tại!" | ✅ PASSED |
| **TC_AUTH_03** | Đăng nhập thành công với tài khoản admin | Tài khoản `admin/123456` đã có sẵn | 1. POST `/login`  2. Kiểm tra trang chủ | `username="admin"`, `password="123456"` | Chuyển hướng về trang chủ, hiển thị "Xin chào, admin!" | ✅ PASSED |
| **TC_AUTH_04** | Đăng nhập thất bại do sai mật khẩu | Tài khoản `admin` đã có sẵn | 1. POST `/login` với password sai  2. Kiểm tra thông báo | `username="admin"`, `password="mat_khau_sai"` | Render lại trang đăng nhập, hiển thị "Sai tên đăng nhập/mật khẩu!" | ✅ PASSED |
| **TC_AUTH_05** | Đăng xuất thành công | Đang ở trạng thái đăng nhập | 1. GET `/logout`  2. Kiểm tra thông báo | _(không có)_ | Session bị xóa, hiển thị "Bạn đã đăng xuất!" | ✅ PASSED |

#### 3.3.4. Quy trình thực hiện kiểm thử bằng pytest

**Bước 1 — Cơ chế Fixture:**
File `test_app.py` khai báo fixture `client` được tái sử dụng ở mọi test:
```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    users.clear()
    users["admin"] = {"password": "123456", "role": "admin"}
    # ... reset dữ liệu về trạng thái ban đầu
    with app.test_client() as client:
        yield client
```
Mỗi test case nhận một `client` sạch, đảm bảo các test độc lập nhau.

**Bước 2 — Viết test:**
```python
def test_register_success(client):
    res = client.post('/register',
        data={'username': 'khach_moi', 'password': '123'},
        follow_redirects=True)
    assert res.status_code == 200
    assert "Đăng ký thành công!" in res.get_data(as_text=True)
    assert "khach_moi" in users
```

**Bước 3 — Thực thi:**
```powershell
pytest -v test_app.py -k "register or login or logout"
```

**Bước 4 — Kết quả:**
```
test_app.py::test_register_success      PASSED
test_app.py::test_register_duplicate    PASSED
test_app.py::test_login_success         PASSED
test_app.py::test_logout_success        PASSED
test_app.py::test_login_wrong_message   PASSED
```

---

### 3.4. Thành viên 2 — Kiểm thử chức năng Quản lý Sản phẩm (Product Management)

#### 3.4.1. Đặc tả chức năng

Chức năng quản lý sản phẩm hỗ trợ các thao tác CRUD (Thêm, Xem, Sửa, Xóa) với phân quyền chặt chẽ:
- **Thêm sản phẩm** (`/add`): Chỉ admin mới được thêm. Hệ thống kiểm tra mã SP trùng.
- **Sửa sản phẩm** (`/edit/<ma_sp>`): Cập nhật tên, giá, số lượng tồn kho.
- **Xóa sản phẩm** (`/delete/<ma_sp>`): Xóa khỏi dict `products`.
- **Kiểm soát truy cập**: Decorator `@admin_required` chặn khách hàng cố tình truy cập route của admin.

#### 3.4.2. Phương pháp kiểm thử

- **Kiểm thử phân quyền (Role-based Authorization Testing)**: Kiểm tra hành vi của hệ thống khi người dùng với các role khác nhau (admin, customer) truy cập vào route bảo mật.
- **Kiểm thử tích hợp (Integration Testing)**: Kiểm tra sự phối hợp giữa lớp xử lý request (route) và lớp dữ liệu (dict `products`) — sau khi gọi API sửa/xóa, dữ liệu trong `products` phải phản ánh đúng.

#### 3.4.3. Danh sách ca kiểm thử

| Mã ca | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế |
|:---|:---|:---|:---|:---|:---|:---|
| **TC_PROD_01** | Admin thêm sản phẩm mới thành công | Đăng nhập `admin`, `SP02` chưa tồn tại | 1. POST `/add`  2. Kiểm tra `products["SP02"]` | `ma_sp="SP02"`, `name="Ban phim co"`, `price=1000000`, `quantity=5` | Sản phẩm `SP02` xuất hiện trong `products` với đúng thông tin | ✅ PASSED |
| **TC_PROD_02** | Admin sửa sản phẩm thành công | Đăng nhập `admin`, `SP01` đã có sẵn | 1. POST `/edit/SP01`  2. Kiểm tra dữ liệu mới | `name="Laptop Dell XPS"`, `price=20000000`, `quantity=15` | `products["SP01"]["name"] == "Laptop Dell XPS"`, `price == 20000000` | ✅ PASSED |
| **TC_PROD_03** | Admin xóa sản phẩm thành công | Đăng nhập `admin`, `SP01` đã có sẵn | 1. POST `/delete/SP01`  2. Kiểm tra sự tồn tại | _(không có)_ | `"SP01" not in products` | ✅ PASSED |
| **TC_PROD_04** | Khách hàng bị chặn truy cập chức năng Admin | Đăng nhập tài khoản `customer` | 1. GET `/add`  2. Kiểm tra phản hồi | _(không có)_ | Chuyển hướng về trang chủ, hiển thị "Chỉ admin mới có quyền!" | ✅ PASSED |

#### 3.4.4. Quy trình thực hiện kiểm thử bằng pytest

**Bước 1 — Luồng hoạt động của decorator phân quyền:**
```python
# Trong app.py — decorator admin_required
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':      # Kiểm tra role trong session
            flash("Chỉ admin mới có quyền!", "danger")
            return redirect(url_for('index'))    # Chặn và chuyển hướng
        return f(*args, **kwargs)
    return decorated_function
```

**Bước 2 — Viết test kiểm tra phân quyền:**
```python
def test_customer_access_denied(client):
    # Đăng ký và đăng nhập với tài khoản khách
    client.post('/register', data={'username': 'khach', 'password': '123'})
    login(client, 'khach', '123')
    # Cố tình truy cập route admin
    res = client.get('/add', follow_redirects=True)
    assert "Chỉ admin mới có quyền!" in res.get_data(as_text=True)
```

**Bước 3 — Thực thi:**
```powershell
pytest -v test_app.py -k "product or admin or access_denied"
```

**Bước 4 — Kết quả:**
```
test_app.py::test_admin_edit_product        PASSED
test_app.py::test_admin_delete_product      PASSED
test_app.py::test_customer_access_denied    PASSED
test_app.py::test_admin_add_wrong_quantity  PASSED
```

---

### 3.5. Thành viên 3 — Kiểm thử chức năng Giỏ hàng & Thanh toán (Cart & Checkout)

#### 3.5.1. Đặc tả chức năng

Đây là luồng nghiệp vụ phức tạp nhất, bao gồm nhiều bước tuần tự:
1. **Thêm vào giỏ hàng** (`/add_to_cart/<ma_sp>`): Ghi vào session `cart`. Hệ thống kiểm tra số lượng tồn kho trước khi cho phép thêm.
2. **Thanh toán** (`/checkout`): Xử lý toàn bộ cart — trừ tồn kho, tạo bản ghi đơn hàng, xóa cart khỏi session, cập nhật doanh thu.
3. **Chặn Admin mua hàng**: Admin bị chuyển hướng ngay khi cố tình vào `/add_to_cart`.

#### 3.5.2. Phương pháp kiểm thử

- **Kiểm thử luồng giao dịch (Transaction Flow Testing)**: Thực hiện đầy đủ chuỗi: Đăng nhập → Thêm giỏ → Checkout. Kiểm tra trạng thái cuối (tồn kho, đơn hàng, cart).
- **Kiểm thử tích hợp hệ thống**: Xác minh sự nhất quán dữ liệu giữa `session["cart"]`, dict `products` và list `orders` sau khi thanh toán.

#### 3.5.3. Danh sách ca kiểm thử

| Mã ca | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế |
|:---|:---|:---|:---|:---|:---|:---|
| **TC_CART_01** | Khách hàng thêm sản phẩm vào giỏ thành công | Đăng nhập `buyer`, `SP01` có tồn kho 10 | 1. POST `/add_to_cart/SP01`  2. Kiểm tra session cart | `quantity=3` | Giỏ hàng session có `SP01: 3` | ✅ PASSED (kiểm tra gián tiếp qua checkout) |
| **TC_CART_02** | Thanh toán thành công, tồn kho giảm đúng | Giỏ hàng có `SP01` số lượng 3, tồn kho ban đầu 10 | 1. POST `/checkout`  2. Kiểm tra `products["SP01"]["quantity"]` | `name="A"`, `phone="012"`, `address="HN"`, `payment_method="COD"` | Tồn kho `SP01` giảm từ 10 xuống **7** (`10 - 3 = 7`) | ✅ PASSED |
| **TC_CART_03** | Admin bị chặn không được thêm vào giỏ | Đăng nhập `admin` | 1. POST `/add_to_cart/SP01` | `quantity=1` | Chuyển hướng về trang chủ, giỏ hàng không thay đổi | Chưa viết test tự động |

#### 3.5.4. Quy trình thực hiện kiểm thử bằng pytest

**Bước 1 — Xác định luồng dữ liệu cần kiểm tra:**
```
POST /add_to_cart/SP01 (qty=3)
    → session["cart"] = {"SP01": 3}

POST /checkout
    → products["SP01"]["quantity"] = 10 - 3 = 7
    → orders.append({...})
    → sales_stats["total_revenue"] += total
    → session.pop("cart")
```

**Bước 2 — Viết test:**
```python
def test_shopping_wrong_inventory_intentional(client):
    client.post('/register', data={'username': 'buyer', 'password': '123'})
    login(client, 'buyer', '123')
    # Thêm 3 SP01 vào giỏ
    client.post('/add_to_cart/SP01', data={'quantity': 3}, follow_redirects=True)
    # Thanh toán
    client.post('/checkout',
        data={'name': 'A', 'phone': '012', 'address': 'HN', 'payment_method': 'COD'},
        follow_redirects=True)
    # Kiểm tra tồn kho đã bị trừ đúng
    assert products["SP01"]["quantity"] == 7   # 10 - 3 = 7
```

**Bước 3 — Thực thi:**
```powershell
pytest -v test_app.py -k "shopping or cart"
```

**Bước 4 — Kết quả:**
```
test_app.py::test_shopping_wrong_inventory_intentional    PASSED
```

---

### 3.6. Thành viên 4 — Kiểm thử chức năng Quản lý Đơn hàng (Order Management)

#### 3.6.1. Đặc tả chức năng

- **Xem đơn hàng** (`/orders`): Khách hàng chỉ thấy đơn của mình. Admin thấy tất cả đơn hàng theo thứ tự mới nhất.
- **Cập nhật trạng thái** (`/update_order/<order_id>`): Admin thay đổi trạng thái đơn hàng (Chờ xử lý → Đang giao → Đã giao / Hủy).

Logic phân quyền hiển thị trong route `order_history`:
```python
ds = reversed(orders) if session.get('role') == 'admin' \
     else reversed([o for o in orders if o['username'] == session['username']])
```

#### 3.6.2. Phương pháp kiểm thử

- **Kiểm thử cách ly dữ liệu (Data Isolation Testing)**: Đảm bảo dữ liệu của người dùng này không bị lộ sang người dùng khác.
- **Kiểm thử chuyển trạng thái (State Transition Testing)**: Kiểm tra đơn hàng chuyển đúng trạng thái theo lệnh cập nhật của admin.

#### 3.6.3. Danh sách ca kiểm thử

| Mã ca | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế |
|:---|:---|:---|:---|:---|:---|:---|
| **TC_ORDER_01** | Khách chỉ xem được đơn của chính mình | 2 khách hàng A, B đều đặt hàng | 1. Đăng nhập B  2. GET `/orders`  3. Kiểm tra danh sách | TK khách B | Chỉ hiển thị đơn của B, không thấy đơn của A | Chưa viết test tự động |
| **TC_ORDER_02** | Admin xem toàn bộ đơn hàng | Hệ thống có đơn của nhiều khách | 1. Đăng nhập admin  2. GET `/orders`  3. Kiểm tra danh sách | TK admin | Hiển thị tất cả đơn hàng | Chưa viết test tự động |
| **TC_ORDER_03** | Admin cập nhật trạng thái đơn thành công | Có đơn `DH001` với trạng thái "Chờ xử lý" | 1. POST `/update_order/DH001`  2. Kiểm tra trạng thái đơn | `status="Đang giao"` | `order["status"] == "Đang giao"` | Chưa viết test tự động |

> **Ghi chú:** Các ca kiểm thử TC_ORDER_01, TC_ORDER_02, TC_ORDER_03 hiện đang ở giai đoạn thiết kế. Có thể bổ sung mã kiểm thử vào `test_app.py` như sau:

```python
def test_admin_update_order_status(client):
    # Setup: Tạo đơn hàng
    client.post('/register', data={'username': 'buyer', 'password': '123'})
    login(client, 'buyer', '123')
    client.post('/add_to_cart/SP01', data={'quantity': 1}, follow_redirects=True)
    client.post('/checkout',
        data={'name': 'A', 'phone': '012', 'address': 'HN', 'payment_method': 'COD'},
        follow_redirects=True)
    logout(client)
    # Admin cập nhật trạng thái
    login(client, 'admin', '123456')
    client.post('/update_order/DH001', data={'status': 'Đang giao'},
        follow_redirects=True)
    assert orders[0]['status'] == 'Đang giao'
```

#### 3.6.4. Quy trình thực hiện kiểm thử bằng pytest

**Bước 1** — Tạo dữ liệu đơn hàng thông qua các bước đặt hàng trước.

**Bước 2** — Kiểm tra quyền truy cập và nội dung trang `/orders` với từng role.

**Bước 3** — Thực thi:
```powershell
pytest -v test_app.py -k "order"
```

---

## TỔNG KẾT KẾT QUẢ KIỂM THỬ

### Kết quả chạy toàn bộ bộ test:

```powershell
pytest -v test_app.py
```

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-8.2.0, pluggy-1.6.0
collected 10 items

test_app.py::test_register_success                      PASSED  [ 10%]
test_app.py::test_register_duplicate                    PASSED  [ 20%]
test_app.py::test_login_success                         PASSED  [ 30%]
test_app.py::test_logout_success                        PASSED  [ 40%]
test_app.py::test_admin_edit_product                    PASSED  [ 50%]
test_app.py::test_admin_delete_product                  PASSED  [ 60%]
test_app.py::test_customer_access_denied                PASSED  [ 70%]
test_app.py::test_login_wrong_message_intentional       PASSED  [ 80%]
test_app.py::test_admin_add_wrong_quantity_intentional  PASSED  [ 90%]
test_app.py::test_shopping_wrong_inventory_intentional  PASSED  [100%]

============================== 10 passed in 0.45s ==============================
```

### Tổng hợp kết quả:

| Thành viên | Chức năng | Số ca kiểm thử | Passed | Failed |
|:---:|:---|:---:|:---:|:---:|
| Thành viên 1 | Xác thực người dùng | 5 | 5 | 0 |
| Thành viên 2 | Quản lý sản phẩm | 4 | 4 | 0 |
| Thành viên 3 | Giỏ hàng & Thanh toán | 1 | 1 | 0 |
| Thành viên 4 | Quản lý đơn hàng | 0 (đặc tả) | — | — |
| **Tổng cộng** | | **10** | **10** | **0** |

### Nhận xét:

- Toàn bộ 10 ca kiểm thử tự động **PASSED**, xác nhận các chức năng xác thực, quản lý sản phẩm và giỏ hàng hoạt động đúng theo đặc tả.
- Công cụ pytest cho phép **kiểm thử tự động lặp lại** (Regression Testing) mỗi khi mã nguồn thay đổi, đảm bảo không có tính năng bị phá vỡ.
- Fixture của pytest giúp **cách ly môi trường** giữa các test case, đảm bảo tính độc lập và tính tái lập của bộ kiểm thử.
