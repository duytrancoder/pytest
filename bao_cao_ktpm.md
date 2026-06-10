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

### 1.3. Mức độ và Phương pháp kiểm thử nhóm sử dụng

Nhóm áp dụng mức độ kiểm thử đơn vị kết hợp các kỹ thuật thiết kế ca kiểm thử hộp đen và hộp trắng:

#### 1.3.1. Mức độ kiểm thử: Kiểm thử đơn vị (Unit Testing)
* **Khái niệm**: Đây là mức độ kiểm thử trọng tâm của nhóm. Nhóm thực hiện kiểm thử độc lập cho từng hàm xử lý (view function) như `register()`, `login()`, `add_product()`, `update_order()`,... trong file [app.py](file:///c:/Users/noqok/Documents/Project/pytestdemo/app.py).
* **Đặc thù**: Sử dụng `app.test_request_context(...)` để giả lập ngữ cảnh request và session trong bộ nhớ, cho phép gọi trực tiếp và kiểm tra tính toán của riêng từng hàm xử lý mà không cần thông qua hệ thống định tuyến (route) hay truyền dữ liệu qua network (không qua Test Client).

#### 1.3.2. Phương pháp thiết kế ca kiểm thử hộp đen (Black-box Testing)
Kiểm thử dựa trên đặc tả yêu cầu nghiệp vụ để xác nhận đầu vào và đầu ra của hàm xử lý hoạt động chính xác. Các kỹ thuật cụ thể gồm:
* **Phân vùng tương đương (Equivalence Partitioning)**: Chia dữ liệu đầu vào thành các lớp tương đương hợp lệ và không hợp lệ để giảm thiểu số lượng test case cần chạy.
  * *Ví dụ*: Kiểm thử đăng ký với tên tài khoản mới (hợp lệ) và tên tài khoản đã tồn tại (không hợp lệ).
* **Phân tích giá trị biên (Boundary Value Analysis)**: Tập trung vào các giá trị biên như số lượng tồn kho sản phẩm bằng `0` (hết hàng) hoặc số lượng mua lớn hơn tồn kho thực tế.

#### 1.3.3. Phương pháp thiết kế ca kiểm thử hộp trắng (White-box Testing)
Kiểm thử dựa trên mã nguồn nội bộ của ứng dụng để đảm bảo độ bao phủ lệnh và kiểm tra logic phân quyền. Các kỹ thuật cụ thể gồm:
* **Kiểm thử đường dẫn/nhánh (Branch Coverage)**: Thiết kế các ca kiểm thử đi qua tất cả các nhánh rẽ nhánh điều kiện `if/else` của hàm (ví dụ: các nhánh xử lý đúng/sai mật khẩu trong hàm `login()`).
* **Kiểm thử phân quyền truy cập (Access Control Testing)**: Kiểm tra trực tiếp cơ chế hoạt động của các decorator kiểm soát quyền hạn như `@login_required` và `@admin_required` bằng cách giả lập session người dùng khác nhau và gọi trực tiếp các hàm view bị giới hạn.

#### 1.3.4. Kiểm thử hồi quy (Regression Testing)
Toàn bộ bộ kiểm thử đơn vị được tự động hóa chạy lại qua `pytest` sau mỗi lần sửa đổi mã nguồn hoặc cập nhật cấu trúc ứng dụng nhằm đảm bảo các sửa đổi không gây ra lỗi (side-effects) lên các tính năng đã hoạt động ổn định.

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

### Tổng hợp kết quả:

| Thành viên | Chức năng | Số ca kiểm thử | Passed | Failed | Error |
|:---:|:---|:---:|:---:|:---:|:---:|
| Thành viên 1 | Xác thực người dùng | 5 | 5 | 0 | 0 |
| Thành viên 2 | Quản lý sản phẩm | 4 | 4 | 0 | 0 |
| Thành viên 3 | Giỏ hàng & Thanh toán | 3 | 3 | 0 | 0 |
| Thành viên 4 | Quản lý đơn hàng | 3 | 3 | 0 | 0 |
| Thành viên 5 | Tìm kiếm & Lọc sản phẩm | 4 | 4 | 0 | 0 |
| **Tổng cộng** | | **19** | **19** | **0** | **0** |

### Nhận xét:

- Bộ kiểm thử tự động gồm **19 ca** đã được thực thi hoàn tất. Kết quả ghi nhận chính xác: **19 PASSED**, **0 FAILED**, và **0 ERROR**.
- Các ca kiểm thử của **Thành viên 4** đã được viết code tự động đầy đủ và đều **PASSED**, đảm bảo phân isolation dữ liệu đơn hàng giữa các khách hàng hoạt động bảo mật, và admin có thể xem toàn bộ đơn hàng cũng như thay đổi trạng thái thành công.
- **Thành viên 5** bổ sung chức năng **Tìm kiếm & Lọc sản phẩm nâng cao** (`/search`) trả về JSON, với 4 ca kiểm thử đều **PASSED** — bao phủ lọc từ khóa, khoảng giá, tình trạng tồn kho và kiểm tra phân quyền truy cập route.
- Mọi ca kiểm thử đều hoạt động đúng đắn và chính xác theo đặc tả của hệ thống.
- Fixture của pytest giúp **cách ly môi trường** giữa các test case, đảm bảo tính độc lập và tính tái lập của bộ kiểm thử. Kỹ thuật **fixture kế thừa** (`search_client` kế thừa `client`) được Thành viên 5 áp dụng để mở rộng môi trường kiểm thử mà không trùng lặp code.

---

## KẾT LUẬN

Qua quá trình tìm hiểu lý thuyết và ứng dụng thực tiễn công cụ **pytest** để thực hiện kiểm thử tự động cho **Hệ thống Quản lý Bán hàng**, nhóm chúng em đã thu hoạch được nhiều kết quả quan trọng và rút ra những kết luận sau:

### 1. Kết quả đạt được của đề tài
* **Về mặt lý thuyết:** Nhóm đã nắm vững các kiến thức cơ bản về quy trình kiểm thử phần mềm, sự khác biệt giữa các phương pháp kiểm thử (Hộp đen, Hộp trắng, Kiểm thử hồi quy) cũng như ý nghĩa của các cấp độ kiểm thử.
* **Về mặt công cụ:** Hiểu rõ cấu trúc và cơ chế hoạt động của framework pytest bao gồm: cách tổ chức các file test, viết các hàm kiểm thử độc lập, thiết lập môi trường bằng Fixture và sử dụng assert để đối chiếu dữ liệu.
* **Về mặt thực hành:** Thiết kế thành công bộ dữ liệu gồm **19 ca kiểm thử tự động** bao phủ các tính năng cốt lõi của website. Bộ kiểm thử đã chạy hoàn tất ổn định và đạt tỷ lệ vượt qua tuyệt đối 100% Passed (19/19), giúp cả nhóm hiểu sâu quy trình quản lý chất lượng phần mềm trong thực tế.

### 2. Ưu điểm của phương pháp kiểm thử tự động bằng pytest
* **Tự động hóa & Tiết kiệm thời gian:** Chỉ với một câu lệnh đơn giản trên terminal, toàn bộ các chức năng phức tạp của ứng dụng được kiểm thử hoàn tất trong chưa đầy 1 giây. Điều này vô cùng hiệu quả so với kiểm thử thủ công (manual testing).
* **Độ tin cậy cao:** Giúp phát hiện nhanh các lỗi hồi quy khi mã nguồn ứng dụng thay đổi, đảm bảo các chức năng cũ không bị ảnh hưởng khi thêm mới tính năng.
* **Báo cáo trực quan:** Pytest cung cấp thông tin traceback chi tiết, chỉ rõ vị trí và nguyên nhân gây lỗi, giúp lập trình viên sửa lỗi nhanh chóng.

### 3. Hạn chế và Hướng phát triển
* **Hạn chế:** Bộ kiểm thử hiện tại chủ yếu giả lập HTTP requests/responses (tầng backend/integration). Chưa kiểm thử trực tiếp các tương tác phức tạp trên giao diện người dùng (UI/UX) như hiệu ứng Javascript, hoạt động click chuột của khách hàng thực tế.
* **Hướng phát triển:** Kết hợp **pytest** với các công cụ kiểm thử giao diện như **Selenium WebDriver** hoặc **Playwright** để xây dựng bộ kiểm thử End-to-End (E2E) toàn diện cho cả giao diện và logic hệ thống trong tương lai.
