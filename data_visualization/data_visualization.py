import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def belgrade_municipalities_most_properties(connection: Engine):
    query = 'SELECT municipality, COUNT(*) AS num_of_properties ' \
            'FROM ads ' \
            'WHERE city = "Beograd" ' \
            'GROUP BY municipality ' \
            'ORDER BY num_of_properties DESC ' \
            'LIMIT 10'
    df = pd.read_sql(query, con=connection)

    df.plot.bar(x='municipality', y='num_of_properties')
    plt.tick_params(axis='x', labelsize=6, rotation=30)
    plt.title('Belgrade municipalities with most properties')
    plt.show()


def number_of_flats_by_square_footage(connection: Engine):
    query = 'SELECT square_footage, COUNT(*) AS num_of_properties ' \
            'FROM ads ' \
            'WHERE property_type = "stanovi" ' \
            'GROUP BY square_footage ' \
            'ORDER BY num_of_properties DESC'
    df = pd.read_sql(query, con=connection)

    counter = {'<=35': 0, '36-50': 0, '51-65': 0, '66-80': 0, '81-95': 0, '96-110': 0, '>=111': 0}

    for _, ad in df.iterrows():
        if ad['square_footage'] <= 35:
            counter['<=35'] += ad['num_of_properties']
        elif 36 <= ad['square_footage'] <= 50:
            counter['36-50'] += ad['num_of_properties']
        elif 51 <= ad['square_footage'] <= 65:
            counter['51-65'] += ad['num_of_properties']
        elif 66 <= ad['square_footage'] <= 80:
            counter['66-80'] += ad['num_of_properties']
        elif 81 <= ad['square_footage'] <= 95:
            counter['81-95'] += ad['num_of_properties']
        elif 96 <= ad['square_footage'] <= 110:
            counter['96-110'] += ad['num_of_properties']
        elif ad['square_footage'] >= 111:
            counter['>=111'] += ad['num_of_properties']

    labels = []
    values = []
    for key, value in counter.items():
        labels.append(key)
        values.append(value)

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel('Number of flats')
    ax.set_xlabel('Square footage')
    ax.set_title('Number of flats by square footage')
    plt.show()


def number_of_properties_by_decade(connection: Engine):
    query = 'SELECT build_year, COUNT(*) AS num_of_properties ' \
            'FROM ads ' \
            'GROUP BY build_year ' \
            'ORDER BY build_year DESC'
    df = pd.read_sql(query, con=connection)

    counter = {'1951-1960': 0, '1961-1970': 0, '1971-1980': 0, '1981-1990': 0,
               '1991-2000': 0, '2001-2010': 0, '2011-2020': 0}

    for _, ad in df.iterrows():
        if 1951 <= ad['build_year'] <= 1960:
            counter['1951-1960'] += ad['num_of_properties']
        elif 1961 <= ad['build_year'] <= 1970:
            counter['1961-1970'] += ad['num_of_properties']
        elif 1971 <= ad['build_year'] <= 1980:
            counter['1971-1980'] += ad['num_of_properties']
        elif 1981 <= ad['build_year'] <= 1990:
            counter['1981-1990'] += ad['num_of_properties']
        elif 1991 <= ad['build_year'] <= 2000:
            counter['1991-2000'] += ad['num_of_properties']
        elif 2001 <= ad['build_year'] <= 2010:
            counter['2001-2010'] += ad['num_of_properties']
        elif 2011 <= ad['build_year'] >= 2020:
            counter['2011-2020'] += ad['num_of_properties']

    labels = []
    values = []
    for key, value in counter.items():
        labels.append(key)
        values.append(value)

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel('Number of properties')
    ax.set_xlabel('Decade')
    ax.set_title('Number of built properties per decade')
    plt.tick_params(axis='x', rotation=27)
    plt.show()


