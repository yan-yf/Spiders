# -*- coding: utf-8 -*-
import scrapy
from DoubanBook.items import DoubanbookItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DoubanBookSpider(scrapy.Spider):
	name = 'douban_book'
	allowed_domain = ['douban.com']
	start_urls = ['https://book.douban.com/top250']
	num = 0
	
	def parse(self, response):
		yield scrapy.Request(response.url, callback = self.parse_book)
		for page in response.xpath('//div[@class="paginator"]/a'):
			link = page.xpath('@href').extract()[0]
			yield scrapy.Request(link, callback = self.parse_book)

	def parse_book(self, response):
		print str(len(response.xpath('//tr[@class="item"]'))) + '1111111111111111'
		for item in response.xpath('//tr[@class="item"]'):
			self.num += 1
			book = DoubanbookItem()
			book['num'] = str(self.num)
			book['bookname'] = item.xpath('td[2]/div[1]/a/@title').extract()[0]
			book_info = item.xpath('td[2]/p[@class="pl"]/text()').extract()[0].split(' / ')
			book['price'] = str(book_info[-1])
			book['publishyear'] = str(book_info[-2])
			book['publisher'] = str(book_info[-3])
			book['author'] =  str(book_info[0])
			if book_info[0] != book_info[-4]:
				book['translator'] =  str(book_info[1])
			book['stars'] = item.xpath('td[2]/div[2]/span[@class="rating_nums"]/text()').extract()[0]
			book['quote'] = item.xpath('td[2]/p[@class="quote"]/span[@class="inq"]/text()').extract()[0]
			yield book