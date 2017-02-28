import scrapy
from DoubanBook.items import DoubanbookItem

class DoubanBookSpider(scrapy.Spider):
	name = 'douban_book'
	allowed_domain = ['douban.com']
	start_urls = ['https://book.douban.com/top250']
	
	def parse(self, response):
		yield scrapy.Request(response.url, callback = self.parse_title)
		for num in range(1, 10):
			url ='https://book.douban.com/top250?start=' + str(num * 25)
			yield scrapy.Request(url, callback = self.parse_title)

	def parse_title(self, response):
		for item in response.xpath('//tr[@class="item"]'):
			book = DoubanbookItem()
			book['name'] = item.xpath('td[2]/div[1]/a/text()').extract()[0].strip()
			yield book
