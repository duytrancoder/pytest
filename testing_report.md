# BÁO CÁO PHÂN TÍCH VÀ THIẾT KẾ KIỂM THỬ HỆ THỐNG QUẢN LÝ BÁN HÀNG

Tài liệu này giới thiệu tổng quan về hệ thống Quản lý Bán hàng viết bằng **Flask** và phân công thiết kế kiểm thử cho nhóm gồm 4 thành viên, mỗi người chịu trách nhiệm kiểm thử 1 chức năng chính bằng công cụ **pytest**.

---

## PHẦN 1: GIỚI THIỆU TỔNG QUAN VỀ HỆ THỐNG (WEB/APP)

Ứng dụng là một trang web thương mại điện tử nhỏ gọn phục vụ quản lý sản phẩm, giỏ hàng, đặt hàng và quản lý đơn hàng. 
* **Công nghệ sử dụng**:
  * **Backend**: Python, Flask Framework.
  * **Frontend**: HTML5, Jinja2 Templates, Bootstrap 5 CSS (giao diện responsive).
  * **Cơ sở dữ liệu**: Dữ liệu lưu tạm thời trong bộ nhớ (In-memory dict/list), reset mỗi khi khởi động lại server.
  * **Công cụ kiểm thử**: pytest (thư viện kiểm thử tự động của Python).

### Các nhóm chức năng chính của hệ thống:
1. **Xác thực & Phân quyền (Authentication)**: Đăng ký tài khoản khách hàng, đăng nhập hệ thống dưới vai trò Khách hàng (`customer`) hoặc Quản trị viên (`admin`), đăng xuất và xóa session.
2. **Quản lý sản phẩm (Product Management)**: Admin có thể thêm, sửa, xóa sản phẩm. Người dùng và khách vãng lai chỉ có quyền xem và tìm kiếm sản phẩm.
3. **Giỏ hàng & Đặt hàng (Cart & Checkout)**: Khách hàng có thể thêm sản phẩm vào giỏ hàng, điều chỉnh số lượng và thực hiện đặt hàng (thanh toán).
4. **Quản lý đơn hàng (Order Management)**: Khách hàng xem lịch sử mua hàng cá nhân. Admin xem danh sách tất cả các đơn hàng trong hệ thống và cập nhật trạng thái đơn hàng (Chờ xử lý, Đang giao, Đã giao, Hủy).

---

## PHẦN 2: PHÂN CÔNG VÀ ĐẶC TẢ CHI TIẾT CA KIỂM THỬ (TEST CASES)

> [!NOTE]
> Để thuận tiện cho việc chạy tự động, các bài kiểm thử dưới đây được thiết kế và thực thi trực tiếp bằng công cụ **pytest** thông qua file [test_app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py).

### 👥 THÀNH VIÊN 1: KIỂM THỬ VIÊN 1 (Chức năng: Xác thực - Authentication)

* **Chức năng đảm nhận**: Đăng ký, Đăng nhập & Đăng xuất tài khoản.
* **Phương pháp kiểm thử**: 
  * Kiểm thử hộp đen (Black-box testing) - Phân vùng tương đương (Equivalence Partitioning).
  * Kiểm thử chức năng (Functional Testing) giả lập HTTP Requests (POST/GET) bằng `pytest` client.
* **Mã nguồn kiểm thử tương ứng**: 
  * [test_register_success](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L29)
  * [test_register_duplicate](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L35)
  * [test_login_success](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L40)
  * [test_logout_success](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L44)
  * [test_login_wrong_message_intentional](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L66)

#### Danh sách ca kiểm thử:

| Mã ca (TC ID) | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_AUTH_01** | Đăng ký thành công tài khoản mới | Chưa đăng nhập, tài khoản chưa tồn tại | 1. Gửi request POST tới `/register`<br>2. Kiểm tra phản hồi | `username="khach_moi"`, `password="123"` | Trả về mã HTTP 200, hiển thị thông báo "Đăng ký thành công!" và tài khoản được tạo trong hệ thống. |
| **TC_AUTH_02** | Đăng ký thất bại do trùng tên tài khoản | Tài khoản `test_user` đã có sẵn | 1. Gửi request POST tới `/register` với tài khoản trùng lặp<br>2. Kiểm tra phản hồi | `username="test_user"`, `password="456"` | Hiển thị thông báo lỗi "Tên đăng nhập đã tồn tại!". |
| **TC_AUTH_03** | Đăng nhập thành công | Tài khoản đã được đăng ký trước | 1. Gửi request POST tới `/login`<br>2. Kiểm tra phản hồi | `username="admin"`, `password="123456"` | Chuyển hướng thành công và hiển thị thông báo chào mừng "Xin chào, admin!". |
| **TC_AUTH_04** | Đăng nhập thất bại do sai mật khẩu | Tài khoản đã được đăng ký trước | 1. Gửi request POST tới `/login` với mật khẩu sai<br>2. Kiểm tra phản hồi | `username="admin"`, `password="mat_khau_sai"` | Không đăng nhập được, hiển thị thông báo lỗi "Sai tên đăng nhập/mật khẩu!". |
| **TC_AUTH_05** | Đăng xuất thành công | Đang ở trạng thái đăng nhập | 1. Gửi request GET tới `/logout`<br>2. Kiểm tra phản hồi | Không có | Session bị xóa, hiển thị thông báo "Bạn đã đăng xuất!". |

