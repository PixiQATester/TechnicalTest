"""
@package base
WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations
"""
import time
from selenium import webdriver
from data import testable_application_url


class WebDriverFactory :
    def __init__(self, browser) :
        """
        Inits WebDriverFactory class
        Returns:
            None
        """
        self.browser = browser

    def getWebDriverInstance(self) :
        """
       Get WebDriver Instance based on the browser configuration
        Returns:
            'WebDriver Instance'
        """
        if self.browser == "chrome" :
            # Set chrome driver
            driver = webdriver.Chrome()
        elif self.browser == "firefox" :
            # Set firefox driver
            driver = webdriver.Firefox()
        elif self.browser == "edge" :
            # Set edge driver
            driver = webdriver.Edge()
            driver.set_window_size(400, 800)
        elif self.browser == "opera" :
            # Set opera driver
            driver = webdriver.Opera()
        else :
            driver = webdriver.Chrome()
        # Setting Driver Implicit Time out for an Element
        driver.implicitly_wait(10)
        # Maximize the window
        driver.maximize_window()
        # Loading browser with App URL
        driver.get(testable_application_url)
        time.sleep(2)
        return driver
