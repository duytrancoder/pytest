import pytest
from flask import session, get_flashed_messages, url_for
from werkzeug.security import generate_password_hash
from app import (
    app,
    users,
    products,
    sales_stats,
    orders,
    register,
    login as app_login,
    logout as app_logout,
    add_product,
    edit_product,
    delete_product,
    add_to_cart,
    checkout,
    order_history,
    update_order,
    search_products,
)

# Reset global state tự động trước mỗi test
@pytest.fixture(autouse=True)
def reset_globals():
    users.clear()
    users["admin"] = {"password": generate_password_hash("123456"), "role": "admin"}
    products.clear()
    sales_stats["total_revenue"] = 0
    orders.clear()
    yield

# Fixture setup sản phẩm phục vụ tìm kiếm nâng cao
@pytest.fixture
def search_setup():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
    products["SP02"] = {"name": "Chuột Logitech", "price": 300000,   "quantity": 50}
    products["SP03"] = {"name": "Bàn phím cơ",   "price": 800000,   "quantity": 0}   # hết hàng
    products["SP04"] = {"name": "Màn hình Dell",  "price": 5000000,  "quantity": 5}

# ==========================================
# 1. Xác thực & Phân quyền (Authentication)
# ==========================================

def test_register_success():
    with app.test_request_context('/register', method='POST', data={'username': 'khach_moi', 'password': '123'}):
        res = register()
        assert res.status_code == 302
        assert res.headers.get('Location') == '/login'
        assert any("Đăng ký thành công!" in m[1] for m in get_flashed_messages(with_categories=True))
        assert "khach_moi" in users
        assert users["khach_moi"]["role"] == "customer"

def test_register_duplicate():
    users["test_user"] = {"password": generate_password_hash("123"), "role": "customer"}
    with app.test_request_context('/register', method='POST', data={'username': 'test_user', 'password': '456'}):
        res = register()
        assert isinstance(res, str)  # Trả về HTML
        assert any("Tên đăng nhập đã tồn tại!" in m[1] for m in get_flashed_messages(with_categories=True))

def test_login_success():
    with app.test_request_context('/login', method='POST', data={'username': 'admin', 'password': '123456'}):
        res = app_login()
        assert res.status_code == 302
        assert res.headers.get('Location') == '/'
        assert session.get('username') == 'admin'
        assert session.get('role') == 'admin'
        assert any("Xin chào, admin!" in m[1] for m in get_flashed_messages(with_categories=True))

def test_logout_success():
    with app.test_request_context('/logout'):
        session['username'] = 'admin'
        session['role'] = 'admin'
        res = app_logout()
        assert res.status_code == 302
        assert res.headers.get('Location') == '/login'
        assert 'username' not in session
        assert any("Bạn đã đăng xuất!" in m[1] for m in get_flashed_messages(with_categories=True))

def test_login_wrong_password_fails():
    with app.test_request_context('/login', method='POST', data={'username': 'admin', 'password': 'mat_khau_sai'}):
        res = app_login()
        assert isinstance(res, str)
        assert any("Sai tên đăng nhập/mật khẩu!" in m[1] for m in get_flashed_messages(with_categories=True))
        assert 'username' not in session

# ==========================================
# 2. Quản lý sản phẩm (Product Management)
# ==========================================

def test_admin_edit_product():
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

def test_admin_delete_product():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
    with app.test_request_context('/delete/SP01', method='POST'):
        session['username'] = 'admin'
        session['role'] = 'admin'
        res = delete_product('SP01')
        assert res.status_code == 302
        assert res.headers.get('Location') == '/'
        assert "SP01" not in products

def test_customer_access_denied():
    with app.test_request_context('/add', method='GET'):
        session['username'] = 'khach'
        session['role'] = 'customer'
        res = add_product()
        assert res.status_code == 302
        assert res.headers.get('Location') == '/'
        assert any("Chỉ admin mới có quyền!" in m[1] for m in get_flashed_messages(with_categories=True))

def test_admin_add_product_success():
    with app.test_request_context('/add', method='POST', data={'ma_sp': 'SP02', 'name': 'Ban phim co', 'price': 1000000, 'quantity': 5}):
        session['username'] = 'admin'
        session['role'] = 'admin'
        res = add_product()
        assert res.status_code == 302
        assert res.headers.get('Location') == '/'
        assert products["SP02"]["quantity"] == 5

