import scrapy
from typing import Dict, Any


class Spider(scrapy.Spider):
    name = "4zida"
    allowed_domains = ["4zida.rs"]

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
        last_page = int(response.xpath('//a[contains(@class, "page-link")]/text()')[-1].extract())
        current_page = int(response.url.split("=")[1])

        apartments = response.xpath('//div[@class="meta-container"]//a/@href').extract()
        print(f"Found {len(apartments)} apartments")

        for apartment in apartments:
            apartment_url = f"{home_url}{apartment}"
            print(f"APARTMENT URL:    {apartment_url}")
            yield scrapy.Request(apartment_url, callback=self.parse_ad_page, dont_filter=False)

        if current_page < last_page:
            next_page_url = f"{base_url}?strana={current_page + 1}"
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_ad_page(response: scrapy.http.Response) -> Dict[str, Any]:
        ad: Dict[str, Any] = {}

        price = response.xpath('//div[@class="prices ng-star-inserted"]//span//strong/text()').get().split(u'\xa0')[0]
        ad["price"] = price

        ad["link"] = response.url
        ad["offer_type"] = response.url.split('/')[3]
        ad["property_type"] = response.url.split('/')[4]

        location = response.xpath('//div[@class="location"]/text()').extract_first().split(',')
        ad["city"] = location[-1].strip()
        if len(location) > 1:
            if location[1] == "Gradske lokacije":
                municipality = location[0].strip()
            else:
                municipality = location[1].strip()
        else:
            municipality = location[0].strip()
        ad["municipality"] = municipality

        labels = response.xpath('//div[@class="wrapper ng-star-inserted"]/.//div[@class="label"]/text()').getall()
        values = response.xpath('//div[@class="wrapper ng-star-inserted"]/.//div[@class="value"]/text()').getall()

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
                if 'teras' in value or 'lo' in value or 'balkon' in value:
                    ad['balcony'] = value
            elif label == "Unutrašnje prostorije":
                baths = 0
                if 'kupatilo' in value or 'toalet' in value:
                    baths += 1
                elif 'kupatila' in value or 'toaleti' in value:
                    for part in value.split(','):
                        if 'kupatila' in part or 'toaleti' in part:
                            temp = part.split('(')[1]
                            baths += int(temp[0:1])
                if baths == 0:
                    # If there are no bathrooms info, we assume that there is one bathroom
                    baths = 1
                ad["bathroom_number"] = baths

        Spider.counter = Spider.counter + 1
        print("=================================")
        print(f"Processed {Spider.counter} flats")
        print("=================================")

        return ad
