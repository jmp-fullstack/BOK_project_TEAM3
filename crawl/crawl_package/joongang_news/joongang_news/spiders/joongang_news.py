import json
import scrapy
from joongang_news.items import JoongangNewsItem

class joongang(scrapy.Spider):
    name = 'joongang'

    def start_requests(self):
        for page in range(1,1000):
            url = f'https://www.joongang.co.kr/search/news?keyword=%EA%B8%88%EB%A6%AC&page={page}'
            yield scrapy.Request(url=url, callback=self.parse_total_pages)
    
    def parse_total_pages(self, response):
        htmls = response.css('h2.headline a::attr(href)').extract()
        for html in htmls:
            yield scrapy.Request(url=html, callback=self.parse)

    def parse(self, response):
        item = JoongangNewsItem()
        # 날짜, 제목, 내용 추출
        date = response.css('p.date time::attr(datetime)').get()
        title = response.css('h1.headline::text').get()
        content = response.css('#article_body p::text').extract()
        stripped_content = ' '.join(content).strip().replace('\n', '').replace('\r', '')
        item['date'] = date.split('T')[0]
        item['title'] = title.replace('\n','')
        item['content'] = stripped_content
        yield item

    def closed(self, reason):
        items = list(self.parse_news)
        with open('edaily_news.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(items, jsonfile, ensure_ascii=False, indent=4)
