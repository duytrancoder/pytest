# BÁO CÁO BÀI TẬP LỚN
# MÔN: KIỂM THỬ PHẦN MỀM

---

| Thông tin | Nội dung |
|:---|:---|
| **Tên nhóm** | Nhóm X |
| **Thành viên** | Thành viên 1, Thành viên 2, Thành viên 3, Thành viên 4, Thành viên 5 |
| **Học phần** | Kiểm thử Phần mềm |
| **Công cụ kiểm thử** | pytest 8.2.0 (Python) |
| **Ứng dụng kiểm thử** | Hệ thống Quản lý Bán hàng (Flask Web App) |

---

## LỜI NÓI ĐẦU

Trong kỷ nguyên số hóa hiện nay, công nghệ thông tin đã và đang trở thành một phần không thể thiếu trong mọi hoạt động kinh tế, xã hội và đời sống. Cùng với sự phát triển mạnh mẽ đó, số lượng và quy mô của các sản phẩm phần mềm ngày càng gia tăng vượt bậc. Tuy nhiên, một hệ thống phần mềm dù có thiết kế tối ưu hay giao diện bắt mắt đến đâu cũng không thể tránh khỏi các lỗi phát sinh (bugs) trong quá trình phát triển. Những sai sót này nếu không được phát hiện kịp thời có thể dẫn đến những thiệt hại nghiêm trọng về cả uy tín, chi phí lẫn trải nghiệm người dùng.

Chính vì vậy, **Kiểm thử phần mềm (Software Testing)** đóng vai trò vô cùng cốt lõi trong quy trình phát triển dự án công nghệ thông tin. Kiểm thử không chỉ đơn thuần là việc tìm kiếm lỗi, mà còn là giải pháp đảm bảo sản phẩm phần mềm được bàn giao đáp ứng đúng các tiêu chí kỹ thuật, hoạt động ổn định, an toàn và hiệu quả theo đúng yêu cầu nghiệp vụ của khách hàng.

Nhận thức được tầm quan trọng đó, dưới sự hướng dẫn của giảng viên bộ môn Kiểm thử phần mềm, nhóm chúng em đã thực hiện đề tài báo cáo bài tập lớn: **"Tìm hiểu và ứng dụng công cụ kiểm thử tự động pytest để kiểm thử Hệ thống Quản lý Bán hàng viết bằng Flask"**. Báo cáo tập trung nghiên cứu lý thuyết cơ bản về kiểm thử, cách thức hoạt động của công cụ pytest và phân tích, thiết kế các ca kiểm thử (test cases) cụ thể cho các tính năng nghiệp vụ chính của ứng dụng.

Cấu trúc của báo cáo gồm 3 chương chính:
* **Chương 1:** Giới thiệu tổng quan về kiểm thử phần mềm và các phương pháp kiểm thử nhóm lựa chọn áp dụng trong đề tài.
* **Chương 2:** Giới thiệu chi tiết về công cụ kiểm thử tự động **pytest** (các thành phần chính, cách thức cài đặt, giao diện hiển thị kết quả và quy trình thực hiện kiểm thử).
* **Chương 3:** Ứng dụng công cụ pytest để thiết kế và thực thi kiểm thử cho các chức năng nghiệp vụ cụ thể của hệ thống Quản lý Bán hàng (Xác thực, Quản lý sản phẩm, Giỏ hàng & Đặt hàng, Quản lý đơn hàng).

Do kiến thức chuyên môn và kinh nghiệm thực tế còn nhiều hạn chế, báo cáo của nhóm không thể tránh khỏi những thiếu sót. Nhóm chúng em rất mong nhận được những ý kiến đóng góp, nhận xét và phê bình từ phía thầy/cô giáo để bài nghiên cứu ngày càng hoàn thiện hơn.

