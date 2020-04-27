from flask import render_template, request, url_for, redirect, flash, session
from libs.controller import Controller

class Account(Controller):
    error = ''

    def actionIndex(self):
        if request.method == 'POST':
            if self.mvalidate(request.form) is True:
                self.update(request.form)
                flash('Account information successfully updated.')
                return redirect(url_for('index'))

        return render_template('account.html', error=self.error, userinfo=self.getAccountInfo(), params=request.form)

    def mvalidate(self, form):
        self.error = ''
        if form['firstname'] == "":
            self.error += '- firstname is not filled<br>'
        if form['lastname'] == "":
            self.error += '- lastname is not filled<br>'
        if len(form.getlist('is_accepted')) == 0:
            self.error += '- terms is not checked<br>'
        if form['password'] != "" or form['cpassword'] != "":
            if form['password'] != form['cpassword']:
                self.error += "- password is not match<br>"

        if self.error != "":
            return False
        else:
            return True

    def update(self, form):
        queries = ["UPDATE user SET password=(CASE '{0}' WHEN '{0}' == '' THEN password ELSE '{0}' END), "
                                   "firstname='{1}', lastname='{2}', birth_date='{3}', image='{4}', date=current_timestamp "
                   "WHERE id='{5}';".format(
            form['password'],
            form['firstname'],
            form['lastname'],
            form['birth_date'],
            '',
            session["user_id"])]
        self.dbconn.execute(queries);

        session["firstname"] = form['firstname']
        session["lastname"] = form['lastname']

    def getAccountInfo(self):
        queries = ["SELECT username, firstname, lastname, is_admin, birth_date, image "
                   "FROM user WHERE id={0};".format(session["user_id"])]
        result = self.dbconn.execute(queries);
        return result;