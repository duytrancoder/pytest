from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import datetime

app = Flask(__name__)
app.secret_key = "khoa_bi_mat_cho_flash_message_va_session"

users = {"admin": {"password": "123456", "role": "admin"}}
products = {
    "SP01": {"name": "Laptop Dell", "price": 15000000, "quantity": 10},
    "SP02": {"name": "Chuột Logitech", "price": 300000, "quantity": 50}
}
sales_stats = {"total_revenue": 0}
orders = [] 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Vui lòng đăng nhập!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("Chỉ admin mới có quyền!", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u, p = request.form['username'].strip(), request.form['password'].strip()
        if u in users: flash("Tên đăng nhập đã tồn tại!", "danger")
        else:
            users[u] = {"password": p, "role": "customer"}
            flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
            return redirect(url_for('login'))
    return render_template('auth.html', action="register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'].strip(), request.form['password'].strip()
        if u in users and users[u]['password'] == p:
            session['username'], session['role'] = u, users[u]['role']
            flash(f"Xin chào, {u}!", "success")
            return redirect(url_for('index'))
        flash("Sai tên đăng nhập/mật khẩu!", "danger")
    return render_template('auth.html', action="login")

@app.route('/logout')
def logout():
    session.clear()
    flash("Bạn đã đăng xuất!", "info")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    q = request.args.get('search', '').lower()
    filtered = {ma: info for ma, info in products.items() if q in ma.lower() or q in info['name'].lower()}
    stats = {"items": len(products), "stock": sum(p['quantity'] for p in products.values()), "revenue": sales_stats["total_revenue"]}
    return render_template('products.html', view="list", products=filtered, stats=stats)

@app.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        ma = request.form['ma_sp'].strip().upper()
        if ma in products:
            flash("Mã SP đã tồn tại!", "danger")
            return redirect(url_for('add_product'))
        products[ma] = {"name": request.form['name'], "price": float(request.form['price']), "quantity": int(request.form['quantity'])}
        flash("Thêm thành công!", "success")
        return redirect(url_for('index'))
    return render_template('products.html', view="form", action="add", title="Thêm Sản Phẩm")

@app.route('/edit/<ma_sp>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(ma_sp):
    if ma_sp not in products: return redirect(url_for('index'))
    if request.method == 'POST':
        products[ma_sp].update({"name": request.form['name'], "price": float(request.form['price']), "quantity": int(request.form['quantity'])})
        flash("Sửa thành công!", "success")
        return redirect(url_for('index'))
    return render_template('products.html', view="form", action="edit", title="Sửa Sản Phẩm", sp=products[ma_sp], ma=ma_sp)

@app.route('/delete/<ma_sp>', methods=['POST'])
@login_required
@admin_required
def delete_product(ma_sp):
    products.pop(ma_sp, None)
    flash("Đã xóa sản phẩm!", "success")
    return redirect(url_for('index'))

@app.route('/add_to_cart/<ma_sp>', methods=['POST'])
@login_required
def add_to_cart(ma_sp):
    if session.get('role') == 'admin': return redirect(url_for('index'))
    qty = int(request.form.get('quantity', 1))
    if ma_sp in products and products[ma_sp]['quantity'] >= qty:
        cart = session.get('cart', {})
        cart[ma_sp] = cart.get(ma_sp, 0) + qty
        session['cart'] = cart
        flash(f"Đã thêm {qty} sản phẩm vào giỏ!", "success")
    return redirect(url_for('index'))

def get_cart():
    items, total = [], 0
    for ma_sp, qty in session.get('cart', {}).items():
        if ma_sp in products:
            t = products[ma_sp]['price'] * qty
            total += t
            items.append({'ma_sp': ma_sp, 'name': products[ma_sp]['name'], 'price': products[ma_sp]['price'], 'qty': qty, 'thanh_tien': t})
    return items, total

@app.route('/cart')
@login_required
def view_cart():
    if session.get('role') == 'admin': return redirect(url_for('index'))
    items, total = get_cart()
    return render_template('transactions.html', view="cart_checkout", cart_items=items, total_bill=total, show_checkout=False)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if session.get('role') == 'admin': return redirect(url_for('index'))
    items, total = get_cart()
    
    if request.method == 'POST' and items:
        order_items = []
        for ma_sp, qty in session['cart'].items():
            if ma_sp in products and products[ma_sp]['quantity'] >= qty:
                products[ma_sp]['quantity'] -= qty
                order_items.append({'name': products[ma_sp]['name'], 'qty': qty})
        
        sales_stats["total_revenue"] += total
        ma_don = f"DH{len(orders)+1:03d}"
        orders.append({
            'order_id': ma_don, 'username': session['username'],
            'customer_name': request.form.get('name'), 'phone': request.form.get('phone'),
            'address': request.form.get('address'), 'payment_method': request.form.get('payment_method'),
            'items': order_items, 'total': total, 'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), 'status': 'Chờ xử lý'
        })
        session.pop('cart', None)
        flash(f"Thanh toán thành công! Mã đơn của bạn là {ma_don}", "success")
        return redirect(url_for('order_history'))
        
    return render_template('transactions.html', view="cart_checkout", cart_items=items, total_bill=total, show_checkout=True)

@app.route('/orders')
@login_required
def order_history():
    ds = reversed(orders) if session.get('role') == 'admin' else reversed([o for o in orders if o['username'] == session['username']])
    return render_template('transactions.html', view="orders", orders=ds)

@app.route('/update_order/<order_id>', methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    new_status = request.form.get('status')
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = new_status
            flash(f"Đã cập nhật trạng thái đơn {order_id} thành: {new_status}", "success")
            break
    return redirect(url_for('order_history'))

if __name__ == '__main__':
    app.run(debug=True)