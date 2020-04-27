from flask import render_template, request, url_for, redirect, flash
from flask_mail import Mail, Message
from config.constants import Constants
from libs.script import Script
from time import gmtime, strftime
from libs.controller import Controller
from libs.fileupload import fileUpload

class Register(Controller):
    error = ''

    def registerForm(self, app):
        if request.method == 'POST':
            if self.mvalidate(request.form) is True:
                extension = ''
                if 'file' in request.files:
                    extension = request.files['file'].filename.rsplit('.', 1)[1]

                filename = Script.getfilename("user")+'.'+extension
                self.error = fileUpload.upload(request.files, filename)

                self.save(request.form, filename)
                self.sendMail(app, request.form)

                flash('Registration is not finished yet, Check your mail and activate your account.')
                return redirect(url_for('index'))

        return render_template('register.html', error=self.error, params=request.form)

    def mvalidate(self, form):
        self.error = ''
        if form['mail'] == "":
            self.error = '- mail is not filled<br>'
        if form['password'] == "":
            self.error += '- password is not filled<br>'
        if form['cpassword'] == "":
            self.error += '- confirm password is not filled<br>'
        if form['firstname'] == "":
            self.error += '- firstname is not filled<br>'
        if form['lastname'] == "":
            self.error += '- lastname is not filled<br>'
        if len(form.getlist('is_accepted')) == 0:
            self.error += '- terms is not checked<br>'
        if form['password'] != "" and form['cpassword'] != "":
            if form['password'] != form['cpassword']:
                self.error += "- password is not match<br>"

        if form['mail'] != "":
            if self.mailcheck(form['mail']) is True:
                self.error += '- Email Address already registered<br>'

        if self.error != "":
            return False
        else:
            return True

    def save(self, form, filename):
        queries = ["INSERT INTO user(username, password, firstname, lastname, is_admin, is_active, birth_date, image, date) "
                   "VALUES('{0}','{1}','{2}','{3}','0','0','{4}', '{5}', current_timestamp);".format(
            form['mail'],
            form['password'],
            form['firstname'],
            form['lastname'],
            form['birth_date'],
            '\\asssets\\upload'+filename )]
        self.dbconn.execute(queries);

    def mailcheck(self, mail):
        queries = ["SELECT username FROM user where username = '{0}' LIMIT 1;".format(mail)]
        result = self.dbconn.execute(queries);
        if len(result) > 0:
            return True;
        else:
            return False;

    def sendMail(self, app, form):
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = Constants.ADMIN_MAIL_ADDR
        app.config['MAIL_PASSWORD'] = Constants.ADMIN_MAIL_PASS
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)

        #generate encrypt key
        encryptkey = Script.encode(form['mail'])

        # read file and prepare mail body
        txtBody = ''
        with open(Constants.MAIL_TEMPLATE_FILE) as f:
            content = f.readlines()
            #content = [x.strip() for x in content]
            for row in content:
                row = row.replace("%ACTIVATION_LINK%", "http://localhost/activate?mail={0}&encryptkey={1}".format(form['mail'], encryptkey))
                row = row.replace("%MAIL_ADDRESS%", form['mail'])
                row = row.replace("%FIRSTNAME%", form['firstname'])
                row = row.replace("%REGISTRATION_DATE%", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                txtBody +=row

        msg = Message('Registration', sender = Constants.ADMIN_MAIL_ADDR, recipients = [form['mail']])
        msg.body = txtBody
        mail.send(msg)

    def activate(self):
        if(Script.encode(request.args['mail']) == request.args['encryptkey']):
            queries = ["UPDATE user SET is_active = 1 WHERE username='{0}';".format(request.args['mail'])]
            self.dbconn.execute(queries);
            flash('Your account is activated successfully. Login using your email address.')
        else:
            flash('Your activation link is not right, check your mail again!!!')

        return redirect(url_for('login'))








