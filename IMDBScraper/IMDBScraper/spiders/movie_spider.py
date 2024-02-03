import scrapy
from scrapy import Spider, Request
from scrapy.utils.defer import maybe_deferred_to_future
from twisted.internet.defer import DeferredList

# REFERENCES: https://doc.scrapy.org/en/latest/intro/tutorial.html#following-links

# EX: scrapy crawl movie_spider -o result.json
# main spider, first crawls start_urls for links, then goes through every link and gets movie attributes
class Product(scrapy.Item):
    title = scrapy.Field()
    plot = scrapy.Field()
    ratings = scrapy.Field()
    director = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    genre = scrapy.Field()
    img = scrapy.Field()
    synopsis = scrapy.Field()
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

# EX: scrapy crawl test_spider2 -o test_result2.json
# Currently set to crawl one movie (dark knight) to see if parsing correct data
class test_spider2(Spider):
    name = "test_spider2"
    START = 111000
    DELTA = 10
    start_urls = ["https://www.imdb.com/title/tt%07d/?ref_=chttp_i_3" % ID for ID in range(START, START+DELTA)]
    def parse_summary(self, response):
        item_data = response.meta["item"]
        try:
            item_data["synopsis"] = response.xpath("//div[@class='ipc-html-content-inner-div']/text()").getall()[1:] #Also includes synopsis but ignores the short summary already grabbed
        except:
            item_data["synopsis"] = ""
        yield item_data

    def parse(self,response):
        result_obj = Product()
        result_obj["title"] = response.xpath("//span[contains(@class, 'hero__primary-text')]/text()").extract()
        result_obj["plot"] = response.xpath("//p[@data-testid='plot']/span[1]/text()").extract()
        result_obj["ratings"] = response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span/text()").extract_first()
        result_obj["director"] = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()").extract()
        result_obj["writers"] = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[2]/div/ul//li/a/text()").extract()
        result_obj["stars"] = response.xpath("//div[@data-testid='title-cast-item']/div[2]/a/text()").extract()
        # genres = response.xpath("//*[@data-testid='storyline-genres']/div/ul//li/a/text()").extract()
        result_obj["img"] = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a/@href").extract()
        new_url = response.url.split("?")[0]
        yield response.follow(new_url + "plotsummary", callback=self.parse_summary, dont_filter=True, meta={"item":result_obj})

# EX: scrapy crawl test_spider_tyborgg -o test_result_ty.json
class test_spider_tyborgg(Spider):
    name = "test_spider_tyborgg"
    # add the ?page=x to the url to start from the page you want to scrape
    start_urls = ["https://m.imdb.com/list/ls502982263/"]
    # https://m.imdb.com/list/ls502982263/?page=11
    
    def parse_summary(self, response):
        item_data = response.meta["item"]
        try:
            item_data["synopsis"] = response.xpath("//div[@class='ipc-html-content-inner-div']/text()").getall()[1:] #Also includes synopsis but ignores the short summary already grabbed
        except:
            item_data["synopsis"] = ""
        yield item_data

    def parse_indiv(self, response):
        m = response.meta["item"]
        m["plot"] = response.xpath("//p[@data-testid='plot']/span[1]/text()").extract()
        m["ratings"] = response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span/text()").extract_first()
        m["director"] = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()").extract()
        m["writers"] = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[2]/div/ul//li/a/text()").extract()
        m["stars"] = response.xpath("//div[@data-testid='title-cast-item']/div[2]/a/text()").extract()
        m["img"] = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a/@href").extract()
        yield response.follow(response.url + "plotsummary", callback=self.parse_summary, dont_filter=True, meta={"item":m})

    def parse(self,response):
        self.page_counter = getattr(self, "page_counter", 1)

        for movie in response.css("div.media"):
            m = Product()
            m["title"]= movie.xpath("a/span/span[@class='h4']/text()").get()
            m["genre"] = movie.xpath("a/span/span[contains(@class, 'cert-and-genres')]/p/span[@class='genre']/text()").get().replace("\n", "").strip()
            yield response.follow("https://m.imdb.com/title/" + movie.xpath("span/@data-tconst").get(), callback=self.parse_indiv, dont_filter=True, meta={"item":m})            

        next_page = response.xpath("//div[contains(@class, 'list-pagination')]/a[contains(@class, 'next-page')]/@href").get()
        # set the self.page_counter < x to x number of pages you want to scrape
        if next_page is not None and self.page_counter < 10:
            self.page_counter += 1
            yield response.follow(next_page, callback=self.parse)
