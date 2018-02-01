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
# First three URL are the given links, I added the other ten to make sure both functions work properly
URLs = ["https://www.lidl-shop.be/nl-BE/ESMARA-Longshirt-voor-dames/p100214261",
        "https://www.lidl-shop.be/nl-BE/LIVARNOLIVING-Spiegelkast/p100211942",
        "https://www.lidl-shop.be/nl-BE/PARKSIDE-Cirkelzaagblad/p100197506",
        "https://www.lidl-shop.be/nl-BE/MIOMARE-Badjas-voor-heren/p100196928",
        "https://www.lidl-shop.be/nl-BE/VitaVerde-Keramische-pan-24-cm/p100195917",
        "https://www.lidl-shop.be/nl-BE/SHEFFIELD-Keyboardstandaard/p100206408",
        "https://www.lidl-shop.be/nl-BE/Saxa-Loquuntur-Uno-2014/p100197423",
        "https://www.lidl-shop.be/nl-BE/Ch-teau-Guiraud-Sauternes-Grand-Cru-Class-AOP-1995/p100161050",
        "https://www.lidl-shop.be/nl-BE/Montepulciano-d-Abruzzo-DOP-2015/p100000087",
        "https://www.lidl-shop.be/nl-BE/PARKSIDE-Set-steen-HSS-of-houtboren/p100214640",
        "https://www.lidl-shop.be/nl-BE/FLORABEST-Handverticuteerder-of-cultivator/p100216438",
        "https://www.lidl-shop.be/nl-BE/Acties/a069967",
        "https://www.google.be"] # Last two links are not productpages, they are added to control the error handling of
                                #  both functions

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
            'old_price': self.old_price,
        }, ensure_ascii=False)  # This option makes sure special characters such as à, é, è, etc are printed correctly


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
        return '{category}: {url}'.format(category=self.name, url=self.url)


def extract_product_data(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    nametag = soup.select('div > div > h1')
    pricetag_new = soup.select('div > div > span > b')
    pricetag_old = soup.select('div > div > span > em > span')
    price_error = False # Added to know if< only a price or a productname isn't found, or if neither is found.
    product_error = False # Idem

    try:
        price_old = float(re.match(r'^\[<span>(?P<price>[0-9.]+)<\/span>\]$', str(pricetag_old[0])).group('price'))
    except:
        price_old = None # If there's no promo, no old price is returned.

    try:
        product_rx = re.match(r'^<h1>(?P<product1>[0-9a-zA-Z \-âéèêà´,]+).?(?P<product2>[0-9a-zA-Z \-âéèêà´,]*)<\/h1>$',
                              str(nametag[0]))
        # Included [-âéèêà´,] in regex to avoid trouble with some wines (e.g. Chàteau, saint-émilion, d´Abruzzo,etc.)
        product = product_rx.group('product1') + product_rx.group('product2')  # Join product names
    except:
        product_error = True

    try:
        price_new_rx = re.match(r'^<b> (?P<price1>[0-9]*)\.<sup>(?P<price2>[0-9]*)\*<\/sup>',
                                re.sub(r'\s+', ' ', str(pricetag_new[0])))
        # Join prices:
        price_new = round(float(price_new_rx.group('price1')) + float(price_new_rx.group('price2')) / 100,2)
    except:
        price_error = True

    if price_error and not product_error:
            return 'No price was found on this page, make sure a Lidl productpage is supplied.'
    elif product_error and not price_error:
            return 'No productname was found on this page, make sure a Lidl productpage is supplied.'
    elif product_error and price_error:
            return 'No price and no productname were found on this page, make sure a Lidl productpage is supplied.'
    else:
        return ProductInfo(name=product, current_price=price_new, old_price=price_old)


def extract_categories(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    categories_tags = soup.select(".secondary-nav > li > a ")
    base_URL_rx = soup.select(".company-area > li > a")

    try:
        base_URL = re.match(r'<a .* href="(?P<base>.+)">.*</a>', str(base_URL_rx[0])).group('base')
    except:
        print('Base-url not found on page, using default: http://www.lidl-shop.be')
        # In case the location of this link changes, we use the default link (which is unlikely to change anyway):
        base_URL = 'http://www.lidl-shop.be'

    categories = []

    if len(categories_tags) == 0:
        print('The default categories are not findable on this page, make sure a Lidl productpage is supplied.')
    else:
        for i in categories_tags:
            a_string = re.sub(r'\s+', ' ', str(i))
            regex = re.match(r'^<a .* href="(?P<link>.+)"> (?P<name>.+)</a>$', a_string)
            category = regex.group('name')
            link = base_URL + regex.group('link')
            categories.append(Category(link, category))

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
