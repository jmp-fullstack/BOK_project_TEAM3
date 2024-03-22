import json
import scrapy
from naver_news.items import MyItem

class News(scrapy.Spider):
    name = 'news'
    page = 1 
    items = []

    # 처음: 연도별 url을 모은다.(첫번째 페이지임)
    def start_requests(self):
        for year in range(2016, 2024):
            year_url = f'https://search.mt.co.kr/searchNewsList.html?srchFd=T&range=IN&reSrchFlag=&preKwd=&search_type=m&kwd=%B1%DD%B8%AE&bgndt={year}0101&enddt={year}1231&category=MTNW&sortType=display&subYear={year}&category=MTNW&subType=mt&pageNum=1'

            yield scrapy.Request(url=year_url, callback=self.parse_total_pages)
    
    # 각각의 연도별 모든 페이지의 url를 모은다
    def parse_total_pages(self, response):
        page_num = response.css('.end::attr(onclick)').get()
        page_num = int(page_num.split('pageNum=')[1].rstrip("';"))
        for page in range(1, page_num + 1):
            page_url = response.url.replace('pageNum=1', f'pageNum={page}')
            yield scrapy.Request(url=page_url, callback=self.parse)

    # 모든 연도,페이지의 url을 통하여 내가 파싱해야하는 하이퍼링크 주소를 모은다
    def parse(self, response):
        hrefs = response.css('.conlist_p1.mgt23 a::attr(href)').extract()

        for href in hrefs[::3]:
            if 'news.mt.co.kr/mtview.php' in href:
                yield scrapy.Request(url=response.urljoin(href), callback=self.parse_news)

    # 필요한 정보(제목, 본문, 날짜 등등) 모은다
    def parse_news(self, response):
        item = MyItem()

        # 날짜, 제목, 내용 추출
        date = response.css('li.date::text').get().replace('\n', '').replace('\r', '').strip()
        title = response.css('h1::text').get().replace('\n', '').replace('\r', '').strip()
        content = response.css('#textBody::text').extract()
        stripped_content = ' '.join(content).strip().replace('\n', '').replace('\r', '')  # 내용을 하나의 문자열로 결합 및 공백 제거

        # MyItem에 데이터 할당
        item['date'] = date.split(' ')[0].replace('.','-')
        item['title'] = title
        item['content'] = stripped_content

        self.items.append({'date': date, 'title': title, 'content': stripped_content})

        yield item

    def closed(self, reason):
        with open('output.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.items, jsonfile, ensure_ascii=False, indent=4)