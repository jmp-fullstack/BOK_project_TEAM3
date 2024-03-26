import json
import scrapy
from edaily_news.items import EdailyNewsItem

class edaily(scrapy.Spider):
    name = 'edaily'

    def start_requests(self):
        for i in range(2012, 2024):
            syear = i
            eyear = i + 1
            url = f'https://www.edaily.co.kr/search/news/?source=title&keyword=%EA%B8%88%EB%A6%AC&include=%EA%B8%88%EB%A6%AC&exclude=\
            &jname=&start={syear}0326&end={eyear}0325&sort=latest&date=years&exact=false&page=1'
            yield scrapy.Request(url=url, callback=self.parse_total_pages)
    
    def parse_total_pages(self, response):
        end_html = response.css('.last::attr(href)').get()
        end_page = int(end_html.split('page=')[1])
        for page in range(1, end_page + 1):
            page_url = response.url.replace('page=1', f'page={page}')
            print('---------------------------------------------------확인 ---------------------------------------------')
            print(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse)

    def parse(self, response):
        htmls = response.css('#newsList a::attr(href)').extract()
        for html in htmls:
            # print(html)
            if '/news/read?newsId=' in html:
                html = 'https://www.edaily.co.kr/' + html
                yield scrapy.Request(url=response.urljoin(html), callback=self.parse_news)

    def parse_news(self, response):
        item = EdailyNewsItem()
        # 날짜, 제목, 내용 추출
        date = response.css('div.dates p::text').extract_first().split(' ')[1]
        title = response.css('div.news_titles h1::text').get()
        content = response.css('div.news_body::text').extract()
        stripped_content = ' '.join(content).strip().replace('\n', '').replace('\r', '')  # 내용을 하나의 문자열로 결합 및 공백 제거
        if '[이데일리 증권부]' == stripped_content:
            pass
        elif '[이데일리 증권시장부]' == stripped_content:
            pass
        else :
            item['date'] = date.split(' ')[0].replace('.','-')
            item['title'] = title
            item['content'] = stripped_content
            yield item

    def closed(self, reason):
        items = list(self.parse_news)
        with open('edaily_news.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(items, jsonfile, ensure_ascii=False, indent=4)
