#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GROUP 44: Johnny Nguyen & Majid Mohamed Hamid"""

from os import path
from inspect import currentframe, getfile
import mysql.connector as mysql
import mysql_details
import pandas as pd

cmd_folder = path.realpath(
    path.abspath(path.split(getfile(currentframe()))[0])) + '/'

def get_products_filtered(categories=None):
    """
    Indata
    Antingen skickas None in (pythons version av NULL) via categories och då
    skall alla produkter hämtas. Om categories inte är None, skickas en
    dictionary in med gender, type och subtype. Gender är plaggets målgrupps
    kön, type representerar huvudkategorin, subtype subkategorin.

    Returdata
    En lista av produkter. Respektive produkts information finns i en
    dictionary med följande nycklar:
    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
       'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans',
     'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]
    """

    # df = pd.read_csv(cmd_folder + 'data/Products.csv')
    # if categories is not None:
    #     for category in categories.keys():
    #         df = df[df[category] == categories[category]]

    #return df.to_dict('records')
    ''' SQL '''
    connection = mysql.connect(user=mysql_details.MYSQL_USER,
                        passwd=mysql_details.MYSQL_PASS,
                        database=mysql_details.MYSQL_DATABASE,
                        host='127.0.0.1')

    cnx = connection.cursor(dictionary=True)
    if categories is None:
        cnx.execute('SELECT * FROM Products;')
    else:
        cnx.execute('SELECT * FROM Products WHERE gender = \'' + categories['gender'] +
        '\' AND type = \'' + categories['type'] +
        '\' AND subtype = \'' + categories['subtype'] + '\'' + ';')
    connection.close()
    return cnx.fetchall()


def get_products_search(values):
    """
    Indata
    En lista (array) utav strängar (enskilda ord) som skall matchas mot märket
    på alla typer av produkter.

    Returdata
    En lista av produkter. Respektive produkts information finns i en
    dictionary med följande nycklar:

    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
      'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans',
     'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'},
    ]
    """

    # df = pd.read_csv(cmd_folder + 'data/Products.csv')
    # df = df[df['brand'].str.contains('(?i)' + '|'.join(values))]

    # return df.to_dict('records')
    ''' SQL '''
    connection = mysql.connect(user=mysql_details.MYSQL_USER,
                           passwd=mysql_details.MYSQL_PASS,
                           database=mysql_details.MYSQL_DATABASE,
                           host='127.0.0.1')

    cnx = connection.cursor(dictionary=True, buffered=True)

    query = 'SELECT * FROM Products WHERE brand LIKE \'%'
    for brand in values:
        query += brand + '%\' OR brand LIKE \'%'

    cnx.execute(query[:-16] + ';') # We remove the last "OR brand LIKE \'%" from the query

    connection.close()
    return cnx.fetchall()


def get_products_ids(ids):
    """
    Indata
    En lista (array) av heltal som representerar artikelnummer på produkter.

    Returdata
    En lista av produkter. Respektive produkts information finns i en
    dictionary med följande nycklar:

    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
      'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans',
     'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]
    """

    # df = pd.read_csv(cmd_folder + 'data/Products.csv')
    # df = df.loc[df['id'].isin(ids)]

    # return df.to_dict('records')
    ''' SQL '''
    connection = mysql.connect(user=mysql_details.MYSQL_USER,
                           passwd=mysql_details.MYSQL_PASS,
                           database=mysql_details.MYSQL_DATABASE,
                           host='127.0.0.1')

    cnx = connection.cursor(dictionary=True)

    prod_list = []
    for id in list(set(ids)):
        cnx.execute('SELECT * FROM Products WHERE id = {};'.format(id))
        prod_list += cnx.fetchall()

    connection.close()
    return prod_list


