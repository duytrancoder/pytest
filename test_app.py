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
    res = client.post('/register', data={
        'username': 'khach_moi',
        'password': '123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert "Đăng ký thành công!" in res.get_data(as_text=True)
    assert "khach_moi" in users

def test_register_duplicate(client):
    client.post('/register', data={'username': 'test_user', 'password': '123'})
    res = client.post('/register', data={'username': 'test_user', 'password': '456'}, follow_redirects=True)
    assert res.status_code == 200
    assert "Tên đăng nhập đã tồn tại!" in res.get_data(as_text=True)

def test_login_success(client):
    res = login(client, 'admin', '123456')
    assert res.status_code == 200
    assert "Xin chào, admin!" in res.get_data(as_text=True)

def test_login_fail(client):
    res = login(client, 'admin', 'mat_khau_sai')
    assert res.status_code == 200
    assert "Sai tên đăng nhập/mật khẩu!" in res.get_data(as_text=True)

def test_logout_success(client):
    login(client, 'admin', '123456')
    res = logout(client)
    assert res.status_code == 200
    assert "Bạn đã đăng xuất!" in res.get_data(as_text=True)
    with client.session_transaction() as sess:
        assert 'username' not in sess

def test_admin_add_product(client):
    login(client, 'admin', '123456')
    res = client.post('/add', data={
        'ma_sp': 'SP02',
        'name': 'Ban phim co',
        'price': 1000000,
        'quantity': 5
    }, follow_redirects=True)
    assert res.status_code == 200
    assert "SP02" in products
    assert products["SP02"]["quantity"] == 5

def test_admin_edit_product(client):
    login(client, 'admin', '123456')
    res = client.post('/edit/SP01', data={
        'name': 'Laptop Dell XPS',
        'price': 20000000,
        'quantity': 15
    }, follow_redirects=True)
    assert res.status_code == 200
    assert products["SP01"]["name"] == "Laptop Dell XPS"
    assert products["SP01"]["price"] == 20000000
    assert products["SP01"]["quantity"] == 15

def test_admin_delete_product(client):
    login(client, 'admin', '123456')
    res = client.post('/delete/SP01', follow_redirects=True)
    assert res.status_code == 200
    assert "SP01" not in products

def test_customer_access_denied(client):
    client.post('/register', data={'username': 'khach', 'password': '123'})
    login(client, 'khach', '123')
    res = client.get('/add', follow_redirects=True)
    assert res.status_code == 200
    assert "Chỉ admin mới có quyền!" in res.get_data(as_text=True)

def test_shopping_and_checkout_flow(client):
    client.post('/register', data={'username': 'buyer', 'password': '123'})
    login(client, 'buyer', '123')
    
    client.post('/add_to_cart/SP01', data={'quantity': 3}, follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['cart']['SP01'] == 3
        
    client.post('/checkout', data={
        'name': 'Nguyen Van A',
        'phone': '0123456789',
        'address': 'Ha Noi',
        'payment_method': 'COD'
    }, follow_redirects=True)
    
    assert products["SP01"]["quantity"] == 7
    assert sales_stats["total_revenue"] == 45000000
    assert len(orders) == 1
    assert orders[0]['total'] == 45000000