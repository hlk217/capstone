from scrapy import Spider, Request
from ins.items import InsItem


class InsSpider(Spider):
	name = "ins_spider"
	allowed_urls = ["http://web.stagram.com"]
	start_urls = ['https://web.stagram.com/juliahengel']

	def parse(self,response):
		allurls = [
		'https://web.stagram.com/juliahengel','https://web.stagram.com/juliahengel?cursor=AQDH8SL0jeRvmVJB7nElXqGdhqnKASG59SQE1CEvAXMYhoWiJQL0DlWONBYmUcR7tIyFSZVdSC1bK-JCuf1x7-bGTu2RNkhz11xOUiKEhpS1WA&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQDgccidKJqj8jVv19Bz5O7X2oLqBFuSmBx7vloIFmKBR4NIRtMznANYG5KI8lxJNfjInVJe4J2lhL4IoQNd-ssb5QxCjDEpSqBw8nuoiEVdww&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQDV2UQ6VHxOX3RR3Dm0EC7dT4IzsKUeVenfV7PMzK5sA4RHmg9T-eDMRnl3GgWF5ydlkxTTXzmWohjyKoTAF965UljhSKwZSjCMMhxTB-WRjg&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQD5o1OVaTiL7yfL1DvEP73oy8mWqQZkiCATBtcWEAq2Cl3_PR7NUApaVxDNal7VkpgDKy2_czzwRqF3TDWKeHIJL9PwvlZ_eZGTv96-2LrhIg&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQDJWm_GNTGT_zyTdXEy4Z5wMf3O0LME9e8lABFev-NCpoKaqubk42CPT9oh35auSQ3N8vQ-RYz5U_Tlwnp9mmaWB4vZ3XWfTjh8OJyviwlQEQ&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQB9NSGjBEXVxGvEXEPJPKTF54H4vCB8hrOGOeYFfN4RbUi2oGz9-5cQlZTSp47vmSPpXo1VuUmTOTkZGk80Vx28DD44WI9VhAcgKm3HjyPeEA&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQA9m0NVOlrWVajGbPXkTPF5nVMFH9Bl_z7qeLGVfKo0rdSW6O3522SlhhJwfip1jWEMicA4Lmy-Op7IBexjlJiFPY9KS7q-AosPTdVOM3--TQ&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQA7VPai8rq9NhaXHLjdoGE7XymmSdjXbdzLZq2CP9MY_ee-Rwb-OYPX1Myhc6O1rcC3yrMaTBHPCnHG7StjkYyQ5Xdj1Q5fFrO7XFz_ZBUGng&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQAFM450UMzNHc67z5L2YqyMtB9I3r6jwitMnep2eiGbv9rh7McUg4Nv4VHHsWqfLDLPGX3XylAZ-U93zihprtQ1h_QnKHsRM9nwOtxs-FCP6Q&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQDo1Jm-Usr1NycfmE42CMfQ3N8RVpPGO-Emz7b0O0sbSUgQAxA_7quEJekoJF3QHLf7xGbt3v7hD5B1O3NcoSR4WjLY1LCYRadwOZxNLP1v2A&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQD9lFNkKaIJgP3B_EpI-0hOUM-kigfEmD7aHiu0pXHHbbz-ELQI0gqX0UJGK55Qjfio3lsOQ4Q7oOW9Jt52xL7kRS9J2fD_umXkBr2YvmG85Q&uid=8204017','https://web.stagram.com/juliahengel?cursor=AQC8ZqD6d1BRgjli6vy8lCn0O3hAFHusG4bu9S7kGZ8Lhj4Wj25QvA_r_-eGQOcwRn6ODg-eJAJ7Q05clMeKpJ9e-KlAL94yEnfFgg12PXIIIA&uid=8204017']

		for r in allurls:
			yield Request(url = r, callback = self.parse_all_urls)

	def parse_all_urls(self,response):
		urls = response.xpath('//div[@class="card"]/a/@href').extract()
		newurls = map(lambda x:"http://web.stagram.com" + x,urls)

		for url in newurls:
			yield Request(url = url, callback = self.parse_result_page)

	def parse_result_page(self, response):
		comments = response.xpath('//li[@class="list-inline-item"]//text()').extract()[1]
		image_url = response.xpath('//div[@class="card mb-4 post"]/img/@src').extract()
		likes = response.xpath('//li[@class="list-inline-item"]//text()').extract()[0]
		pic_cap = ' '.join(response.xpath('//h3[@class="card-text h6"]//text()').extract())
		post_date = response.xpath('//div[@class="header card-block clearfix pb-3"]/small/text()').extract_first()

		item = InsItem()
		item['comments'] = comments
		item['image_url'] = image_url
		item['likes'] = likes
		item['pic_cap'] = pic_cap
		item['post_date'] = post_date

		yield item
