from flask import Flask, render_template, request, redirect, url_for
from app.routes import auth
from app.db.passwords_handler import PasswordsHandler
from app.db.password_share_handler import PasswordShareHandler
from hashlib import sha256
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import random
from app.db import logs_handler
from app import password_importer
from app.db.category_handler import CategoryHandler
from app.db import passwords_handler

app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    token = request.cookies.get('token')
    user_id = request.cookies.get('user_id')
    key = auth.get_key_from_token(token)
    if not key:
        return redirect("/login")
    password_handler = PasswordsHandler(key)
    if not auth.verify_token(token, user_id):
        return redirect("/login")
    passwords = password_handler.get_passwords(user_id)
    if not passwords:
        passwords = []
    fernet = Fernet(key)
    passwords_dicts = []
    category_manager = CategoryHandler()
    for row in passwords:
        id = row[0]
        categories = category_manager.get_categories_for_password(password_id=id)
        passwords_dicts.append({
            'id': id,
            'username': row[1],
            'site': row[3],
            'password': fernet.decrypt(row[2].encode()).decode(),
            'categories': categories
        })
    logsmanager = logs_handler.LogsHandler()
    logs = logsmanager.get_logs(user_id)
    all_categories = category_manager.get_all_categories()
    return render_template('home.html', passwords=passwords_dicts, logs=logs, categories=all_categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        resp = auth.login()
        if resp.status_code == 200:
            return redirect("/home")
        return resp
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return auth.register()
    return auth.register()

@app.route('/add_password', methods=['POST'])
def add_password():
    token = request.cookies.get('token')
    user_id = request.cookies.get('user_id')
    key = auth.get_key_from_token(token)
    if not key:
        return redirect("/login")
    password_handler = PasswordsHandler(key)
    if not auth.verify_token(token, user_id):
        return redirect("/login")
    data = request.form
    username = data['username']
    site = data['site']
    password = data['password']
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode()).decode()
    category_name = request.form.get('category')
    password_id = password_handler.add_password(user_id, username, site, encrypted_password)
    if category_name:
        category_handler = CategoryHandler()
        category_handler.add_category(category_name)
        category_id = category_handler.get_category_by_name(category_name)
        category_handler.assign_category_to_password(password_id, category_id)
    return redirect("/home")

@app.route('/delete_password', methods=['POST'])
def delete_password():
    token = request.cookies.get('token')
    user_id = request.cookies.get('user_id')
    key = auth.get_key_from_token(token)
    if not key:
        return redirect("/login")
    password_handler = PasswordsHandler(key)
    if not auth.verify_token(token, user_id):
        return redirect("/login")
    data = request.form
    site = data['site']
    password_handler.delete_password(user_id, site)
    return redirect("/home")

@app.route('/share_password', methods=['POST'])
def share_password():
    token = request.cookies.get('token')
    user_id = request.cookies.get('user_id')
    key = auth.get_key_from_token(token)
    if not key:
        return redirect("/login")
    password_handler = PasswordsHandler(key)
    if not auth.verify_token(token, user_id):
        return redirect("/login")
    site = request.args.get('site')
    passwords = password_handler.get_passwords(user_id)
    if not passwords:
        passwords = []
    if site:
        password = password_handler.get_password(user_id, site)
        if not password:
            return redirect("/home")
    data = request.form
    if not data :
        return redirect("/home")
    site = data.get('site')
    username = data.get('username')
    password = data.get('password')
    if not password or not site or not username:
        return redirect("/home")
    password_share_handler = PasswordShareHandler(key)
    hash = hex(random.getrandbits(128))[2:] 
    random_key = Fernet.generate_key()
    fernet = Fernet(random_key)
    site = fernet.encrypt(site.encode()).decode()
    username = fernet.encrypt(username.encode()).decode()
    password = fernet.encrypt(password.encode()).decode()
    password_share_handler.share_password(site, username, password, hash, datetime.now() + timedelta(minutes=45), user_id)
    link = f"http://127.0.0.1:5000/get_shared_password?hash={hash}&key={random_key.decode()}"
    return render_template('share_password.html', link=link)

@app.route('/get_shared_password', methods=['GET'])
def get_shared_password():
    hash = request.args.get('hash')
    if not hash:
        return redirect("/home")
    decrypt_key = request.args.get('key')
    password_share_handler = PasswordShareHandler("")
    shared_password = password_share_handler.get_shared_password(hash)
    send_password = [None, None, None]
    send_password[0] = Fernet(decrypt_key.encode()).decrypt(shared_password[0].encode()).decode()
    send_password[1] = Fernet(decrypt_key.encode()).decrypt(shared_password[1].encode()).decode()
    send_password[2] = Fernet(decrypt_key.encode()).decrypt(shared_password[2].encode()).decode()
    if not send_password:
        return redirect("/home")
    return render_template('shared_password_get.html', shared_password=send_password)

