# -*- coding: utf-8 -*-

import logging

import scrapy
#from stackoverflow.spiders.items import StackoverflowItem
from .items import StackoverflowItem
from scrapy.selector import Selector
import time


formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('quantidade_de_scrap')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('quantidade_de_scrap.log')
fh.setLevel(logging.INFO)

fh.setFormatter(formatter)
logger.addHandler(fh)


class StackoverflowSpider(scrapy.Spider):


    name = "stackoverflow"

    def __init__(self):
        self.count = 1

    def start_requests(self):
        item = StackoverflowItem()
        #Cathing all link and some informations from tag PHP, using select in mysql for view urls and put in other scrapy
        _url = 'https://stackoverflow.com/questions/tagged/php?tab=newest&page={page}&pagesize=50'
        urls = [_url.format(page=page) for page in range(1, 4528)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        for index in range(1, 51):
            self.count += 1
            if self.count % 100 == 0:
                logger.info(self.count)
            selector = response.xpath('//*[@id="questions"]/div[{index}]'.format(index=index))
            item = StackoverflowItem()
          
            item['answersNumber'] = "".join(selector.xpath(
                'div[1]/div[2]/span[1]/text()').extract())
            item['views'] = "".join(
                selector.xpath('div[1]/div[3]/span[1]/text()').extract()).split()[0].replace(",", "")
            item['votes'] = "".join(selector.xpath(
                'div[1]/div[1]/span[1]/text()').extract())
            item['questions'] = selector.xpath('div[2]/h3/a/text()').extract()
            item['links'] = "https://stackoverflow.com{}".format("".join(selector.xpath('div[2]//h3/a/@href').extract()))
            item['tags'] = ", ".join(selector.xpath('div[@class="s-post-summary--content"]/div[@class="s-post-summary--meta"]/div[1]//li//text()').extract())
            item['questionTime'] = selector.xpath('.//span[contains(@class,"relativetime")]/@title').extract()
            yield item

        time.sleep(0.6)

