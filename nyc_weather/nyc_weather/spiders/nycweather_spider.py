from scrapy 			import Spider, Request
from nyc_weather.items 	import NycWeatherItem
from datetime 			import date, timedelta

class NycWeatherSpider(Spider):

	name         = "nyc_weather_spider"
	allowed_urls = ["https://www.wunderground.com/history/airport"]
	start_urls   = ["https://www.wunderground.com/history/airport"]

	def parse(self, response):

		# calculate total date range:
		def gen_dates():
			step = timedelta(days=1)
			d    = date(2012, 7, 1)  #start date 
			end  = date(2018, 2, 1)  #end date exclusive

			while d < end:
				yield d
				d += step # have tested on jupyter notebook: works.

		# high qulaity weather stations for NYC:
		weather_stations = [["KNYC", 40.780487  , -73.971340 ], # central park observation station, NYC
							["KJFK", 40.6399257 , -73.7786950], # John F. Kennedy airport
							["KEWR", 40.6924798 , -74.1686868], # Newark airport
							["KLGA", 40.7772500 , -73.8726111]]	# Laguardia airport	

		root_url = "https://www.wunderground.com/history/airport"
		
		lst = weather_stations[3]
		#for lst in weather_stations: #lst = weather_stations[1]
		gen_d = gen_dates()
		for idx, d in enumerate(gen_d):
			link = "{0}/{1}/{2}/{3}/{4}/DailyHistory.html".format(\
				   root_url, lst[0], d.year, d.month, d.day)

			yield Request(link, callback=self.parse_top, priority = idx, \
				          meta={'station': lst[0], 'lati': lst[1], 'longi': lst[2], 'date': d})

	def parse_top(self, response):

		# This is the data format of the webpage for one line of data items.
		# txt means text, num means number.
		# [column name,   item name, type]
		line_format = \
			{'Time ': 		['time',		'txt'],\
			 'Temp.': 		['temp',		'num'],\
			 'Windchill': 	['temp2',		'num'],\
			 'Heat Index': 	['temp2',		'num'],\
			 'Dew Point': 	['dewpoint', 	'num'],\
			 'Humidity': 	['humi', 		'txt'],\
			 'Pressure': 	['pressure', 	'num'],\
			 'Visibility': 	['visi', 		'num'],\
			 'Wind Dir': 	['winddir', 	'txt'],\
			 'Wind Speed': 	['windspeed', 	'num'],\
			 'Gust Speed': 	['gustspeed', 	'num'],\
			 'Precip': 		['precip',		'num'],\
			 'Events': 		['events',		'txt'],\
			 'Conditions': 	['conditions',	'txt']}

		# get header column names of each data item on a line:
		names = response.xpath('//div[@id="observations_details"]//thead//th/text()').extract()

		line_items = []

		# figure out actual data items on this particular page:
		for idx, name_ in enumerate(names):
			line_items.append([idx] + line_format[name_]) # [item_idx, item_name, type]

		lines = response.xpath('//div[@id="observations_details"]//tr[@class="no-metars"]')

		for line in lines:
			d_items = line.xpath('./td')

			item = NycWeatherItem() 

			def grab_line_item(item_idx, item_name, type):
				if type == 'num':
					tmp = d_items[item_idx].xpath('.//span[@class="wx-value"]/text()').extract_first()							
				else:
					tmp = d_items[item_idx].xpath('./text()').extract_first()

				tmp	= tmp.strip() if tmp != None else 'na'	

				item[item_name]	= 'na' if tmp == '' else tmp			

			for lst in line_items:
				grab_line_item(*lst)

			item['humi']    = item['humi'].strip('%')

			item['station']	= response.meta['station']
			item['longi']	= response.meta['longi']
			item['lati']	= response.meta['lati']
			item['date']	= response.meta['date'].isoformat()

			yield item