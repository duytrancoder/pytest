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
    assert "SP01" not in products

def test_customer_access_denied(client):
    client.post('/register', data={'username': 'khach', 'password': '123'})
    login(client, 'khach', '123')
    res = client.get('/add', follow_redirects=True)
    assert "Chỉ admin mới có quyền!" in res.get_data(as_text=True)

def test_login_wrong_message_intentional(client):
    res = login(client, 'admin', 'mat_khau_sai')
    assert "Sai tên đăng nhập/mật khẩu!" in res.get_data(as_text=True)

def test_admin_add_wrong_quantity_intentional(client):
    login(client, 'admin', '123456')
    client.post('/add', data={'ma_sp': 'SP02', 'name': 'Ban phim co', 'price': 1000000, 'quantity': 5}, follow_redirects=True)
    assert products["SP02"]["quantity"] == 5

def test_shopping_wrong_inventory_intentional(client):
    client.post('/register', data={'username': 'buyer', 'password': '123'})
    login(client, 'buyer', '123')
    client.post('/add_to_cart/SP01', data={'quantity': 3}, follow_redirects=True)
    client.post('/checkout', data={'name': 'A', 'phone': '012', 'address': 'HN', 'payment_method': 'COD'}, follow_redirects=True)
    assert products["SP01"]["quantity"] == 7