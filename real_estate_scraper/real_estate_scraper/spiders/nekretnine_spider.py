from typing import Dict, Any

import scrapy


class Spider(scrapy.Spider):
    name = "4zida"
    allowed_domains = ["4zida.rs"]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    start_urls = [
        "https://www.4zida.rs/izdavanje-stanova?strana=1",
        "https://www.4zida.rs/izdavanje-kuca?strana=1",
        "https://www.4zida.rs/prodaja-stanova?strana=1",
        "https://www.4zida.rs/prodaja-kuca?strana=1"
    ]

    counter = 0

    def parse(self, response):
        home_url = "https://www.4zida.rs"

        base_url = response.url.split("?")[0]
        last_page = int(response.xpath("//a[contains(@class, 'page-link')]/text()")[-1].extract())
        current_page = int(response.url.split("=")[1])

        apartments = response.xpath("//div[@class='meta-container']//a/@href").extract()
        print(f"Found {len(apartments)} apartments")

        for apartment in apartments:
            apartment_url = f"{home_url}{apartment}"
            print(f"APARTMENT URL:    {apartment_url}")
            yield scrapy.Request(apartment_url, callback=self.parse_ad_page, dont_filter=False, headers=Spider.headers)

        if current_page < last_page:
            next_page_url = f"{base_url}?strana={current_page + 1}"
            yield scrapy.Request(next_page_url, callback=self.parse, headers=Spider.headers)

    def parse_ad_page(self, response: scrapy.http.Response) -> Dict[str, Any]:
        ad: Dict[str, Any] = {}

        ad["price"] = \
            response.xpath("//div[@class='prices ng-star-inserted']//span//strong/text()").get().split(u'\xa0')[0]

        ad["link"] = response.url
        ad["offer_type"] = response.url.split('/')[3]
        ad["property_type"] = response.url.split('/')[4]

        location = response.xpath("//div[@class='location']/text()").extract_first().split(',')
        ad["city"] = location[-1].strip()
        if len(location) > 1:
            if location[1] == "Gradske lokacije":
                municipality = location[0].strip()
            else:
                municipality = location[1].strip()
        else:
            municipality = location[0].strip()
        ad["municipality"] = municipality

        ad["address"] = response.xpath("//div[@class='address']/text()").get()

        labels = response.xpath("//div[@class='wrapper ng-star-inserted']/.//div[@class='label']/text()").getall()
        values = response.xpath("//div[@class='wrapper ng-star-inserted']/.//div[@class='value']/text()").getall()

        labels_values = list(zip([label[:-1] for label in labels], values))
        for label, value in labels_values:
            if label == "Parking":
                ad["parking"] = value
            elif label == "Lift":
                ad["elevator"] = value
            elif label == "Grejanje":
                ad["heating"] = value
            elif label == "Površina":
                ad["square_footage"] = value.split('m')[0] if value else ""
            elif label == "Plac":
                ad["land_area"] = value
            elif label == "Godina izgradnje":
                ad["build_year"] = value.split('.')[0] if value else ""
            elif label == "Uknjiženost":
                ad["registered"] = value
            elif label == "Spratnost":
                ad["floor"] = value
            elif label == "Broj soba":
                ad["room_number"] = value.split(" ")[0] if value else ""
            elif label == "Infrastruktura":
                if "teras" in value or "lo" in value or "balkon" in value:
                    ad['balcony'] = "terasa"
            elif label == "Unutrašnje prostorije":
                baths = 0
                if "kupatilo" in value or "toalet" in value:
                    baths += 1
                elif "kupatila" in value or "toaleti" in value:
                    for part in value.split(','):
                        if "kupatila" in part or "toaleti" in part:
                            temp = part.split('(')[1]
                            baths += int(temp[0:1])
                if baths == 0:
                    # If there are no bathrooms info, we assume that there is one bathroom
                    baths = 1
                ad["bathroom_number"] = baths

        Spider.counter = Spider.counter + 1
        print(f"Processed {Spider.counter} flats")

        return ad