Chúng em xin chân thành cảm ơn!

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
| Thành viên 5 | Tìm kiếm & Lọc sản phẩm nâng cao (Advanced Search & Filter) |

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
| **TC_PROD_01** | Admin thêm sản phẩm mới | Đăng nhập `admin`, `SP02` chưa tồn tại | 1. POST `/add`  2. Kiểm tra `products["SP02"]` | `ma_sp="SP02"`, `name="Ban phim co"`, `price=1000000`, `quantity=5` | Sản phẩm `SP02` xuất hiện trong `products` với đúng thông tin | ❌ ERROR (Cố tình) |
| **TC_PROD_02** | Admin sửa sản phẩm thành công | Đăng nhập `admin`, `SP01` đã có sẵn | 1. POST `/edit/SP01`  2. Kiểm tra dữ liệu mới | `name="Laptop Dell XPS"`, `price=20000000`, `quantity=15` | `products["SP01"]["name"] == "Laptop Dell XPS"`, `price == 20000000` | ✅ PASSED |
| **TC_PROD_03** | Admin xóa sản phẩm thành công | Đăng nhập `admin`, `SP01` đã có sẵn | 1. POST `/delete/SP01`  2. Kiểm tra sự tồn tại | _(không có)_ | `"SP01" not in products` | ❌ FAILED (Cố tình) |
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
test_app.py::test_admin_edit_product                    PASSED
test_app.py::test_admin_delete_product                  FAILED
test_app.py::test_customer_access_denied                PASSED
test_app.py::test_admin_add_wrong_quantity_intentional  ERROR
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
| **TC_CART_01** | Khách hàng thêm sản phẩm vào giỏ thành công | Đăng nhập `buyer`, `SP01` có tồn kho 10 | 1. POST `/add_to_cart/SP01`  2. Kiểm tra session cart | `quantity=3` | Giỏ hàng session có `SP01: 3` | ✅ PASSED |
| **TC_CART_02** | Thanh toán thành công, tồn kho giảm đúng | Giỏ hàng có `SP01` số lượng 3, tồn kho ban đầu 10 | 1. POST `/checkout`  2. Kiểm tra `products["SP01"]["quantity"]` | `name="A"`, `phone="012"`, `address="HN"`, `payment_method="COD"` | Tồn kho `SP01` giảm từ 10 xuống **7** (`10 - 3 = 7`) | ✅ PASSED |
| **TC_CART_03** | Admin bị chặn không được thêm vào giỏ | Đăng nhập `admin` | 1. POST `/add_to_cart/SP01` | `quantity=1` | Chuyển hướng về trang chủ, giỏ hàng không thay đổi | ✅ PASSED |

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
def test_cart_add_success(client):
    client.post('/register', data={'username': 'buyer', 'password': '123'})
    login(client, 'buyer', '123')
    res = client.post('/add_to_cart/SP01', data={'quantity': 3}, follow_redirects=True)
    assert res.status_code == 200
    assert "Đã thêm 3 sản phẩm vào giỏ!" in res.get_data(as_text=True)
    with client.session_transaction() as sess:
        assert sess.get('cart', {}).get('SP01') == 3

def test_shopping_wrong_inventory_intentional(client):
    client.post('/register', data={'username': 'buyer', 'password': '123'})
    login(client, 'buyer', '123')
    client.post('/add_to_cart/SP01', data={'quantity': 3}, follow_redirects=True)
    client.post('/checkout', data={'name': 'A', 'phone': '012', 'address': 'HN', 'payment_method': 'COD'}, follow_redirects=True)
    assert products["SP01"]["quantity"] == 7

def test_admin_add_to_cart_blocked(client):
    login(client, 'admin', '123456')
    res = client.post('/add_to_cart/SP01', data={'quantity': 1}, follow_redirects=True)
    assert res.status_code == 200
    with client.session_transaction() as sess:
        assert 'cart' not in sess or 'SP01' not in sess['cart']
```

**Bước 3 — Thực thi:**
```powershell
pytest -v test_app.py -k "cart or shopping"
```

**Bước 4 — Kết quả:**
```
test_app.py::test_cart_add_success                        PASSED
test_app.py::test_shopping_wrong_inventory_intentional    PASSED
test_app.py::test_admin_add_to_cart_blocked               PASSED
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
| **TC_ORDER_01** | Khách chỉ xem được đơn của chính mình | 2 khách hàng A, B đều đặt hàng | 1. Đăng nhập B  2. GET `/orders`  3. Kiểm tra danh sách | TK khách B | Chỉ hiển thị đơn của B, không thấy đơn của A | ✅ PASSED |
| **TC_ORDER_02** | Admin xem toàn bộ đơn hàng | Hệ thống có đơn của nhiều khách | 1. Đăng nhập admin  2. GET `/orders`  3. Kiểm tra danh sách | TK admin | Hiển thị tất cả đơn hàng | ✅ PASSED |
| **TC_ORDER_03** | Admin cập nhật trạng thái đơn thành công | Có đơn `DH001` với trạng thái "Chờ xử lý" | 1. POST `/update_order/DH001`  2. Kiểm tra trạng thái đơn | `status="Đang giao"` | `order["status"] == "Đang giao"` | ✅ PASSED |

