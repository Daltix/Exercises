"""
  DALTIX CONFIDENTIAL
  __________________
  
  [2017] Daltix  
   All Rights Reserved.
  
  NOTICE:  All information contained herein is, and remains
  the property of Daltix  and its suppliers,
  if any.  The intellectual and technical concepts contained
  herein are proprietary to Daltix 
  and its suppliers and may be covered by U.S. and Foreign Patents,
  patents in process, and are protected by trade secret or copyright law.
  Dissemination of this information or reproduction of this material
  is strictly forbidden unless prior written permission is obtained
  from Daltix .
 """

import re, json
import requests, bs4

"""
Objective
----------
Implement the 2 functions below:
    - extract_product_data
    - extract_categories
    
The objective is to learn as much as possible about parsing web pages.
In case you get stuck you can always ask for help of course.
You don't have to worry about strange error cases (like what if the site is offline).
Try to document your code as much as possible.

Put your solution in a new file under the solutions directory.

To run the code
----------------
python parsing.py
"""

# TODO insert your urls here!
# First three URLs are the given links, the other four are added to make sure function extract_product_data works properly
URLs = ["https://www.lidl-shop.be/nl-BE/ESMARA-Longshirt-voor-dames/p100214261",
        "https://www.lidl-shop.be/nl-BE/LIVARNOLIVING-Spiegelkast/p100211942",
        "https://www.lidl-shop.be/nl-BE/PARKSIDE-Cirkelzaagblad/p100197506",
        "https://www.lidl-shop.be/nl-BE/MIOMARE-Badjas-voor-heren/p100196928",
        "https://www.lidl-shop.be/nl-BE/VitaVerde-Keramische-pan-24-cm/p100195917",
        "https://www.lidl-shop.be/nl-BE/SHEFFIELD-Keyboardstandaard/p100206408",
        "https://www.lidl-shop.be/nl-BE/Saxa-Loquuntur-Uno-2014/p100197423"]



class ProductInfo:
    """
    Container class for product information.
    Feel free to extend this in case you want to gather more product information.
    """

    def __init__(self, name=None, current_price=None, old_price=None):
        self.name = name
        self.current_price = current_price
        self.old_price = old_price

    def __str__(self):
        return json.dumps({
            'name': self.name,
            'current_price': self.current_price,
            'old_price': self.old_price
        })


class Category:
    """
    Holds information about a category.
    """

    def __init__(self, url: str, name: str = None):
        """
        :param url: the url to the category.
        :param name: the name of the category (text of the element).
        """
        self.url = url
        self.name = name

    def __str__(self):
        return '{category}: {url}'.format(category=name, url=url)


def extract_product_data(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    nametag = str(soup.select('div > div > h1')[0])
    pricetag_new = re.sub(r'\s+', ' ', str(soup.select('div > div > span > b')[0]))  # I did use string editing to remove tabs and newlines
    pricetag_old = str(soup.select('div > div > span > em > span'))

    if pricetag_old == '[]': #If there's no promo for an article, no old_price is returned
        price_old = None
    else:
        price_old = float(re.match(r'^\[<span>(?P<price>[0-9.]+)<\/span>\]$', pricetag_old).group('price'))

    product_rx = re.match(r'^<h1>(?P<product1>[0-9a-zA-Z ]+).(?P<product2>[0-9a-zA-Z ]+)<\/h1>$', nametag, flags=0)
    price_new_rx = re.match(r'^<b> (?P<price1>[0-9]*)\.<sup>(?P<price2>[0-9]*)\*<\/sup>', pricetag_new, flags=0)

    product = product_rx.group('product1') + product_rx.group('product2')
    price_new = float(price_new_rx.group('price1')) + float(price_new_rx.group('price2')) / 100

    return ProductInfo(name=product, current_price=price_new, old_price=price_old)


def extract_categories(html): # Does this also have to be made for the LIDL exercise? Since the screenshot only shows categories from the gamma website
    """
    There are quite some links to other categories on the website, the goal of this function is to return
    all of them. I added a screenshot to show what I mean.
    For every category you should create a Category object holding the url and the name of the category.
    :param html: the html in text form.
    :return: a list of Category objects with one entry for each category under 'assortiment'.
    """
    categories = []
    return categories


if __name__ == '__main__':
    """
    This is the program's entry point. DO NOT EDIT THIS FUNCTION.
    """
    if len(URLs) == 0:
        print('ERROR - add some urls first...')
        exit(1)

    # holds the products
    for url in URLs:
        response = requests.get(url)
        if response and response.text:
            html = response.text

            print('results for: {}'.format(url))
            product = extract_product_data(html)
            print(str(product))

            categories = extract_categories(html)
            for category in categories:
               print(str(category))

    exit(0)
