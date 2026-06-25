from flask import Flask, render_template, request, redirect, url_for, session

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

        if action == 'register' and username not in users_db:
            users_db[username] = password
            
        if users_db.get(username) == password:
            session['username'] = username
        else:
            error = "Invalid credentials or username taken!"

    if 'username' not in session:
        # Flask сам ищет файл auth.html в папке templates/
        return render_template('auth.html', error=error)
        
    # Flask сам ищет файл feed.html в папке templates/
    return render_template('feed.html', birds_data=birds_data, username=session['username'])

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)