# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
import pandas as pd
from datetime import datetime, timedelta, date
import calendar
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import PolynomialFeatures

app = Flask(__name__)
app.config.from_pyfile('config.py')
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = 'dev-secret-change-me'

mysql = MySQL(app)

# ---- Helpers ----
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return wrapped

def ensure_tables_exist():
    cur = mysql.connection.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      email VARCHAR(255) NOT NULL UNIQUE,
      password_hash VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
      id INT AUTO_INCREMENT PRIMARY KEY,
      date DATE NOT NULL,
      category VARCHAR(100) NOT NULL,
      amount DECIMAL(10,2) NOT NULL,
      user_id INT,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    mysql.connection.commit()
    cur.close()

# ---- ROUTES ----

# 1) Strict auth entry point: always show login/signup first
@app.route('/')
def root():
    # Always direct to the login page as the strict first page.
    # If you prefer to show a public landing page, change this.
    return redirect(url_for('login'))

# Login page (GET shows form; POST authenticates)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        if row and check_password_hash(row[1], password):
            # Successful authentication: set session and go to /index
            session.clear()
            session['user_id'] = row[0]
            session['user_email'] = email
            # Optionally set session.permanent = True with lifetime if needed
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    # GET
    return render_template('login.html', logged_in=('user_id' in session), user_email=session.get('user_email'))

# Signup (register) — after signup redirect to login (user must authenticate)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not email or not password:
            flash('Email and password required.', 'error')
            return redirect(url_for('signup'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('login'))

        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful. Please log in to continue.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', logged_in=('user_id' in session), user_email=session.get('user_email'))

# Explicit index route — protected; only reachable after authentication
@app.route('/index')
@login_required
def index():
    # index.html contains the add-expense form and top-right welcome/logout
    return render_template('index.html', logged_in=True, user_email=session.get('user_email'))

# keep /home as alias if needed
@app.route('/home')
@login_required
def home():
    return redirect(url_for('index'))

# Redirect /dashboard to /index (you asked not to use dashboard.html)
@app.route('/dashboard')
@login_required
def dashboard_redirect():
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

# Add expense (user-scoped)
@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    date = request.form.get('date')
    category = request.form.get('category', '').strip().lower()
    amount_raw = request.form.get('amount', '0').strip()
    if not date or not category or not amount_raw:
        return "Missing fields", 400
    try:
        amount = float(amount_raw)
    except ValueError:
        return "Invalid amount", 400
    if amount < 0:
        return "Invalid amount", 400
    if amount > 1000:
        return "Amount exceeds ₹1000 limit", 400
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO expenses (date, category, amount, user_id) VALUES (%s, %s, %s, %s)",
                (date, category, amount, user_id))
    mysql.connection.commit()
    cur.close()
    # After adding expense, redirect to report (your flow can change this)
    return "OK", 200


