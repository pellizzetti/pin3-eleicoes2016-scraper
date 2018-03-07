from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class Eleicoes2016Spider(CrawlSpider):
    name = 'eleicoes2016'
    allowed_domains = ['www.eleicoes2016.com.br']
    start_urls = ['http://www.eleicoes2016.com.br/']
    rules = (Rule(LxmlLinkExtractor(
        allow=[r'.*']), callback='parse_obj', follow=True),)

    def parse_obj(self, response):
        badge = response.css('div.badge::text').extract_first()
        if badge == 'Eleito':
            yield {
                'badge': response.css('div.badge::text').extract_first(),
            }
