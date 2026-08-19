from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def init_db():
    conn = sqlite3.connect('staj.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            student_number TEXT,
            tc_no TEXT,
            birth_date TEXT,
            start_date TEXT,
            end_date TEXT,
            insurance_start TEXT,
            day_count TEXT,
            health_status TEXT,
            abroad TEXT,
            salary TEXT,
            company_name TEXT,
            company_address TEXT,
            employee_count TEXT,
            company_phone TEXT,
            tax_number TEXT,
            iban TEXT,
            government_support TEXT
            
        )
    ''')
    

    conn.commit()
    conn.close()

def add_ek16_column():
        conn = sqlite3.connect('staj.db')
        cursor = conn.cursor()

        try:
            cursor.execute("ALTER TABLE applications ADD COLUMN ek16 TEXT")
            conn.commit()
            print("ek16 sütunu eklendi.")
        except sqlite3.OperationalError:
            print("ek16 sütunu zaten mevcut.")

        conn.close()

def add_is_read_column():
    conn = sqlite3.connect('staj.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "ALTER TABLE applications ADD COLUMN is_read INTEGER DEFAULT 0"
        )
        conn.commit()
        print("is_read sütunu eklendi.")
    except sqlite3.OperationalError:
        print("is_read sütunu zaten mevcut.")

    conn.close()

def add_status_column():
    conn = sqlite3.connect('staj.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "ALTER TABLE applications ADD COLUMN status TEXT DEFAULT 'Bekliyor'"
        )
        conn.commit()
        print("status sütunu eklendi.")
    except sqlite3.OperationalError:
        print("status sütunu zaten mevcut.")

    conn.close()    

def add_submitted_at_column():
    conn = sqlite3.connect('staj.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "ALTER TABLE applications ADD COLUMN submitted_at TEXT"
        )
        conn.commit()
        print("submitted_at sütunu eklendi.")
    except sqlite3.OperationalError:
        print("submitted_at sütunu zaten mevcut.")

    conn.close()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/academic-login")
def academic_login():
    return render_template("academic_login.html")

@app.route('/academic-home', methods=['GET', 'POST'])
def academic_home():

    conn = sqlite3.connect('staj.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY id DESC
    """)

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        'academic_home.html',
        applications=applications
    )

@app.route("/student-login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Şimdilik test kullanıcı bilgileri
        if username == "ogrenci" and password == "1234":
            return redirect(url_for("student_home"))

        return render_template(
            "student_login.html",
            error="Kullanıcı adı veya şifre hatalı."
        )

    return render_template("student_login.html")

@app.route("/student")
def student_home():
    return render_template("student_home.html")

@app.route("/application",methods=['GET','POST'])
def application():
    if request.method == 'POST':
        name = request.form.get('name')
        student_number = request.form.get('student_number')
        tc_no = request.form.get('tc_no')
        birth_date = request.form.get('birth_date')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        insurance_start = request.form.get('insurance_start')
        day_count = request.form.get('day_count')
        health_status = request.form.get('health_status')
        abroad = request.form.get('abroad')
        salary = request.form.get('salary')

        company_name = request.form.get('company_name')
        company_address = request.form.get('company_address')
        employee_count = request.form.get('employee_count')
        company_phone = request.form.get('company_phone')
        tax_number = request.form.get('tax_number')
        iban = request.form.get('iban')
        government_support = request.form.get('government_support')

        filename = None
        file = request.files.get('ek16')
       
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("Dosya kaydedildi:", filename)

        conn = sqlite3.connect('staj.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO applications (
            name,
            student_number,
            tc_no,
            birth_date,
            start_date,
            end_date,
            insurance_start,
            day_count,
            health_status,
            abroad,
            salary,
            company_name,
            company_address,
            employee_count,
            company_phone,
            tax_number,
            iban,
            government_support,
            ek16,
            submitted_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        name,
        student_number,
        tc_no,
        birth_date,
        start_date,
        end_date,
        insurance_start,
        day_count,
        health_status,
        abroad,
        salary,
        company_name,
        company_address,
        employee_count,
        company_phone,
        tax_number,
        iban,
        government_support,
        filename,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        ))

        conn.commit()
        conn.close()
        return redirect(url_for('success'))

    return render_template("application.html")

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == "__main__": 
    init_db()
    
    app.run(debug=True)

   