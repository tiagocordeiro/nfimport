from pybling.products import list_products


def update_from_bling():
    products = list_products(page='all')

    products_list = products['retorno']['produtos']
    return products_list


if __name__ == '__main__':
    update_from_bling()
