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
    rules = [Rule(LinkExtractor(allow=r'concordia.ca', deny=r'explore.concordia.ca', deny_extensions=r'pdf'), callback='parse', follow=True)]
    allowed_domains = ["concordia.ca"]#concordia.ca/(.*?).html"]
    #deny_domains = ["explore.concordia.ca"]
    #deny_extensions = ["pdf"]

    def __init__(self):
        self.links = []
        self.directory = "DISK"
        

    def parse(self, response):
        title = response.css('title::text').extract_first()
        extractor = Extractor(extractor='ArticleExtractor', html=response.text)
        #div = response.xpath('//div[@class="d-grid-main"]')
        #res = div.xpath('.//p[@class="class-name"]/text()').extract()
        #res = div.xpath('normalize-space(.//p[@class="class-name"])').extract()
        #my_res = response.xpath('normalize-space(.//p[@class="class-name"])').extract()

        #soup = BeautifulSoup(extractor.getHTML(), 'html.parser')

        #res = soup.get_text()
        if "Explore" in title:
            return
        try:
            my_text = extractor.getText()
        except scrapy.exceptions.NotSupported:
            return
        afinn = Afinn()
        scored_text = afinn.score(my_text)
        yield ScrapycrawlerItem(title=title,
                        text=my_text,
                        url=response.url,
                        field=self.name,
                        sentiment=scored_text)
        self.links.append(response.url)

        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)
