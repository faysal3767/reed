import scrapy
class AlldiscountcoursesItem(scrapy.Item):
	# Define variables to be scraped
	courseTitle = scrapy.Field()
	courseLink = scrapy.Field()
	subTitle = scrapy.Field()
	unitSold = scrapy.Field()
	soldOrEnq = scrapy.Field()
	offerPrice = scrapy.Field()
	originalPrice = scrapy.Field()
	savings =  scrapy.Field()
	courseProvider = scrapy.Field()
	haveCpd = scrapy.Field()
	cpdAccreditedBy = scrapy.Field()
	haveProfQual = scrapy.Field()
	isRegulated = scrapy.Field()
