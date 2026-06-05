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