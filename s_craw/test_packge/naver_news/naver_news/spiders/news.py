import scrapy
from bs4 import BeautifulSoup

class news(scrapy.Spider):
    name = 'news'

    def start_requests(self):
        base_url = 'https://search.mt.co.kr/searchNewsList.html'
        page = 1
        while True:
            url = f'{base_url}?srchFd=T&range=TOTAL&reSrchFlag=&preKwd=&search_type=m&kwd=%B1%DD%B8%AE&bgndt=20150101&enddt=20211231&category=MTNW&sortType=display&subYear=&category=MTNW&subType=mt&pageNum={page}'
            yield scrapy.Request(url=url, callback=self.parse)
            page += 1

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        money_links = [link['href'] for link in soup.select('.conlist_p1.mgt23 a')]
        if money_links:
            for link in money_links:
                yield {
                    'link': link
                }
        else:
            self.log(f"No links found on page {response.url}")