#### Quy trình thực hiện bằng pytest:
1. Mở PowerShell trong thư mục dự án.
2. Thực thi lệnh chạy riêng các test case của chức năng Xác thực:
   ```powershell
   pytest -v test_app.py -k "register or login or logout"
   ```

---

### 👥 THÀNH VIÊN 2: KIỂM THỬ VIÊN 2 (Chức năng: Quản lý sản phẩm - Product Management)

* **Chức năng đảm nhận**: Thêm, Sửa, Xóa sản phẩm và Phân quyền truy cập đối với Admin/Khách.
* **Phương pháp kiểm thử**: 
  * Kiểm thử phân quyền (Role-based Authorization Testing).
  * Kiểm thử đơn vị & Kiểm thử tích hợp (Unit & Integration Testing).
* **Mã nguồn kiểm thử tương ứng**: 
  * [test_admin_edit_product](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L49)
  * [test_admin_delete_product](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L55)
  * [test_customer_access_denied](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L60)
  * [test_admin_add_wrong_quantity_intentional](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L70)

#### Danh sách ca kiểm thử:

| Mã ca (TC ID) | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_PROD_01** | Admin thêm sản phẩm thành công | Đăng nhập bằng tài khoản `admin` | 1. Gửi POST tới `/add`<br>2. Kiểm tra dữ liệu trong dict `products` | `ma_sp="SP02"`, `name="Ban phim co"`, `price=1000000`, `quantity=50` | Sản phẩm được lưu thành công vào hệ thống với số lượng tồn kho bằng 50. |
| **TC_PROD_02** | Admin sửa sản phẩm thành công | Đăng nhập bằng tài khoản `admin`, SP `SP01` đã tồn tại | 1. Gửi POST tới `/edit/SP01`<br>2. Kiểm tra thông tin sản phẩm | `name="Laptop Dell XPS"`, `price=20000000`, `quantity=15` | Dữ liệu sản phẩm `SP01` được cập nhật chính xác (Tên mới: Laptop Dell XPS, Giá mới: 20.000.000đ). |
| **TC_PROD_03** | Admin xóa sản phẩm thành công | Đăng nhập bằng tài khoản `admin`, SP `SP01` đã tồn tại | 1. Gửi POST tới `/delete/SP01`<br>2. Kiểm tra sự tồn tại của sản phẩm | Không có | Mã sản phẩm `SP01` không còn tồn tại trong hệ thống. |
| **TC_PROD_04** | Khách hàng bị từ chối truy cập chức năng Admin | Đăng nhập bằng tài khoản khách thường | 1. Gửi GET tới route admin `/add`<br>2. Kiểm tra phản hồi trả về | Không có | Trình duyệt chuyển hướng và hiển thị thông báo lỗi chặn quyền: "Chỉ admin mới có quyền!". |

#### Quy trình thực hiện bằng pytest:
1. Thực thi lệnh chạy riêng các test case của chức năng Quản lý sản phẩm:
   ```powershell
   pytest -v test_app.py -k "product or access_denied"
   ```

---

### 👥 THÀNH VIÊN 3: KIỂM THỬ VIÊN 3 (Chức năng: Giỏ hàng & Thanh toán - Cart & Checkout)

* **Chức năng đảm nhận**: Thêm sản phẩm vào giỏ hàng và thực hiện mua hàng (Thanh toán).
* **Phương pháp kiểm thử**: 
  * Kiểm thử luồng giao dịch (Transaction Flow Testing).
  * Kiểm thử tích hợp hệ thống (Integration Testing) – Đảm bảo thông tin giỏ hàng khớp với số lượng tồn kho khi thanh toán thành công.