def get_categories():
    """
    Returdata
    En lista innehållande dictionaries med nycklarna title och children.
    title representerar könet plaggen är gjorda för (t.ex. Dam och Herr).
    children skall hålla en lista utav ytterligare dictionary object, där
    varje dictionary innehåller nycklarna url och name.
    url tilldelar ni en tom sträng (d.v.s. '') och nyckeln name tilldelar
    ni en huvudkategori.

    Exempelvis:
    [{'title': 'Dam', 'children': [{'url': '', 'name': 'Tröjor'},
                                   {'url': '', 'name': 'Byxor'}]},
    {'title': 'Herr', 'children': [{'url': '', 'name': 'Tröjor'},
                                   {'url': '', 'name': 'Väskor'}]}]
    """

    # df = pd.read_csv(cmd_folder + 'data/Products.csv')
    # genders = df['gender'].unique()
    # types = [
    #     df[(df['gender'] == genders[0])]['type'].unique().tolist(),
    #     df[(df['gender'] == genders[1])]['type'].unique().tolist()
    # ]
    # children = [[{
    #     'url': '',
    #     'name': name
    # } for name in types[0]], [{
    #     'url': '',
    #     'name': name
    # } for name in types[1]]]
    ''' SQL '''
    connection = mysql.connect(user=mysql_details.MYSQL_USER,
                           passwd=mysql_details.MYSQL_PASS,
                           database=mysql_details.MYSQL_DATABASE,
                           host='127.0.0.1')

    cnx = connection.cursor(dictionary=True)

    cnx.execute('SELECT DISTINCT gender FROM Products;')
    genders = cnx.fetchall()
    cnx.execute('SELECT DISTINCT type FROM Products WHERE gender = \'' + genders[0]['gender'] + '\';')
    female_types = cnx.fetchall()
    cnx.execute('SELECT DISTINCT type FROM Products WHERE gender = \'' + genders[1]['gender'] + '\';')
    male_types = cnx.fetchall()
    types = [
        female_types,
        male_types
    ]
    children = [[{
        'url': '',
        'name': name['type']
    } for name in types[0]], [{
        'url': '',
        'name': name['type']
    } for name in types[1]]]

    connection.close()

    result = [{
        'title': genders[0]['gender'],
        'children': children[0]
    }, {
        'title': genders[1]['gender'],
        'children': children[1]
    }]
    return result


def get_subcategories(gender, category):
    """
    Indata
    Två strängar, gender och category, där gender är könet som det efterfrågas
    kläder för och category är huvudkategorin vars subkategorier vi vill hämta.

    Returdata
    En lista innahållande dictionaries med nycklarna gender, category, och
    children. gender representerar könet plaggen är gjorda för (t.ex. Dam och
    Herr). category är den inkommande kategorin vi hämtar subkategorier för
    children skall hålla en lista utav ytterligare dictionary object, där
    varje dictionary
    innehåller nycklarna url och name.
    url tilldelar ni en tom sträng (d.v.s. '') och nyckeln name tilldelar ni en
    subkategori.

    Exempelvis:
    [{'gender': 'Dam', 'category': 'Tröjor', 'children':
        [{'url': '', 'name': 'T-shirts'}, {'url': '', 'name': 'Linnen'}]}]
    """

    # df = pd.read_csv(cmd_folder + 'data/Products.csv')
    # types = df[(df['gender'] == gender)
    #            & (df['type'] == category)]['subtype'].unique().tolist()
    # children = [{'url': '', 'name': name} for name in types]
    # result = [{'gender': gender, 'category': category, 'children': children}]
    ''' SQL '''
    connection = mysql.connect(user=mysql_details.MYSQL_USER,
                           passwd=mysql_details.MYSQL_PASS,
                           database=mysql_details.MYSQL_DATABASE,
                           host='127.0.0.1')

    cnx = connection.cursor(dictionary=True)

    cnx.execute(
        'SELECT DISTINCT subtype FROM Products WHERE gender = \'' + gender +
        '\' AND type = \'' + category + '\';'
        )
    types = cnx.fetchall()
    children = [{'url': '', 'name': name['subtype']} for name in types]
    result = [{'gender': gender, 'category': category, 'children': children}]

    connection.close()
    return result