# Report — user-scoped (renders graphs)
@app.route('/report')
@login_required
def report():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, category, amount FROM expenses WHERE user_id = %s ORDER BY date", (user_id,))
    rows = cur.fetchall()
    cur.close()

    if not rows:
        return render_template('report.html',
                               category_plots_line={},
                               category_plots_bar={},
                               category_plots_pie={},
                               combined_plot_line=None,
                               combined_plot_bar=None,
                               combined_plot_pie=None,
                               logged_in=True,
                               user_email=session.get('user_email'))

    df = pd.DataFrame(rows, columns=['date', 'category', 'amount'])
    df['date'] = pd.to_datetime(df['date'])

    category_plots_line = {}
    category_plots_bar = {}
    category_plots_pie = {}

    for category in df['category'].unique():
        subset = df[df['category'] == category].sort_values('date')

        # ---------- Line plot ----------
        plt.figure(figsize=(8, 4.5))
        plt.plot(subset['date'], subset['amount'], marker='o', label=category)
        plt.xticks(rotation=30)
        plt.ylim(0, 1000)
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title(f'{category} Expense Trend (line)')
        plt.legend()
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        category_plots_line[category] = base64.b64encode(buf.getvalue()).decode()
        plt.close()

        # ---------- Bar plot (sum by date) ----------
        grouped = subset.groupby('date')['amount'].sum().sort_index()
        plt.figure(figsize=(8, 4.5))
        plt.bar(grouped.index.astype('O'), grouped.values)
        plt.xticks(rotation=30)
        plt.ylim(0, 1000)
        plt.xlabel('Date')
        plt.ylabel('Total amount')
        plt.title(f'{category} Expense (daily total) (bar)')
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        category_plots_bar[category] = base64.b64encode(buf.getvalue()).decode()
        plt.close()

        # ---------- Pie: distribution across dates (daily totals for this category) ----------
        # NOTE: pies with many slices may look crowded; we cap labels if necessary.
        labels = [d.strftime('%Y-%m-%d') for d in grouped.index]
        sizes = grouped.values
        plt.figure(figsize=(8, 6))
        if len(sizes) == 0:
            # create a tiny blank pie
            plt.pie([1], labels=['no data'])
        else:
            plt.pie(sizes, labels=labels, autopct=lambda p: f'{p:.0f}%' if p > 3 else '', startangle=90)
        plt.title(f'{category} Distribution by Date (pie)')
        plt.axis('equal')
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        category_plots_pie[category] = base64.b64encode(buf.getvalue()).decode()
        plt.close()

    # ---------- Combined line ----------
    plt.figure(figsize=(10, 6))
    for category in df['category'].unique():
        subset = df[df['category'] == category].sort_values('date')
        plt.plot(subset['date'], subset['amount'], marker='o', label=category)
    plt.xticks(rotation=30)
    plt.ylim(0, 1000)
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Combined Expense Trend (line)')
    plt.legend()
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    combined_plot_line = base64.b64encode(buf.getvalue()).decode()
    plt.close()

    # ---------- Combined bar (total per date across categories) ----------
    combined_by_date = df.groupby('date')['amount'].sum().sort_index()
    plt.figure(figsize=(10, 6))
    plt.bar(combined_by_date.index.astype('O'), combined_by_date.values)
    plt.xticks(rotation=30)
    plt.ylim(0, 5000)
    plt.xlabel('Date')
    plt.ylabel('Total amount')
    plt.title('Combined Expense (daily total) (bar)')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    combined_plot_bar = base64.b64encode(buf.getvalue()).decode()
    plt.close()

    # ---------- Combined pie: distribution across categories (total spent per category) ----------
    by_category = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    labels = by_category.index.tolist()
    sizes = by_category.values
    plt.figure(figsize=(8, 6))
    if len(sizes) == 0:
        plt.pie([1], labels=['no data'])
    else:
        plt.pie(sizes, labels=labels, autopct=lambda p: f'{p:.0f}%' if p > 3 else '', startangle=90)
    plt.title('Spending Distribution by Category (pie)')
    plt.axis('equal')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    combined_plot_pie = base64.b64encode(buf.getvalue()).decode()
    plt.close()

    return render_template('report.html',
                           category_plots_line=category_plots_line,
                           category_plots_bar=category_plots_bar,
                           category_plots_pie=category_plots_pie,
                           combined_plot_line=combined_plot_line,
                           combined_plot_bar=combined_plot_bar,
                           combined_plot_pie=combined_plot_pie,
                           logged_in=True,
                           user_email=session.get('user_email'))




