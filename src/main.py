#encoding=utf-8
import logging
import datetime
import calendar
import time
import threading

from traffic import Trafic
import yamlparser
import mqtt

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

traffic = Trafic()

def process_traffic(client, home_latitude, home_longitude, work_latitude, work_longitude, interval):
	while True:
		try:
			home_to_work=traffic.get_route_as_json(home_latitude, home_longitude, work_latitude, work_longitude)
			work_to_home=traffic.get_route_as_json(work_latitude, work_longitude, home_latitude, home_longitude)
			data = dict({
				"home_to_work_time": home_to_work['min_duration_value'], 
				"home_to_work_text": home_to_work['reports'][0], 
				"work_to_home_time": work_to_home['min_duration_value'],
				"work_to_home_text": work_to_home['reports'][0]
			})
			mqttclient.publish("yandex", "traffic", data, False)
		except Exception as e:
			_LOGGER.error('Error while retrieving data from yandex: ', str(e))
		time.sleep(interval)

if __name__ == "__main__":
	global mqttclient
	_LOGGER.info("Loading config file...")
	config=yamlparser.load_yaml('config/config.yaml')

	_LOGGER.info("Init mqtt client.")
	client = mqtt.Mqtt(config)
	client.connect()
	mqttclient = client

	yandex = config.get("yandex", None)
	if yandex == None:
		_LOGGER.error("yandex not defined in config")

	home_latitude = yandex.get("home_latitude", 0)
	home_longitude = yandex.get("home_longitude", 0)
	work_latitude = yandex.get("work_latitude", 0)
	work_longitude = yandex.get("work_longitude", 0)
	interval = yandex.get("interval", 60)

	t1 = threading.Thread(target=process_traffic, args=[client, home_latitude, home_longitude, work_latitude, work_longitude, interval])
	t1.daemon = True
	t1.start()

	while True:
		time.sleep(10)