# -*- coding: utf-8 -*-

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class Eleicoes2016Spider(CrawlSpider):
    name = 'eleicoes2016'
    allowed_domains = ['www.eleicoes2016.com.br']
    start_urls = ['https://www.eleicoes2016.com.br/']
    rules = [
        Rule(LxmlLinkExtractor(allow=[r'.*']),
             callback='parse_obj', follow=True),
    ]

    def parse_obj(self, response):
        cargo = response.css('div.cargo-upper::text').extract_first() or ''
        vereador = bool(re.match(r'Vereador[a]?', cargo))
        eleito = response.css('div.badge::text').extract_first() == 'Eleito'

        if (vereador and eleito):
            infos_candidato = response.css('div.info-candidato div')
            candidato_data = {}

            for info_candidato in infos_candidato:
                info = info_candidato.css('div::text').extract()

                if (info and len(info) >= 2):
                    chave = info[0]
                    valor = info[1]

                    candidato_data[''+chave] = valor

            yield candidato_data
