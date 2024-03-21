import scrapy
from naver_news.items import MyItem


class News(scrapy.Spider):
    name = 'news'

    def start_requests(self):
        # 2022년부터 2023년까지의 첫 페이지 URL을 생성합니다.
        for year in range(2022, 2024):
            yield scrapy.Request(url=f'https://search.mt.co.kr/searchNewsList.html?srchFd=T&range=IN&reSrchFlag=&preKwd=&search_type=m&kwd=%B1%DD%B8%AE&bgndt={year}0101&enddt={year}1231&category=MTNW&sortType=display&subYear={year}&category=MTNW&subType=mt&pageNum=1',
                                 callback=self.parse_total_pages,
                                 meta={'year': year})

    def parse_total_pages(self, response):
    # 마지막 페이지 버튼을 선택합니다.
        last_page_button = response.css('button.end')
        if last_page_button:
        # 마지막 페이지 버튼의 텍스트를 가져옵니다.
            last_page_text = last_page_button.css('button.end::text').get()
        # 텍스트에서 숫자 부분을 추출합니다.
            last_page_number = int(last_page_text)
        
        # 각 페이지에 대한 요청을 보냅니다.
            year = response.meta['year']
            for page_num in range(1, last_page_number + 1):
                page_url = f'https://search.mt.co.kr/searchNewsList.html?srchFd=T&range=IN&reSrchFlag=&preKwd=&search_type=m&kwd=%B1%DD%B8%AE&bgndt={year}0101&enddt={year}1231&category=MTNW&sortType=display&subYear={year}&category=MTNW&subType=mt&pageNum={page_num}'
            yield scrapy.Request(url=page_url, callback=self.parse)
        else:
            self.logger.warning("Last page button not found.")

    def parse(self, response):
        # href 가져오기
        hrefs = response.css('.conlist_p1.mgt23 a::attr(href)').extract()

        for href in hrefs[::3]:
            if 'news.mt.co.kr/mtview.php' in href:
                # 새로운 request 보내기
                yield scrapy.Request(url=response.urljoin(href), callback=self.parse_news)

    def parse_news(self, response):
        # 여기서 두 번째 페이지에서 필요한 정보를 스크랩합니다.
        item = MyItem()
        # 제목 가져오기
        item['title'] = response.css('h1::text').get()
        # 내용 가져오기
        # item['content'] = '\n'.join(response.css('.view_text::text').extract())
        yield item