class NekretnineSpider(scrapy.Spider):
    name = "nekretnine"
    allowed_domains = ["www.nekretnine.rs"]

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    start_urls = [
        "https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/lista/po-stranici/10/stranica/2/",
        "https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici/10/stranica/2/",
        "https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/izdavanje/lista/po-stranici/10/stranica/2/",
        "https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/prodaja/lista/po-stranici/10/stranica/2/"
    ]

    counter = 0
    scraped = []

    def parse(self, response):
        home_url = "https://www.nekretnine.rs"

        base_url = response.url.rsplit('/', 2)[0]
        current_page = int(response.url.rsplit('/', 2)[-2])

        apartments = response.xpath("//div[@class='advert-list']//div[@class='row offer']//h2//a/@href").extract()
        print(f"Found {len(apartments)} apartments")

        for apartment in apartments:
            apartment_url = f"{home_url}{apartment}"
            if apartment_url not in self.scraped:
                self.scraped.append(apartment_url)
                yield scrapy.Request(apartment_url, callback=self.parse_ad_page,
                                     dont_filter=False, headers=Spider.headers)

        if apartments:
            next_page_url = f"{base_url}/{current_page + 1}"
            print(f"next page url: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse, headers=Spider.headers)

    def parse_ad_page(self, response: scrapy.http.Response) -> Dict[str, Any]:
        ad: Dict[str, Any] = {}

        ad["price"] = response.xpath("//h4[@class='stickyBox__price']/text()").get().split(" EUR")[0]

        ad["link"] = response.url
        ad["offer_type"] = \
            response.xpath("//h2[@class='detail-seo-subtitle']/text()").get().split(",")[1].strip().lower()
        ad["property_type"] = response.url.split('/')[4]

        location = response.xpath("//div[@class='property__location']//ul//li//text()").getall()
        ad["city"] = location[2]

        if len(location) == 3:
            ad["municipality"] = location[2]
            ad["address"] = ""
        elif len(location) == 4:
            ad["municipality"] = location[3]
            ad["address"] = location[3]
        elif len(location) > 4:
            ad["municipality"] = location[3]
            ad["address"] = location[4]

        ad["square_footage"] = \
            response.xpath("//span[normalize-space()='Kvadratura:']/../text()").getall()[1].split(" m")[0].strip()
        ad["room_number"] = response.xpath("//span[normalize-space()='Sobe:']/../text()").get()
        ad["heating"] = response.xpath("//span[normalize-space()='Grejanje:']/../text()").get()
        if response.xpath("//span[normalize-space()='Parking:']/../text()").get() == "Da":
            ad["parking"] = "da"
        ad["land_area"] = response.xpath("//span[normalize-space()='Površina zemljišta:']/../text()").get()
        ad["registered"] = response.xpath("//span[normalize-space()='Uknjiženo:']/../text()").get()
        ad["floor"] = response.xpath("//span[normalize-space()='Sprat:']/../text()").get()

        state = response.xpath("//div[@class='property__amenities']"
                               "//text()[normalize-space()='Stanje nekretnine:']//../strong/text()").get()
        if state:
            ad["state"] = state.strip()

        labels = " ".join(response.xpath("//div[@class='property__amenities']//text()").getall()).lower()

        if "lift" in labels:
            ad["elevator"] = "lift"

        if "terasa" in labels or "lođa" in labels or "balkon" in labels:
            ad['balcony'] = "terasa"

        bathroom_number = response.xpath("//div[@class='property__amenities']"
                                         "//text()[normalize-space()='Broj kupatila:']//../strong/text()").get()
        ad["bathroom_number"] = float(bathroom_number.strip()) if bathroom_number else 1

        Spider.counter = Spider.counter + 1
        print(f"Processed {Spider.counter} flats")

        return ad