**Mã nguồn kiểm thử tự động tương ứng:**

```python
def test_order_customer_isolation(client):
    # Đăng ký và đặt đơn cho buyer1
    client.post('/register', data={'username': 'buyer1', 'password': '123'})
    login(client, 'buyer1', '123')
    client.post('/add_to_cart/SP01', data={'quantity': 1}, follow_redirects=True)
    client.post('/checkout', data={'name': 'Buyer One', 'phone': '011', 'address': 'HN', 'payment_method': 'COD'}, follow_redirects=True)
    logout(client)

    # Đăng ký và đặt đơn cho buyer2
    client.post('/register', data={'username': 'buyer2', 'password': '123'})
    login(client, 'buyer2', '123')
    client.post('/add_to_cart/SP01', data={'quantity': 1}, follow_redirects=True)
    client.post('/checkout', data={'name': 'Buyer Two', 'phone': '022', 'address': 'SG', 'payment_method': 'COD'}, follow_redirects=True)
    
    # buyer2 xem danh sách đơn hàng
    res = client.get('/orders')
    html_content = res.get_data(as_text=True)
    
    # buyer2 phải thấy đơn của mình (DH002) nhưng KHÔNG được thấy đơn của buyer1 (DH001)
    assert "DH002" in html_content
    assert "Buyer Two" in html_content
    assert "DH001" not in html_content
    assert "Buyer One" not in html_content

def test_order_admin_view_all(client):
    # Đặt đơn cho buyer1
    client.post('/register', data={'username': 'buyer1', 'password': '123'})
    login(client, 'buyer1', '123')
    client.post('/add_to_cart/SP01', data={'quantity': 1}, follow_redirects=True)
    client.post('/checkout', data={'name': 'Buyer One', 'phone': '011', 'address': 'HN', 'payment_method': 'COD'}, follow_redirects=True)
    logout(client)

    # Admin đăng nhập và xem orders
    login(client, 'admin', '123456')
    res = client.get('/orders')
    html_content = res.get_data(as_text=True)
    
    # Admin phải thấy đơn của buyer1 (DH001)
    assert "DH001" in html_content
    assert "Buyer One" in html_content

def test_order_admin_update_status(client):
    # Đặt đơn cho buyer1
    client.post('/register', data={'username': 'buyer1', 'password': '123'})
    login(client, 'buyer1', '123')
    client.post('/add_to_cart/SP01', data={'quantity': 1}, follow_redirects=True)
    client.post('/checkout', data={'name': 'Buyer One', 'phone': '011', 'address': 'HN', 'payment_method': 'COD'}, follow_redirects=True)
    logout(client)

    # Admin đăng nhập và cập nhật trạng thái đơn DH001
    login(client, 'admin', '123456')
    res = client.post('/update_order/DH001', data={'status': 'Đang giao'}, follow_redirects=True)
    
    # Kiểm tra trạng thái trong biến orders của app
    assert orders[0]['status'] == 'Đang giao'
    
    # Kiểm tra giao diện hiển thị trạng thái mới
    html_content = res.get_data(as_text=True)
    assert "Đang giao" in html_content
```

#### 3.6.4. Quy trình thực hiện kiểm thử bằng pytest

**Bước 1** — Tạo dữ liệu đơn hàng và kiểm tra cách ly hiển thị giữa các tài khoản (Customer vs Customer, Customer vs Admin).

**Bước 2** — Thực hiện gửi request POST để cập nhật trạng thái đơn hàng và xác thực trạng thái mới.

**Bước 3** — Thực thi lệnh chạy riêng các test case của chức năng Quản lý Đơn hàng:
```powershell
pytest -v test_app.py -k "order"
```

---

### 3.7. Thành viên 5 — Kiểm thử chức năng Tìm kiếm & Lọc Sản phẩm nâng cao (Advanced Search & Filter)

#### 3.7.1. Đặc tả chức năng

Chức năng **Tìm kiếm & Lọc sản phẩm nâng cao** được triển khai tại route `GET /search` trả về dữ liệu JSON, hỗ trợ các bộ lọc kết hợp:

