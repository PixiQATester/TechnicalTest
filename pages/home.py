from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from faker import Faker
from selenium.webdriver import Keys
import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
from utilities.util import Util
from bs4 import BeautifulSoup

class Shopping(BasePage, Util) :
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver) :
        super().__init__(driver)
        self.article_name = ""
        self.driver = driver

    # Locators
    _first_item = "/html/body/div[2]/div[2]/div[3]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/a"
    _products_btn = "/html/body/div[2]/section/div/div/div/span[2]/a/span"
    _results = "/html/body/div[2]/div[2]/div[1]/div"
    _path = "/html/body/div[2]/div[2]/div[2]/div/nav/ul/li["  # path of the pages counter
    _item_path = "/html/body/div[2]/div[2]/div[2]/div/div/div["  # path of the item in the products page
    _colors_field = "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/form/table/tbody/tr[1]/td/select"
    _size_field = "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/form/table/tbody/tr[2]/td/select"
    _color_option = "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/form/table/tbody/tr[1]/td/select/option["
    _size_option = "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/form/table/tbody/tr[2]/td/select/option["
    _add_to_card = "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/form/div/div[2]/button"

    _out_of_stock = "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/form/div/div[1]/div[3]"

    _text_to_verify = "/html/body/div[2]/div[2]/div/div/div[1]/div"
    _view_card_btn = "/html/body/div[2]/div[2]/div/div/div[1]/div/a"
    _total_price = "/html/body/div[1]/div[2]/main/article/div/div/form/table/tbody/tr[1]/td[3]"
    _quantity = "/html/body/div[1]/div[2]/main/article/div/div/form/table/tbody/tr[1]/td[4]/div/div/input"
    _card_price = "/html/body/div[1]/header/div[2]/div/div/div/ul/li/a/span/span[2]"
    _card_quantity = "/html/body/div[1]/header/div[2]/div/div/div/ul/li/a/span/span[2]"

    _checkout_btn = "/html/body/div[1]/div[2]/main/article/div/div/div[2]/div[2]/div/a"
    _first_name = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div/div[1]/div[1]/div/p[1]/span/input"
    _last_name = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div/div[1]/div[1]/div/p[2]/span/input"
    _country = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div/div[1]/div[1]/div/p[4]/span/span/span[1]/span/span[1]"
    _input_country = "/html/body/span/span/span[1]/input"
    _street_address = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div/div[1]/div[1]/div/p[5]/span/input"
    _town = "billing_city"

    _state = "select2-billing_state-container"
    _province = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div[2]/div[1]/div[1]/div/p[8]/span/span/span[1]/span"
    _province_input = "/html/body/span/span/span[1]/input"

    _zip = "billing_postcode"
    _phone = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div/div[1]/div[1]/div/p[10]/span/input"
    _email = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div/div[1]/div[1]/div/p[11]/span/input"
    _accept_terms = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div[2]/div[2]/div/div/div/div/p/label/input"
    _place_order_btn = "/html/body/div[1]/div[2]/main/article/div/div/form[3]/div/div[2]/div/div/div/button"

    _order_received = "/html/body/div[1]/div[2]/main/article/div/div/div/p[1]"
    _name = "/html/body/div[1]/div[2]/main/article/div/div/div/section/table/tbody/tr/td[1]/a"
    _item_quantity = "/html/body/div[1]/div[2]/main/article/div/div/div/section/table/tbody/tr/td[1]/strong"
    _price = "/html/body/div[1]/div[2]/main/article/div/div/div/section/table/tfoot/tr[3]/td/span"
    _color = "/html/body/div[1]/div[2]/main/article/div/div/div/section/table/tbody/tr/td[1]/ul/li[1]/p"
    _size = "/html/body/div[1]/div[2]/main/article/div/div/div/section/table/tbody/tr/td[1]/ul/li[2]/p"

    def navigate_to_shop_page(self) :
        """While there is no CTA in the home page to navigate directly to the shop page I will use this function to """
        global pageURL
        self.elementClick(self._first_item)
        self.elementClick(self._products_btn)  # Click on products btn to navigate to the shop list page
        pageURL = self.getPageURL()
        return pageURL

    def select_random_item(self) :
        global article_name, color_text, size_text
        results_text = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, self._results))).get_attribute("innerHTML")
        all_results = int((str(results_text).partition("results")[0]).rpartition("of ")[2])
        per_page = int(((str(results_text).partition("of")[0])).rpartition("–")[2])
        div = all_results // per_page
        rest = all_results % per_page
        if rest == 0 :
            page_num = div
        else :
            page_num = div + 1
        page = random.randint(1, page_num)  # Select random page of products list pages
        path = self._path + str(page) + "]"
        self.elementClick(path)
        self.log.info("We are moved to the page " + str(page))
        if page != page_num :
            item = random.randint(1, per_page)
            item_path = self._item_path + str(item) + "]/div/h3/a"
            article_name = self.getText(item_path)
            self.log.info("The selected item is :: " + str(article_name))
            self.elementClick(item_path)
        else : # In every page we have 20 products, but in the last page the products number can be variable so we have to check it in this part
            self.log.info("This last page contain :: " + str(rest) + " products")
            item = random.randint(1, rest)
            item_path = self._item_path + str(item) + "]/div/h3/a"
            article_name = self.getText(item_path)
            self.log.info("The selected item is :: " + str(article_name))
            self.elementClick(item_path)

        """This part of function aim to select size and color of the selected item"""
        if self.isElementPresent(self._colors_field) :   # we have to check if the color field is displayed or not
            self.elementClick(self._colors_field)
            i = 1
            while True :
                paths = self._color_option + str(i) + "]"
                EP = self.isElementPresent(paths)
                if EP :
                    i = i + 1
                    continue
                break
            self.log.info("######## The color options list length is " + str(i - 1))
            color = random.randint(2, i - 1)  # Select random page of products list pages
            color_path = self._color_option + str(color) + "]"
            color_text = self.getText(color_path)
            self.log.info("The selected item color is : " + str(color_text))
            self.elementClick(color_path)
        else :
            self.log.info("This item has a unique color color")
            pass
        self.elementClick(self._size_field)
        i = 1
        while True :
            paths = self._size_option + str(i) + "]"
            EP = self.isElementPresent(paths)
            if EP :
                i = i + 1
                continue
            break
        self.log.info("######## The size options list length is " + str(i - 1))
        size = random.randint(2, i - 1)  # Select random page of products list pages
        size_path = self._size_option + str(size) + "]"
        size_text = self.getText(size_path)
        self.log.info("The selected item size is : " + str(size_text))
        self.elementClick(size_path)

        self.elementClick(self._add_to_card)   # Add the random selected item to the card
        self.sleep(3)
        if self.isElementDisplayed(self._out_of_stock) :    # If the item is out of stock we have to repeat the work
            self.driver.get(pageURL)
            self.select_random_item()
        return article_name, color_text, size_text

    def random_item(self) :
        self.navigate_to_shop_page()
        self.select_random_item()

    def verify_item_added(self):
        global status
        expected_text = '“' + article_name + '”' + " has been added to your cart."
        actual_text = self.getText(self._text_to_verify)
        if (str(expected_text).lower()) in (str(actual_text).lower()):
            self.log.info("### VERIFICATION CONTAINS !!!")
            status = True
        else:
            self.log.info("### VERIFICATION DOES NOT CONTAINS !!!")
            status = False
        return status

    def view_card(self):
        global item_price, item_card_price, item_quantity,card_quantity
        self.elementClick(self._view_card_btn)

        """get the item price in the card table"""
        elem = self.getElement(self._total_price, locatorType="xpath")
        html_path = str(elem.get_attribute('innerHTML'))
        mainSoup = BeautifulSoup("""<html>""" + html_path + """</html>""")
        external_span = mainSoup.find('span')
        unwanted = external_span.find('span')
        unwanted.extract()
        item_price = external_span.text.strip()
        self.log.info("The item Price in the card table is : " + str(item_price))
        """get the item price in the page header"""
        elem = self.getElement(self._card_price, locatorType="xpath")
        html_path = str(elem.get_attribute('innerHTML'))
        mainSoup = BeautifulSoup("""<html>""" + html_path + """</html>""")
        external_span = mainSoup.find('span')
        unwanted = external_span.find('span')
        unwanted.extract()
        item_card_price = external_span.text.strip()
        self.log.info("The item Price in the page header is : " + str(item_card_price))
        """Get The item quantity in the card table"""
        elem = self.getElement(self._quantity, locatorType="xpath")
        item_quantity = elem.get_attribute('value')
        self.log.info("The item quantity in the card table is : " + str(item_quantity))
        """Get the item quantity in the page header"""
        elem = self.getElement(self._card_quantity, locatorType="xpath")
        html_path = str(elem.get_attribute('innerHTML'))
        num = html_path.rpartition(')')[0]
        card_quantity = num[5:11]
        self.log.info("The item Price in the card table is : " + str(card_quantity))
        return item_price, item_card_price, item_quantity, card_quantity

    def verify_card(self) :
        global card_status
        if (item_price == item_card_price) and (item_quantity == card_quantity) :
            card_status = True
            self.log.info("Verify card : Successful")
        else :
            card_status = False
            self.log.info("Verify card : Failed")
        return card_status

    def checkout(self):
        self.elementClick(self._checkout_btn)
        """We will use the faker package to generate fake data"""
        fake = Faker()
        Name = fake.name()
        name = Name.rpartition(' ')[0]
        last_name = Name.rpartition(' ')[2]
        email = name.replace(" ", "").lower() + "." + last_name.replace(" ", "").lower() + "@" + "gmail.com"
        """The other data will be geted from a json file"""
        count_zip = self.count_zip()
        country = count_zip[0]
        town = self.read_from_jsonfile(data="town")
        state = self.read_from_jsonfile(data="state")
        zip = count_zip[1]
        phone = self.read_from_jsonfile(data="phone")
        self.sendKeys(name, self._first_name)
        self.sendKeys(last_name, self._last_name)
        self.elementClick(self._country)
        self.sendKeys(country, self._input_country)
        self.sendKeys(Keys.ENTER, self._input_country)
        self.sendKeys(fake.address(), self._street_address)
        self.sleep(2)
        self.sendKeys(phone, self._phone)
        self.sendKeys(email, self._email)
        self.sendKeys(zip, self._zip, locatorType='id')
        self.sendKeys(town, self._town, locatorType='id')
        self.elementClick(self._province, locatorType='xpath')
        if self.isElementPresent(self._province_input, locatorType='xpath') :
            self.sendKeys(Keys.ENTER, self._province_input, locatorType='xpath')
        else :
            self.sendKeys(state, self._state, locatorType='id')
        try :
            self.elementClick(self._accept_terms)
        except :
            self.sleep(3)
            self.elementClick(self._accept_terms)
        self.elementClick(self._place_order_btn)   # Click in the CTA Place order

    def verify_checkout(self):
        """In this part we get the details of the purchase order"""
        global details_status
        checkout_verified = self.isElementPresent(self._order_received)
        ch_item_name = str(self.getText(self._name)).rpartition(" - ")[0]
        ch_item_quantity = (str(self.getText(self._item_quantity)).partition("×")[2]).replace(" ", "")
        ch_item_price = (str(self.getText(self._price)).partition("₹")[2]).replace(" ", "")
        ch_item_color = (self.getText(self._color)).replace(" ", "")
        ch_item_size = (self.getText(self._size)).replace(" ", "")
        """In this part we will verify the details of the purchase order in the checkout page"""
        if checkout_verified : #if item_price  item_quantity  article_name  color_text  size_text
            self.log.info("The order has been received")
            if ((ch_item_name).lower() == (article_name).lower()) and (ch_item_quantity == item_quantity) and \
                    (ch_item_price == item_price) and (ch_item_color == color_text) and (ch_item_size == size_text) :
                self.log.info("All Item details are verified")
                details_status = True
            else :
                self.log.info("Item details are not verified")
                details_status = False
                if (ch_item_name != (article_name).lower()) :
                    self.log.info("ch_item_name : " + ch_item_name + ", article_name " + article_name)
                elif (ch_item_quantity != item_quantity) :
                    self.log.info("ch_item_quantity : " + ch_item_quantity + ", item_quantity " + item_quantity)
                elif (ch_item_price != item_price) :
                    self.log.info("ch_item_price : " + ch_item_price + ", item_price " + item_price)
                elif (ch_item_color != color_text) :
                    self.log.info("ch_item_color : " + ch_item_color + ", color_text " + color_text)
                elif(ch_item_size == size_text) :
                    self.log.info("ch_item_size : " + ch_item_size + ", size_text " + size_text)
        else :
            details_status = False
        return details_status
