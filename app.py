from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify
from functools import wraps
import datetime
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

try:
    import pymysql
    pymysql_installed = True
except ImportError:
    pymysql_installed = False

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

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
        cursorclass=pymysql.cursors.DictCursor
    )

@app.before_request
def open_db():
    if db_enabled:
        g.db = get_db_connection()

@app.teardown_request
def close_db(error):
    if db_enabled and hasattr(g, 'db'):
        g.db.close()

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
                    ("admin", generate_password_hash("123456"), "admin")
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
        conn.commit()
    finally:
        conn.close()

if db_enabled:
    try:
        init_db()
    except Exception as e:
        import sys
        print(f"Failed to initialize database: {e}", file=sys.stderr)

# Global variables kept for testing fallback and compatibility
users = {"admin": {"password": generate_password_hash("123456"), "role": "admin"}}
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
            try:
                with g.db.cursor() as cursor:
                    cursor.execute("SELECT username FROM users WHERE username = %s", (u,))
                    exists = cursor.fetchone()
                    if exists:
                        flash("Tên đăng nhập đã tồn tại!", "danger")
                    else:
                        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (u, generate_password_hash(p), "customer"))
                        g.db.commit()
                        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
                        return redirect(url_for('login'))
            except Exception as e:
                g.db.rollback()
                flash("Có lỗi xảy ra, vui lòng thử lại!", "danger")
        else:
            if u in users: flash("Tên đăng nhập đã tồn tại!", "danger")
            else:
                users[u] = {"password": generate_password_hash(p), "role": "customer"}
                flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
                return redirect(url_for('login'))
    return render_template('auth.html', action="register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'].strip(), request.form['password'].strip()
        if db_enabled:
            with g.db.cursor() as cursor:
                cursor.execute("SELECT password, role FROM users WHERE username = %s", (u,))
                user = cursor.fetchone()
                if user and check_password_hash(user['password'], p):
                    session['username'], session['role'] = u, user['role']
                    flash(f"Xin chào, {u}!", "success")
                    return redirect(url_for('index'))
            flash("Sai tên đăng nhập/mật khẩu!", "danger")
        else:
            if u in users and check_password_hash(users[u]['password'], p):
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
        with g.db.cursor() as cursor:
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
        try:
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])
        except ValueError:
            flash("Giá hoặc số lượng không hợp lệ!", "danger")
            return redirect(url_for('add_product'))

        if price <= 0 or quantity < 0:
            flash("Giá phải > 0 và số lượng phải >= 0!", "danger")
            return redirect(url_for('add_product'))

        if db_enabled:
            try:
                with g.db.cursor() as cursor:
                    cursor.execute("SELECT ma_sp FROM products WHERE ma_sp = %s", (ma,))
                    if cursor.fetchone():
                        flash("Mã SP đã tồn tại!", "danger")
                        return redirect(url_for('add_product'))
                    cursor.execute(
                        "INSERT INTO products (ma_sp, name, price, quantity) VALUES (%s, %s, %s, %s)",
                        (ma, name, price, quantity)
                    )
                g.db.commit()
                flash("Thêm thành công!", "success")
                return redirect(url_for('index'))
            except Exception:
                g.db.rollback()
                flash("Có lỗi xảy ra!", "danger")
                return redirect(url_for('add_product'))
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
        with g.db.cursor() as cursor:
            cursor.execute("SELECT ma_sp, name, price, quantity FROM products WHERE ma_sp = %s", (ma_sp,))
            sp_row = cursor.fetchone()
            if not sp_row:
                return redirect(url_for('index'))
            sp = {'name': sp_row['name'], 'price': float(sp_row['price']), 'quantity': sp_row['quantity']}
            if request.method == 'POST':
                name = request.form['name']
                try:
                    price = float(request.form['price'])
                    quantity = int(request.form['quantity'])
                except ValueError:
                    flash("Giá hoặc số lượng không hợp lệ!", "danger")
                    return redirect(url_for('edit_product', ma_sp=ma_sp))
                
                if price <= 0 or quantity < 0:
                    flash("Giá phải > 0 và số lượng phải >= 0!", "danger")
                    return redirect(url_for('edit_product', ma_sp=ma_sp))
                
                try:
                    cursor.execute(
                        "UPDATE products SET name = %s, price = %s, quantity = %s WHERE ma_sp = %s",
                        (name, price, quantity, ma_sp)
                    )
                    g.db.commit()
                    flash("Sửa thành công!", "success")
                    return redirect(url_for('index'))
                except Exception:
                    g.db.rollback()
                    flash("Có lỗi xảy ra!", "danger")
                    return redirect(url_for('edit_product', ma_sp=ma_sp))
                    
        return render_template('products.html', view="form", action="edit", title="Sửa Sản Phẩm", sp=sp, ma=ma_sp)
    else:
        if ma_sp not in products: return redirect(url_for('index'))
        if request.method == 'POST':
            try:
                price = float(request.form['price'])
                quantity = int(request.form['quantity'])
            except ValueError:
                flash("Giá hoặc số lượng không hợp lệ!", "danger")
                return redirect(url_for('edit_product', ma_sp=ma_sp))
                
            if price <= 0 or quantity < 0:
                flash("Giá phải > 0 và số lượng phải >= 0!", "danger")
                return redirect(url_for('edit_product', ma_sp=ma_sp))
                
            products[ma_sp].update({"name": request.form['name'], "price": price, "quantity": quantity})
            flash("Sửa thành công!", "success")
            return redirect(url_for('index'))
        return render_template('products.html', view="form", action="edit", title="Sửa Sản Phẩm", sp=products[ma_sp], ma=ma_sp)

