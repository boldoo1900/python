from flask import render_template, redirect, url_for, request, session, flash
from libs.db import DB
from config.constants import Constants


class Auth(object):
    @staticmethod
    def checkLogin():
        if Auth.isLogged():
            return redirect(url_for('index'))

        error = None
        if request.method == 'POST':
            if request.form['username'] == "" or request.form['password'] == "":
                error = 'username or password is not filled'
            else:
                dbconn = DB()

                # retrieving multiple query results
                queries = ["SELECT * FROM user where username = '{0}' AND password = '{1}' LIMIT 1;".format(
                    request.form['username'], request.form['password'])]
                result = dbconn.execute(queries);
                if len(result) < 1:
                    error = 'Invalid Username/Password.'
                else:
                    if result[0][6] == 1:
                        session["auth"] = True
                        session["user_id"] = result[0][0]
                        session["username"] = result[0][1]
                        session["firstname"] = result[0][3]
                        session["lastname"] = result[0][4]
                        session["is_admin"] = (True if result[0][5] == 1 else False)
                        return redirect(url_for('index'))
                    else:
                        error = 'Account is not activated yet, Please check your mail and activate your account'

        return render_template('login.html', error=error)

    @staticmethod
    def isLogged():
        if 'auth' in session:
            if session["auth"]:
                return True
            else:
                return redirect(url_for('login'))
        else:
            return False

    @staticmethod
    def Logout():
        session.clear();
        flash('You are logged out')