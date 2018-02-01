__author__ = 'Nicolas Daelemans'
"""
Task for summerjob with Daltix (System Expansion Engineer)
Issue parsing101:dreamland

Nicolas Daelemans (nicolas.daelemans@hotmail.com) +32497894006
"""

#-----------------------------------------------------------------------------------------------------------------------
###############
### REMARKS ###
###############
# 1) The program is written for dreamland-products only.
#
# 2) The given dreamland url's didn't have original prices or discounts. I went looking on the site for products who
#    did. Because of the special approach I wrote another function (extract_values2,see later).
#    Other exceptions were taken into account as well, so the program could handle most of the url's. A consequence
#    was that some of the code seems sloppy (E.g. alot of if statements). This can be improved,
#    but because it wasn't the original assigmnent I left it as a TO DO (for later on).
#
# 3) The first 3 url's are the given url's, the others were included to test the program and can be removed.
#
########################################################################################################################

import re, json
import requests
from bs4 import BeautifulSoup as BS

URLs = ["https://www.dreamland.be/e/nl/dl/luchtmatras-voor-1-persoon-lachend-kakske-124700",
"https://www.dreamland.be/e/nl/dl/banzai-wip-water-totter-124616",
"https://www.dreamland.be/e/nl/dl/waterpistool-minions-124712",
"https://www.dreamland.be/e/nl/dl/pennenzak-yo-kai-watch-watch-me-blauw-169797",
"https://www.dreamland.be/e/nl/dl/smoby-driewieler-disney-cars-3-be-move-123457",
"https://www.dreamland.be/e/nl/dl/dekbedovertrek-miraculous-ladybug-katoen-140-x-200-cm-677855",
"https://www.dreamland.be/e/nl/dl/nachtlampje-mobile-nightlight-grote-smurf-129617",
"https://www.dreamland.be/e/nl/dl/pompom-wow%21-locker-en-room-decor-set-118846",
"https://www.dreamland.be/e/nl/dl/popsocket-phone-grip-star-cluster-183510",
"https://www.dreamland.be/e/nl/dl/dekbedovertrek-disney-cars-racing-katoen-b-140-x-l-200-cm-677762",
"https://www.dreamland.be/e/nl/dl/lego-brickheadz-41590-iron-man-116399"
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

    The following are the most important: Name - Current price - Old price

    Once you have the HTML elements, extract their values using a regex.

    After extracting the values using a regex you can save the strings in a ProductInfo object, like so:
    ProductInfo(name='Grasmaaier', current_price='50,50', old_price='55,50')

    As mentioned before, the original price wasn't important for the given url's. When an empty string is rendered in
    extract_values function the program works as asked, it was only for the purpose of completeness that extract_values2
    function was designed.

    It is essential the extract_values functions work with the appropriate given string (E.g. "product_name").
    It is a property of the html of dreamland-url's, which is the reason this program is only designed for
    Dreamland-products.

    :param html: the html string.
    :return: a ProductInfo object holding all found product data.
    """
    name = extract_values("product_name")
    current_price = extract_values("product_unitprice_ati")
    original_price = extract_values2("price price--strikethrough")

    return ProductInfo(name,current_price,original_price)


def extract_categories(html):
    """
    There are quite some links to other categories on the website, the goal of this function is to return
    all of them. I added a screenshot to show what I mean.
    For every category you should create a Category object holding the url and the name of the category.
    :param html: the html in text form.
    :return: a list of Category objects with one entry for each category under 'assortiment'.
    """
    categories = []
    categ = ["product_top_cat","product_sub_cat","product_bottom_cat"]
    for cat in categ:
        name = extract_values(cat)
        if name:
            ## If there is no third category, the url doesn't need to be calculated.
            url = extract_url(name)
        else:
            url = None
        categories.append(Category(url,name))
    return categories

def extract_values(str):
    """
    General function to retrieve information using BeautifulSoup and regex. The function will return a string
    which contains the necessary information.

    - Creating soup with BeautifulSoup-function.
    - soup.find finds the first mention of str (E.g product_name) and stores it in temp. (soup.find_all also possible)
    - re.search uses regular expression to select the strings property we need from the selected line in the soup
    - m matches what we need, the last group is the needed information
    - re.search selects only the string with regular expression

    :param str: the string we want information about. (E.g. product_name)
    :return: extracted values with a regex (E.g. 'Waterpistool Minions')
    """
    result = None
    soup = BS(html, 'html.parser')
    if len(str) == 0:
        ## Makes sure empty strings don't disrupt the program. (E.g. the original price)
        return None
    temp = soup.find(string=re.compile(str))
    m = re.search(str+':\s\[(.*)\]', temp)
    l = m.group(0)
    k = re.search('(?<=\')(.*)(?=\')', l)
    if k:
        ## If there is no third category the bottom category is excluded.
        result = k.group(0)
    return result

#TODO: combine extract_values and extractvalues2 functions.
# These can be implemented together but were treated seperately because of the different approach

def extract_values2(str):
    """
    Special function to retrieve information using BeautifulSoup and regex. The function will return a string
    which contains the necessary information. This function is needed in case a promotion is given
    in the form of a percentage-discount. The information is then stored in an other part of the html than the
    information we need for the name and current price. A slightly other approach is given below.

    An important note is that the input string is a class-name.

    - Creating soup with BeautifulSoup-function.
    - soup.find_all finds the first appearance of str (A class name) and stores it in temp2.
    - temp2 is a ResultSet, temp2[0] a Tag and the .string makes a string of the tag.
    - m matches what we need, the last group is the needed information
    - re.search selects only the old price with regular expression

    :param str: the class linked to the discount, for dreamworld this is "price price--strikethrough"
    :return: extracted values with a regex (E.g. '34,95')
    """
    result2 = None
    soup = BS(html, 'html.parser')

    if len(str) == 0:
        ## Makes sure empty strings don't disrupt program. (E.g. the original price)
        return None
    temp2 = soup.find_all("p", class_=str)

    if temp2:
        ## Only if there is an old price in the html.
        m2 = temp2[0].string
    else:
        return None

    l2 = re.search('(\d+)\,(\d+)',m2)

    if l2:
        ## If there is no third category the bottom category is excluded.
        result2 = l2.group(0)

    return result2

def extract_url(str):
    """
    General function to retrieve url from relevant name of category. E.g. the top category "Buitenspeelgoed"
    can be extracted with extracted_values, this function returns the coupled link to that category.

    - To find the necessary category, lower-case strings are needed
    - When a category contains spaces, the link is found by replacing the spaces with hyphens.
      (Exceptions exist, see below)
    - Creating soup with BeautifulSoup-function.
    - All the links in the html who contain the category-name, are stored in a list. This list is
      eventually a list with the same links, so one element suffices.

    :param str: name of the product, result of function extract_values
    :return: url of the category
    """
    if '-' in str:
        ## Exception: When a name of a category contains multiple elements connected with a hyphen,
        ## the link to that category consists only of the first word in that category.
        ## E.g.: "Waterpistolen en -ballonnen"-category has as url: "https://www.dreamland.be/e/nl/dl/waterpistolen"
        t = re.search('(\w+)',str)
        str = t.group(0)

    if 'solden' in str:
        ## Exception: sometimes when a set of products is in discount, the category changes its name
        ## to "Category-name solden". This should be removed if we want the correct link to the category-page
        patt = re.compile('(\s*)solden(\s*)')
        str = patt.sub('',str)

    str = str.lower()
    str = re.sub(' +','-',str)
    soup = BS(html, 'html.parser')
    lst = []

    for a in soup.find_all('a'):
        if str.lower() in a['href'] and 'http' in a['href']:
            lst.append(a['href'])

    return lst[0]

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

