import pytest
from app import app, users, products, sales_stats, orders

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    users.clear()
    users["admin"] = {"password": "123456", "role": "admin"}
    
    products.clear()
    products["SP01"] = {"name": "Laptop Dell", "price": 15000000, "quantity": 10}
    
    sales_stats["total_revenue"] = 0
    orders.clear()

    with app.test_client() as client:
        yield client

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_register_success(client):
    res = client.post('/register', data={'username': 'khach_moi', 'password': '123'}, follow_redirects=True)
    assert res.status_code == 200
    assert "Đăng ký thành công!" in res.get_data(as_text=True)
    assert "khach_moi" in users

def test_register_duplicate(client):
    client.post('/register', data={'username': 'test_user', 'password': '123'})
    res = client.post('/register', data={'username': 'test_user', 'password': '456'}, follow_redirects=True)
    assert "Tên đăng nhập đã tồn tại!" in res.get_data(as_text=True)

def test_login_success(client):
    res = login(client, 'admin', '123456')
    assert "Xin chào, admin!" in res.get_data(as_text=True)

def test_logout_success(client):
    login(client, 'admin', '123456')
    res = logout(client)
    assert "Bạn đã đăng xuất!" in res.get_data(as_text=True)

def test_admin_edit_product(client):
    login(client, 'admin', '123456')
    client.post('/edit/SP01', data={'name': 'Laptop Dell XPS', 'price': 20000000, 'quantity': 15}, follow_redirects=True)
    assert products["SP01"]["name"] == "Laptop Dell XPS"
    assert products["SP01"]["price"] == 20000000

def test_admin_delete_product(client):
    login(client, 'admin', '123456')
    client.post('/delete/SP01', follow_redirects=True)
    # Cố tình gây lỗi FAILED (AssertionError)
    assert "SP01" in products

def test_customer_access_denied(client):
    client.post('/register', data={'username': 'khach', 'password': '123'})
    login(client, 'khach', '123')
    res = client.get('/add', follow_redirects=True)
    assert "Chỉ admin mới có quyền!" in res.get_data(as_text=True)

def test_login_wrong_message_intentional(client):
    res = login(client, 'admin', 'mat_khau_sai')
    assert "Sai tên đăng nhập/mật khẩu!" in res.get_data(as_text=True)

@pytest.fixture
def admin_setup_error():
    # Fixture ném ra ngoại lệ để tạo lỗi ERROR trong giai đoạn Setup của pytest
    raise RuntimeError("Lỗi kết nối cơ sở dữ liệu admin (Lỗi thiết lập Fixture)!")

def test_admin_add_wrong_quantity_intentional(client, admin_setup_error):
    login(client, 'admin', '123456')
    client.post('/add', data={'ma_sp': 'SP02', 'name': 'Ban phim co', 'price': 1000000, 'quantity': 5}, follow_redirects=True)
    assert products["SP02"]["quantity"] == 5

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

# ════════════════════════════════════════════════════════════════════════════════
# Thành viên 5 — Kiểm thử chức năng Tìm kiếm & Lọc Sản phẩm nâng cao (/search)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def search_client(client):
    """
    Mở rộng fixture `client`: thêm sẵn 3 sản phẩm đa dạng
    để phục vụ các ca kiểm thử tìm kiếm/lọc.
    """
    products["SP02"] = {"name": "Chuột Logitech", "price": 300000,   "quantity": 50}
    products["SP03"] = {"name": "Bàn phím cơ",   "price": 800000,   "quantity": 0}   # hết hàng
    products["SP04"] = {"name": "Màn hình Dell",  "price": 5000000,  "quantity": 5}
    login(client, "admin", "123456")
    return client

def test_search_by_keyword(search_client):
    """
    TC_SEARCH_01 — Tìm kiếm theo từ khóa tên sản phẩm.
    Đầu vào : q=dell
    Mong đợi: trả về 2 SP chứa 'dell' (Laptop Dell + Màn hình Dell), count == 2
    """
    res = search_client.get("/search?q=dell")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 2
    names = [p["name"] for p in data["products"]]
    assert "Laptop Dell"  in names
    assert "Màn hình Dell" in names

def test_search_filter_by_price_range(search_client):
    """
    TC_SEARCH_02 — Lọc sản phẩm theo khoảng giá.
    Đầu vào : min_price=200000, max_price=1000000
    Mong đợi: chỉ trả về SP trong khoảng giá đó (Chuột Logitech 300k + Bàn phím cơ 800k), count == 2
    """
    res = search_client.get("/search?min_price=200000&max_price=1000000")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 2
    for p in data["products"]:
        assert 200000 <= p["price"] <= 1000000

def test_search_filter_in_stock_only(search_client):
    """
    TC_SEARCH_03 — Lọc chỉ sản phẩm còn hàng (in_stock=1).
    Đầu vào : in_stock=1
    Mong đợi: 'Bàn phím cơ' (quantity=0) bị loại, count == 3
    """
    res = search_client.get("/search?in_stock=1")
    assert res.status_code == 200
    data = res.get_json()
    names = [p["name"] for p in data["products"]]
    assert "Bàn phím cơ" not in names
    assert data["count"] == 3

def test_search_unauthenticated_blocked(client):
    """
    TC_SEARCH_04 — Người dùng chưa đăng nhập bị chặn truy cập /search.
    Đầu vào : Không có session, GET /search
    Mong đợi: Chuyển hướng về trang đăng nhập (không trả về JSON)
    """
    res = client.get("/search", follow_redirects=True)
    assert res.status_code == 200
    assert "Vui lòng đăng nhập!" in res.get_data(as_text=True)