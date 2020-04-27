from flask import render_template, redirect, url_for, request, session, flash
from libs.controller import Controller
# from config.constants import Constants


class Auth(Controller):
    def checklogin(self):
        if Auth.is_logged():
            return redirect(url_for('index'))

        error = None
        if request.method == 'POST':
            if request.form['username'] == "" or request.form['password'] == "":
                error = 'username or password is not filled'
            else:
                # retrieving multiple query results
                queries = ["select * from user where username = '{0}' AND password = '{1}' LIMIT 1;".format(
                    request.form['username'],
                    request.form['password'])]

                result = self.conn.execute(queries)

                if len(result) < 1:
                    error = 'Invalid Username/Password.'
                else:
                    if result[0]["is_active"] == 1:
                        session["auth"] = True
                        session["user_id"] = result[0]["user_id"]
                        session["username"] = result[0]["username"]

                        return redirect(url_for('index'))
                    else:
                        error = 'Account is not activated yet, Please check your mail and activate your account'

        return render_template('login.html', error=error)

    @staticmethod
    def is_logged():
        if 'auth' in session:
            if session["auth"]:
                return True
            else:
                return redirect(url_for('login'))
        else:
            return False

    @staticmethod
    def logout():
        session.clear()
        # flash('You have been successfully logged out of your account')