- **Tìm kiếm theo từ khóa** (`?q=`): So khớp với tên sản phẩm hoặc mã SP, không phân biệt chữ hoa/thường.
- **Lọc khoảng giá** (`?min_price=`, `?max_price=`): Chỉ trả về sản phẩm có giá nằm trong khoảng `[min_price, max_price]`.
- **Lọc tình trạng tồn kho** (`?in_stock=1`): Chỉ trả về sản phẩm có `quantity > 0`.
- **Yêu cầu đăng nhập**: Route được bảo vệ bởi `@login_required` — người dùng chưa đăng nhập bị chuyển hướng về trang login.

Phản hồi JSON có cấu trúc:
```json
{
  "count": 2,
  "products": [
    {"ma_sp": "SP01", "name": "Laptop Dell", "price": 15000000, "quantity": 10, "in_stock": true},
    ...
  ]
}
```

#### 3.7.2. Phương pháp kiểm thử

- **Kiểm thử phân vùng tương đương (Equivalence Partitioning)**:
  - Vùng hợp lệ — từ khóa khớp → trả về đúng số lượng sản phẩm.
  - Vùng không hợp lệ — bộ lọc giá loại bỏ sản phẩm ngoài khoảng.
  - Vùng đặc biệt — lọc `in_stock` loại bỏ sản phẩm hết hàng.
- **Kiểm thử phân quyền (Authorization Testing)**: Đảm bảo route `/search` không thể truy cập khi chưa đăng nhập.
- **Kiểm thử API (API Testing)**: Xác nhận cấu trúc và nội dung phản hồi JSON (`status_code`, `count`, `products`).

#### 3.7.3. Fixture chuyên dụng

Thành viên 5 xây dựng fixture `search_client` kế thừa từ `client`, bổ sung thêm 3 sản phẩm đa dạng giá và tình trạng tồn kho để phục vụ kiểm thử:

```python
@pytest.fixture
def search_client(client):
    products["SP02"] = {"name": "Chuột Logitech", "price": 300000,  "quantity": 50}
    products["SP03"] = {"name": "Bàn phím cơ",   "price": 800000,  "quantity": 0}  # hết hàng
    products["SP04"] = {"name": "Màn hình Dell",  "price": 5000000, "quantity": 5}
    login(client, "admin", "123456")
    return client
```

Sau khi fixture này chạy, bộ sản phẩm trong DB thử nghiệm gồm:

| Mã SP | Tên | Giá | Tồn kho |
|:---:|:---|---:|:---:|
| SP01 | Laptop Dell | 15.000.000 đ | 10 |
| SP02 | Chuột Logitech | 300.000 đ | 50 |
| SP03 | Bàn phím cơ | 800.000 đ | 0 (hết hàng) |
| SP04 | Màn hình Dell | 5.000.000 đ | 5 |

#### 3.7.4. Danh sách ca kiểm thử

| Mã ca | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế |
|:---|:---|:---|:---|:---|:---|:---|
| **TC_SEARCH_01** | Tìm kiếm sản phẩm theo từ khóa tên | Đăng nhập admin, có 4 sản phẩm trong DB | 1. GET `/search?q=dell` 2. Kiểm tra JSON phản hồi | `q="dell"` | `count == 2`, danh sách chứa "Laptop Dell" và "Màn hình Dell" | ✅ PASSED |
| **TC_SEARCH_02** | Lọc sản phẩm theo khoảng giá | Đăng nhập admin, có 4 sản phẩm trong DB | 1. GET `/search?min_price=200000&max_price=1000000` 2. Kiểm tra JSON | `min_price=200000`, `max_price=1000000` | `count == 2`, mọi SP trong kết quả có giá từ 200.000đ đến 1.000.000đ | ✅ PASSED |
| **TC_SEARCH_03** | Lọc chỉ sản phẩm còn hàng | Đăng nhập admin, SP03 "Bàn phím cơ" có quantity=0 | 1. GET `/search?in_stock=1` 2. Kiểm tra danh sách | `in_stock=1` | `count == 3`, "Bàn phím cơ" không xuất hiện trong kết quả | ✅ PASSED |
| **TC_SEARCH_04** | Người dùng chưa đăng nhập bị chặn | Không có session đăng nhập | 1. GET `/search` 2. Kiểm tra phản hồi | _(không có)_ | HTTP 200 (sau redirect), hiển thị "Vui lòng đăng nhập!", không trả về JSON | ✅ PASSED |

#### 3.7.5. Mã nguồn kiểm thử tự động

