# Import item modules and item class
import scrapy
from allDiscountCourses.items import AlldiscountcoursesItem


class AllDiscountCoursesSpider(scrapy.Spider):
	name = "allDiscountCourses"
	start_urls = ["https://www.reed.co.uk/courses/discount"] # All discount courses


	# Go to next page
	def parse(self, response):
		nextPageUrl = response.xpath("//a[@title='Go to next page']/@href")
		for item in self.scrapeTitleAndLink(response):
			yield item

		# Check if next page url exists
		if nextPageUrl:
			path = nextPageUrl.extract_first()
			nextPage = response.urljoin(path)
			print("Found url: {}".format(nextPage))
			yield scrapy.Request(nextPage, dont_filter=True, callback=self.parse)

	# Scrape course title and course link
	def scrapeTitleAndLink(self, response):
		for resource in response.css("div.desktop-main-content"): # Main container
			item = AlldiscountcoursesItem()
			item["courseTitle"] = resource.css("h2.mt-4.mt-sm-1.mr-5.mb-0 a::text").extract_first()
			indvidualCourseLink = response.urljoin(resource.css("h2.mt-4.mt-sm-1.mr-5.mb-0 a::attr(href)").extract_first())
			item["courseLink"] = indvidualCourseLink
			request = scrapy.Request(indvidualCourseLink, callback=self.getInside) # To get inside of individual course page
			request.meta["item"] = item
			yield request

	# Get inside of the page and scrape items
	def getInside(self, response):
		item = response.meta["item"]
		item["subTitle"] = response.css("div.course-title h2::text").extract_first()
		item["unitSold"] = response.css("div.summary-content strong::text").extract_first()
		item["soldOrEnq"] = response.css("div.summary-content::text")[-1].extract()
		item["offerPrice"] = response.css("span.current-price::text").extract_first()
		item["originalPrice"] = response.css("small.vat-status::text").extract_first()
		item["savings"] = response.css("span.icon-savings-tag.price-saving::text").extract_first()
		item["courseProvider"] = response.css("section.sidebar-actions a.provider-link::text").extract_first()

		# CPD provider name
		try:
			item["cpdAccreditedBy"] = response.css("div.col div::text")[-1].extract().strip()
		except:
			pass

		# Does the course have cpd?
		try:
			haveCpd = []
			cpdTag = response.css("div.badge.badge-dark.badge-cpd.mt-2")
			for tag in cpdTag:
				if tag:
					haveCpd.append("yes")
			item["haveCpd"] = haveCpd
		except:
			pass

		# Does the course have professional qualification?
		try:
			haveProfQual = []
			profQualTag = response.css("div.badge.badge-dark.badge-professional.mt-2")
			for tag in profQualTag:
				if tag:
					haveProfQual.append("yes")
			item["haveProfQual"] = haveProfQual
		except:
			pass

		# Is the course qualification regulated?
		try:
			isRegulated = []
			reguTag = response.css("div.badge.badge-dark.badge-regulated.mt-2")
			for tag in reguTag:
				if tag:
					isRegulated.append("yes")
			item["isRegulated"] = isRegulated
		except:
			pass

		yield item