@app.route('/delete/<ma_sp>', methods=['POST'])
@login_required
@admin_required
def delete_product(ma_sp):
    if db_enabled:
        try:
            with g.db.cursor() as cursor:
                cursor.execute("DELETE FROM products WHERE ma_sp = %s", (ma_sp,))
            g.db.commit()
        except Exception:
            g.db.rollback()
    else:
        products.pop(ma_sp, None)
    flash("Đã xóa sản phẩm!", "success")
    return redirect(url_for('index'))

@app.route('/add_to_cart/<ma_sp>', methods=['POST'])
@login_required
def add_to_cart(ma_sp):
    if session.get('role') == 'admin':
        flash("Admin không thể mua hàng!", "danger")
        return redirect(url_for('index'))
        
    try:
        qty = int(request.form.get('quantity', 1))
    except ValueError:
        flash("Số lượng không hợp lệ!", "danger")
        return redirect(url_for('index'))
        
    if qty <= 0:
        flash("Số lượng phải lớn 0!", "danger")
        return redirect(url_for('index'))
        
    available_qty = 0
    if db_enabled:
        with g.db.cursor() as cursor:
            cursor.execute("SELECT quantity FROM products WHERE ma_sp = %s", (ma_sp,))
            res = cursor.fetchone()
            if res:
                available_qty = res['quantity']
    else:
        if ma_sp in products:
            available_qty = products[ma_sp]['quantity']
            
    cart = session.get('cart', {})
    current_qty_in_cart = cart.get(ma_sp, 0)
    
    if current_qty_in_cart + qty <= available_qty:
        cart[ma_sp] = current_qty_in_cart + qty
        session['cart'] = cart
        session.modified = True
        flash(f"Đã thêm {qty} sản phẩm vào giỏ!", "success")
    else:
        flash(f"Không thể thêm. Kho chỉ còn {available_qty} sản phẩm, giỏ của bạn đã có {current_qty_in_cart}.", "danger")
    return redirect(url_for('index'))

