import requests
import codecs
import re
import json
import sys

class Trafic:
	def __init__(self, lang = "ru_RU"):
		self.session = requests.Session()
		self.lang = lang
		self.token = self._get_token()

	def _get_token(self):
		setup = self.session.get("https://api-maps.yandex.ru/2.1/?lang=" + self.lang)
		m = re.findall('\"token\":\"(.+?)\"', setup.text)
		token = m[0]
		return token

	def get_route(self, from_lat, from_lng, to_lat, to_lng, results=2):
		js = self._get_route_json(from_lat, from_lng, to_lat, to_lng, results)
		routes = self._parse_route_json(js)
		return routes
	
	def get_route_as_text(self, from_lat, from_lng, to_lat, to_lng, results=2):
		js = self._get_route_json(from_lat, from_lng, to_lat, to_lng, results)
		routes = self._parse_route_json(js)
		report = self.format_report_as_text(routes)
		return report

	def get_route_as_json(self, from_lat, from_lng, to_lat, to_lng, results=2):
		js = self._get_route_json(from_lat, from_lng, to_lat, to_lng, results)
		routes = self._parse_route_json(js)
		report = self.format_report_as_json(routes)
		return report

	def format_report_as_json(self, routes):
		data = dict({})
		data['reports'] = []
		for route in routes:
			data['min_duration_text'] = route.durationText
			data['min_duration_value'] = route.durationVal
			report = ""
			for routeItem in route.routeItems:
				if (routeItem.distanceVal > 1000 or (routeItem.distanceVal > 500 and routeItem.avgspeed < 40) or routeItem.durationVal > 2*60):
					line = (routeItem.street + " - " + routeItem.durationText + " (расстояние: " + routeItem.distanceText + "; скорость: " + str(routeItem.avgspeed) + " км\ч)")
					report = report + "\n" +  line
			data['reports'].append(report)
		return data

	def format_report_as_text(self, routes):
		report = ""
		delim = "-----------------------------"
		for route in routes:
			line = "Время в пути: " + route.durationText
			report = report + "\n" + line
			for routeItem in route.routeItems:
				# print(routeItem)
				if (routeItem.distanceVal > 1000 or (routeItem.distanceVal > 500 and routeItem.avgspeed < 40) or routeItem.durationVal > 2*60):
					line = (routeItem.street + " - " + routeItem.durationText + " (расстояние: " + routeItem.distanceText + "; скорость: " + str(routeItem.avgspeed) + " км\ч)")
					report = report + "\n" +  line
			report = report + "\n" + delim
		return report[1:-1*(len(delim)+1)]

	def _get_route_json(self, from_lat, from_lng, to_lat, to_lng, results=2):
		routeURL = "https://api-maps.yandex.ru/services/route/2.0/"
		path = str(from_lng) + "," + str(from_lat) + "~" + str(to_lng) + "," + str(to_lat)
		payload = {'lang': self.lang, 'token': self.token, 'rtm':'atm', 'results':results, 'rll': path}
		resp = self.session.get(routeURL, params=payload)
		return resp.json()

	def _parse_route_json(self, js):
		routes = []
		jsroutes = js['data']['features']
		for jsroute in jsroutes:
			properties = jsroute['properties']
			metadata = properties['RouteMetaData']
			rtdurationText = metadata['DurationInTraffic']['text']
			rtdurationVal = metadata['DurationInTraffic']['value']

			routeItems = []
			routeGroups = jsroute['features']
			for routeGroup in routeGroups:
				routeGroupFeatures = routeGroup['features']
				
				# for f in routeGroup['features']:
				for i in range(0,len(routeGroupFeatures)):
					f = routeGroupFeatures[i]
					segmentMetaData = f['properties']['SegmentMetaData']
					street = segmentMetaData['street']
					# turns have no street - so skip them to allow correct grouping
					if (street == ''):
						# street = segmentMetaData['text'] + ' на ' + routeGroupFeatures[i+1]['properties']['SegmentMetaData']['street']
						# street = segmentMetaData['text']
						continue

					durationText = segmentMetaData['Duration']['text']
					durationVal = segmentMetaData['DurationInTraffic']['value']
					distanceText = segmentMetaData['Distance']['text']
					distanceVal = segmentMetaData['Distance']['value']

					routeItem = RouteItem(street, durationText, durationVal, distanceText, distanceVal)
					routeItems.append(routeItem)
			route = Route(rtdurationText, rtdurationVal, routeItems)
			route.group()
			routes.append(route)
		return routes

class Route:
	def __init__(self, durationText, durationVal, routeItems):
		self.durationText = durationText
		self.durationVal = durationVal
		self.routeItems = routeItems

	def group(self):
		r = 1
		while r > 0:
			r = self._group()

	def _group(self):
		groupped = 0
		tmpRouteItems = []
		skip = []
		for i in range(0, len(self.routeItems)):
			if (i in skip):
				continue

			routeItem = self.routeItems[i]
			if (i < (len(self.routeItems)-1) and routeItem.street == self.routeItems[i+1].street):
				nextItem = self.routeItems[i+1]
				# print("duplicate found: " + routeItem.street)
				street = routeItem.street
				durationVal = routeItem.durationVal + nextItem.durationVal
				distanceVal = routeItem.distanceVal + nextItem.distanceVal

				distanceText = self.format_dist(routeItem.distanceVal)
				durationText = self.format_time(routeItem.durationVal)
				route = RouteItem(street, durationText, durationVal, distanceText, distanceVal)
				tmpRouteItems.append(route)
				skip.append(i+1)
				groupped = groupped + 1
			else:
				tmpRouteItems.append(routeItem)
		self.routeItems = tmpRouteItems
		return groupped

	def format_dist(self, val):
		unit = 'м'
		if (val > 1000):
			val = val / 1000
			unit = 'км'
		
		if val == round(val,1):
			val = int(val)
		else:
			val = round(val,1)

		return self.dot2zap(str(val)) + ' ' + unit

	def format_time(self, val):
		unit = 'сек'
		if (val > 60):
			val = val / 60
			unit = 'мин'
		if (unit == 'мин' and val > 60):
			val = val / 60
			unit = 'час'
		val = int(val)
		return self.dot2zap(str(val)) + ' ' + unit
	def dot2zap(self, string):
		return string.replace(".", ",")

class RouteItem:
	def __init__(self, street, durationText, durationVal, distanceText, distanceVal):
		self.street = street
		self.durationText = durationText
		self.durationVal = durationVal
		self.distanceText = distanceText
		self.distanceVal = distanceVal
		self.avgspeed = round(self.distanceVal / self.durationVal * 3.6)