@app.route('/share_category_passwords', methods=['POST'])
def share_category_passwords():
    token = request.cookies.get('token')
    user_id = request.cookies.get('user_id')
    key = auth.get_key_from_token(token)
    if not key:
        return redirect("/login")
    if not auth.verify_token(token, user_id):
        return redirect("/login")
    category_name = request.form.get('category')
    if not category_name:
        return redirect("/home")
    category_handler = CategoryHandler()
    category_id = category_handler.get_category_by_name(category_name)
    if not category_id:
        return redirect("/home")
    password_handler = PasswordsHandler(key)
    query = """
        SELECT p.id, p.site, p.username, p.password
        FROM passwords p
        JOIN passwords_categories pc ON p.id = pc.password_id
        WHERE pc.category_id = ? AND p.user_id = ?
    """
    passwords = password_handler.db_handler.send_query(query, (category_id, user_id))
    if not passwords:
        return redirect("/home")
    random_key = Fernet.generate_key()
    fernet = Fernet(random_key)
    hash = hex(random.getrandbits(128))[2:]
    password_share_handler = PasswordShareHandler(key)
    for row in passwords:
        site = fernet.encrypt(row[1].encode()).decode()
        username = fernet.encrypt(row[2].encode()).decode()
        password = fernet.encrypt(row[3].encode()).decode()
        password_share_handler.share_password(site, username, password, hash, datetime.now() + timedelta(minutes=45), user_id)
    link = f"http://127.0.0.1:5000/get_shared_category_passwords?hash={hash}&key={random_key.decode()}"
    return render_template('share_password.html', link=link)

@app.route('/get_shared_category_passwords', methods=['GET'])
def get_shared_category_passwords():
    hash = request.args.get('hash')
    decrypt_key = request.args.get('key')
    if not hash or not decrypt_key:
        return redirect("/home")
    password_share_handler = PasswordShareHandler("")
    shared_passwords = password_share_handler.get_all_shared_passwords(hash)
    if not shared_passwords:
        return redirect("/home")
    fernet = Fernet(decrypt_key.encode())
    passwords = []
    for row in shared_passwords:
        try:
            print("Sharing row : " + str(row))
            site = fernet.decrypt(row[0].encode()).decode()
            username = fernet.decrypt(row[2].encode()).decode()
            password =  fernet.decrypt(row[1].encode()).decode()
            passwords.append({'site': site, 'username': username, 'password': password})
        except Exception:
            continue
    print("our passwords: " ,  str(shared_passwords))
    return render_template('shared_passwords_get.html', passwords=passwords)

@app.route('/import_csv', methods=['POST'])
def import_csv():
    token = request.cookies.get('token')
    user_id = request.cookies.get('user_id')
    key = auth.get_key_from_token(token)
    if not key:
        return redirect("/login")
    password_handler = PasswordsHandler(key)
    if not auth.verify_token(token, user_id):
        return redirect("/login")
    file = request.files['file']
    if not file or not file.filename.endswith('.csv'):
        return redirect("/home")
    passwords = []
    password_importer_instance = password_importer.PasswordImporter(key)
    try:
        print("Importing CSV file...")
        import pandas as pd
        passwords_df = pd.read_csv(file, encoding='utf-8', sep=";")
        passwords_df.columns = [col.strip().lower() for col in passwords_df.columns]
        print(list(passwords_df.columns))
        password_importer_instance.import_passwords_from_csv(passwords_df, user_id)
    except Exception as e:
        print(f"Error importing CSV: {e}")
        return redirect("/home")
    return redirect("/home")

@app.route('/import_json', methods=['POST'])
def import_json():
    token = request.cookies.get('token')
    user_id = request.cookies.get('user_id')
    key = auth.get_key_from_token(token)
    if not key:
        return redirect("/login")
    password_handler = PasswordsHandler(key)
    if not auth.verify_token(token, user_id):
        return redirect("/login")
    file = request.files['file']
    if not file or not file.filename.endswith('.json'):
        return redirect("/home")
    import json
    passwords = json.load(file)
    password_importer_instance = password_importer.PasswordImporter(key)
    password_importer_instance.import_password_from_json(passwords, user_id)
    return redirect("/home")

@app.route('/logout')
def logout():
    auth.logout()
    return redirect("/login")
    

def get_secret_key():
    return "SECRET_KEYXQKHJDSQOIUEZ"

if __name__ == "__main__":
    app.secret_key = get_secret_key()
    app.run(debug=True)