from flask import Flask, render_template, request, redirect, url_for
from app.routes import auth
from app.db.passwords_handler import PasswordsHandler

app = Flask(__name__)
# / or /home
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
    return render_template('home.html', passwords=passwords)

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
    print("ALLO")
    password_handler.add_password(user_id, username, site, password)
    return redirect("/home")

@app.route('/logout')
def logout():
    response = auth.logout()
    return redirect("/login")
    

def get_secret_key():
    return "SECRET_KEYXQKHJDSQOIUEZ"

if __name__ == "__main__":
    app.secret_key = get_secret_key()
    app.run(debug=True)