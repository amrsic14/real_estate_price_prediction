import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def sales_rental_ratio(connection: Engine):
    query = 'SELECT COUNT(*) as number_of_ads, offer_type ' \
            'FROM ads ' \
            'GROUP BY offer_type'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'a_sales_rental_ratio.csv', index_label=False, encoding="utf-8", index=False)


def sales_per_city(connection: Engine):
    query = 'SELECT COUNT(*) as number_of_selling_properties, city ' \
            'FROM ads ' \
            'WHERE offer_type = "prodaja" ' \
            'GROUP BY city ' \
            'ORDER BY number_of_selling_properties DESC'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'b_sales_per_city.csv', index_label=False, encoding="utf-8", index=False)


def registered_properties(connection: Engine):
    query = 'SELECT COUNT(*) as number_of_properties, registered, property_type ' \
            'FROM ads ' \
            'GROUP BY registered, property_type'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'c_registered_properties.csv', index_label=False, encoding="utf-8", index=False)


def top_30_sales(connection: Engine):
    query = '(SELECT * ' \
            'FROM ads ' \
            'WHERE property_type = "kuce" AND offer_type = "prodaja" ' \
            'ORDER BY price DESC ' \
            'LIMIT 30) ' \
            'UNION ' \
            '(SELECT * ' \
            'FROM ads ' \
            'WHERE property_type = "stanovi" AND offer_type = "prodaja" ' \
            'ORDER BY price DESC ' \
            'LIMIT 30)'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'd_top_30_sales.csv', index_label=False, encoding="utf-8", index=False)


def top_100_square_footage(connection: Engine):
    query = '(SELECT * ' \
            'FROM ads ' \
            'WHERE property_type = "kuce" ' \
            'ORDER BY square_footage DESC ' \
            'LIMIT 100) ' \
            'UNION ' \
            '(SELECT * ' \
            'FROM ads ' \
            'WHERE property_type = "stanovi" ' \
            'ORDER BY square_footage DESC ' \
            'LIMIT 100)'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'e_top_100_square_footage.csv', index_label=False, encoding="utf-8", index=False)


def built_2020_price(connection: Engine):
    query = 'SELECT * ' \
            'FROM ads ' \
            'WHERE offer_type = "prodaja" AND build_year = 2020 ' \
            'ORDER BY price DESC'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'f_built_2020_price_sale.csv', index_label=False, encoding="utf-8", index=False)

    query = 'SELECT * ' \
            'FROM ads ' \
            'WHERE offer_type = "izdavanje" AND build_year = 2020 ' \
            'ORDER BY price DESC'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'f_built_2020_price_rent.csv', index_label=False, encoding="utf-8", index=False)


def top_30_room_count(connection: Engine):
    query = 'SELECT * ' \
            'FROM ads ' \
            'ORDER BY room_number DESC ' \
            'LIMIT 30'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'g_top_30_room_count.csv', index_label=False, encoding="utf-8", index=False)


def top_30_square_footage(connection: Engine):
    query = 'SELECT * ' \
            'FROM ads ' \
            'WHERE property_type = "stanovi" ' \
            'ORDER BY square_footage DESC ' \
            'LIMIT 30'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'g_top_30_square_footage.csv', index_label=False, encoding="utf-8", index=False)


def top_30_land_area(connection: Engine):
    query = 'SELECT * ' \
            'FROM ads ' \
            'WHERE property_type = "kuce" ' \
            'ORDER BY land_area DESC ' \
            'LIMIT 30'
    df = pd.read_sql(query, con=connection)
    df.to_csv(f'g_top_30_land_area.csv', index_label=False, encoding="utf-8", index=False)


if __name__ == '__main__':
    db_connection = create_engine('mysql+pymysql://root:root@localhost/real_estate_ads')

    sales_rental_ratio(db_connection)
    sales_per_city(db_connection)
    registered_properties(db_connection)
    top_30_sales(db_connection)
    top_100_square_footage(db_connection)
    built_2020_price(db_connection)
    top_30_room_count(db_connection)
    top_30_square_footage(db_connection)
    top_30_land_area(db_connection)

    db_connection.dispose()
