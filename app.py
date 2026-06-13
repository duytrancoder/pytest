from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import datetime
import os
try:
    import pymysql
    pymysql_installed = True
except ImportError:
    pymysql_installed = False

app = Flask(__name__)
app.secret_key = "khoa_bi_mat_cho_flash_message_va_session"

# Database Configuration
DB_HOST = os.environ.get("MYSQL_HOST")
DB_USER = os.environ.get("MYSQL_USER")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = os.environ.get("MYSQL_DB")
DB_PORT = int(os.environ.get("MYSQL_PORT", 3306))

db_enabled = pymysql_installed and all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME])

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    if not db_enabled:
        return
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Table users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL
                )
            """)
            
            # Table products
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    ma_sp VARCHAR(50) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price DECIMAL(15, 2) NOT NULL,
                    quantity INT NOT NULL
                )
            """)
            
            # Table orders
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id VARCHAR(50) PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    customer_name VARCHAR(255) NOT NULL,
                    phone VARCHAR(50) NOT NULL,
                    address TEXT NOT NULL,
                    payment_method VARCHAR(50) NOT NULL,
                    total DECIMAL(15, 2) NOT NULL,
                    date VARCHAR(50) NOT NULL,
                    status VARCHAR(50) NOT NULL
                )
            """)
            
            # Table order_items
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id VARCHAR(50) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    qty INT NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
                )
            """)
            
            # Seed users if empty
            cursor.execute("SELECT COUNT(*) as cnt FROM users")
            if cursor.fetchone()["cnt"] == 0:
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    ("admin", "123456", "admin")
                )
                
            # Seed products if empty
            cursor.execute("SELECT COUNT(*) as cnt FROM products")
            if cursor.fetchone()["cnt"] == 0:
                cursor.executemany(
                    "INSERT INTO products (ma_sp, name, price, quantity) VALUES (%s, %s, %s, %s)",
                    [
                        ("SP01", "Laptop Dell", 15000000.0, 10),
                        ("SP02", "Chuột Logitech", 300000.0, 50)
                    ]
                )
    finally:
        conn.close()

if db_enabled:
    try:
        init_db()
    except Exception as e:
        import sys
        print(f"Failed to initialize database: {e}", file=sys.stderr)

# Global variables kept for testing fallback and compatibility
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
        if db_enabled:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT username FROM users WHERE username = %s", (u,))
                    exists = cursor.fetchone()
                    if exists:
                        flash("Tên đăng nhập đã tồn tại!", "danger")
                    else:
                        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (u, p, "customer"))
                        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
                        return redirect(url_for('login'))
            finally:
                conn.close()
        else:
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
        if db_enabled:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT password, role FROM users WHERE username = %s", (u,))
                    user = cursor.fetchone()
                    if user and user['password'] == p:
                        session['username'], session['role'] = u, user['role']
                        flash(f"Xin chào, {u}!", "success")
                        return redirect(url_for('index'))
            finally:
                conn.close()
            flash("Sai tên đăng nhập/mật khẩu!", "danger")
        else:
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
    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ma_sp, name, price, quantity FROM products")
                db_products = cursor.fetchall()
                prod_dict = {row['ma_sp']: {'name': row['name'], 'price': float(row['price']), 'quantity': row['quantity']} for row in db_products}
                filtered = {ma: info for ma, info in prod_dict.items() if q in ma.lower() or q in info['name'].lower()}
                
                cursor.execute("SELECT SUM(total) as revenue FROM orders")
                rev_row = cursor.fetchone()
                total_revenue = float(rev_row['revenue']) if rev_row and rev_row['revenue'] is not None else 0.0
                
                stats = {
                    "items": len(prod_dict),
                    "stock": sum(p['quantity'] for p in prod_dict.values()),
                    "revenue": total_revenue
                }
        finally:
            conn.close()
    else:
        filtered = {ma: info for ma, info in products.items() if q in ma.lower() or q in info['name'].lower()}
        stats = {"items": len(products), "stock": sum(p['quantity'] for p in products.values()), "revenue": sales_stats["total_revenue"]}
    return render_template('products.html', view="list", products=filtered, stats=stats)

