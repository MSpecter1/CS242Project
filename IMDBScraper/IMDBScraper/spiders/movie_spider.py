import scrapy
from scrapy import Spider, Request
import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

class Product(scrapy.Item):
    #pos = scrapy.Field()
    title = scrapy.Field()
    plot = scrapy.Field()
    ratings = scrapy.Field()
    director = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    genre = scrapy.Field()
    img = scrapy.Field()
    synopsis = scrapy.Field()
    url = scrapy.Field()
    descriptors = scrapy.Field() # will usually contain: type (other than movie), PG rating, release year, etc


# EX: scrapy crawl test_spider -o test_result.json
class test_spider(Spider):
    name = "test_spider"
    start_urls = ["https://m.imdb.com/list/ls502982263/"]
    
    def parse_summary(self, response):
        item_data = response.meta["item"]
        try:
            item_data["synopsis"] = "".join(response.xpath("//div[@class='ipc-html-content-inner-div']/text()").getall()[1:]) #Also includes synopsis but ignores the short summary already grabbed
        except:
            item_data["synopsis"] = ""
        yield item_data

    def parse_indiv(self, response):
        m = response.meta["item"]
        try:
            m["plot"] = response.xpath("//p[@data-testid='plot']/span[3]/text()").extract()
        except:
            try:
                m["plot"] = response.xpath("//p[@data-testid='plot']/span[2]/text()").extract()
            except:
                try:
                    m["plot"] = response.xpath("//p[@data-testid='plot']/span[1]/text()").extract()
                except:
                    m["plot"] = ""
        try:
            m["ratings"] = response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span/text()").extract_first()
        except:
            m["ratings"] = ""

        try:
            m["director"] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/div/div/ul/li[1]/div/text()").extract()
        except:
            m["director"] = ""
        

        try:
            m["writers"] = response.xpath("//*[@id='__next']/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[2]/div/ul//li/a/text()").extract()
        except: 
            m["writers"] = ""

        try:
            m["stars"] = response.xpath("//div[@data-testid='title-cast-item']/div[2]/a/text()").extract()
        except:
            m["stars"] = ""

        try:
            m["img"] = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a/@href").extract()
        except:
            m["img"] = ""
        m["img"] = "https://m.imdb.com" + "".join(m["img"])

        try:
            m["descriptors"] = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul//li/a/text()").extract()
        except:
            m["descriptors"] = ""

        try:
            m["url"] = response.request.url
        except:
            m["url"] = ""
        yield response.follow(response.url + "plotsummary", callback=self.parse_summary, dont_filter=True, meta={"item":m})

    def parse(self,response):
        for movie in response.css("div.media"):
            m = Product()
            #m["pos"] = movie.xpath("a/span/span[@class='h4 unbold']/text()").get()
            m["title"]= movie.xpath("a/span/span[@class='h4']/text()").get()
            try:
                m["genre"] = movie.xpath("a/span/span[contains(@class, 'cert-and-genres')]/p/span[@class='genre']/text()").get().replace("\n", "").strip()
            except:
                m["genre"] = ""
            yield response.follow("https://m.imdb.com/title/" + movie.xpath("span/@data-tconst").get(), callback=self.parse_indiv, dont_filter=True, meta={"item":m})            

        next_page = response.xpath("//div[contains(@class, 'list-pagination')]/a[contains(@class, 'next-page')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def close(self, reason):
        print("\n=======================================")
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = datetime.datetime.now(datetime.timezone.utc)
        print("Total run time: ", finish_time-start_time)
        print("Total movies parsed: ", self.crawler.stats.get_value('item_scraped_count'))
        print("\n=======================================")