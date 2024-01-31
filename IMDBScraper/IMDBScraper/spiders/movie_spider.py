import scrapy
from scrapy import Spider, Request
from scrapy.utils.defer import maybe_deferred_to_future
from twisted.internet.defer import DeferredList

# REFERENCES: https://doc.scrapy.org/en/latest/intro/tutorial.html#following-links

# EX: scrapy crawl movie_spider -o result.json
# main spider, first crawls start_urls for links, then goes through every link and gets movie attributes
class movie_spider(Spider):
    name = "movie_spider"
    start_urls = ["https://www.imdb.com/chart/top?ref_=nv_mv_250"]
    
    def parse(self,response):
        # links = response.xpath("//*[@id=\"__next\"]/main/div/div[3]/section/div/div[2]/div/ul//li/div[2]/div/div/div[1]/a/@href").extract()
        # yield {
        #     "Top_250_Links": links
        # }
        yield from response.follow_all(xpath="//*[contains(@class, 'cli-title')]/a/@href", callback=self.parse_movie_link)

    def parse_movie_link(self,response):
        title = response.xpath("//span[contains(@class, 'hero__primary-text')]/text()").extract()
        plot = response.xpath("//p[@data-testid='plot']/span[1]/text()").extract()
        # synopsis = response.xpath("//span[contains(@class, 'hero__primary-text')]/text()").extract()
        ratings = response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span/text()").extract_first()
        director = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()").extract()
        writers = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[2]/div/ul//li/a/text()").extract()
        stars = response.xpath("//div[@data-testid='title-cast-item']/div[2]/a/text()").extract()
        # genres = response.xpath("//*[@data-testid='storyline-genres']/div/ul//li/a/text()").extract()
        img = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a/@href").extract()
        
        yield {
            "title": title, 
            "plot" : plot,
            # "synopsis" : synopsis,
            "ratings" : ratings,
            "director": director,
            "writers": writers,
            "stars": stars,
            # "genres": genres,
            "img" : img
        }

# EX: scrapy crawl test_spider -o test_result.json
# Currently set to crawl one movie (dark knight) to see if parsing correct data
class test_spider(Spider):
    name = "test_spider"
    start_urls = ["https://www.imdb.com/title/tt0468569/?ref_=chttp_i_3"]
    
    def parse(self,response):
        title = response.xpath("//span[contains(@class, 'hero__primary-text')]/text()").extract()
        plot = response.xpath("//p[@data-testid='plot']/span[1]/text()").extract()
        # synopsis = response.xpath("//span[contains(@class, 'hero__primary-text')]/text()").extract()
        ratings = response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span/text()").extract_first()
        director = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()").extract()
        writers = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[2]/div/ul//li/a/text()").extract()
        stars = response.xpath("//div[@data-testid='title-cast-item']/div[2]/a/text()").extract()
        # genres = response.xpath("//*[@data-testid='storyline-genres']/div/ul//li/a/text()").extract()
        img = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a/@href").extract()
        
        yield {
            "title": title, 
            "plot" : plot,
            # "synopsis" : synopsis,
            "ratings" : ratings,
            "director": director,
            "writers": writers,
            "stars": stars,
            # "genres": genres,
            "img" : img
        }

    def parse_movie(self,response):
        test = response.xpath("//h1/text()").extract()
        yield {
            "test": test
        }

# EX: scrapy crawl test_spider -o test_result.json
# Currently set to crawl one movie (dark knight) to see if parsing correct data
class test_spider2(Spider):
    name = "test_spider2"
    start_urls = ["https://www.imdb.com/title/tt%07d/?ref_=chttp_i_3" % ID for ID in range(1000)]
    
    def parse(self,response):
        title = response.xpath("//span[contains(@class, 'hero__primary-text')]/text()").extract()
        plot = response.xpath("//p[@data-testid='plot']/span[1]/text()").extract()
        # synopsis = response.xpath("//span[contains(@class, 'hero__primary-text')]/text()").extract()
        ratings = response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span/text()").extract_first()
        director = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()").extract()
        writers = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[2]/div/ul//li/a/text()").extract()
        stars = response.xpath("//div[@data-testid='title-cast-item']/div[2]/a/text()").extract()
        # genres = response.xpath("//*[@data-testid='storyline-genres']/div/ul//li/a/text()").extract()
        img = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a/@href").extract()
        url = response.request.url
        yield {
            "url" : url,
            "title": title, 
            "plot" : plot,
            # "synopsis" : synopsis,
            "ratings" : ratings,
            "director": director,
            "writers": writers,
            "stars": stars,
            # "genres": genres,
            "img" : img
        }