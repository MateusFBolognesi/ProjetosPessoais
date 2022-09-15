import scrapy
import csv
import re

class SpiderGPU(scrapy.Spider):
    name = "robo_gpu"

    def start_requests(self):
        start_url='https://sp.olx.com.br/?q=placa%20de%20video'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        links = response.xpath('//a[@class="sc-12rk7z2-1 huFwya sc-giadOv dXANPZ"]/@href').getall()
        for link in links:
            #print(link)
            yield scrapy.Request(url=link, callback=self.parse_info)
        next_page=response.xpath('//a[@data-lurker-detail="next_page"]/@href').extract()[0]
        if re.match(r'.*?100',str(next_page)):
            self.crawler.engine.close_spider(self, 'timeout')
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_info(self, response):
        modelo = response.xpath('//h1[@class="sc-45jt43-0 eCghYu sc-ifAKCX cmFKIN"]/text()').extract()[0]
        publicado = response.xpath('//span[@class="sc-1oq8jzc-0 jvuXUB sc-ifAKCX fizSrB"]/text()').extract()[1]
        price = response.xpath('//h2[@class="sc-1wimjbb-1 bQzdqU sc-ifAKCX cmFKIN"]/text()').extract()[0]
        CEP = response.xpath('//dd[@class="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ"]/text()').getall()[0]
        municipio = response.xpath('//dd[@class="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ"]/text()').getall()[1]
        bairro = response.xpath('//dd[@class="sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ"]/text()').getall()[2]
        #print(modelo, publicado, price, CEP, municipio, bairro)
        tabela = {
            'modelo':modelo,
            'publicado':publicado,
            'preco':price,
            'CEP':CEP,
            'municipio':municipio,
            'bairro':bairro
            }

        with open('info_gpu.csv', 'a', newline='', encoding='utf-8') as output_file:
            dict_writer=csv.DictWriter(output_file, tabela.keys())
            dict_writer.writerows([tabela])
