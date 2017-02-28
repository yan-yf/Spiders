import scrapy
from DoubanBook.items import DoubanbookItem

class DoubanBookSpider(scrapy.Spider):
	name = 'douban_book'
	# allowed_domain = ['douban.com']
	start_urls = ['https://book.douban.com/top250']

	def parse(self, response):
		yield scrapy.Request(response.url, callback = parse_title)
		for num in xrange(1, 10):
			url = scrapy.urljoin(self.start_urls, 'top250?start=' + num * 25)
			yield scrapy.Request(url, callback = parse_title)

	def parse_title(self, response):
		for item in response.xpath('//tr[@class="item"]'):
			book = DoubanbookItem()
			book['name'] = item.xpath('div[@class="pl2"]/a/text()').extract()[0]
			yield book