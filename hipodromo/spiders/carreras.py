# -*- coding: utf-8 -*-
import scrapy


class CarrerasSpider(scrapy.Spider):
    name = 'carreras'
    allowed_domains = ['palermo.com.ar']
    start_urls = [
        #'https://www.palermo.com.ar/en/turf/racing-schedule-and-results/2017'
        #'https://www.palermo.com.ar/en/turf/racing-schedule-and-results/2016'
        #'https://www.palermo.com.ar/en/turf/racing-schedule-and-results/2015'
        #'https://www.palermo.com.ar/en/turf/racing-schedule-and-results/2014'
        #'https://www.palermo.com.ar/en/turf/racing-schedule-and-results/2013'
        'https://www.palermo.com.ar/en/turf/racing-schedule-and-results/2012'
    ]

    def parse(self, response):
        for href in response.css('.resultado_carrera a'):
            yield response.follow(href, self.parse_race)

    def parse_race(self, response):
        date = response.css('div.ruta:nth-child(7) > h2:nth-child(1)::text').extract_first().encode('utf-8')
        for href in response.css('.tabla_ver_caballo tr:not(.tabla_head) td.tabla_premio a'):
            yield response.follow(href, self.parse_positions)

    def parse_positions(self, response):
        for pos in response.css('.tabla_ver_caballo:nth-child(4) tr:nth-child(even):not(tabla_thead)'):
            date = response.css('table.tabla_ver_caballo:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text').extract_first()
            race_id = response.css('.calendario > div:nth-child(1) > h2:nth-child(1)::text').extract_first()
            race_distance = response.css('table.tabla_ver_caballo:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4)::text').extract_first()
            
            yield {
                'pos': pos.css('td:nth-child(1)::text').extract_first(),
                'nro': pos.css('td:nth-child(2)::text').extract_first(),
                'challenger': pos.css('td:nth-child(3)::text').extract_first(),
                'distance': pos.css('td:nth-child(4)::text').extract_first(),
                'jockey': pos.css('td:nth-child(5)::text').extract_first(),
                'keeper': pos.css('td:nth-child(6)::text').extract_first(),
                'caballeriza': pos.css('td:nth-child(7)::text').extract_first(),
                'weight_jocket_horse': pos.css('td:nth-child(8)::text').extract_first(),
                'pagaria': pos.css('td:nth-child(9)::text').extract_first(),
                'date': date,
                'race_id': race_id,
                'race_distance': race_distance
            }