@app.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        ma = request.form['ma_sp'].strip().upper()
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        if db_enabled:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ma_sp FROM products WHERE ma_sp = %s", (ma,))
                    if cursor.fetchone():
                        flash("Mã SP đã tồn tại!", "danger")
                        return redirect(url_for('add_product'))
                    cursor.execute(
                        "INSERT INTO products (ma_sp, name, price, quantity) VALUES (%s, %s, %s, %s)",
                        (ma, name, price, quantity)
                    )
            finally:
                conn.close()
            flash("Thêm thành công!", "success")
            return redirect(url_for('index'))
        else:
            if ma in products:
                flash("Mã SP đã tồn tại!", "danger")
                return redirect(url_for('add_product'))
            products[ma] = {"name": name, "price": price, "quantity": quantity}
            flash("Thêm thành công!", "success")
            return redirect(url_for('index'))
    return render_template('products.html', view="form", action="add", title="Thêm Sản Phẩm")

@app.route('/edit/<ma_sp>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(ma_sp):
    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ma_sp, name, price, quantity FROM products WHERE ma_sp = %s", (ma_sp,))
                sp_row = cursor.fetchone()
                if not sp_row:
                    return redirect(url_for('index'))
                sp = {'name': sp_row['name'], 'price': float(sp_row['price']), 'quantity': sp_row['quantity']}
                if request.method == 'POST':
                    name = request.form['name']
                    price = float(request.form['price'])
                    quantity = int(request.form['quantity'])
                    cursor.execute(
                        "UPDATE products SET name = %s, price = %s, quantity = %s WHERE ma_sp = %s",
                        (name, price, quantity, ma_sp)
                    )
                    flash("Sửa thành công!", "success")
                    return redirect(url_for('index'))
        finally:
            conn.close()
        return render_template('products.html', view="form", action="edit", title="Sửa Sản Phẩm", sp=sp, ma=ma_sp)
    else:
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
    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM products WHERE ma_sp = %s", (ma_sp,))
        finally:
            conn.close()
    else:
        products.pop(ma_sp, None)
    flash("Đã xóa sản phẩm!", "success")
    return redirect(url_for('index'))

@app.route('/add_to_cart/<ma_sp>', methods=['POST'])
@login_required
def add_to_cart(ma_sp):
    if session.get('role') == 'admin': return redirect(url_for('index'))
    qty = int(request.form.get('quantity', 1))
    
    available_qty = 0
    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT quantity FROM products WHERE ma_sp = %s", (ma_sp,))
                res = cursor.fetchone()
                if res:
                    available_qty = res['quantity']
        finally:
            conn.close()
    else:
        if ma_sp in products:
            available_qty = products[ma_sp]['quantity']
            
    if available_qty >= qty:
        cart = session.get('cart', {})
        cart[ma_sp] = cart.get(ma_sp, 0) + qty
        session['cart'] = cart
        flash(f"Đã thêm {qty} sản phẩm vào giỏ!", "success")
    return redirect(url_for('index'))

def get_cart():
    items, total = [], 0
    cart_session = session.get('cart', {})
    if not cart_session:
        return items, total
        
    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                placeholders = ', '.join(['%s'] * len(cart_session))
                cursor.execute(f"SELECT ma_sp, name, price FROM products WHERE ma_sp IN ({placeholders})", list(cart_session.keys()))
                rows = cursor.fetchall()
                prod_map = {row['ma_sp']: row for row in rows}
                for ma_sp, qty in cart_session.items():
                    if ma_sp in prod_map:
                        price = float(prod_map[ma_sp]['price'])
                        t = price * qty
                        total += t
                        items.append({'ma_sp': ma_sp, 'name': prod_map[ma_sp]['name'], 'price': price, 'qty': qty, 'thanh_tien': t})
        finally:
            conn.close()
    else:
        for ma_sp, qty in cart_session.items():
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
        if db_enabled:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) as cnt FROM orders")
                    order_count = cursor.fetchone()['cnt']
                    ma_don = f"DH{order_count+1:03d}"
                    
                    cursor.execute(
                        """
                        INSERT INTO orders (order_id, username, customer_name, phone, address, payment_method, total, date, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            ma_don, session['username'],
                            request.form.get('name'), request.form.get('phone'),
                            request.form.get('address'), request.form.get('payment_method'),
                            total, datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), 'Chờ xử lý'
                        )
                    )
                    
                    for ma_sp, qty in session['cart'].items():
                        cursor.execute("SELECT name, quantity FROM products WHERE ma_sp = %s", (ma_sp,))
                        p_row = cursor.fetchone()
                        if p_row and p_row['quantity'] >= qty:
                            new_qty = p_row['quantity'] - qty
                            cursor.execute("UPDATE products SET quantity = %s WHERE ma_sp = %s", (new_qty, ma_sp))
                            cursor.execute(
                                "INSERT INTO order_items (order_id, name, qty) VALUES (%s, %s, %s)",
                                (ma_don, p_row['name'], qty)
                            )
            finally:
                conn.close()
            session.pop('cart', None)
            flash(f"Thanh toán thành công! Mã đơn của bạn là {ma_don}", "success")
            return redirect(url_for('order_history'))
        else:
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
    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if session.get('role') == 'admin':
                    cursor.execute("SELECT * FROM orders ORDER BY order_id DESC")
                else:
                    cursor.execute("SELECT * FROM orders WHERE username = %s ORDER BY order_id DESC", (session['username'],))
                db_orders = cursor.fetchall()
                
                orders_list = []
                for o in db_orders:
                    cursor.execute("SELECT name, qty FROM order_items WHERE order_id = %s", (o['order_id'],))
                    db_items = cursor.fetchall()
                    orders_list.append({
                        'order_id': o['order_id'],
                        'username': o['username'],
                        'customer_name': o['customer_name'],
                        'phone': o['phone'],
                        'address': o['address'],
                        'payment_method': o['payment_method'],
                        'items': [{'name': item['name'], 'qty': item['qty']} for item in db_items],
                        'total': float(o['total']),
                        'date': o['date'],
                        'status': o['status']
                    })
                ds = orders_list
        finally:
            conn.close()
    else:
        ds = reversed(orders) if session.get('role') == 'admin' else reversed([o for o in orders if o['username'] == session['username']])
    return render_template('transactions.html', view="orders", orders=ds)

@app.route('/update_order/<order_id>', methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    new_status = request.form.get('status')
    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
        finally:
            conn.close()
        flash(f"Đã cập nhật trạng thái đơn {order_id} thành: {new_status}", "success")
    else:
        for order in orders:
            if order['order_id'] == order_id:
                order['status'] = new_status
                flash(f"Đã cập nhật trạng thái đơn {order_id} thành: {new_status}", "success")
                break
    return redirect(url_for('order_history'))

@app.route('/search')
@login_required
def search_products():
    from flask import jsonify

    keyword   = request.args.get('q', '').strip().lower()
    in_stock  = request.args.get('in_stock', '0') == '1'

    try:
        min_price = float(request.args.get('min_price', 0))
        max_price = float(request.args.get('max_price', float('inf')))
    except (ValueError, TypeError):
        min_price, max_price = 0, float('inf')

    if db_enabled:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = "SELECT ma_sp, name, price, quantity FROM products WHERE 1=1"
                params = []
                
                if max_price != float('inf'):
                    query += " AND price BETWEEN %s AND %s"
                    params.extend([min_price, max_price])
                else:
                    query += " AND price >= %s"
                    params.append(min_price)
                
                if in_stock:
                    query += " AND quantity > 0"
                
                cursor.execute(query, params)
                db_products = cursor.fetchall()
                
                results = []
                for row in db_products:
                    ma = row['ma_sp']
                    name = row['name']
                    price = float(row['price'])
                    quantity = int(row['quantity'])
                    
                    if keyword and keyword not in ma.lower() and keyword not in name.lower():
                        continue
                        
                    results.append({
                        'ma_sp': ma,
                        'name': name,
                        'price': price,
                        'quantity': quantity,
                        'in_stock': quantity > 0
                    })
        finally:
            conn.close()
        return jsonify({'count': len(results), 'products': results})
    else:
        results = []
        for ma, info in products.items():
            if keyword and keyword not in ma.lower() and keyword not in info['name'].lower():
                continue
            if not (min_price <= info['price'] <= max_price):
                continue
            if in_stock and info['quantity'] <= 0:
                continue
            results.append({
                'ma_sp'   : ma,
                'name'    : info['name'],
                'price'   : info['price'],
                'quantity': info['quantity'],
                'in_stock': info['quantity'] > 0
            })

        return jsonify({'count': len(results), 'products': results})

if __name__ == '__main__':
    app.run(debug=True)