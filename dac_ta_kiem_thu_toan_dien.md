# TÀI LIỆU ĐẶC TẢ KIỂM THỬ VÀ QUY TRÌNH THỰC THI KIỂM THỬ TỰ ĐỘNG
## HỆ THỐNG QUẢN LÝ BÁN HÀNG (FLASK WEB APPLICATION)

---

| Thông tin                | Nội dung                                                                       |
| :-------------------------| :-------------------------------------------------------------------------------|
| **Tên tài liệu**         | Tài liệu Đặc tả Kiểm thử & Quy trình thực thi kiểm thử bằng pytest             |
| **Dự án**                | Hệ thống Quản lý Bán hàng — Flask Web App                                      |
| **Phiên bản**            | 1.1                                                                            |
| **Ngày tạo**             | 06/06/2026                                                                     |
| **Công cụ kiểm thử**     | pytest 8.2.0 (Python 3.12)                                                     |
| **Đối tượng kiểm thử**   | [app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/app.py)           |
| **Bộ mã nguồn kiểm thử** | [test_app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py) |

---

## MỤC LỤC

1. [Giới thiệu hệ thống & Phạm vi kiểm thử](#1-giới-thiệu-hệ-thống--phạm-vi-kiểm-thử)
2. [Phương pháp kiểm thử áp dụng](#2-phương-pháp-kiểm-thử-áp-dụng)
3. [Môi trường kiểm thử & Cơ chế Fixture](#3-môi-trường-kiểm-thử--cơ-cơ-chế-fixture)
4. [Đặc tả chi tiết và các ca kiểm thử (Test Cases)](#4-đặc-tả-chi-tiết-và-các-ca-kiểm-thử-test-cases)
   - [Module 1: Xác thực người dùng (Authentication)](#module-1-xác-thực-người-dùng-authentication)
   - [Module 2: Quản lý Sản phẩm (Product Management)](#module-2-quản-lý-sản-phẩm-product-management)
   - [Module 3: Giỏ hàng & Thanh toán (Cart & Checkout)](#module-3-giỏ-hàng--thanh-toán-cart--checkout)
   - [Module 4: Quản lý Đơn hàng (Order Management)](#module-4-quản-lý-đơn-hàng-order-management)
   - [Module 5: Tìm kiếm & Lọc Sản phẩm (Advanced Search & Filter)](#module-5-tìm-kiếm--lọc-sản-phẩm-advanced-search--filter)
5. [Ma trận truy xuất yêu cầu (RTM)](#5-ma-trận-truy-xuất-yêu-cầu-rtm)
6. [Quy trình thực hiện kiểm thử tự động bằng pytest](#6-quy-trình-thực-hiện-kiểm-thử-tự-đồng-bằng-pytest)
7. [Kết quả thực thi kiểm thử và phân tích lỗi](#7-kết-quả-thực-thi-kiểm-thử-và-phân-tích-lỗi)

---

## 1. GIỚI THIỆU HỆ THỐNG & PHẠM VI KIỂM THỬ

### 1.1. Giới thiệu hệ thống
Hệ thống Quản lý Bán hàng là ứng dụng web viết bằng **Flask (Python)** hỗ trợ hai phân quyền người dùng chính:
* **Khách hàng (Customer)**: Đăng ký tài khoản, đăng nhập, xem danh sách sản phẩm, thêm vào giỏ hàng, đặt hàng (checkout), và xem lịch sử đơn hàng cá nhân.
* **Quản trị viên (Admin)**: Quản lý sản phẩm (thêm, sửa, xóa), xem tất cả đơn hàng của mọi khách hàng và cập nhật trạng thái đơn hàng.

### 1.2. Phạm vi kiểm thử (In-Scope)
Kiểm thử tích hợp API và logic nghiệp vụ thông qua Flask Request Context được cấu trúc trong [test_app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py). Bao gồm 5 module chức năng:
* **M1 — Xác thực người dùng**: Đăng ký, Đăng nhập, Đăng xuất.
* **M2 — Quản lý sản phẩm**: Thêm, Sửa, Xóa sản phẩm và kiểm soát phân quyền Admin.
* **M3 — Giỏ hàng & Thanh toán**: Thêm vào giỏ, Thanh toán đơn hàng, khấu trừ tồn kho.
* **M4 — Quản lý đơn hàng**: Xem lịch sử đơn hàng, cập nhật trạng thái đơn.
* **M5 — Tìm kiếm & Lọc sản phẩm nâng cao**: API tìm kiếm kết hợp nhiều điều kiện.

### 1.3. Ngoài phạm vi kiểm thử (Out-of-Scope)
* Kiểm thử giao diện đồ họa (UI/UX) trên trình duyệt.
* Kiểm thử hiệu năng (Performance, Load Testing).
* Kiểm thử bảo mật chuyên sâu (Penetration Testing).

---

## 2. PHƯƠNG PHÁP KIỂM THỬ ÁP DỤNG

Nhằm đảm bảo tính chính xác và bao phủ toàn bộ các yêu cầu nghiệp vụ, tài liệu này áp dụng kết hợp các phương pháp sau:

* **Kiểm thử hộp đen (Black-box Testing)**:
  * **Phân vùng tương đương (Equivalence Partitioning)**: Chia dữ liệu đầu vào thành các lớp tương đương hợp lệ và không hợp lệ (ví dụ: đăng ký trùng tên vs đăng ký tên mới; đăng nhập đúng mật khẩu vs đăng nhập sai mật khẩu).
  * **Phân tích giá trị biên (Boundary Value Analysis)**: Lọc các biên đặc biệt như số lượng tồn kho của sản phẩm bằng `0` (hết hàng) hoặc bằng `1` (còn hàng).
* **Kiểm thử hộp trắng (White-box Testing)**:
  * **Kiểm thử đường dẫn (Branch Coverage)**: Đảm bảo mọi nhánh rẻ của câu lệnh điều kiện `if/else` trong [app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/app.py) đều có ít nhất một test case đi qua.
  * **Kiểm thử phân quyền (Access Control Testing)**: Kiểm tra hoạt động của các decorator kiểm soát phiên làm việc như `@login_required` và `@admin_required`.

---

## 3. MÔI TRƯỜNG KIỂM THỬ & CƠ CHẾ FIXTURE

### 3.1. Cấu hình môi trường
* **Hệ điều hành**: Windows 10/11
* **Ngôn ngữ**: Python 3.12
* **Các thư viện chính**: Flask 3.0.3, pytest 8.2.0

### 3.2. Cơ chế Fixture thiết lập dữ liệu ban đầu
Để đảm bảo tính cách ly tuyệt đối (Test Isolation) và tính tái lập giữa các test case, pytest sử dụng `fixture` để thiết lập lại dữ liệu in-memory về trạng thái sạch trước mỗi lần chạy test:

```python
# Không sử dụng client fixture. Các test case thiết lập trực tiếp dữ liệu giả lập 
# và sử dụng request context để gọi trực tiếp các hàm view của Flask:
with app.test_request_context('/route', method='POST', data={...}):
    session['username'] = '...'
    res = function_to_test()
```

---

## 4. ĐẶC TẢ CHI TIẾT VÀ CÁC CA KIỂM THỬ (TEST CASES)

### Module 1: Xác thực người dùng (Authentication)

#### **TC_AUTH_01 — Đăng ký tài khoản mới thành công**
* **Đặc tả chức năng**: Cho phép người dùng tạo tài khoản mới. Tài khoản được ghi nhận vào hệ thống với role mặc định là `customer`.
* **Phương pháp kiểm thử**: Phân vùng tương đương (Vùng dữ liệu hợp lệ).
* **Điều kiện tiên quyết**: Tài khoản `khach_moi` chưa tồn tại trong danh sách.
* **Dữ liệu đầu vào**: `username="khach_moi"`, `password="123"` và gọi trực tiếp register() với context POST.
* **Các bước thực hiện**:
  1. Khởi tạo request context (/register, POST) và gọi trực tiếp register()
  2. Kiểm tra status code và sự tồn tại trong `users`.
* **Kết quả mong đợi**: HTTP `200 OK`, hiển thị thông điệp `"Đăng ký thành công!"`, tài khoản `khach_moi` có trong `users`.
* **Mã kiểm thử tự động**:
  ```python
  def test_register_success():
      users.clear()
      users["admin"] = {"password": "123456", "role": "admin"}
      with app.test_request_context('/register', method='POST', data={'username': 'khach_moi', 'password': '123'}):
          res = register()
          assert res.status_code == 302
          assert res.headers.get('Location') == '/login'
          assert any("Đăng ký thành công!" in m[1] for m in get_flashed_messages(with_categories=True))
          assert "khach_moi" in users
          assert users["khach_moi"]["role"] == "customer"

  ```

#### **TC_AUTH_02 — Đăng ký thất bại do trùng tên tài khoản**
* **Đặc tả chức năng**: Ngăn chặn người dùng tạo tài khoản trùng lặp `username`.
* **Phương pháp kiểm thử**: Phân vùng tương đương (Vùng dữ liệu không hợp lệ).
* **Điều kiện tiên quyết**: Tài khoản `test_user` đã được tạo trước.
* **Dữ liệu đầu vào**: `username="test_user"`, `password="456"` và gọi trực tiếp register() với context POST.
* **Các bước thực hiện**:
  1. Gọi trực tiếp hàm register() để tạo `test_user`.
  2. Khởi tạo request context (/register, POST) lần thứ hai với cùng username `test_user` và gọi trực tiếp register().
* **Kết quả mong đợi**: Hiển thị thông báo lỗi `"Tên đăng nhập đã tồn tại!"`.
* **Mã kiểm thử tự động**:
  ```python
  def test_register_duplicate():
      users.clear()
      users["test_user"] = {"password": "123", "role": "customer"}
      with app.test_request_context('/register', method='POST', data={'username': 'test_user', 'password': '456'}):
          res = register()
          assert isinstance(res, str)  # Trả về chuỗi HTML của trang auth.html
          assert any("Tên đăng nhập đã tồn tại!" in m[1] for m in get_flashed_messages(with_categories=True))

  ```

#### **TC_AUTH_03 — Đăng nhập thành công với tài khoản admin**
* **Đặc tả chức năng**: Đăng nhập đúng thông tin tài khoản giúp ghi session `username` và `role`.
* **Phương pháp kiểm thử**: Phân vùng tương đương (Dữ liệu hợp lệ).
* **Điều kiện tiên quyết**: Tài khoản `admin` tồn tại sẵn với mật khẩu `123456`.
* **Dữ liệu đầu vào**: `username="admin"`, `password="123456"` và gọi trực tiếp login() với context POST.
* **Các bước thực hiện**:
  1. Gọi login() với thông tin hợp lệ.
  2. Kiểm tra flash message và session.
* **Kết quả mong đợi**: Redirect thành công, hiển thị flash message `"Xin chào, admin!"`.
* **Mã kiểm thử tự động**:
  ```python
  def test_login_success():
      users.clear()
      users["admin"] = {"password": "123456", "role": "admin"}
      with app.test_request_context('/login', method='POST', data={'username': 'admin', 'password': '123456'}):
          res = app_login()
          assert res.status_code == 302
          assert res.headers.get('Location') == '/'
          assert session.get('username') == 'admin'
          assert session.get('role') == 'admin'
          assert any("Xin chào, admin!" in m[1] for m in get_flashed_messages(with_categories=True))

  ```

#### **TC_AUTH_04 — Đăng nhập thất bại do sai mật khẩu**
* **Đặc tả chức năng**: Ngăn chặn đăng nhập khi nhập sai mật khẩu.
* **Phương pháp kiểm thử**: Phân vùng tương đương (Dữ liệu không hợp lệ).
* **Điều kiện tiên quyết**: Tài khoản `admin` tồn tại với mật khẩu `123456`.
* **Dữ liệu đầu vào**: `username="admin"`, `password="mat_khau_sai"`.
* **Các bước thực hiện**:
  1. Gọi trực tiếp hàm login() với mật khẩu sai.
  2. Kiểm tra flash error message.
* **Kết quả mong đợi**: Hiển thị lỗi `"Sai tên đăng nhập/mật khẩu!"`.
* **Mã kiểm thử tự động**:
  ```python
  def test_login_wrong_message_intentional():
      users.clear()
      users["admin"] = {"password": "123456", "role": "admin"}
      with app.test_request_context('/login', method='POST', data={'username': 'admin', 'password': 'mat_khau_sai'}):
          res = app_login()
          assert isinstance(res, str)  # Trả về chuỗi HTML quay lại trang đăng nhập
          assert any("Sai tên đăng nhập/mật khẩu!" in m[1] for m in get_flashed_messages(with_categories=True))
          assert 'username' not in session

  ```

#### **TC_AUTH_05 — Đăng xuất thành công**
* **Đặc tả chức năng**: Xóa session của người dùng và điều hướng về trang đăng nhập.
* **Phương pháp kiểm thử**: Kiểm thử hộp đen.
* **Điều kiện tiên quyết**: Đang đăng nhập.
* **Dữ liệu đầu vào**: Không có.
* **Các bước thực hiện**:
  1. Thực hiện Gọi logout().
  2. Kiểm tra flash message và trạng thái session.
* **Kết quả mong đợi**: Hiển thị thông điệp `"Bạn đã đăng xuất!"`, session bị xóa sạch.
* **Mã kiểm thử tự động**:
  ```python
  def test_logout_success():
      with app.test_request_context('/logout'):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = app_logout()
          assert res.status_code == 302
          assert res.headers.get('Location') == '/login'
          assert 'username' not in session
          assert any("Bạn đã đăng xuất!" in m[1] for m in get_flashed_messages(with_categories=True))

  ```

---

### Module 2: Quản lý Sản phẩm (Product Management)

#### **TC_PROD_01 — Admin thêm sản phẩm mới thành công**
* **Đặc tả chức năng**: Admin thêm sản phẩm thành công vào hệ thống.
* **Phương pháp kiểm thử**: Kiểm thử tích hợp.
* **Điều kiện tiên quyết**: Đăng nhập admin.
* **Dữ liệu đầu vào**: `ma_sp="SP02"`, `name="Ban phim co"`, `price=1000000`, `quantity=5`.
* **Các bước thực hiện**:
  1. Gọi trực tiếp hàm add_product() với thông tin sản phẩm mẫu.
  2. Xác minh sản phẩm có tồn tại và đúng số lượng trong `products`.
* **Kết quả mong đợi**: Sản phẩm `SP02` được thêm thành công vào `products` với số lượng tồn kho bằng 5.
* **Mã kiểm thử tự động**:
  ```python
  def test_admin_add_wrong_quantity_intentional():
      products.clear()
      with app.test_request_context('/add', method='POST', data={'ma_sp': 'SP02', 'name': 'Ban phim co', 'price': 1000000, 'quantity': 5}):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = add_product()
          assert res.status_code == 302
          assert res.headers.get('Location') == '/'
          assert products["SP02"]["quantity"] == 5

  ```

#### **TC_PROD_02 — Admin sửa thông tin sản phẩm thành công**
* **Đặc tả chức năng**: Cho phép Admin cập nhật tên, giá và số lượng của một sản phẩm hiện có.
* **Phương pháp kiểm thử**: Kiểm thử tích hợp.
* **Điều kiện tiên quyết**: Đăng nhập admin. Sản phẩm `SP01` đã tồn tại.
* **Dữ liệu đầu vào**: `name="Laptop Dell XPS"`, `price=20000000`, `quantity=15` và gọi trực tiếp edit_product("SP01") với context POST.
* **Các bước thực hiện**:
  1. Gọi trực tiếp hàm edit_product("SP01") với thông tin cập nhật mới.
  2. Xác minh thông tin mới trong dictionary `products`.
* **Kết quả mong đợi**: Dữ liệu của `SP01` được thay đổi hoàn toàn thành công.
* **Mã kiểm thử tự động**:
  ```python
  def test_admin_edit_product():
      products.clear()
      products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
      with app.test_request_context('/edit/SP01', method='POST', data={'name': 'Laptop Dell XPS', 'price': 20000000, 'quantity': 15}):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = edit_product('SP01')
          assert res.status_code == 302
          assert res.headers.get('Location') == '/'
          assert products["SP01"]["name"] == "Laptop Dell XPS"
          assert products["SP01"]["price"] == 20000000
          assert products["SP01"]["quantity"] == 15

  ```

#### **TC_PROD_03 — Admin xóa sản phẩm thành công**
* **Đặc tả chức năng**: Cho phép Admin xóa một sản phẩm khỏi danh sách.
* **Phương pháp kiểm thử**: Kiểm thử tích hợp.
* **Điều kiện tiên quyết**: Đăng nhập admin, sản phẩm `SP01` tồn tại.
* **Dữ liệu đầu vào**: Không có (và gọi trực tiếp delete_product("SP01") với context POST).
* **Các bước thực hiện**:
  1. Khởi tạo request context (/delete/SP01, POST) và gọi trực tiếp delete_product("SP01").
  2. Kiểm tra `SP01` không còn trong dictionary `products`.
* **Kết quả mong đợi**: Sản phẩm bị xóa thành công, assert trả về True khi kiểm tra `"SP01" not in products`.
* **Mã kiểm thử tự động**:
  ```python
  def test_admin_delete_product():
      products.clear()
      products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
      with app.test_request_context('/delete/SP01', method='POST'):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = delete_product('SP01')
          assert res.status_code == 302
          assert res.headers.get('Location') == '/'
          assert "SP01" not in products

  ```

#### **TC_PROD_04 — Khách hàng bị chặn truy cập chức năng Admin**
* **Đặc tả chức năng**: Khách hàng không được quyền truy cập vào các route quản trị của Admin.
* **Phương pháp kiểm thử**: Kiểm thử phân quyền truy cập.
* **Điều kiện tiên quyết**: Đăng nhập với role `customer`.
* **Dữ liệu đầu vào**: Khởi tạo request context (/add, GET) và gọi trực tiếp add_product().
* **Các bước thực hiện**:
  1. Đăng ký & đăng nhập tài khoản khách `khach`.
  2. Gọi trực tiếp hàm add_product().
* **Kết quả mong đợi**: Bị chặn truy cập, chuyển hướng về trang chủ và hiển thị flash warning `"Chỉ admin mới có quyền!"`.
* **Mã kiểm thử tự động**:
  ```python
  def test_customer_access_denied():
      with app.test_request_context('/add', method='GET'):
          session['username'] = 'khach'
          session['role'] = 'customer'
          res = add_product()
          # Chuyển hướng vì chỉ admin mới có quyền
          assert res.status_code == 302
          assert res.headers.get('Location') == '/'
          assert any("Chỉ admin mới có quyền!" in m[1] for m in get_flashed_messages(with_categories=True))

  ```

---

### Module 3: Giỏ hàng & Thanh toán (Cart & Checkout)

#### **TC_CART_01 — Khách hàng thêm sản phẩm vào giỏ thành công**
* **Đặc tả chức năng**: Cho phép khách hàng thêm sản phẩm vào giỏ hàng với số lượng xác định.
* **Phương pháp kiểm thử**: Kiểm thử chức năng & kiểm tra Session.
* **Điều kiện tiên quyết**: Đăng nhập customer. Sản phẩm `SP01` có đủ tồn kho.
* **Dữ liệu đầu vào**: `quantity=3` và gọi trực tiếp add_to_cart("SP01") với context POST.
* **Các bước thực hiện**:
  1. Gọi trực tiếp hàm add_to_cart("SP01") với số lượng là 3.
  2. Kiểm tra dữ liệu giỏ hàng lưu trong `session`.
* **Kết quả mong đợi**: HTTP `200 OK`, hiển thị `"Đã thêm 3 sản phẩm vào giỏ!"`, biến session giỏ hàng lưu đúng số lượng sản phẩm.
* **Mã kiểm thử tự động**:
  ```python
  def test_cart_add_success():
      products.clear()
      products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
      with app.test_request_context('/add_to_cart/SP01', method='POST', data={'quantity': 3}):
          session['username'] = 'buyer'
          session['role'] = 'customer'
          res = add_to_cart('SP01')
          assert res.status_code == 302
          assert res.headers.get('Location') == '/'
          assert any("Đã thêm 3 sản phẩm vào giỏ!" in m[1] for m in get_flashed_messages(with_categories=True))
          assert session.get('cart', {}).get('SP01') == 3

  ```

#### **TC_CART_02 — Thanh toán thành công và tự động trừ tồn kho**
* **Đặc tả chức năng**: Khi khách hàng checkout giỏ hàng, hệ thống tự động trừ lượng tồn kho sản phẩm, tạo hóa đơn mới, tăng tổng doanh thu và xóa giỏ hàng trong session.
* **Phương pháp kiểm thử**: Kiểm thử luồng giao dịch tích hợp.
* **Điều kiện tiên quyết**: Đăng nhập khách hàng, giỏ hàng đã có sản phẩm `SP01` với số lượng 3.
* **Dữ liệu đầu vào**: Thông tin giao hàng (`name="A"`, `phone="012"`, `address="HN"`, `payment_method="COD"`).
* **Các bước thực hiện**:
  1. Giả lập luồng: Đăng nhập → Thêm giỏ hàng → Khởi tạo request context (/checkout, POST) và gọi trực tiếp checkout().
  2. Kiểm tra tồn kho của `SP01` sau giao dịch.
* **Kết quả mong đợi**: Tồn kho `SP01` giảm từ 10 xuống còn 7, hóa đơn được ghi nhận vào danh sách `orders`.
* **Mã kiểm thử tự động**:
  ```python
  def test_shopping_wrong_inventory_intentional():
      products.clear()
      products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
      sales_stats["total_revenue"] = 0
      orders.clear()
      with app.test_request_context('/checkout', method='POST', data={'name': 'A', 'phone': '012', 'address': 'HN', 'payment_method': 'COD'}):
          session['username'] = 'buyer'
          session['role'] = 'customer'
          session['cart'] = {'SP01': 3}
          res = checkout()
          assert res.status_code == 302
          assert products["SP01"]["quantity"] == 7
          assert sales_stats["total_revenue"] == 45000000
          assert 'cart' not in session

  ```

#### **TC_CART_03 — Admin bị chặn khi cố ý mua hàng**
* **Đặc tả chức năng**: Ngăn chặn tài khoản có role `admin` thêm sản phẩm vào giỏ hàng.
* **Phương pháp kiểm thử**: Kiểm thử phân quyền.
* **Điều kiện tiên quyết**: Đăng nhập admin.
* **Dữ liệu đầu vào**: gọi trực tiếp add_to_cart("SP01") với context POST với `quantity=1`.
* **Các bước thực hiện**:
  1. Đăng nhập admin (thiết lập session).
  2. Khởi tạo request context (/add_to_cart/SP01, POST) và gọi trực tiếp add_to_cart("SP01").
* **Kết quả mong đợi**: Admin bị từ chối chuyển hướng về trang sản phẩm, session giỏ hàng trống.
* **Mã kiểm thử tự động**:
  ```python
  def test_admin_add_to_cart_blocked():
      products.clear()
      products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
      with app.test_request_context('/add_to_cart/SP01', method='POST', data={'quantity': 1}):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = add_to_cart('SP01')
          assert res.status_code == 302
          assert res.headers.get('Location') == '/'
          assert 'cart' not in session or 'SP01' not in session['cart']

  ```

---

### Module 4: Quản lý Đơn hàng (Order Management)

#### **TC_ORDER_01 — Đảm bảo cách ly dữ liệu đơn hàng giữa các khách hàng**
* **Đặc tả chức năng**: Khách hàng chỉ được phép xem lịch sử đơn hàng của chính bản thân mình (không hiển thị đơn của khách hàng khác).
* **Phương pháp kiểm thử**: Kiểm thử cách ly dữ liệu (Data Isolation).
* **Điều kiện tiên quyết**: Có hai tài khoản khách hàng `buyer1` và `buyer2` đều đã tạo đơn hàng.
* **Dữ liệu đầu vào**: Khởi tạo request context (/orders, GET) và gọi trực tiếp order_history() khi đăng nhập là `buyer2`.
* **Các bước thực hiện**:
  1. Tài khoản `buyer1` đặt đơn `DH001`.
  2. Tài khoản `buyer2` đặt đơn `DH002`.
  3. Đăng nhập `buyer2`, gọi trực tiếp order_history() với context GET.
* **Kết quả mong đợi**: Trên màn hình của `buyer2` xuất hiện đơn `DH002` nhưng hoàn toàn không hiển thị đơn `DH001`.
* **Mã kiểm thử tự động**:
  ```python
  def test_order_customer_isolation():
      orders.clear()
      orders.append({
          'order_id': 'DH001', 'username': 'buyer1',
          'customer_name': 'Buyer One', 'phone': '011',
          'address': 'HN', 'payment_method': 'COD',
          'items': [{'name': 'Laptop Dell', 'qty': 1}], 'total': 15000000, 'date': '10/06/2026 12:00', 'status': 'Chờ xử lý'
      })
      orders.append({
          'order_id': 'DH002', 'username': 'buyer2',
          'customer_name': 'Buyer Two', 'phone': '022',
          'address': 'SG', 'payment_method': 'COD',
          'items': [{'name': 'Laptop Dell', 'qty': 1}], 'total': 15000000, 'date': '10/06/2026 12:05', 'status': 'Chờ xử lý'
      })
      with app.test_request_context('/orders'):
          session['username'] = 'buyer2'
          session['role'] = 'customer'
          res = order_history()
          assert "DH002" in res
          assert "Buyer Two" in res
          assert "DH001" not in res
          assert "Buyer One" not in res

  ```

#### **TC_ORDER_02 — Admin có quyền xem tất cả đơn hàng trong hệ thống**
* **Đặc tả chức năng**: Tài khoản Admin được quyền quản lý và xem toàn bộ danh sách đơn hàng đã phát sinh.
* **Phương pháp kiểm thử**: Kiểm thử phân quyền hiển thị.
* **Điều kiện tiên quyết**: Hệ thống đã có đơn hàng của khách.
* **Dữ liệu đầu vào**: Đăng nhập admin và gọi trực tiếp order_history() với context GET.
* **Các bước thực hiện**:
  1. Tài khoản `buyer1` tạo đơn hàng.
  2. Đăng nhập `admin`, gọi trực tiếp order_history() với context GET.
* **Kết quả mong đợi**: Admin xem được đơn hàng của `buyer1`.
* **Mã kiểm thử tự động**:
  ```python
  def test_order_admin_view_all():
      orders.clear()
      orders.append({
          'order_id': 'DH001', 'username': 'buyer1',
          'customer_name': 'Buyer One', 'phone': '011',
          'address': 'HN', 'payment_method': 'COD',
          'items': [{'name': 'Laptop Dell', 'qty': 1}], 'total': 15000000, 'date': '10/06/2026 12:00', 'status': 'Chờ xử lý'
      })
      with app.test_request_context('/orders'):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = order_history()
          assert "DH001" in res
          assert "Buyer One" in res

  ```

#### **TC_ORDER_03 — Admin cập nhật trạng thái đơn hàng thành công**
* **Đặc tả chức năng**: Cho phép Admin cập nhật trạng thái của đơn hàng (ví dụ: Chờ xử lý -> Đang giao).
* **Phương pháp kiểm thử**: Kiểm thử chuyển trạng thái.
* **Điều kiện tiên quyết**: Đơn hàng `DH001` đang ở trạng thái mặc định là "Chờ xử lý".
* **Dữ liệu đầu vào**: Khởi tạo request context (/update_order/DH001, POST) và gọi trực tiếp update_order("DH001") với `status="Đang giao"`.
* **Các bước thực hiện**:
  1. Tạo đơn hàng `DH001`.
  2. Đăng nhập admin.
  3. Gọi trực tiếp update_order("DH001") với context POST để cập nhật trạng thái.
* **Kết quả mong đợi**: Trạng thái của đơn chuyển thành `"Đang giao"` cả trong database in-memory và trên giao diện.
* **Mã kiểm thử tự động**:
  ```python
  def test_order_admin_update_status():
      orders.clear()
      orders.append({
          'order_id': 'DH001', 'username': 'buyer1',
          'customer_name': 'Buyer One', 'phone': '011',
          'address': 'HN', 'payment_method': 'COD',
          'items': [{'name': 'Laptop Dell', 'qty': 1}], 'total': 15000000, 'date': '10/06/2026 12:00', 'status': 'Chờ xử lý'
      })
      with app.test_request_context('/update_order/DH001', method='POST', data={'status': 'Đang giao'}):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = update_order('DH001')
          assert res.status_code == 302
          assert res.headers.get('Location') == '/orders'
          assert orders[0]['status'] == 'Đang giao'
          assert any("Đã cập nhật trạng thái đơn DH001 thành: Đang giao" in m[1] for m in get_flashed_messages(with_categories=True))

  ```

---

### Module 5: Tìm kiếm & Lọc Sản phẩm (Advanced Search & Filter)

#### **TC_SEARCH_01 — Tìm kiếm sản phẩm theo từ khóa**
* **Đặc tả chức năng**: Tìm kiếm các sản phẩm có tên hoặc mã chứa từ khóa tìm kiếm (không phân biệt hoa/thường).
* **Phương pháp kiểm thử**: Phân vùng tương đương (Hợp lệ).
* **Điều kiện tiên quyết**: Đăng nhập tài khoản. Fixture nạp sẵn 4 sản phẩm mẫu.
* **Dữ liệu đầu vào**: `q="dell"`.
* **Các bước thực hiện**: Khởi tạo request context (/search?q=dell) và gọi trực tiếp search_products().
* **Kết quả mong đợi**: Trả về đúng 2 sản phẩm chứa từ khóa "dell" là Laptop Dell và Màn hình Dell.
* **Mã kiểm thử tự động**:
  ```python
  def test_search_by_keyword(search_setup):
      with app.test_request_context('/search?q=dell'):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = search_products()
          assert res.status_code == 200
          data = res.get_json()
          assert data["count"] == 2
          names = [p["name"] for p in data["products"]]
          assert "Laptop Dell" in names
          assert "Màn hình Dell" in names

  ```

#### **TC_SEARCH_02 — Lọc sản phẩm theo khoảng giá**
* **Đặc tả chức năng**: Chỉ hiển thị các sản phẩm có mức giá nằm trong khoảng `[min_price, max_price]`.
* **Phương pháp kiểm thử**: Phân vùng tương đương.
* **Điều kiện tiên quyết**: Đăng nhập hệ thống.
* **Dữ liệu đầu vào**: `min_price=200000`, `max_price=1000000`.
* **Các bước thực hiện**: Khởi tạo request context (/search?min_price=200000&max_price=1000000) và gọi trực tiếp search_products().
* **Kết quả mong đợi**: Phản hồi chứa 2 sản phẩm nằm trong khoảng giá là Chuột Logitech (300K) và Bàn phím cơ (800K).
* **Mã kiểm thử tự động**:
  ```python
  def test_search_filter_by_price_range(search_setup):
      with app.test_request_context('/search?min_price=200000&max_price=1000000'):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = search_products()
          assert res.status_code == 200
          data = res.get_json()
          assert data["count"] == 2
          for p in data["products"]:
              assert 200000 <= p["price"] <= 1000000

  ```

#### **TC_SEARCH_03 — Lọc chỉ sản phẩm còn hàng**
* **Đặc tả chức năng**: Khi tham số lọc `in_stock=1`, loại bỏ các sản phẩm có số lượng tồn kho bằng `0`.
* **Phương pháp kiểm thử**: Phân tích giá trị biên (số lượng bằng 0).
* **Điều kiện tiên quyết**: Đăng nhập hệ thống, sản phẩm Bàn phím cơ hết hàng (`quantity=0`).
* **Dữ liệu đầu vào**: `in_stock=1`.
* **Các bước thực hiện**: Khởi tạo request context (/search?in_stock=1) và gọi trực tiếp search_products().
* **Kết quả mong đợi**: Loại bỏ hoàn toàn Bàn phím cơ ra khỏi kết quả tìm kiếm.
* **Mã kiểm thử tự động**:
  ```python
  def test_search_filter_in_stock_only(search_setup):
      with app.test_request_context('/search?in_stock=1'):
          session['username'] = 'admin'
          session['role'] = 'admin'
          res = search_products()
          assert res.status_code == 200
          data = res.get_json()
          names = [p["name"] for p in data["products"]]
          assert "Bàn phím cơ" not in names
          assert data["count"] == 3

  ```

#### **TC_SEARCH_04 — Người dùng chưa đăng nhập bị chặn**
* **Đặc tả chức năng**: Chỉ cho phép người dùng có session đăng nhập truy cập API tìm kiếm nâng cao.
* **Phương pháp kiểm thử**: Kiểm thử phân quyền truy cập.
* **Điều kiện tiên quyết**: Người dùng chưa đăng nhập.
* **Dữ liệu đầu vào**: Khởi tạo request context (/search) và gọi trực tiếp search_products().
* **Các bước thực hiện**: 
  1. Khởi tạo request context (/search, GET) không thiết lập session.
  2. Gọi trực tiếp hàm search_products().
* **Kết quả mong đợi**: Bị chuyển hướng điều hướng về `/login` với thông báo cảnh báo.
* **Mã kiểm thử tự động**:
  ```python
  def test_search_unauthenticated_blocked(search_setup):
      with app.test_request_context('/search'):
          # Không truyền session, để login_required kích hoạt
          res = search_products()
          assert res.status_code == 302
          assert res.headers.get('Location') == '/login'
          assert any("Vui lòng đăng nhập!" in m[1] for m in get_flashed_messages(with_categories=True))

  ```

---

## 5. MA TRẬN TRUY XUẤT YÊU CẦU (RTM)

Ma trận RTM giúp xác thực toàn bộ yêu cầu nghiệp vụ (Requirements) đã được bao phủ bởi ít nhất một ca kiểm thử:

| Mã yêu cầu | Yêu cầu nghiệp vụ | Mã ca kiểm thử tương ứng | Trạng thái |
| :---: | :--- | :--- | :---: |
| **REQ_01** | Đăng ký tài khoản khách hàng mới | TC_AUTH_01, TC_AUTH_02 | ✅ Đạt |
| **REQ_02** | Đăng nhập tài khoản | TC_AUTH_03, TC_AUTH_04 | ✅ Đạt |
| **REQ_03** | Đăng xuất và xóa phiên đăng nhập | TC_AUTH_05 | ✅ Đạt |
| **REQ_04** | Admin cập nhật thông tin sản phẩm | TC_PROD_02 | ✅ Đạt |
| **REQ_05** | Admin xóa sản phẩm khỏi danh sách | TC_PROD_03 | ✅ Đạt |
| **REQ_06** | Khách hàng bị chặn truy cập màn hình Admin | TC_PROD_04 | ✅ Đạt |
| **REQ_07** | Thêm sản phẩm có sẵn vào giỏ hàng | TC_CART_01 | ✅ Đạt |
| **REQ_08** | Đặt hàng và khấu trừ tồn kho thực tế | TC_CART_02 | ✅ Đạt |
| **REQ_09** | Chặn Admin thêm giỏ hàng mua sắm | TC_CART_03 | ✅ Đạt |
| **REQ_10** | Cách ly hiển thị đơn hàng giữa các khách | TC_ORDER_01 | ✅ Đạt |
| **REQ_11** | Admin xem tất cả danh sách đơn hàng | TC_ORDER_02 | ✅ Đạt |
| **REQ_12** | Admin cập nhật trạng thái xử lý đơn hàng | TC_ORDER_03 | ✅ Đạt |
| **REQ_13** | Tìm kiếm sản phẩm theo từ khóa tên | TC_SEARCH_01 | ✅ Đạt |
| **REQ_14** | Lọc sản phẩm theo khoảng giá tối thiểu - tối đa | TC_SEARCH_02 | ✅ Đạt |
| **REQ_15** | Lọc loại bỏ sản phẩm đã hết hàng | TC_SEARCH_03 | ✅ Đạt |
| **REQ_16** | Chặn truy cập API `/search` khi chưa đăng nhập | TC_SEARCH_04 | ✅ Đạt |

---

## 6. QUY TRÌNH THỰC HIỆN KIỂM THỬ TỰ ĐỘNG BẰNG PYTEST

Để thực thi kiểm thử chức năng tự động trong môi trường thực tế, kiểm thử viên thực hiện theo quy trình 4 bước:

### **Bước 1: Chuẩn bị môi trường**
Đảm bảo đã cài đặt Python 3.8+ và cài đặt các thư viện phụ thuộc bằng lệnh:
```powershell
pip install -r requirements.txt
```

### **Bước 2: Viết mã nguồn kiểm thử**
Tạo và cập nhật tệp [test_app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py). Các hàm test phải có tiền tố `test_` và sử dụng `assert` để so khớp kết quả thực tế với giá trị kỳ vọng.

### **Bước 3: Thực thi các lệnh kiểm thử qua CLI**
Chạy các dòng lệnh kiểm thử bằng cách mở terminal trong thư mục dự án:
* **Chạy toàn bộ các test case trong hệ thống**:
  ```powershell
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

============================= 19 passed in 0.41s =============================
```

### 7.2. Phân tích kết quả chạy
* Toàn bộ 19 ca kiểm thử tích hợp và API đều đạt trạng thái **PASSED**.
* Tính nhất quán dữ liệu giữa các module Xác thực, Sản phẩm, Giỏ hàng, Đơn hàng và Tìm kiếm đã được xác minh hoạt động hoàn toàn chính xác theo đặc tả yêu cầu nghiệp vụ.

---
*Tài liệu được cập nhật đầy đủ và đồng bộ hóa với hệ thống kiểm thử tự động của dự án bán hàng Flask.*
