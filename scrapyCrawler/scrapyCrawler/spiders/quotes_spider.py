import scrapy
import collections
import os
import os.path

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boilerpipe.extract import Extractor

from scrapyCrawler.items import ScrapycrawlerItem
from scrapy.contracts.default import ReturnsContract
from bs4 import BeautifulSoup

from afinn import Afinn
# to run spider and save json.line type
# scrapy crawl quotes -o items.jl

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://www.concordia.ca/about.html']
    list_domains = ['explore.concordia.ca', 'twitter.com', 'facebook.com', 'youtube.com', 'flickr.com','legisquebec.gouv.qc.ca']
    rules = [Rule(LinkExtractor(allow=r'concordia.ca', deny=r'explore.concordia.ca'), callback='parse', follow=True)]
    allowed_domains = ["concordia.ca"]#concordia.ca/(.*?).html"]
    #deny_domains = ["explore.concordia.ca"]
    #deny_extensions = ["pdf"]

    def __init__(self):
        self.links = []
        self.directory = "DISK"
        

    def parse(self, response):
        
        extractor = Extractor(extractor='ArticleExtractor', html=response.text)

        current_page = response.url
        extension = str(current_page)[-4:]
        
        afinn = Afinn()
        if extension == "html":
            title = response.css('title::text').extract_first()

            if "Explore" in title:
                return
            my_text = extractor.getText()
            scored_text = afinn.score(my_text)
            yield ScrapycrawlerItem(title=title,
                        text=my_text,
                        url=response.url,
                        field=self.name,
                        sentiment=scored_text)
                
            for href in response.css('a::attr(href)').extract():
                if ".pdf" not in href:
                    yield scrapy.Request(response.urljoin(href),
                                            callback=self.parse)
                
                #urls = le.extract_links(response)
"""         for href in response.css('a::attr(href)'):
            _url = str(href)
            _url = href('data')
            print("_url is "+_url.data)
            if href.data[-4:] == "html":
                yield response.follow(href, self.parse) """
