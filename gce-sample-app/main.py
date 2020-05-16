from flask import Flask, render_template, render_template_string, jsonify
from pages.index import Index
from pages.other import Other

app = Flask(__name__)

# report
@app.route("/", methods=["GET"])
def index():
    obj = Index()
    data = obj.getReports()
    return render_template("index.html", data=data)

# sql related work
@app.route("/executeddl", methods=["GET"])
def executeddl():
    ot = Other()
    message = ot.executeDDL()
    return render_template_string("<html><tbody>{}</body></html>".format(message))

@app.route("/importcsv", methods=["GET"])
def importcsv():
    ot = Other()
    message = ot.importCSV()
    return render_template_string("<html><tbody>{}</body></html>".format(message))

# api (conversion, purchase)
@app.route("/api/conversion", methods=["GET"])
def api_convertion():
    idx = Index()
    result = idx.getConvertions()
    return jsonify(result)
    
@app.route("/api/purchase", methods=["GET"])
def api_purchase():
    idx = Index()
    result = idx.getPurchases()
    return jsonify(result)

if __name__ == '__main__':
    #note: if debug is true, hot reloading also work
    app.run(host='127.0.0.1', port=8080, debug=True)