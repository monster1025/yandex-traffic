#flask
from flask import Flask, request, jsonify
from traffic import Trafic

app = Flask(__name__)
traffic = Trafic()

@app.route('/report/text/<string:from_lat>,<string:from_lng>;<string:to_lat>,<string:to_lng>', methods=['GET'])
def get_text_report(from_lat, from_lng, to_lat, to_lng):
	report = traffic.get_route_as_text(from_lat, from_lng, to_lat, to_lng)
	return report

@app.route('/report/json/<float:from_lat>,<float:from_lng>;<float:to_lat>,<float:to_lng>', methods=['GET'])
def get_json_report(from_lat, from_lng, to_lat, to_lng):
	report = traffic.get_route_as_json(from_lat, from_lng, to_lat, to_lng)
	return jsonify(report)

@app.route('/report/text/', methods=['POST'])
def post_text_report():
	json = request.get_json()
	from_lat = json.get("from_lat", 0)
	from_lng = json.get("from_lng", 0)
	to_lat = json.get("to_lat", 0)
	to_lng = json.get("to_lng", 0)
	report = traffic.get_route_as_json(from_lat, from_lng, to_lat, to_lng)
	return report

@app.route('/report/json/', methods=['POST'])
def post_json_report():
	json = request.get_json()
	from_lat = json.get("from_lat", 0)
	from_lng = json.get("from_lng", 0)
	to_lat = json.get("to_lat", 0)
	to_lng = json.get("to_lng", 0)
	report = traffic.get_route_as_json(from_lat, from_lng, to_lat, to_lng)
	return jsonify(report)
 

@app.route('/')
def index():
    return '''
    <h1>Yandex traffic reports</h1>
    <pre>GET /report/text/55.67,37.76;55.79,37.66 - get text report</pre>
    <pre>GET /report/json/55.67,37.76;55.79,37.66 - get json report</pre>
    <pre>POST /report/text/ - get text report</pre>
    <pre>POST /report/json/ - get json report</pre>
    <pre>json exmple:</pre>
    <pre>{"from_lat":55.67,"from_lng":37.76, "to_lat":55.79, "to_lng":37.66}</pre>
    '''

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
