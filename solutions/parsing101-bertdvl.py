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
However you should pay attention, when selecting items, that your program does not crash if a certain
element is not found (e.g a product with no promo, name, ...). The Pythonic way is to catch exceptions and handle them.
Try to document your code as much as possible.

Put your solution in a new file under the solutions directory.

To run the code
----------------
python parsing.py
"""

URLs = ["https://www.hubo.be/nl/p/zelftrekkende-benzine-grasmaaier-98-5cc-41cm-poweg63772/827608.html",
"https://www.hubo.be/nl/p/klopboormachine-1200w-powx028/497678.html",
"https://www.hubo.be/nl/p/reserverolhouder-pleeboy-chroom/103015.html"
]


"https://www.hubo.be/nl/p/klopboormachine-1200w-powx028/497678.html",
"https://www.hubo.be/nl/p/reserverolhouder-pleeboy-chroom/103015.html"

class ProductInfo:
    """
    Container class for product information.
    Feel free to extend this in case you want to gather more product information.
    """
    def __init__(self, name=None, current_price=None, old_price=None, extra_info=None):
        self.name = name
        self.current_price = current_price
        self.old_price = old_price
        self.extra_info = extra_info
    def __str__(self):
        return json.dumps({
            'name': self.name,
            'current_price': self.current_price,
            'old_price': self.old_price,
            'extra_info': self.extra_info
        })


class Category:
    """
    Holds information about a category.
    """

    def __init__(self, url: str, name: str = None, parentcategory = None):
        self.url = url
        self.name = name
        #self.parentcategory = parentcategory
        #maybe add a tree-like structure for moving through categories

    """
            :param url: the url to the category.
            :param name: the name of the category (text of the element).
            """


    def __str__(self):
        return '{category}: {url}'.format(category=self.name, url=self.url)




def extract_product_data(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    #try to look for a name and price, if those are not present, the product page is invalid
    try:
        name_html = soup.find_all("div", class_="hubo-title__text")[0]
        new_price_html = soup.find_all("div", class_="price")[0]
    except:
        print("Invalid product page")
        return ProductInfo()

    #get content of "price" and "name" html tags
    name = re.search(r'<div class="hubo-title__text">(.*)</div>',str(name_html)).group(1)

    #get the new/current price
    testnewprice = re.search(r'<div class="price">([0-9]*)<span>([0-9,]*).*</span></div>', str(new_price_html))
    new_price = float(testnewprice.group(1) + re.sub(r',', '.', testnewprice.group(2)))

    #if there is a discount, find it otherwise new_price and old_price are the same
    old_price = new_price
    try:
        old_price_html = soup.find_all("span", class_="striped")[0]
        old_price = re.search(r'<span class="striped">([0-9,]*).*</span>', str(old_price_html)).group(1)
        old_price = float(re.sub(',', '.', old_price))
    except:
        pass

    #collects all of the extra information and stores it in a dict
    extra_info_html_div = soup.find_all("div", class_="hb_specs")[0]
    extra_info_html = extra_info_html_div.find_all("tr")
    extra_info = {}
    extra_info_list = re.findall(r'<td width="50%">(.*)</td>[.\n]*<td>(\s)*(.*)</td>', str(extra_info_html))
    for element in extra_info_list:
        extra_info[element[0]] = re.sub(r'\xa0', '',element[2])

    return ProductInfo(name, new_price, old_price, extra_info)
    #remark: extra_info seems to not work with "Uitworp": "Achterwaarts, Opvangsysteem, Zijwaarts" => written wrong by webdesigner


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
