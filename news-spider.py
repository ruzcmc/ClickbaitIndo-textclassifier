import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news_spider'
	#inserturl = input("Insert starting page url to scrap:")
    start_urls = ["https://news.detik.com/indeks","https://news.detik.com/indeks?date=09/30/2020","https://news.detik.com/indeks?date=08%2F31%2F2020"]

    def parse(self, response):
        SET_SELECTOR = '.media__link'
        for judul in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'a ::text'
            #PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            #MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            #IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': judul.css(NAME_SELECTOR).extract_first(),
                }

        NEXT_PAGE_SELECTOR = '.pagination a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR)[-1].extract()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )