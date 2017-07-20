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

# TODO insert your urls here!
URLs = ["""https://www.brico.be/nl/bouw-materialen/ladders/omvormbare-ladders/sencys-omvormbare-ladder-aluminium-3-x-9-treden/5289839""",
        """https://www.brico.be/nl/gereedschap-installatie/elektra/kabels-en-behuizing/elektrische-kabels/sencys-elektrische-kabel-'xvb-f2-3g1-5'-grijs-50-m/5233773""",
"""https://www.brico.be/nl/gereedschap-installatie/elektra/kabels-en-behuizing/elektrakabel-accessoires/flesfitting-e27-met-schak.-2m-zwart/9806900"""]


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
      #My code
    try:
        soup = bs4.BeautifulSoup(html,"html.parser")
    except:
        print("Unable to parse the provided link")
        return ProductInfo()#Returns the method empty handed
    try:
        #Name
        name_dummy = soup.find('div',{"class":"product-detail_sections"}).find('h1',{"class":"product-detail_title"}).text.strip()#this is another way to get the data of interest, not sure if you approve of this way, so added the regex 
        namehtml = soup.find('div',{"class":"product-detail_sections"}).find('h1',{"class":"product-detail_title"})
        name = re.search(r'.*>(?P<name>.+\S)<.*',str(namehtml)).group('name')#regex code that does the same as name_dummy
        #Price
        price = soup.find('div',{"class":"product-detail_price"})
        discount = re.search(r'.*product-detail_price-old-price.*',str(price))#Is there a discount?
        new_price_dummy = soup.find('div',{"class":"product-detail_price-new-price"}).find('span',{"class":"product-detail_price-new-price-amount"}).text.strip()#again..the other way
        new_pricehtml = soup.find('div',{"class":"product-detail_price-new-price"}).find('span',{"class":"product-detail_price-new-price-amount"})
        new_price = re.search(r'\w*>\s+(?P<newprice_euro>\d+\.)<span class="product-detail_price-new-price-cent">(?P<newprice_cent>\d+)</span>',str(new_pricehtml))#The regex way
        new_price = new_price.group('newprice_euro') + new_price.group('newprice_cent')#This is because of the splitted euro and cent parts in the HTML
        if discount == None:#If there is no discount, the old price is the same as the new price
            old_price = new_price
        else:
            old_price_dummy = soup.find('div',{"class":"product-detail_price-old-price"}).find('span',{"class":"product-detail_price-old-price-amount"}).text.strip()
            old_pricehtml = soup.find('div',{"class":"product-detail_price-old-price"}).find('span',{"class":"product-detail_price-old-price-amount"})
            old_price = re.search(r'.*>(?P<oldprice_euro>\d+\.)<span class="product-detail_price-old-price-cent">(?P<oldprice_cent>\d+)</span>',str(old_pricehtml))
            old_price = old_price.group('oldprice_euro') + old_price.group('oldprice_cent')#again because the euro and cents are splitted in the html file

        return ProductInfo(name, new_price, old_price)
    except:
        print("Unable to fetch the right info, either name or price")
        return ProductInfo()


def extract_categories(html):#in progress
    """
    There are quite some links to other categories on the website, the goal of this function is to return
    all of them. I added a screenshot to show what I mean.
    For every category you should create a Category object holding the url and the name of the category.
    :param html: the html in text form.
    :return: a list of Category objects with one entry for each category under 'assortiment'.
    """
    categories = []
    try:
        soup = bs4.BeautifulSoup(html,"html.parser")
    except ParseError:
        print("Unable to parse the provided link")
        return ProductInfo()#Returns the method empty handed
    index = 0#to keep track of where to write in the categories list
    for categories in soup.findAll('ul',{"class":"nav-main_links nav-main_links--icons nav-main_links--2col"}):
        categories_name = re.search(r'<li>$\n^<a href=".+">\s(?P<category>.*)</a>',str(categories),re.M)#this keeps the name of the category
        for subcategories in categories.findAll('li'):
            subcategories_link = re.search(r'<li>$\n^<a href="(?P<link>.*)">',str(subcategories),re.M)
            try:
                subcategory_link = ("https://www.brico.be"+subcategories_link.group('link'))#This searches for the link of the category
                
            except:
                print("Something went wrong in the regex")
            
            subcategories_name = re.search(r'<li>$\n^<a href=".+">\s(?P<subcategory>.*)</a>$',str(subcategories),re.M)
            try:
                subcategory_name = subcategories_name.group('subcategory')
            except:
                print("Something went wrong in the regex")
            categories[index] = Category(subcategory_link, subcategory_name)
            print(categories[index])
            index+=1
        
    
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
