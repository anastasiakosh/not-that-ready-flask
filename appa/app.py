from flask import Flask 
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super_secret_key'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://developer:qwery12345@localhost:3307/birds_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from routes.auth import auth_bp
    from routes.feed import feed_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(feed_bp)
    
    with app.app_context():
        db.create_all()
        
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    