@app.route('/predict', methods=['GET'])
@login_required
def predict():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, category, amount FROM expenses WHERE user_id = %s ORDER BY date", (user_id,))
    rows = cur.fetchall()
    cur.close()
    if not rows:
        return jsonify({'error': 'No data available for predictions.'}), 400

    df = pd.DataFrame(rows, columns=['date', 'category', 'amount'])
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = (df['date'] - df['date'].min()).dt.days

    results = {}
    for category in df['category'].unique():
        cat_df = df[df['category'] == category].sort_values('date')
        if len(cat_df) < 2:
            results[category] = {'error': 'Not enough data to predict.'}
            continue

        X = cat_df[['days']].values
        y = cat_df['amount'].values
        degree = 2
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        model = SVR(kernel='rbf', C=100, epsilon=10)
        model.fit(X_poly, y)

        future_days = np.array([[int(cat_df['days'].max()) + i] for i in range(1, 31)])
        future_dates = [cat_df['date'].max() + pd.Timedelta(days=i) for i in range(1, 31)]
        future_poly = poly.transform(future_days)
        preds = model.predict(future_poly)
        preds = np.clip(preds, 0, 1000)

        # ---------- Line image ----------
        plt.figure(figsize=(10, 6))
        plt.plot(cat_df['date'], cat_df['amount'], marker='o', label='Historical')
        plt.plot(future_dates, preds, linestyle='--', label='Predicted')
        plt.xticks(rotation=30)
        plt.ylim(0, 1000)
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title(f'{category} Predicted Expenses (line)')
        plt.legend()
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_line_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.close()

        # ---------- Bar image ----------
        plt.figure(figsize=(10, 6))
        plt.bar(future_dates, preds)
        plt.xticks(rotation=30)
        plt.ylim(0, 1000)
        plt.xlabel('Date')
        plt.ylabel('Predicted amount')
        plt.title(f'{category} Predicted Expenses (bar)')
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_bar_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.close()

        # ---------- Pie image: distribution of predicted daily amounts across next 30 days ----------
        labels = [d.strftime('%Y-%m-%d') for d in future_dates]
        sizes = preds
        plt.figure(figsize=(8, 6))
        # If there are many slices, autopct will only show larger slices; yaha theek hai.
        plt.pie(sizes, labels=labels, autopct=lambda p: f'{p:.0f}%' if p > 3 else '', startangle=90)
        plt.title(f'{category} Predicted Distribution (next 30 days) (pie)')
        plt.axis('equal')
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_pie_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.close()

        results[category] = {'line': img_line_b64, 'bar': img_bar_b64, 'pie': img_pie_b64}

    return jsonify(results)


@app.route('/report_total', methods=['GET'])
@login_required
def report_total():
    """
    Supports:
      - start_date & end_date (YYYY-MM-DD)  --> preferred (custom / picked date/week/month/range)
      - or duration parameter ('daily','weekly','monthly') for rolling windows (backward-looking)
      - category param: 'all' or category name

    Response:
      { total: float, count: int, period_start: 'YYYY-MM-DD', period_end: 'YYYY-MM-DD' }
    """
    user_id = session['user_id']
    category = (request.args.get('category') or 'all').lower()

    # Attempt to read explicit start/end
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')

    start_date = None
    end_date = None

    try:
        if start_str and end_str:
            # client should send YYYY-MM-DD
            start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
        else:
            # fallback to rolling duration param (as before)
            duration = (request.args.get('duration') or 'monthly').lower()
            today = datetime.now().date()  # local server date; adjust if you want UTC/Kolkata explicitly
            if duration == 'daily':
                start_date = end_date = today
            elif duration == 'weekly':
                start_date = today - timedelta(days=6)
                end_date = today
            else:
                start_date = today - timedelta(days=29)
                end_date = today
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD.", 400

    # SQL query (safe params)
    cur = mysql.connection.cursor()
    if category == 'all':
        cur.execute("""
            SELECT SUM(amount) as total, COUNT(*) as cnt
            FROM expenses
            WHERE user_id = %s AND date BETWEEN %s AND %s
        """, (user_id, start_date, end_date))
    else:
        cur.execute("""
            SELECT SUM(amount) as total, COUNT(*) as cnt
            FROM expenses
            WHERE user_id = %s AND category = %s AND date BETWEEN %s AND %s
        """, (user_id, category, start_date, end_date))

    row = cur.fetchone()
    cur.close()

    total = float(row[0]) if row and row[0] is not None else 0.0
    count = int(row[1]) if row and row[1] is not None else 0

    return jsonify({
        'total': round(total, 2),
        'count': count,
        'period_start': start_date.isoformat(),
        'period_end': end_date.isoformat(),
    })


if __name__ == '__main__':
    try:
        ensure_tables_exist()
    except Exception as e:
        print("Warning: ensure_tables_exist failed:", e)
    app.run(debug=True)