```python
def test_search_by_keyword(search_client):
    res = search_client.get("/search?q=dell")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 2
    names = [p["name"] for p in data["products"]]
    assert "Laptop Dell"   in names
    assert "Màn hình Dell" in names

def test_search_filter_by_price_range(search_client):
    res = search_client.get("/search?min_price=200000&max_price=1000000")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 2
    for p in data["products"]:
        assert 200000 <= p["price"] <= 1000000

def test_search_filter_in_stock_only(search_client):
    res = search_client.get("/search?in_stock=1")
    assert res.status_code == 200
    data = res.get_json()
    names = [p["name"] for p in data["products"]]
    assert "Bàn phím cơ" not in names
    assert data["count"] == 3

def test_search_unauthenticated_blocked(client):
    res = client.get("/search", follow_redirects=True)
    assert res.status_code == 200
    assert "Vui lòng đăng nhập!" in res.get_data(as_text=True)
```

#### 3.7.6. Quy trình thực hiện kiểm thử

**Bước 1 — Xác định luồng xử lý:**
```
GET /search?q=dell&min_price=0&max_price=inf&in_stock=0
    → Lặp qua products dict
    → Lọc theo từ khóa (tên hoặc mã SP)
    → Lọc theo khoảng giá
    → Lọc theo tình trạng tồn kho
    → jsonify({'count': N, 'products': [...]})
```

**Bước 2 — Thực thi:**
```powershell
pytest -v test_app.py -k "search"
```

**Bước 3 — Kết quả:**
```
test_app.py::test_search_by_keyword              PASSED
test_app.py::test_search_filter_by_price_range   PASSED
test_app.py::test_search_filter_in_stock_only    PASSED
test_app.py::test_search_unauthenticated_blocked PASSED
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
collected 19 items

test_app.py::test_register_success                      PASSED  [  5%]
test_app.py::test_register_duplicate                    PASSED  [ 10%]
test_app.py::test_login_success                         PASSED  [ 15%]
test_app.py::test_logout_success                        PASSED  [ 21%]
test_app.py::test_admin_edit_product                    PASSED  [ 26%]
test_app.py::test_admin_delete_product                  FAILED  [ 31%]
test_app.py::test_customer_access_denied                PASSED  [ 36%]
test_app.py::test_login_wrong_message_intentional       PASSED  [ 42%]
test_app.py::test_admin_add_wrong_quantity_intentional  ERROR   [ 47%]
test_app.py::test_cart_add_success                      PASSED  [ 52%]
test_app.py::test_shopping_wrong_inventory_intentional  PASSED  [ 57%]
test_app.py::test_admin_add_to_cart_blocked             PASSED  [ 63%]
test_app.py::test_order_customer_isolation              PASSED  [ 68%]
test_app.py::test_order_admin_view_all                  PASSED  [ 73%]
test_app.py::test_order_admin_update_status             PASSED  [ 78%]
test_app.py::test_search_by_keyword                     PASSED  [ 84%]
test_app.py::test_search_filter_by_price_range          PASSED  [ 89%]
test_app.py::test_search_filter_in_stock_only           PASSED  [ 94%]
test_app.py::test_search_unauthenticated_blocked        PASSED  [100%]

=================================== ERRORS ====================================
_________ ERROR at setup of test_admin_add_wrong_quantity_intentional _________
RuntimeError: Lỗi kết nối cơ sở dữ liệu admin (Lỗi thiết lập Fixture)!

================================== FAILURES ===================================
__________________________ test_admin_delete_product __________________________
AssertionError: assert 'SP01' in {}

==================== 1 failed, 17 passed, 1 error in 0.99s ====================
```

### Tổng hợp kết quả:

| Thành viên | Chức năng | Số ca kiểm thử | Passed | Failed | Error |
|:---:|:---|:---:|:---:|:---:|:---:|
| Thành viên 1 | Xác thực người dùng | 5 | 5 | 0 | 0 |
| Thành viên 2 | Quản lý sản phẩm | 4 | 2 | 1 | 1 |
| Thành viên 3 | Giỏ hàng & Thanh toán | 3 | 3 | 0 | 0 |
| Thành viên 4 | Quản lý đơn hàng | 3 | 3 | 0 | 0 |
| Thành viên 5 | Tìm kiếm & Lọc sản phẩm | 4 | 4 | 0 | 0 |
| **Tổng cộng** | | **19** | **17** | **1** | **1** |

### Nhận xét:

