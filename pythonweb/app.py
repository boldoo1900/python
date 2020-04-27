from flask import Flask, render_template, redirect, url_for, send_from_directory, session
#import sqlite3
#from libs.db import DB
from pages.index import Index
from pages.news import News
from libs.string import String

from pages.auth import Auth
from pages.register import Register
from pages.account import Account
from pages.testExamples import Example
#from config.constants import Constants

app = Flask(__name__, static_url_path='')
app.jinja_env.globals.update(cutnews=String.cutnews)
app.secret_key = 'secret key'

# --------- index ------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    if Auth.isLogged():
        inn = Index()
        return render_template('index.html', tData = inn.gettopnews())
    else:
        return redirect(url_for('login'))

# --------- news ------------------------------------------------------------------------
@app.route('/news')
def news():
    if Auth.isLogged():
        inn = News()
        return render_template('newsList.html', tData = inn.getnews(), is_admin = session["is_admin"])
    else:
        return redirect(url_for('login'))

@app.route('/news/<int:news_id>')
def news_more(news_id):
    if Auth.isLogged():
        inn = News()
        return render_template('newsDetail.html', more_data = inn.getnewsmore(news_id),
                                                  comment_data = inn.getnewscomment(news_id),
                                                  firstname =  session["firstname"],
                                                  lastname =  session["lastname"],
                                                  user_id =  session["user_id"],
                                                  is_admin = session["is_admin"],
                                                  news_id = news_id )
    else:
        return redirect(url_for('login'))

@app.route('/newsadd', methods=['GET', 'POST'])
def newsadd():
    if Auth.isLogged():
        inn = News()
        return inn.newsAdd();
    else:
        return redirect(url_for('login'))

@app.route('/commentadd', methods=['GET', 'POST'])
def commentadd():
    if Auth.isLogged():
        inn = News()
        return inn.commentadd();
    else:
        return redirect(url_for('login'))

@app.route('/commentdelete', methods=['GET', 'POST'])
def commentdelete():
    if Auth.isLogged():
        inn = News()
        return inn.commentdelete();
    else:
        return redirect(url_for('login'))

# --------- registration -----------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    register = Register()
    return register.registerForm(app)

@app.route('/activate', methods=['GET'])
def activate():
    register = Register()
    return register.activate()

@app.route('/account', methods=['GET', 'POST'])
def account():
    acc = Account();
    return acc.actionIndex()

# --------- login -------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    return Auth.checkLogin()

# route for logout
@app.route('/logout')
def logout():
    Auth.Logout()
    return redirect(url_for('login'))

# used for call assets directory
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

# --------- TEST -------------------------------------------------------------------------
@app.route('/test/<postid>')
def posttest(postid):
    return Example.testcsv(postid)

# -------------------------------------------------------------------------------------------
# APP RUN
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # dbconn = DB()
    # result = dbconn.execute("SELECT * FROM user;")
    # print(result)

    # conn = sqlite3.connectR(Constants.FILES_DIR+"\\testdb.db")
    # cursor = conn.execute("SELECT * FROM user")
    # for row in cursor:
    #     print(row)

    #Example.strreverse('1234567fasdfasd')
    #Example.testfile([5, 7, 8, 23, 1, 0])
    #Example.testtable()
    #Example.testcsv(1840004)
    #Example.getaddressbypostalcode()

    app.run(port=5000)