def get_cart():
    items, total = [], 0
    cart_session = session.get('cart', {})
    if not cart_session:
        return items, total
        
    if db_enabled:
        with g.db.cursor() as cursor:
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
    if session.get('role') == 'admin':
        flash("Admin không thể xem giỏ hàng!", "danger")
        return redirect(url_for('index'))
    items, total = get_cart()
    return render_template('transactions.html', view="cart_checkout", cart_items=items, total_bill=total, show_checkout=False)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if session.get('role') == 'admin':
        flash("Admin không thể thanh toán!", "danger")
        return redirect(url_for('index'))
    items, total = get_cart()
    
    if request.method == 'POST' and items:
        if db_enabled:
            try:
                with g.db.cursor() as cursor:
                    ma_don = uuid.uuid4().hex[:10].upper()
                    
                    # Lock rows
                    placeholders = ', '.join(['%s'] * len(session['cart']))
                    cursor.execute(f"SELECT ma_sp, name, quantity FROM products WHERE ma_sp IN ({placeholders}) FOR UPDATE", list(session['cart'].keys()))
                    p_rows = cursor.fetchall()
                    p_map = {r['ma_sp']: r for r in p_rows}
                    
                    # Verify quantities
                    for ma_sp, qty in session['cart'].items():
                        if ma_sp not in p_map or p_map[ma_sp]['quantity'] < qty:
                            g.db.rollback()
                            flash(f"Sản phẩm {ma_sp} không đủ số lượng tồn kho!", "danger")
                            return redirect(url_for('view_cart'))
                    
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
                        new_qty = p_map[ma_sp]['quantity'] - qty
                        cursor.execute("UPDATE products SET quantity = %s WHERE ma_sp = %s", (new_qty, ma_sp))
                        cursor.execute(
                            "INSERT INTO order_items (order_id, name, qty) VALUES (%s, %s, %s)",
                            (ma_don, p_map[ma_sp]['name'], qty)
                        )
                g.db.commit()
            except Exception as e:
                g.db.rollback()
                flash("Có lỗi xảy ra khi thanh toán, vui lòng thử lại!", "danger")
                return redirect(url_for('view_cart'))
                
            session.pop('cart', None)
            flash(f"Thanh toán thành công! Mã đơn của bạn là {ma_don}", "success")
            return redirect(url_for('order_history'))
        else:
            order_items = []
            for ma_sp, qty in session['cart'].items():
                if ma_sp not in products or products[ma_sp]['quantity'] < qty:
                    flash(f"Sản phẩm {ma_sp} không đủ số lượng tồn kho!", "danger")
                    return redirect(url_for('view_cart'))
                    
            for ma_sp, qty in session['cart'].items():
                products[ma_sp]['quantity'] -= qty
                order_items.append({'name': products[ma_sp]['name'], 'qty': qty})
            
            sales_stats["total_revenue"] += total
            ma_don = uuid.uuid4().hex[:10].upper()
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
        with g.db.cursor() as cursor:
            if session.get('role') == 'admin':
                cursor.execute("""
                    SELECT o.*, i.name as item_name, i.qty as item_qty 
                    FROM orders o 
                    LEFT JOIN order_items i ON o.order_id = i.order_id 
                    ORDER BY o.order_id DESC
                """)
            else:
                cursor.execute("""
                    SELECT o.*, i.name as item_name, i.qty as item_qty 
                    FROM orders o 
                    LEFT JOIN order_items i ON o.order_id = i.order_id 
                    WHERE o.username = %s 
                    ORDER BY o.order_id DESC
                """, (session['username'],))
            rows = cursor.fetchall()
            
            orders_map = {}
            # Ensure stable sorting by inserting them in the order they appear
            for row in rows:
                oid = row['order_id']
                if oid not in orders_map:
                    orders_map[oid] = {
                        'order_id': oid,
                        'username': row['username'],
                        'customer_name': row['customer_name'],
                        'phone': row['phone'],
                        'address': row['address'],
                        'payment_method': row['payment_method'],
                        'total': float(row['total']),
                        'date': row['date'],
                        'status': row['status'],
                        'items': []
                    }
                if row['item_name']:
                    orders_map[oid]['items'].append({'name': row['item_name'], 'qty': row['item_qty']})
            
            ds = list(orders_map.values())
    else:
        ds = list(reversed(orders)) if session.get('role') == 'admin' else list(reversed([o for o in orders if o['username'] == session['username']]))
    return render_template('transactions.html', view="orders", orders=ds)

@app.route('/update_order/<order_id>', methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    new_status = request.form.get('status')
    if not new_status:
        flash("Trạng thái không hợp lệ!", "danger")
        return redirect(url_for('order_history'))
        
    if db_enabled:
        try:
            with g.db.cursor() as cursor:
                cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
            g.db.commit()
            flash(f"Đã cập nhật trạng thái đơn {order_id} thành: {new_status}", "success")
        except Exception:
            g.db.rollback()
            flash("Lỗi cập nhật!", "danger")
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
    keyword   = request.args.get('q', '').strip().lower()
    in_stock  = request.args.get('in_stock', '0') == '1'

    try:
        min_price = request.args.get('min_price', 0, type=float)
        max_price = request.args.get('max_price', float('inf'), type=float)
    except (ValueError, TypeError):
        min_price, max_price = 0, float('inf')

    if db_enabled:
        with g.db.cursor() as cursor:
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