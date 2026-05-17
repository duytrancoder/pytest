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

def test_register_and_login_success(client):
    res_reg = client.post('/register', data={
        'username': 'khach_test',
        'password': '123'
    }, follow_redirects=True)
    assert res_reg.status_code == 200
    assert "Đăng ký thành công!" in res_reg.get_data(as_text=True)
    
    res_login = login(client, 'khach_test', '123')
    assert res_login.status_code == 200
    assert "Xin chào, khach_test!" in res_login.get_data(as_text=True)

def test_login_fail(client):
    response = login(client, 'admin', 'sai_pass')
    assert response.status_code == 200
    assert "Sai tên đăng nhập/mật khẩu!" in response.get_data(as_text=True)

def test_admin_add_product(client):
    login(client, 'admin', '123456')
    response = client.post('/add', data={
        'ma_sp': 'SP02',
        'name': 'Ban phim co',
        'price': 1000000,
        'quantity': 5
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert "SP02" in products
    assert products["SP02"]["name"] == "Ban phim co"

def test_customer_cannot_add_product(client):
    client.post('/register', data={'username': 'khach', 'password': '123'})
    login(client, 'khach', '123')
    
    response = client.get('/add', follow_redirects=True)
    
    assert response.status_code == 200
    assert "Chỉ admin mới có quyền!" in response.get_data(as_text=True)

def test_shopping_flow(client):
    client.post('/register', data={'username': 'buyer', 'password': '123'})
    login(client, 'buyer', '123')
    
    response_add = client.post('/add_to_cart/SP01', data={'quantity': 2}, follow_redirects=True)
    assert response_add.status_code == 200
    
    with client.session_transaction() as sess:
        assert 'cart' in sess
        assert sess['cart']['SP01'] == 2
        
    response_checkout = client.post('/checkout', data={
        'name': 'Nguyen Van A',
        'phone': '0123456789',
        'address': 'Ha Noi',
        'payment_method': 'COD'
    }, follow_redirects=True)
    
    assert products["SP01"]["quantity"] == 8
    assert sales_stats["total_revenue"] == 30000000
    assert len(orders) == 1
    assert orders[0]['customer_name'] == 'Nguyen Van A'
    assert orders[0]['total'] == 30000000