* **Mã nguồn kiểm thử tương ứng**:
  * [test_shopping_wrong_inventory_intentional](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py#L75) (Bài test này giả lập luồng giỏ hàng -> thanh toán thành công).

#### Danh sách ca kiểm thử:

| Mã ca (TC ID) | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_CART_01** | Thêm sản phẩm vào giỏ hàng thành công | Đăng nhập là Khách hàng, SP `SP01` có sẵn | 1. Gửi POST tới `/add_to_cart/SP01`<br>2. Kiểm tra biến giỏ hàng trong session | `quantity=3` | Giỏ hàng của session có sản phẩm `SP01` với số lượng là 3. |
| **TC_CART_02** | Thanh toán đơn hàng thành công & Giảm tồn kho | Giỏ hàng đã có sản phẩm `SP01` (số lượng 3), tồn kho ban đầu là 10 | 1. Gửi POST tới `/checkout`<br>2. Kiểm tra tồn kho của sản phẩm `SP01` | `name="Nguyen Van A"`, `phone="012"`, `address="Ha Noi"`, `payment_method="COD"` | Đơn hàng được tạo thành công, tồn kho của `SP01` giảm từ 10 xuống còn 7 (`10 - 3 = 7`). Doanh thu tăng tương ứng. Giỏ hàng trống. |
| **TC_CART_03** | Chặn Admin thực hiện mua hàng | Đăng nhập bằng tài khoản `admin` | 1. Gửi POST tới `/add_to_cart/SP01`<br>2. Kiểm tra phản hồi | `quantity=1` | Hệ thống tự động chuyển hướng admin về trang chủ, không cho phép thêm vào giỏ hàng. |

#### Quy trình thực hiện bằng pytest:
1. Thực thi lệnh chạy riêng test case chức năng mua hàng:
   ```powershell
   pytest -v test_app.py -k "shopping or cart"
   ```

---

### 👥 THÀNH VIÊN 4: KIỂM THỬ VIÊN 4 (Chức năng: Quản lý đơn hàng - Order Management)

* **Chức năng đảm nhận**: Hiển thị đơn hàng cá nhân (Khách), hiển thị toàn bộ đơn hàng và cập nhật trạng thái đơn (Admin).
* **Phương pháp kiểm thử**: 
  * Kiểm thử phân quyền hiển thị dữ liệu (Data Isolation / Access Control Testing).
  * Kiểm thử tích hợp thay đổi trạng thái (State Transition Testing).
* **Mã nguồn kiểm thử tương ứng**: (Có thể viết thêm các bài test bổ sung trong file [test_app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py)).

#### Danh sách ca kiểm thử:

| Mã ca (TC ID) | Tên ca kiểm thử | Điều kiện đầu vào | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_ORDER_01** | Khách hàng chỉ xem được đơn hàng của chính mình | Tài khoản khách hàng A đã đặt 1 đơn hàng | 1. Đăng nhập với tài khoản khách hàng B<br>2. Gửi GET tới `/orders`<br>3. Kiểm tra danh sách hiển thị | Tài khoản khách hàng B | Không xuất hiện đơn hàng của khách hàng A trên giao diện của B. |
| **TC_ORDER_02** | Admin xem được toàn bộ đơn hàng của tất cả khách hàng | Hệ thống đã có các đơn hàng do nhiều khách đặt | 1. Đăng nhập với tài khoản `admin`<br>2. Gửi GET tới `/orders`<br>3. Kiểm tra danh sách hiển thị | Tài khoản admin | Danh sách hiển thị đầy đủ thông tin tất cả các đơn hàng của khách hàng trong hệ thống. |
| **TC_ORDER_03** | Admin cập nhật trạng thái đơn hàng thành công | Đăng nhập `admin`, có đơn hàng mã `DH001` đang ở trạng thái 'Chờ xử lý' | 1. Gửi POST tới `/update_order/DH001`<br>2. Kiểm tra trạng thái đơn hàng | `status="Đang giao"` | Đơn hàng `DH001` đổi trạng thái thành "Đang giao" thành công. |

#### Quy trình thực hiện bằng pytest:
1. Viết các test case kiểm tra việc lấy danh sách đơn và cập nhật trạng thái đơn hàng.
2. Thực thi kiểm thử:
   ```powershell
   pytest -v test_app.py -k "order"
   ```

---

## PHẦN 3: HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY KIỂM THỬ BẰNG CÔNG CỤ (PYTEST)

### 1. Chuẩn bị môi trường
Cài đặt các thư viện cần thiết từ file [requirements.txt](file:///c:/Users/noqok/Documents/Project/pytestdemo/requirements.txt):
```powershell
pip install -r requirements.txt
```

### 2. Chạy toàn bộ các bài kiểm thử
Thực hiện chạy toàn bộ test case có sẵn trong file [test_app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/test_app.py) bằng lệnh:
```powershell
pytest -v test_app.py
```

### 3. Đọc hiểu kết quả báo cáo lỗi từ pytest
* Các ca kiểm thử hiển thị `PASSED` màu xanh nghĩa là tính năng đang hoạt động đúng như đặc tả.
* Các ca kiểm thử hiển thị `FAILED` màu đỏ đi kèm mô tả lỗi chỉ ra sự khác biệt giữa **kết quả thực tế (Actual)** và **kết quả mong đợi (Expected)**. Điều này giúp kiểm thử viên định vị chính xác vị trí lỗi mã nguồn trong [app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/app.py) để tiến hành sửa đổi (Bug Fixing).
