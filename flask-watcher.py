from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key' 

users_db = {}

birds_data = [
    {"id": "1", "name": "Eurasian Eagle-Owl", "desc": "Largest owl species, famous for orange eyes.", "loc": "Carpathian Mountains", "img": "/static/images/eurasian_eagle_owl.jpg"},
    {"id": "2", "name": "Golden Eagle", "desc": "Majestic predator with a 2km vision range.", "loc": "Alpine Peaks", "img": "/static/images/golden_eagle.jpg"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        action = request.form.get('action')

        if action == 'register':
            if username in users_db:
                error = "Username already exists!"
            elif len(password) < 5: 
                error = "Password must be at least 5 characters long!"
            else:
                users_db[username] = generate_password_hash(password)
                session['username'] = username
                
        elif action == 'login':
            saved_hash = users_db.get(username)
            if saved_hash and check_password_hash(saved_hash, password):
                session['username'] = username
            else:
                error = "Invalid credentials!"

    if 'username' not in session:
        return render_template('auth.html', error=error)
        
    return render_template('feed.html', birds_data=birds_data, username=session['username'])

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)