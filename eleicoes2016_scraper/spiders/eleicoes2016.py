# -*- coding: utf-8 -*-

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class Eleicoes2016Spider(CrawlSpider):
    name = 'eleicoes2016'
    allowed_domains = ['www.eleicoes2016.com.br']
    start_urls = ['http://www.eleicoes2016.com.br/']
    rules = [
        Rule(LxmlLinkExtractor(allow = [r'.*']), callback = 'parse_obj', follow = True),
        Rule(LxmlLinkExtractor(deny = [r'.+\/candidato.+']), follow = False),
    ]

    def parse_obj(self, response):
        cargo = response.css('div.cargo-upper::text').extract_first() or ''
        vereador = re.match(r'Vereador[a]?', cargo)
        eleito = response.css('div.badge::text').extract_first() == 'Eleito'

        if (vereador and eleito):
            infoCandidato = response.css('div.info-candidato div')
            nome = infoCandidato[0].css('div::text')[1].extract()
            
            yield {
                'nome': nome,
            }