- Bộ kiểm thử tự động gồm **19 ca** đã được thực thi hoàn tất. Kết quả ghi nhận chính xác: **17 PASSED**, **1 FAILED**, và **1 ERROR**.
- Các ca kiểm thử của **Thành viên 4** đã được viết code tự động đầy đủ và đều **PASSED**, đảm bảo phân isolation dữ liệu đơn hàng giữa các khách hàng hoạt động bảo mật, và admin có thể xem toàn bộ đơn hàng cũng như thay đổi trạng thái thành công.
- **Thành viên 5** bổ sung chức năng **Tìm kiếm & Lọc sản phẩm nâng cao** (`/search`) trả về JSON, với 4 ca kiểm thử đều **PASSED** — bao phủ lọc từ khóa, khoảng giá, tình trạng tồn kho và kiểm tra phân quyền truy cập route.
- Các ca lỗi **FAILED** và **ERROR** được thiết kế cố ý nhằm minh họa khả năng phát hiện lỗi của pytest trong thực tế (AssertionError ở giai đoạn chạy test và RuntimeError ở giai đoạn Setup).
- Fixture của pytest giúp **cách ly môi trường** giữa các test case, đảm bảo tính độc lập và tính tái lập của bộ kiểm thử. Kỹ thuật **fixture kế thừa** (`search_client` kế thừa `client`) được Thành viên 5 áp dụng để mở rộng môi trường kiểm thử mà không trùng lặp code.

---

## KẾT LUẬN

Qua quá trình tìm hiểu lý thuyết và ứng dụng thực tiễn công cụ **pytest** để thực hiện kiểm thử tự động cho **Hệ thống Quản lý Bán hàng**, nhóm chúng em đã thu hoạch được nhiều kết quả quan trọng và rút ra những kết luận sau:

### 1. Kết quả đạt được của đề tài
* **Về mặt lý thuyết:** Nhóm đã nắm vững các kiến thức cơ bản về quy trình kiểm thử phần mềm, sự khác biệt giữa các phương pháp kiểm thử (Hộp đen, Hộp trắng, Kiểm thử hồi quy) cũng như ý nghĩa của các cấp độ kiểm thử.
* **Về mặt công cụ:** Hiểu rõ cấu trúc và cơ chế hoạt động của framework pytest bao gồm: cách tổ chức các file test, viết các hàm kiểm thử độc lập, thiết lập môi trường bằng Fixture và sử dụng assert để đối chiếu dữ liệu.
* **Về mặt thực hành:** Thiết kế thành công bộ dữ liệu gồm **15 ca kiểm thử tự động** bao phủ các tính năng cốt lõi của website. Đặc biệt, việc mô phỏng được cả các trạng thái lỗi **FAILED** (lỗi assertion logic) và **ERROR** (lỗi setup môi trường/fixture) đã giúp nhóm hiểu sâu hơn cách debug và kiểm soát chất lượng phần mềm trong thực tế.

### 2. Ưu điểm của phương pháp kiểm thử tự động bằng pytest
* **Tự động hóa & Tiết kiệm thời gian:** Chỉ với một câu lệnh đơn giản trên terminal, toàn bộ các chức năng phức tạp của ứng dụng được kiểm thử hoàn tất trong chưa đầy 1 giây. Điều này vô cùng hiệu quả so với kiểm thử thủ công (manual testing).
* **Độ tin cậy cao:** Giúp phát hiện nhanh các lỗi hồi quy khi mã nguồn ứng dụng thay đổi, đảm bảo các chức năng cũ không bị ảnh hưởng khi thêm mới tính năng.
* **Báo cáo trực quan:** Pytest cung cấp thông tin traceback chi tiết, chỉ rõ vị trí và nguyên nhân gây lỗi, giúp lập trình viên sửa lỗi nhanh chóng.

### 3. Hạn chế và Hướng phát triển
* **Hạn chế:** Bộ kiểm thử hiện tại chủ yếu giả lập HTTP requests/responses (tầng backend/integration). Chưa kiểm thử trực tiếp các tương tác phức tạp trên giao diện người dùng (UI/UX) như hiệu ứng Javascript, hoạt động click chuột của khách hàng thực tế.
* **Hướng phát triển:** Kết hợp **pytest** với các công cụ kiểm thử giao diện như **Selenium WebDriver** hoặc **Playwright** để xây dựng bộ kiểm thử End-to-End (E2E) toàn diện cho cả giao diện và logic hệ thống trong tương lai.
