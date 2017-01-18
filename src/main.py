#flask
from flask import Flask, request
from traffic import Trafic

app = Flask(__name__)
traffic = Trafic()

@app.route('/report/json/<float:from_lat>,<float:from_lng>;<float:to_lat>,<float:to_lng>', methods=['GET'])
def get_json_report(from_lat, from_lng, to_lat, to_lng):
	report = traffic.get_route_as_json(from_lat, from_lng, to_lat, to_lng)
	return format(report)

@app.route('/report/text/<string:from_lat>,<string:from_lng>;<string:to_lat>,<string:to_lng>', methods=['GET'])
def get_text_report(from_lat, from_lng, to_lat, to_lng):
	report = traffic.get_route_as_text(from_lat, from_lng, to_lat, to_lng)
	return report

@app.route('/')
def index():
    return '''
    <h1>Yandex traffic reports</h1>
    <pre>/report/text/55.67,37.76;55.79,37.66 - get text report</pre>
    <pre>/report/json/55.67,37.76;55.79,37.66 - get json report</pre>
    '''

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')