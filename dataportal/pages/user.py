from flask import render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from time import gmtime, strftime

from libs.controller import Controller
from libs.script import Script
from config.constants import Constants

class User(Controller):

    def manage_action(self, app):
        error = ''

        if request.method == 'GET':
            if request.args.get('action') == "add":
                return render_template('user_form.htm', error=error)
            elif request.args.get('action') == "edit":
                return render_template('user_form.htm', error=error)
            else:
                return self.register(app)
        else:
            return self.register(app)

    def register(self, app):
        if request.method == 'POST':
            if request.form["action"] == "add":
                queries = ["insert into user(username,password,first_name,last_name,mail,address,role,is_active) "
                           "VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}',{7})".format(request.form['username'],
                                                                                          request.form['password'],
                                                                                          request.form['first_name'],
                                                                                          request.form['last_name'],
                                                                                          request.form['mail'],
                                                                                          request.form['address'],
                                                                                          'basic',
                                                                                          0)]
                self.conn.execute(queries)
                self.sendMail(app, request.form)
            elif request.method == 'POST' & request.form["action"] == "edit":
                queries = ["update user set first_name = {0}, last_name = {1}, mail = {2}, address = {3}) "
                           "VALUES('{0}','{1}', '{2}')".format(request.form['first_name'],
                                                               request.form['last_name'],
                                                               request.form['mail'],
                                                               request.form['address'])]
                self.conn.execute(queries)
                self.sendMail(app, request.form)
        else:
            queries = ["delete from user where user_id = {0} ".format(request.args.get('user_id'))]
            self.conn.execute(queries)

        flash('Success.')
        return redirect(url_for('user_list'))

    def get_users(self):
        query = ["select * from user where role <> 'super'"]
        return self.conn.execute(query)

    def sendMail(self, app, form):
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = Constants.ADMIN_MAIL_ADDR
        app.config['MAIL_PASSWORD'] = Constants.ADMIN_MAIL_PASS
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)

        # generate encrypt key
        encryptkey = Script.encode(form['mail'])

        # read file and prepare mail body
        txtBody = ''
        with open(Constants.MAIL_TEMPLATE_FILE) as f:
            content = f.readlines()
            # content = [x.strip() for x in content]
            for row in content:
                row = row.replace("%ACTIVATION_LINK%", "http://127.0.0.1:5000/api/activate?mail={0}&encryptkey={1}".format(form['mail'], encryptkey))
                row = row.replace("%MAIL_ADDRESS%", form['mail'])
                row = row.replace("%FIRSTNAME%", form['first_name'])
                row = row.replace("%REGISTRATION_DATE%", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                txtBody +=row

        msg = Message('Registration', sender=Constants.ADMIN_MAIL_ADDR, recipients=[form['mail']])
        msg.body = txtBody
        mail.send(msg)

    def activate(self):
        if Script.encode(request.args['mail']) == request.args['encryptkey']:
            queries = ["UPDATE user SET is_active = 1 WHERE mail='{0}';".format(request.args['mail'])]
            self.conn.execute(queries)
            flash('Your account is activated successfully. Login using your email address.')
        else:
            flash('Your activation link is not right, check your mail again!!!')

        return redirect(url_for('user_list'))
