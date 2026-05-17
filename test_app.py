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
    response = client.post('/register', data={
        'username': 'khach_test',
        'password': '123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Vui l\xc3\xb2ng \xc4\x91\xc4\x83ng nh\xc3\xa2p" in response.data
    assert "khach_test" in users
    assert users["khach_test"]["role"] == "customer"

def test_login_success(client):
    response = login(client, 'admin', '123456')
    assert response.status_code == 200
    assert b"Xin ch\xc3\xa0o, admin" in response.data

def test_login_fail(client):
    response = login(client, 'admin', 'sai_pass')
    assert response.status_code == 200
    assert b"Sai t\xc3\xaan \xc4\x91\xc4\x83ng nh\xc3\xa2p ho\xe1\xba\xb7c m\xe1\xba\xadt kh\xe1\xba\xa9u" in response.data

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
    assert b"Ch\xe1\xbb\x89 admin" in response.data

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