from flask import Blueprint, current_app, request, render_template, session, flash, redirect, url_for
from extensions import mysql
from passlib.hash import sha256_crypt

lg = Blueprint('auth', __name__)


@lg.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form fields
        username = request.form['username']
        password_candidate = request.form['password']
        
        # create cursor
        cur = mysql.connection.cursor()
        
        # get user by name
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        
        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data['password']
            
            # compare password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                
                flash('You are now logged in!', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid password!"
                return render_template("login.html", error=error)
            
            # close connection
            cur.close()
        
        else:
            error = "Username not found!"
            return render_template("login.html", error=error)
    
    return render_template('login.html')
    
# logout
@lg.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('auth.login'))
    #return str(current_app.url_map)
    
    
    
