from flask import Flask, render_template, redirect, url_for, send_from_directory, session, jsonify
from libs.string import String
from pages.route import Route
from pages.stop import Stop
from pages.auth import Auth
from pages.user import User

app = Flask(__name__, static_url_path='')
app.jinja_env.globals.update(cutnews=String.cutnews)
app.secret_key = 'secret key'

# --------- index ------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
@app.route('/services')
def index():
    return render_template('index.html', tData=[])
    # if Auth.isLogged():
    #     inn = Index()
    #     return render_template('index.html', tData = inn.gettopnews())
    # else:
    #     return redirect(url_for('login'))


@app.route('/trips', methods=['GET'])
def trips():
    route = Route()
    return render_template('trips.html',
                           routes=route.get_routes(),
                           stops=route.get_stops_locations_by_route())


@app.route('/stops', methods=['GET'])
def stops():
    route = Route()
    return render_template('stops.html',
                           routes=route.get_routes(),
                           stops=route.get_stops_by_route())


@app.route('/nearest', methods=['GET'])
def nearest():
    route = Route()
    stop = Stop()
    return render_template('nearest.html',
                           routes=route.get_routes(),
op=stop.get_stop_by_id())


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/user_list')
def user_list():
    if Auth.is_logged() is False:
        return redirect(url_for('login'))

    user = User()
    return render_template('user_list.html', users=user.get_users())


@app.route('/user', methods=['POST', 'GET'])
def user_action():
    if Auth.is_logged() is False:
        return redirect(url_for('login'))

    user = User()
    return user.manage_action(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = Auth()
    return auth.checklogin()


@app.route('/logout')
def logout():
    Auth.logout()
    return redirect(url_for('login'))

# --------------------------------------  API --------------------------------------------------
@app.route('/api/stations', methods=['GET'])
def api_stations():
    stop = Stop()
    return jsonify(stop.get_stations())


@app.route('/api/activate', methods=['GET'])
def api_activate():
    user = User()
    return user.activate()
# ----------------------------------------------------------------------------------------------

# make assets directory accessible from outside
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)


if __name__ == '__main__':
    app.run(port=5000)

