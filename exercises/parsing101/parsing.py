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
URLs = [
]


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
    def __init__(self, url: str, name: str =None):
        """
        :param url: the url to the category.
        :param name: the name of the category (text of the element).
        """
        self.url = url
        self.name = name

    def __str__(self):
        return '{category}: {url}'.format(category=self.name, url=self.url)


def extract_product_data(html):
    """
    Parse the HTML using BeautifulSoup to find the most important HTML elements which contain information 
    about the main product on the page. You can ignore any other products which might be on the bottom of the page.
      
    The following are the most important:
        - Name (sometimes they put extra info in the product's name e.g Grasmachine 4 wielen) 
        - Current price
            Note that often prices are split in 2 like this: 
            <span>
                19
                <span>00</span>
            <span> 
            In this case grab the enclosing <span>.
        
        - Old price (if the product is in promo).
        
    Once you have the HTML elements, extract their values using a regex. 
    Do NOT use string operations such as split or whatever...
      
      Example: 
        HTML element:   <p> Name of the product </p>
        regex:          '^<p>(?P<name>[\w\-\s]+)<\/p>$'          (Tip: we use named capturing groups in our regexes.)
        name:           Name of the product
    
    After extracting the values using a regex you can save the strings in a ProductInfo object, like so:
    ProductInfo(name='Grasmaaier', current_price='50,50', old_price='55,50')
    
    :param html: the html string.
    :return: a ProductInfo object holding all found product data.
    """
    return ProductInfo()


def extract_categories(html):
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
