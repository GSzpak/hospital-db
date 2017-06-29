import scrapy


class HospitalsScraper(scrapy.Spider):
    name = 'hospitals'

    start_urls = ['http://www.medbiz.pl/szpitale/']

    def parse(self, response):
        # follow links to hospitals in voivodeships pages
        for href in response.xpath('//div[@class="center-box-info"]/h2/a/@href').extract():
            print(href)
            voivodeship_hospitals_url = response.urljoin(href)
            yield response.follow(voivodeship_hospitals_url, self.parse_voivodeship_hospitals)

    def parse_voivodeship_hospitals(self, response):
        for href in response.xpath('//div[@class="center-box-info"]/h3/a/@href').extract():
            hospital_url = response.urljoin(href)
            yield response.follow(hospital_url, self.parse_hospital)

    def parse_hospital(self, response):
        hospital_name = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        if hospital_name is None:
            # Different page layout
            hospital_name = response.xpath('//h1[@class="page-title"]/text()').extract_first()
        street = response.xpath('//span[@itemprop="streetAddress"]/text()').extract_first()
        postal_code = response.xpath('//span[@itemprop="postalCode"]/text()').extract_first()
        city = response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first()
        address = '{}, {} {}'.format(street, postal_code, city)
        yield {
            'name': hospital_name,
            'address': address
        }
