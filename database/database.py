import json

import mysql.connector


class DBConnection:

    def __init__(self, user: str, password: str, host: str, database: str):
        self.__connection = mysql.connector.connect(user=user, password=password, host=host, database=database)
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__connection.commit()
        self.__connection.close()

    def clear_table(self, table: str):
        self.__cursor.execute(f"TRUNCATE TABLE {table}")

    def insert_from_json(self, table: str, json_file: str):
        with open(json_file, 'r') as file:
            data = json.load(file)
            for ad in data:
                operation = f"INSERT INTO {table} " \
                            f"(price, link, offer_type, property_type, city, municipality, room_number, " \
                            f"square_footage, heating, bathroom_number, build_year, elevator, balcony, " \
                            f"land_area, registered, parking, state) " \
                            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                params = (ad['price'], ad['link'], ad['offer_type'], ad['property_type'], ad['city'],
                          ad['municipality'], ad['room_number'], ad['square_footage'], ad['heating'],
                          ad['bathroom_number'], ad.get('build_year', None), ad['elevator'], ad['balcony'],
                          ad['land_area'], ad['registered'], ad['parking'], ad.get('state', None))

                self.__cursor.execute(operation, params)


if __name__ == '__main__':
    db_conn = DBConnection(
        user='root',
        password='root',
        host='localhost',
        database='real_estate_ads'
    )

    db_conn.clear_table('ads')
    db_conn.insert_from_json(table='ads', json_file='../data_cleaning/4zida_cleaned.json')
    # db_conn.insert_from_json(table='ads', json_file='../data_cleaning/nekretnine_cleaned.json')