def test_admin_add_duplicate_product_fails():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
    with app.test_request_context('/add', method='POST', data={'ma_sp': 'SP01', 'name': 'Laptop Mới', 'price': 20000000, 'quantity': 5}):
        session['username'] = 'admin'
        session['role'] = 'admin'
        res = add_product()
        assert res.status_code == 302
        assert any("Mã SP đã tồn tại!" in m[1] for m in get_flashed_messages(with_categories=True))
        assert products["SP01"]["name"] == "Laptop Dell"  # Không bị thay đổi

# ==========================================
# 3. Giỏ hàng & Thanh toán (Cart & Checkout)
# ==========================================

def test_cart_add_success():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
    with app.test_request_context('/add_to_cart/SP01', method='POST', data={'quantity': 3}):
        session['username'] = 'buyer'
        session['role'] = 'customer'
        res = add_to_cart('SP01')
        assert res.status_code == 302
        assert res.headers.get('Location') == '/'
        assert any("Đã thêm 3 sản phẩm vào giỏ!" in m[1] for m in get_flashed_messages(with_categories=True))
        assert session.get('cart', {}).get('SP01') == 3

def test_shopping_checkout_success():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
    with app.test_request_context('/checkout', method='POST', data={'name': 'A', 'phone': '012', 'address': 'HN', 'payment_method': 'COD'}):
        session['username'] = 'buyer'
        session['role'] = 'customer'
        session['cart'] = {'SP01': 3}
        res = checkout()
        assert res.status_code == 302
        assert products["SP01"]["quantity"] == 7
        assert sales_stats["total_revenue"] == 45000000
        assert 'cart' not in session
        assert len(orders) == 1
        assert orders[0]['status'] == 'Chờ xử lý'

def test_admin_add_to_cart_blocked():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
    with app.test_request_context('/add_to_cart/SP01', method='POST', data={'quantity': 1}):
        session['username'] = 'admin'
        session['role'] = 'admin'
        res = add_to_cart('SP01')
        assert res.status_code == 302
        assert res.headers.get('Location') == '/'
        assert any("Admin không thể mua hàng!" in m[1] for m in get_flashed_messages(with_categories=True))
        assert 'cart' not in session or 'SP01' not in session['cart']

def test_shopping_exceeds_inventory_fails():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 5}
    with app.test_request_context('/add_to_cart/SP01', method='POST', data={'quantity': 10}):
        session['username'] = 'buyer'
        session['role'] = 'customer'
        res = add_to_cart('SP01')
        assert res.status_code == 302
        assert any("Không thể thêm" in m[1] for m in get_flashed_messages(with_categories=True))
        assert 'cart' not in session or session['cart'].get('SP01', 0) == 0

def test_add_to_cart_cumulative_exceeds_inventory():
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 5}
    with app.test_request_context('/add_to_cart/SP01', method='POST', data={'quantity': 3}):
        session['username'] = 'buyer'
        session['role'] = 'customer'
        session['cart'] = {'SP01': 3} # Giả sử đã có 3 cái trong giỏ
        res = add_to_cart('SP01')
        assert res.status_code == 302
        assert any("Không thể thêm" in m[1] for m in get_flashed_messages(with_categories=True))
        assert session['cart']['SP01'] == 3 # Số lượng trong giỏ không tăng

# ==========================================
# 4. Quản lý đơn hàng (Order Management)
# ==========================================

def test_order_customer_isolation():
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

def test_order_admin_view_all():
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

def test_order_admin_update_status():
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

# ==========================================
# 5. Tìm kiếm & Lọc nâng cao (Search)
# ==========================================

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

def test_search_no_results(search_setup):
    with app.test_request_context('/search?q=khongtontai'):
        session['username'] = 'admin'
        session['role'] = 'admin'
        res = search_products()
        assert res.status_code == 200
        data = res.get_json()
        assert data["count"] == 0
        assert len(data["products"]) == 0

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

def test_search_unauthenticated_blocked(search_setup):
    with app.test_request_context('/search'):
        # Không truyền session, để login_required kích hoạt
        res = search_products()
        assert res.status_code == 302
        assert res.headers.get('Location') == '/login'
        assert any("Vui lòng đăng nhập!" in m[1] for m in get_flashed_messages(with_categories=True))