def write_order(order):
    """
    Indata
    order som är en dictionary med nycklarna och dess motsvarande värden:
    town: Kundens stad
    name: Kundens namn
    zipcode: Kundens postkod
    address: Kundens address
    email: Kundens email
    items: En lista av heltal som representerar alla produkters artikelnummer.
        Så många gånger ett heltal finns i listan, så många artiklar av den
        typen har kunden köpt. Exempelvis: [1,2,2,3]. I den listan har kunden
        köpt 1 styck av produkt 1, 2 styck av produkt 2, och 1 styck av
        produkt 3.
    """
    connection = mysql.connect(user=mysql_details.MYSQL_USER,
                           passwd=mysql_details.MYSQL_PASS,
                           database=mysql_details.MYSQL_DATABASE,
                           host='127.0.0.1')

    cnx = connection.cursor(dictionary=True, buffered=True)

    # df_orders = pd.read_csv(cmd_folder + 'data/Orders.csv')
    # Get new order ID
    cnx.execute('SELECT MAX(orderid) FROM Orders;')
    orderID = cnx.fetchone()['MAX(orderid)'] + 1
    # orderID = df_orders['orderid'].max() + 1
    # Grab the products id number and the amount of each product
    item_ids = list(map(int, order['items'].strip('[]').split(',')))
    items = [{
        'id': int(x),
        'amount': item_ids.count(x)
    } for x in list(set(item_ids))]

    # Get the name and so on for the customer.
    try:
        firstname, lastname = order['name'].split()
    except Exception:
        firstname = order['name']
        lastname = ''
    email = order['email']
    address = order['address']
    zipcode = order['zipcode']
    town = order['town']

    # Suggested by OLIVER LJUNG Jan 13, 2022
    if firstname == None:
        raise Exception("Beställnings formulär(Namn) saknas. Försök igen...")
    if email == None:
        raise Exception("Beställnings formulär(E-post) saknas. Försök igen...")
    if address == None:
        raise Exception("Beställnings formulär(Address) saknas. Försök igen...")
    if zipcode == None:
        raise Exception("Beställnings formulär(Postnummer) saknas. Försök igen...")
    if town == None:
        raise Exception("Beställnings formulär(Ort) saknas. Försök igen...")
    #

    cnx.execute('SELECT id FROM Customers WHERE firstname = \'' + firstname +
    '\' AND lastname = \'' + lastname +
    '\' AND street = \'' + address +
    '\' AND city = \'' + town +
    '\' AND zipcode = ' + zipcode + ';'
    )
    customerID = cnx.fetchone()

    # If the customer does not already exist in the DB, make a new entry
    if customerID is None:
        # Get new customer ID
        cnx.execute('SELECT MAX(id) FROM Customers;')
        customerID = cnx.fetchone()['MAX(id)'] + 1  # Although it's already autoincremented we need this variable for when inserting into Orders

        cnx.execute(
                '''INSERT INTO Customers
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');'''.format(
                firstname, lastname, address, town, zipcode, customerID, email
        ))
        connection.commit()
    else:
        customerID = customerID['id']

    # Write the actual order
    #df_products = pd.read_csv(cmd_folder + 'data/Products.csv')
    for item in items:
        # product = df_products[df_products['id'] == item['id']].to_dict(
        #     'records')[0]
        # df_orders.loc[len(df_orders)] = [
        #     orderID, firstname, lastname, address, town, zipcode,
        #     product['id'], product['brand'], product['type'],
        #     product['subtype'], product['color'], product['gender'],
        #     product['price'], product['size'], item['amount']
        # ]
        cnx.execute('''INSERT INTO Orders (orderid, productid, amount)
                    VALUES ({}, {}, {});'''.format(
                        orderID, item['id'], item['amount']
                    )
                )
        connection.commit()
        cnx.execute('''INSERT INTO OrderDetails (orderid, customerid)
            VALUES ({}, {});'''.format(
                orderID, customerID
            )
        )
        connection.commit()

    #df_orders.to_csv(cmd_folder + 'data/Orders.csv', index=False, encoding='utf-8')
    connection.close()


def get_20_most_popular():
    """
    Returdata
    En lista av de 20 produkter som är mest sålda i webshopen.
    Respektive produkts information finns i en dictionary med följande nycklar:
    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
      'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants,
     'subtype': 'Jeans', 'color': 'Black', 'gender': 'Male', 'price': 449,
     'size': 'S'}]
    """

    # df = pd.read_csv(cmd_folder + 'data/Orders.csv')
    # top20_ids = df.groupby(['id']).sum().loc[:, ['amount']].sort_values(
    #     'amount', ascending=False).iloc[:20].index.tolist()
    # df = pd.read_csv(cmd_folder + 'data/Products.csv')

    # return df.iloc[top20_ids, :].to_dict('records')
    ''' SQL '''
    connection = mysql.connect(user=mysql_details.MYSQL_USER,
                           passwd=mysql_details.MYSQL_PASS,
                           database=mysql_details.MYSQL_DATABASE,
                           host='127.0.0.1')

    cnx = connection.cursor(dictionary=True)

    cnx.execute(
        'SELECT DISTINCT productid, COUNT(productid) AS `top` FROM Orders GROUP BY productid ORDER BY `top` DESC LIMIT 0,20;'
        )

    result = []
    rows = cnx.fetchall()
    for row in rows:
        if row['productid'] is None:
            break
        cnx.execute(
            'SELECT * FROM Products WHERE id = {};'.format(row['productid'])
            )
        result += cnx.fetchall()

    connection.close()
    return result


def main():
    # test = get_products_filtered({'type': 'Bags', 'subtype': 'Leather bag'})
    # test = get_products_ids([1,2,3])
    # test = get_categories()
    # test = get_subcategories('Female', 'Bags')
    # test = get_20_most_popular()
    test = write_order({
        'town':
        'asad',
        'name':
        'öäåasd asd',
        'items':
        '[2160,2160,2160,2160,2160,2160,2160,2160,2160]',
        'zipcode':
        '123123',
        'address':
        'asd',
        'email':
        'asd'
    })
    # test = get_products_search(['jack', 'and', 'jones'])
    print(test)


if __name__ == '__main__':
    main()