def sales_rental_ratio_top_5(connection: Engine):
    query = 'SELECT SUM(ad.renting) AS rent_count, SUM(ad.selling) AS sell_count, ad.city, ' \
            'SUM(ad.selling) + SUM(ad.renting) AS total ' \
            'FROM (' \
            'SELECT IF(offer_type = "izdavanje", 1, 0) AS renting, IF(offer_type= "prodaja", 1, 0) AS selling, city ' \
            'FROM ads' \
            ') ad ' \
            'GROUP BY ad.city ' \
            'ORDER BY total DESC ' \
            'LIMIT 5'
    df = pd.read_sql(query, con=connection)
    print(df)

    df.plot.bar(x='city', y=['rent_count', 'sell_count'])
    plt.tick_params(axis='x', labelsize=8, rotation=30)
    plt.title('Sales-Rental ratio of top 5 cities')

    for index, ad in df.iterrows():
        total = ad['total']
        sell_count = ad['sell_count']
        plt.text(x=index, y=sell_count+1, s=f"{round(sell_count * 100 / total, 2)}%", fontdict=dict(fontsize=8))
    plt.show()


def selling_properties_price_category(connection: Engine):
    query = 'SELECT price, COUNT(*) as num_of_properties ' \
            'FROM ads ' \
            'WHERE offer_type = "prodaja" ' \
            'GROUP BY price ' \
            'ORDER BY price ASC'
    df = pd.read_sql(query, con=connection)

    counter = {'<=49.999': 0, '50.000-99.999': 0, '100.000-149.999': 0, '150.000-199.999': 0, '>=200.000': 0}

    for _, ad in df.iterrows():
        if ad['price'] <= 49_999:
            counter['<=49.999'] += ad['num_of_properties']
        elif 50_000 <= ad['price'] <= 99_999:
            counter['50.000-99.999'] += ad['num_of_properties']
        elif 100_000 <= ad['price'] <= 149_999:
            counter['100.000-149.999'] += ad['num_of_properties']
        elif 150_000 <= ad['price'] <= 199_999:
            counter['150.000-199.999'] += ad['num_of_properties']
        elif ad['price'] >= 200_000:
            counter['>=200.000'] += ad['num_of_properties']

    labels = []
    values = []
    for key, value in counter.items():
        labels.append(key)
        values.append(value)

    fig, ax = plt.subplots()
    ax.bar(labels, values, align='center', width=0.8)
    ax.set_ylabel('Number of properties')
    ax.set_xlabel('Price range in €')
    ax.set_title('Number of selling properties per price range')
    plt.tick_params(axis='x', labelsize=7)

    total = sum(values)
    for index, properties in enumerate(values):
        plt.text(x=index, y=properties+50, s=f"{round(properties * 100 / total, 2)}%", fontdict=dict(fontsize=10))

    plt.show()


def properties_with_parking_in_belgrade(connection: Engine):
    query = 'SELECT COUNT(*) as have_parking ' \
            'FROM ads ' \
            'WHERE city = "Beograd" AND parking = True'
    df = pd.read_sql(query, con=connection)
    have_parking = df['have_parking'][0]

    query = 'SELECT COUNT(*) as properties_in_Belgrade ' \
            'FROM ads ' \
            'WHERE city = "Beograd"'
    df = pd.read_sql(query, con=connection)
    properties_in_belgrade = df['properties_in_Belgrade'][0]

    fig, ax = plt.subplots()
    ax.bar(['have parking', 'properties in Belgrade'], [have_parking, properties_in_belgrade])
    plt.text(x=0, y=have_parking+50,
             s=f"{round(have_parking * 100 / properties_in_belgrade, 2)}%", fontdict=dict(fontsize=20))
    ax.set_ylabel('Number of properties')
    ax.set_title('Number of properties with parking in Belgrade')
    plt.show()


if __name__ == '__main__':
    db_connection = create_engine('mysql+pymysql://root:root@localhost/real_estate_ads')

    belgrade_municipalities_most_properties(db_connection)
    number_of_flats_by_square_footage(db_connection)
    number_of_properties_by_decade(db_connection)
    sales_rental_ratio_top_5(db_connection)
    selling_properties_price_category(db_connection)
    properties_with_parking_in_belgrade(db_connection)

    db_connection.dispose()
