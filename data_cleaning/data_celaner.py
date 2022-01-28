import json
from typing import Optional, List

import pandas as pd


def clean_bathroom_number(num: Optional[int]) -> int:
    return num if num else 1


def clean_land_area(area: Optional[str]) -> float:
    return float(area.split(' ')[0].rstrip('a')) if area else 0


def clean_registered(reg: Optional[str]) -> Optional[bool]:
    if not reg:
        return None

    return True if reg in ['uknjiženo', 'delimično uknjiženo', 'u procesu uknjižavanja'] else False


def clean_floor(floor: Optional[str]) -> Optional[str]:
    if not floor:
        return None

    floor = floor.replace('podrum', '-1')
    floor = floor.replace('suteren', '-1')
    floor = floor.replace('nisko prizemlje', '0')
    floor = floor.replace('visoko prizemlje', '0')
    floor = floor.replace('prizemlje', '0')
    floor = floor.replace('potkrovlje', 'max')

    floor = floor.split(' ')[0].strip('.')
    if '/' not in floor:
        return f'{floor}/null'

    return floor


def __debug_data(file: str):
    df = pd.read_json(file)
    dups_price = df.pivot_table(index=['price'], aggfunc='size')
    dups_city = df.pivot_table(index=['city'], aggfunc='size')
    dups_municipality = df.pivot_table(index=['municipality'], aggfunc='size')
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
    print(df.info())


def remove_null_containing_entries(file: str, fields: List[str]):
    df = pd.read_json(file)
    df.dropna(subset=fields, inplace=True)
    df.to_json(file, orient='records')


if __name__ == '__main__':
    input_file = '4zida.json'
    cleaned_file = '4zida_cleaned.json'

    with open(input_file, 'r') as file:
        data = json.load(file)
        for ad in data:
            if not ad['room_number']:
                del ad
                continue
            ad['price'] = int(str(ad['price']).replace('.', ''))
            # ad['link'] =
            # ad['offer_type'] =
            # ad['property_type'] =
            # ad['city'] =
            # ad['municipality'] =
            # ad['room_number'] =
            # ad['square_footage'] =
            ad['heating'] = True if ad['heating'] else False
            ad['floor'] = clean_floor(ad['floor'])
            ad['bathroom_number'] = clean_bathroom_number(ad['bathroom_number'])
            ad['build_year'] = int(ad['build_year']) if ad['build_year'] else None
            ad['elevator'] = True if ad['elevator'] else False
            ad['balcony'] = True if ad['balcony'] else False
            ad['land_area'] = clean_land_area(ad['land_area'])
            ad['registered'] = bool(clean_registered(ad['registered']))
            ad['parking'] = True if ad['parking'] else False
        with open(cleaned_file, 'w') as output_cleaned:
            json.dump(data, output_cleaned)

    remove_null_containing_entries(cleaned_file, ['room_number'])

    # __debug_data(cleaned_file)

    print(f"Cleaned {input_file} file. Output is saved in {cleaned_file} file.")
