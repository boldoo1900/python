
database - sqlite


#must install libraries
	pip install flask	-- python web development framework
	pip install Flask-Mail

	# mysql library installation
	brew install mysql-client
    echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile
    source ~/.bash_profile
    pip install mysqlclient
    or
    pip install flask-mysqldb

error fixes
    .flaskenv uses this plugin
    pip3 install python-dotenv

    use 5000 or higher ports when u using system interpreter