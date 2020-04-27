from libs.db import DB
from flask import render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime

class News(object):
    dbconn = None
    error = ''

    def __init__(self):
        self.dbconn = DB()

    def getnews(self):
        queries = ["SELECT * FROM news ORDER BY DATE DESC;"]
        result = self.dbconn.execute(queries);
        return result;

    def getnewsmore(self, news_id):
        queries = ["SELECT * FROM news WHERE id = {0} ORDER BY DATE DESC;".format(news_id)]
        result = self.dbconn.execute(queries);
        return result;

    def getnewscomment(self, news_id):
        queries = ["SELECT a.id, b.firstname, b.lastname, a.comment, a.comment_date "
                   "FROM comment a INNER JOIN user b ON b.id=a.user_id WHERE a.news_id={0} ORDER BY DATE DESC;".format(news_id)]
        result = self.dbconn.execute(queries);
        return result;

    #------------------------------ news add ---------------------------------------------------------------------------
    def newsAdd(self):
        if request.method == 'POST':
            if self.mvalidate(request.form) is True:
                dbconn = DB()
                queries = ["INSERT INTO news(title, content, date, image) VALUES('{0}','{1}', current_timestamp, '{2}');".format(
                    request.form['title'],
                    request.form['content'],
                    '', )]
                dbconn.execute(queries);

                flash('News succesfully added.')
                return redirect(url_for('news'))

        return render_template('newsAdd.html', error=self.error, params=request.form)

    def mvalidate(self, form):
        self.error = ''
        if form['title'] == "":
            self.error = '- title is not filled<br>'
        if form['content'] == "":
            self.error += '- content is not filled<br>'

        if self.error != "":
            return False
        else:
            return True

    #------------------------------ comment add ------------------------------------------------------------------------
    def commentadd(self):
        if request.method == 'POST':
            ctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
            dbconn = DB()
            queries = ["INSERT INTO comment(user_id, news_id, comment, comment_date) VALUES('{0}','{1}', '{2}', '{3}');".format(
                        request.form['user_id'],
                        request.form['news_id'],
                        request.form['comment'],
                        ctime)]
            result = dbconn.execute(queries);

        return jsonify([{ 'date':ctime, 'comment_id':result }])

    #------------------------------ comment delete ---------------------------------------------------------------------
    def commentdelete(self):
        if request.method == 'POST':
            dbconn = DB()
            queries = ["DELETE FROM comment WHERE id= '{0}';".format(request.form['comment_id'])]
            dbconn.execute(queries);

        return jsonify([{ 'status':'success' }])