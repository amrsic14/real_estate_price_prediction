import json

import pandas as pd


def __debug_data(file: str):
    df = pd.read_json(file)
    dups_offer_type = df.pivot_table(index=['offer_type'], aggfunc='size')
    dups_property_type = df.pivot_table(index=['property_type'], aggfunc='size')
    dups_price = df.pivot_table(index=['price'], aggfunc='size')
    dups_link = df.pivot_table(index=['link'], aggfunc='size')
    dups_city = df.pivot_table(index=['city'], aggfunc='size')
    dups_municipality = df.pivot_table(index=['municipality'], aggfunc='size')
    dups_address = df.pivot_table(index=['address'], aggfunc='size')
    dups_room_number = df.pivot_table(index=['room_number'], aggfunc='size')
    dups_square_footage = df.pivot_table(index=['square_footage'], aggfunc='size')
    dups_heating = df.pivot_table(index=['heating'], aggfunc='size')
    dups_floor = df.pivot_table(index=['floor'], aggfunc='size')
    dups_bathroom_number = df.pivot_table(index=['bathroom_number'], aggfunc='size')
    # dups_build_year = df.pivot_table(index=['build_year'], aggfunc='size')
    dups_elevator = df.pivot_table(index=['elevator'], aggfunc='size')
    dups_balcony = df.pivot_table(index=['balcony'], aggfunc='size')
    dups_land_area = df.pivot_table(index=['land_area'], aggfunc='size')
    dups_registered = df.pivot_table(index=['registered'], aggfunc='size')
    dups_parking = df.pivot_table(index=['parking'], aggfunc='size')
    print(df.info())


def change_proxies():
    new_lines = []
    with open('proxies.txt', 'r') as file:
        lines = file.readlines()
        lines = list(set(lines))

        for line in lines:
            new_lines.append(f'http://{line}')

    with open('proxy_list.txt', 'w') as file:
        file.writelines(new_lines)


if __name__ == '__main__':
    # df = pd.read_json('4zida_links.json')
    #
    # data = json.load(r'C:\Users\Aleksandar\Desktop\nekretnine.json')
    #
    # for ad in data:
    #     {"Cena": "110.000",
    #      "Link": "https://www.4zida.rs/prodaja/stanovi/novi-sad/oglas/bulevar-oslobodjenja/5b4f8fd4b70c5956c46def54",
    #      "Tip nekretnine": "stanovi", "Tip ponude": "prodaja", "Lokacija1": "Novi Sad",
    #      "Lokacija2": "Bulevar Oslobo\u0111enja", "Kvadratura": "54", "Godina izgradnje": "2005",
    #      "Povrsina zemljista": null, "Spratnost": "4/6 spratova", "Uknji\u017eenost": null,
    #      "Tip grejanja": "centralno grejanje", "Broj soba": "2 sobe", "Broj kupatila": null, "Parking": null,
    #      "Lift": "ima lift (1)", "Terasa": "terasa|lodja"}
    #     entry = {"price": ad["Cena"], "link": ad["Link"], "offer_type": ad["Tip ponude"],
    #              "property_type": ad["Tip nekretnine"], "city": "Subotica", "municipality": "Gradske lokacije", "address": "Nusiceva ", "room_number": "2.5", "square_footage": "72", "heating": "grejanje na struju", "floor": "1/1 sprat", "bathroom_number": 1}
    #     df.append()

    # __debug_data("cleaned.json")

    # with open('4zida_new.json', 'r') as json_file:
    #     data = json.load(json_file)
    #
    #     with open('cleaned.json', 'w') as output_file:
    #         output_file.write('[\n')
    #
    #         for i, ad in enumerate(data):
    #             if ad['property_type'] in ('kuce', 'stanovi'):
    #                 if ad["balcony"] == "terasa|lodja":
    #                     ad["balcony"] = "terasa"
    #                 output_file.write(f'{json.dumps(ad)},\n')
    #
    #         output_file.write(']\n')

    # __debug_data("nekretnine.json")
    __debug_data("4zida.json")
