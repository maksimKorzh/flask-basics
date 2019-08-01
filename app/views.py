from flask import render_template, Blueprint

views = Blueprint('views', __name__, template_folder='templates')

@views.route('/')
def index():
    return render_template('home.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@views.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)
