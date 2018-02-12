# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class NycWeatherItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    station 	= Field()
    longi 		= Field()
    lati  		= Field()
    date 		= Field()
    time 		= Field()
    temp 		= Field()
    temp2 		= Field()  # for either Windchill or Heat Index temp  
    dewpoint  	= Field()
    humi 		= Field()
    pressure 	= Field()
    visi 		= Field()
    winddir 	= Field()
    windspeed 	= Field()
    gustspeed 	= Field()
    precip 		= Field()
    events 		= Field()
    conditions 	= Field()

