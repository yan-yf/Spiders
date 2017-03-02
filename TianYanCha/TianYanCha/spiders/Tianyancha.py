import scrapy
from TianYanCha.items import TianyanchaItem
import re

class TianyanchaSpider(scrapy.Spider):
	name = 'tianyancha'
	allowed_domain = ['tianyancha.com']
	start_urls = ['http://www.tianyancha.com/search?key=%E7%99%BE%E5%BA%A6&checkFrom=searchBox']

	def parse(self, response):
		# print response.body + '222222222222222222222222'
		print str(len(response.xpath('//a[@class="query_name search-new-color"]'))) + "123456789123456789123456789"
		for item in response.xpath('//a[@class="query_name search-new-color"]'):
			url = item.xpath('@href').extract()[0]
			yield scrapy.Request(url, callback=self.parse_next)

	def parse_next(self, response):
		temp = response.xpath('//div[@class="company_info_text"]')
		print temp
		company = TianyanchaItem()
		company['name'] = response.xpath('//p[@class="in-block ml10 ng-binding"]').extract()[0]
		# company['phone'] = re.findall(r^"(0[0-9]{2,3}\-)?([2-9][0-9]{6,7})+(\-[0-9]{1,4})?", str(info[1]))
		company['phone'] = response.xpath('span[1]/text()').extract()[0]
		# company['email'] = re.findall(r^"(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})", str(info[1]))
		company['email'] = response.xpath('span[2]/text()').extract()[0]
		# company['http'] = str(info[2])[3:]
		company['http'] = response.xpath('span[3]/a/@href').extract()[0]
		# company['address'] = str(info[3])[3:]
		company['address'] = response.xpath('span[4]/text()').extract()[0]
		yield company
