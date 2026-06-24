from flask import Flask, render_template_string

app = Flask(__name__)

birds_data = [
    {"id": "1", "name": "Eurasian Eagle-Owl", "desc": "Largest owl species, famous for orange eyes.", "loc": "Carpathian Mountains", "img": "/static/images/eurasian_eagle_owl.jpg"},
    {"id": "2", "name": "Golden Eagle", "desc": "Majestic predator with a 2km vision range.", "loc": "Alpine Peaks", "img": "/static/images/golden_eagle.jpg"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Bird Feed | Pro UI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');
        
        html, body { margin: 0; padding: 0; width: 100%; background: #ffffff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        body { display: flex; justify-content: center; align-items: center; min-height: 100vh; cursor: pointer; }
        
        #feed { width: 100%; max-width: 500px; display: flex; flex-direction: column; align-items: center; }
        
        .post { width: 90%; aspect-ratio: 4/5; border-radius: 24px; overflow: hidden; background: #1a1a1a; position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .post-img { width: 100%; height: 100%; object-fit: cover; display: block; }
        
        .info { position: absolute; bottom: 20px; left: 20px; right: 20px; padding: 20px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px); border-radius: 20px; pointer-events: none; }
        .title { font-size: 1.4rem; font-weight: 700; margin-bottom: 5px; color: #000; }
        .desc { font-size: 0.9rem; color: #555; }
        .loc { font-size: 0.75rem; color: #007aff; font-weight: 600; margin-top: 10px; display: block; }
    </style>
</head>
<body onclick="nextBird()">
    
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

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, birds_data=birds_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)