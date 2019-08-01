from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from views import views
from login import lg
from extensions import mysql

app = Flask(__name__)



# config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '342124'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)

app.register_blueprint(lg)
Articles = Articles()

app.register_blueprint(views)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords don't match")
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        # create cursor
        cur = mysql.connection.cursor()
        
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))            
        mysql.connection.commit()
        cur.close()
        
        flash('You are now registered and can login', 'success')
        
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)



# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please log in first', 'danger')
            return redirect(url_for('login'))
    
    return wrap





# login
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')




if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
