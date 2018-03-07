# -*- coding: utf-8 -*-

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class Eleicoes2016Spider(CrawlSpider):
    name = 'eleicoes2016'
    allowed_domains = ['www.eleicoes2016.com.br']
    start_urls = ['http://www.eleicoes2016.com.br/']
    rules = (Rule(LxmlLinkExtractor(
        allow=[r'.*']), callback='parse_obj', follow=True),)

    def parse_obj(self, response):
            cargo = response.css('div.cargo-upper::text').extract_first() or ''
            eleito = response.css('div.badge::text').extract_first() == 'Eleito'

            if (re.match(r'Vereador[a]?', cargo) and eleito):
            yield {
                'badge': response.css('div.badge::text').extract_first(),
            }
