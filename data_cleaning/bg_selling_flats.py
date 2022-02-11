import json
import pandas as pd
import urllib.request
import urllib.parse
import time

from sqlalchemy import create_engine


def load_belgade_selling_flats_db():
    connection = create_engine('mysql+pymysql://root:root@localhost/real_estate_ads')
    query = 'SELECT price, municipality, address, room_number, square_footage, floor, elevator, balcony, registered ' \
            'FROM ads ' \
            'WHERE city = "Beograd" AND offer_type = "prodaja" AND property_type = "stanovi"'
    df = pd.read_sql(query, con=connection)

    connection.dispose()
    return df


def clean_floor_data(df):
    # drop null values
    df.dropna(subset=['floor'], inplace=True)
    drop_ind = []
    for ind, row in df.iterrows():
        if "null" in row['floor']:
            drop_ind.append(ind)
    df.drop(drop_ind, inplace=True)

    # extract floor
    for ind, row in df.iterrows():
        floor, max_floor = row['floor'].split('/')
        df.at[ind, 'floor'] = max_floor if "max" in floor else floor
    df['floor'] = df['floor'].apply(pd.to_numeric)


def add_distance_to_center(df):
    bing_maps_key = "Ag2JbMXKFJqnkx9KFbScUGJ0szlyR7_BYzeo4ZfiEkfjr_SZMz24FOpVBImTndnk"
    for ind, row in df.iterrows():
        wp0 = urllib.parse.quote(f"Beograd,{row['municipality']}", safe='')
        wp1 = urllib.parse.quote(f"Beograd,{row['municipality']},{row['address']}", safe='')
        route_url = \
            f"http://dev.virtualearth.net/REST/v1/Routes/Walking?wp.0={wp0}&wp.1={wp1}&output=json&key={bing_maps_key}"

        try:
            request = urllib.request.Request(route_url)
            response = urllib.request.urlopen(request)
            result_str = response.read().decode(encoding="utf-8")
            result = json.loads(result_str)

            distance = result['resourceSets'][0]['resources'][0]['travelDistance']
            df.at[ind, 'distance'] = float(distance)
        except BaseException as e:
            print(route_url)
            print(e)

        if ind % 50 == 0:
            print(ind)
            time.sleep(60)


def drop_columns(df, columns):
    df.drop(columns=columns, inplace=True)


def save_belgrade_selling_flats_to_csv(file: str):
    df = load_belgade_selling_flats_db()
    clean_floor_data(df)
    add_distance_to_center(df)
    drop_columns(df, ['municipality', 'address'])
    df.to_csv(file, index_label=False, encoding="utf-8", index=False)


if __name__ == '__main__':
    save_belgrade_selling_flats_to_csv('belgrade_selling_flats.csv')
