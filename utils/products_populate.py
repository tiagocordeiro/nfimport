import pandas as pd

import os

local = os.path.dirname(__file__)


def create_products():
    file = str(local + '/csv_data/products.csv')
    df = pd.read_csv(file)

    products = []

    for product in df.T.to_dict().values():
        products.append(product)

    return list(products)


if __name__ == '__main__':
    create_products()
