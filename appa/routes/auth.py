from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        form_username = request.form.get('username')
        action = request.form.get('action')
       
        if not form_username:
            error = "Username is required!"
            return render_template('auth.html', error=error)
       
        if action == 'register':
            existing_user = User.query.filter_by(login=form_username).first()
            if not existing_user:
                new_user = User(login=form_username, password="dummy_password")
                db.session.add(new_user)
                db.session.flush()
                db.session.commit()
                
                session['user_id'] = new_user.id
                session['username'] = new_user.login
                return redirect(url_for('feed.show_feed'))
            else:
                error = "Username already taken!"
                return render_template('auth.html', error=error)
            
        elif action == 'login':
            user = User.query.filter_by(login=form_username).first()
            if user:
                session['user_id'] = user.id
                session['username'] = user.login
                return redirect(url_for('feed.show_feed'))
            else: 
                error = "User not found! Register first."
                return render_template('auth.html', error=error)
    
    return render_template('auth.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))

           
               
               
