# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, Rule, Request


def printhxs(hxs):
    a = ""
    for i in hxs:
        a += i.encode('utf-8')
    print a


class ToScrapeDYTTXPath(CrawlSpider):
    name = 'dytt'
    start_urls = [
        'http://www.ygdy8.net/html/gndy/index.html',
    ]

    rules = (
        # Rule(LinkExtractor(allow=('http://www.ygdy8.net/html/([\w]+)/index.html', ),), callback='parse_category', follow=True),
        Rule(LinkExtractor(allow=('.*?www.ygdy8.net/html/gndy/[\w]+/index.html', ), deny=('.*?html/(game)|(3gp)/index\.html')), follow=True),
        # Rule(LinkExtractor(allow=('http://www.ygdy8.net/html/([\w]+)/list_([\d]+)_([\d]+)\.html', ),), callback='parse_list', follow=True),

        Rule(LinkExtractor(allow=('http://www.ygdy8.net/html/gndy/[\w]+/list_[\d]+_[\d]+\.html', ),), follow=True),
        Rule(LinkExtractor(allow=('http://www.ygdy8.net/html/gndy/[\w]+/[\d]+/[\d]+\.html', ),), callback='parse_movie'),
    )

    def parse_category(self, response):
        for quote in response.xpath('//div[@class="title_all"]/p/em/a'):
            yield {
                'more_url': quote.xpath('./@href').extract_first(),
                'title': quote.xpath('//descendant::strong/text()').extract_first()
            }

        # next_page_url = response.xpath('//div[@class="title_all"]/p/em/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield Request(next_page_url, callback=self.parse2)

    def parse_list(self, response):
        for content in response.xpath('//a[@class="ulink"]'):
            ti = content.xpath('./text()').extract_first()
            printhxs(ti)
            yield {
                'title': ti,
                'url': content.xpath('./@href').extract_first(),
            }
        # for movie_url in response.xpath('//a[@class="ulink"]/@href'):
        #     yield scrapy.Request(movie_url, callback=self.parse3)

    def parse_movie(self, response):
        for content in response.xpath('//div[@class="co_area2"]'):
            yield {
                "tiltle": content.xpath('//div[@class="title_all"]/h1/font/text()').extract(),
                "down_url": content.xpath('//td[@bgcolor="#fdfddf"]/a/text()').extract(),
            }
