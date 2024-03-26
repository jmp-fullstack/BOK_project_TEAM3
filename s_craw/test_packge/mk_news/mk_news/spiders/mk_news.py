import scrapy
from mk_news.items import MkNewsItem
import json

class mk_news(scrapy.Spider):
    name = "mk_news"
    items = []

    def start_requests(self):
        start_year = 2016
        end_year = 2024
        pages =  5
        base_url = 'https://www.mk.co.kr/'
        for page in range(1,pages+1):
            urls = f'{base_url}_CP/243?word=%EA%B8%88%EB%A6%AC&sort=desc&dateType=direct&startDate={start_year}-01-01&endDate={end_year}-03-23&searchField=title&page={page}&highlight=Y&page_size=null&id=null'
            print(urls)
            yield scrapy.Request(url=urls, callback=self.parse_total_href)


    def parse_total_href(self, response):
        print('------------------------------------------response.url----------------------------------------------')
        print(response.url)
        href = response.css('#list_area a::attr(href)').extract()
        print('--------------------------------------------href------------------------------------------------------')
        print(href)
        yield scrapy.Request(url=response.urljoin(href), callback=self.parse)


    def pasrse(self, response):
        item = MkNewsItem()

        title = response.css('h2.news_ttl::text').get().replace('\n', '').replace('\r', '').strip()
        date = response.css('.registration dd::text').get().replace('\n', '').replace('\r', '').strip()
        content = response.css('div.news_cnt_detail_wrap p::text')
        stripped_content = ' '.join(content).strip().replace('\n', '').replace('\r', '')

        item['date'] = date.split(' ')[0].replace('.','-')
        item['title'] = title
        item['content'] = stripped_content

        self.items.append({'date': date, 'title': title, 'content': stripped_content})

        yield item

    def closed(self, reason):
        with open('output.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.items, jsonfile, ensure_ascii=False, indent=4)