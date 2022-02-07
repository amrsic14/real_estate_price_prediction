import json
import re
from typing import Optional, List

import pandas as pd


def clean_bathroom_number(num: Optional[int]) -> int:
    return num if num else 1


def clean_land_area(area: Optional[str]) -> float:
    if area == '-':
        return 0

    return float(area.split(' ')[0].rstrip('a')) if area else 0


def clean_registered(reg: Optional[str]) -> Optional[bool]:
    if not reg:
        return None

    return True if reg in ['uknjiženo', 'delimično uknjiženo', 'u procesu uknjižavanja', 'Da'] else False


def clean_floor(floor: Optional[str]) -> Optional[str]:
    if not floor:
        return None

    floor = floor.lower()
    floor = floor.replace('null', '-')
    floor = floor.replace('podrum', '-1')
    floor = floor.replace('suteren', '-1')
    floor = floor.replace('nisko prizemlje', '0')
    floor = floor.replace('visoko prizemlje', '0')
    floor = floor.replace('prizemlje', '0')
    floor = floor.replace('potkrovlje', 'max')

    if re.match(r'^.* / .*$', floor):
        current, max_floor = floor.split(' / ')
        return f'{current}/{max_floor}'

    floor = floor.split(' ')[0].strip('.')
    if '/' not in floor:
        return f'{floor}/null'

    return floor


def __debug_data(file: str):
    df = pd.read_json(file)
    dups_price = df.pivot_table(index=['price'], aggfunc='size')
    dups_city = df.pivot_table(index=['city'], aggfunc='size')
    dups_municipality = df.pivot_table(index=['municipality'], aggfunc='size')
    dups_address = df.pivot_table(index=['address'], aggfunc='size')
    dups_room_number = df.pivot_table(index=['room_number'], aggfunc='size')
    dups_square_footage = df.pivot_table(index=['square_footage'], aggfunc='size')
    dups_heating = df.pivot_table(index=['heating'], aggfunc='size')
    dups_floor = df.pivot_table(index=['floor'], aggfunc='size')
    dups_bathroom_number = df.pivot_table(index=['bathroom_number'], aggfunc='size')
    dups_build_year = df.pivot_table(index=['build_year'], aggfunc='size')
    dups_elevator = df.pivot_table(index=['elevator'], aggfunc='size')
    dups_balcony = df.pivot_table(index=['balcony'], aggfunc='size')
    dups_land_area = df.pivot_table(index=['land_area'], aggfunc='size')
    dups_registered = df.pivot_table(index=['registered'], aggfunc='size')
    dups_parking = df.pivot_table(index=['parking'], aggfunc='size')
    # dups_state = df.pivot_table(index=['state'], aggfunc='size')
    print(df.info())


def remove_null_containing_entries(file: str, fields: List[str]):
    df = pd.read_json(file)
    df.dropna(subset=fields, inplace=True)
    df.to_json(file, orient='records')


def json_to_csv(file: str):
    df = pd.read_json(file, encoding="utf-8")
    df.to_csv(f'{file.split(".")[0]}.csv', index_label=False, encoding="utf-8", index=False)


def clean_json_file(input_file: str):
    cleaned_file = f"{input_file.split('/')[-1].rstrip('.json')}_cleaned.json"

    with open(input_file, 'r') as json_file:
        data = json.load(json_file)
        for i, ad in enumerate(data):
            if not ad['room_number']:
                del ad
                continue
            ad['price'] = None if ad['price'] in (' ', '-', '--- ', 'Po dogovoru ', '1') else \
                int(str(ad['price']).replace('.', '').replace(' ', ''))
            # ad['link'] =
            # ad['offer_type'] =
            # ad['property_type'] =
            # ad['city'] =
            ad['municipality'] = ad['municipality'] if ad['municipality'] != '-' else None
            ad['address'] = ad['address'] if ad['address'] != '' else None
            ad['room_number'] = ad['room_number'].split(' ')[0] if ad['room_number'] != '-' else None
            ad['square_footage'] = ad['square_footage'] if ad['square_footage'] != '-' else None
            ad['heating'] = ad['heating'] if ad['heating'] != '-' else None
            ad['floor'] = clean_floor(ad['floor'])
            ad['bathroom_number'] = clean_bathroom_number(ad['bathroom_number'])
            ad['build_year'] = int(ad['build_year']) if ad.get('build_year', None) else None
            ad['elevator'] = True if ad.get('elevator', None) else False
            ad['balcony'] = True if ad.get('balcony', None) else False
            ad['land_area'] = clean_land_area(ad['land_area'])
            ad['registered'] = bool(clean_registered(ad['registered']))
            ad['parking'] = True if ad.get('parking', None) else False
        with open(cleaned_file, 'w') as output_cleaned:
            json.dump(data, output_cleaned)

    remove_null_containing_entries(cleaned_file, ['price', 'room_number', 'municipality', 'square_footage'])

    print(f"Cleaned {input_file} file. Output is saved in {cleaned_file} file.")


if __name__ == '__main__':
    clean_json_file('../real_estate_scraper/4zida.json')
    __debug_data('4zida_cleaned.json')
    # clean_json_file('../real_estate_scraper/nekretnine.json')
    # __debug_data('nekretnine_cleaned.json')
