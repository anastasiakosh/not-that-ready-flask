from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key' 

users_db = {}

birds_data = [
    {"id": "1", "name": "Eurasian Eagle-Owl", "desc": "Largest owl species, famous for orange eyes.", "loc": "Carpathian Mountains", "img": "/static/images/eurasian_eagle_owl.jpg"},
    {"id": "2", "name": "Golden Eagle", "desc": "Majestic predator with a 2km vision range.", "loc": "Alpine Peaks", "img": "/static/images/golden_eagle.jpg"}
]

AUTH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BirdTok | Login</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');
        
        html, body { 
            margin: 0; padding: 0; width: 100%; height: 100vh; 
            background: #f0f4f8; /* Мягкий светлый фон */
            font-family: 'Inter', sans-serif; 
            display: flex; justify-content: center; align-items: center; 
        }
        
        .auth-container { 
            width: 90%; max-width: 380px; 
            background: #ffffff; /* Белая карточка */
            color: #111111; /* Темный текст */
            border-radius: 24px; 
            padding: 40px 30px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.08); /* Мягкая тень */
            text-align: center;
            box-sizing: border-box;
        }
        
        h3 { 
            margin: 0 0 30px 0; 
            font-size: 1.8rem; 
            font-weight: 700; 
            letter-spacing: -0.5px; 
        }
        
        .alert { 
            background: #ffe6e6; 
            color: #d93025; 
            border: 1px solid #f5c2c7;
            padding: 12px; 
            border-radius: 16px; 
            margin-bottom: 20px; 
            font-size: 0.9rem; 
            font-weight: 500;
        }
        
        input { 
            width: 100%; 
            padding: 16px 20px; 
            margin-bottom: 16px; 
            background: #f9f9f9; 
            border: 1px solid #e0e0e0; 
            color: #111; 
            border-radius: 16px; 
            font-size: 1rem; 
            font-family: 'Inter', sans-serif;
            box-sizing: border-box; 
            outline: none; 
            transition: all 0.3s ease;
        }
        
        input::placeholder { color: #999; }
        
        input:focus { 
            border-color: #bbb; 
            background: #fff; 
        }
        
        .btn { 
            width: 100%; 
            padding: 16px; 
            border: none; 
            border-radius: 16px; 
            font-size: 1rem; 
            font-weight: 700; 
            font-family: 'Inter', sans-serif; 
            cursor: pointer; 
            transition: 0.2s; 
        }
        
        .btn-login { 
            background: #111; /* Черная кнопка */
            color: #fff; 
            margin-bottom: 12px; 
        }
        
        .btn-login:hover { background: #333; }
        
        .btn-register { 
            background: transparent; 
            color: #555; 
            border: 1px solid #ccc; 
        }
        
        .btn-register:hover { 
            background: #f0f0f0; 
            color: #111; 
            border-color: #999; 
        }
    </style>
</head>
<body>
    <div class="auth-container">
        <h3>BirdTok</h3>
        
        {% if error %}<div class="alert">{{ error }}</div>{% endif %}
        
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            
            <button type="submit" name="action" value="login" class="btn btn-login">Login</button>
            <button type="submit" name="action" value="register" class="btn btn-register">Create Account</button>
        </form>
    </div>
</body>
</html>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Bird Feed | Pro UI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');
        
        html, body { margin: 0; padding: 0; width: 100%; background: #f0f4f8; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        body { display: flex; justify-content: center; align-items: center; min-height: 100vh; cursor: pointer; }
        
        #feed { width: 100%; max-width: 500px; display: flex; flex-direction: column; align-items: center; }
        
        .post { width: 90%; aspect-ratio: 4/5; border-radius: 24px; overflow: hidden; background: #fff; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
        .post-img { width: 100%; height: 100%; object-fit: cover; display: block; }
        
        .info { position: absolute; bottom: 20px; left: 20px; right: 20px; padding: 20px; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); border-radius: 20px; pointer-events: none; }
        .title { font-size: 1.4rem; font-weight: 700; margin-bottom: 5px; color: #111; }
        .desc { font-size: 0.9rem; color: #444; }
        .loc { font-size: 0.75rem; color: #007aff; font-weight: 600; margin-top: 10px; display: block; }
        
        .logout-btn { position: absolute; top: 20px; right: 20px; background: #fff; color: #111; border: 1px solid #ddd; padding: 8px 15px; border-radius: 20px; text-decoration: none; font-family: 'Inter', sans-serif; font-size: 0.9rem; font-weight: 500; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: 0.2s;}
        .logout-btn:hover { background: #f9f9f9; border-color: #bbb; }
    </style>
</head>
<body onclick="if(event.target.tagName !== 'A') nextBird()">
    
    <a href="/logout" class="logout-btn">Logout ({{ username }})</a>

    <div id="feed">
        <div class="post">
            <img id="bird-img" class="post-img" src="{{ birds_data[0].img }}" alt="Bird">
            <div class="info">
                <div id="bird-name" class="title">{{ birds_data[0].name }}</div>
                <div id="bird-desc" class="desc">{{ birds_data[0].desc }}</div>
                <span id="bird-loc" class="loc">{{ birds_data[0].loc }}</span>
            </div>
        </div>
    </div>

    <script>
        const birds = {{ birds_data | tojson | safe }};
        let currentIndex = 0;

        function nextBird() {
            currentIndex = (currentIndex + 1) % birds.length;
            
            document.getElementById('bird-img').src = birds[currentIndex].img;
            document.getElementById('bird-name').innerText = birds[currentIndex].name;
            document.getElementById('bird-desc').innerText = birds[currentIndex].desc;
            document.getElementById('bird-loc').innerText = birds[currentIndex].loc;
        }
    </script>
</body>
</html>
"""

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
        return render_template_string(AUTH_TEMPLATE, error=error)
        
    return render_template_string(HTML_TEMPLATE, birds_data=birds_data, username=session['username'])

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)