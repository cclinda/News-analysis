# -*- coding: utf-8 -*-
import scrapy
from zqrbtest.items import ZqrbtestItem
from scrapy.http import Request
import datetime
import time
from openpyxl import Workbook
import importlib, sys
importlib.reload(sys)


class ZqrbSpider(scrapy.Spider):
    name = 'sinaf'
    allowed_domains = ['finance.sina.com.cn']
    start_urls = ['http://roll.finance.sina.com.cn/finance/zq1/ssgs/index_1.shtml']

    def parse(self, response):
        item = ZqrbtestItem()
        for b in response.xpath('//div[@id="Main"]/div/ul/li'):
            timea = b.xpath('./span/text()').extract_first()
            titlec = b.xpath('./a/text()').extract()[0]
            if timea is None:
                pass
            else:
                timec = timea.split(' ')[0].replace('(', '').replace('年', '-').replace('月', '-').replace('日', '')

            for timel in timec:
                if timec.startswith("2"):
                    pass
                else:
                    timec = str(datetime.datetime.now().year)+'-'+timec

            item['timec'] = timec
            item['titlec'] = titlec
            yield item

        next_page = response.xpath('//span[@class="pagebox_next"]/a[contains(text(), "下一页")]/@href').extract()
        if next_page:
            next_page = next_page[0]
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse, dont_filter=False)
        else:
            print(str(next_page))
