"""
@package base
Base Page class implementation
It implements methods which are common to all the pages throughout the application
This class needs to be inherited by all the page classes
This should not be used by creating object instances

"""
# Use pip install PyAutoIt to install autoit
from base.selenium_driver import SeleniumDriver
from traceback import print_stack
from utilities.util import Util


class BasePage(SeleniumDriver) :

    def __init__(self, driver) :
        """
        Inits BasePage class
        Returns:
            None
        """
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def verifyPageTitle(self, titleToVerify) :
        """
        Verify the page Title
        Parameters:
            titleToVerify: Title on the page that needs to be verified
        """
        try :
            actualTitle = self.getTitle()
            return self.util.verifyTextContains(actualTitle, titleToVerify)
        except :
            self.log.error("Failed to get page title")
            print_stack()
            return False

    def verifyPageURL(self, URLToVerify) :
        """
        Verify the page URL
        Parameters:
            urlToVerify: url of the page that needs to be verified
            :param URLToVerify:
        """
        try :
            actualURL = self.driver.current_url
            return self.util.verifyTextContains(actualURL, URLToVerify)
        except :
            self.log.error("Failed to get page url")
            print_stack()
            return False

    def openNewTab(self, URL) :
        """Open new tab and navigate to the requested URL  --
        """
        self.driver.execute_script("window.open('" + URL + "','icoTab');")

    def switchTab(self, index) :
        """Switch to a different tab
        index = 1 for the new tab
        index = 0 for the last opened tab
        """
        var = self.driver.window_handles[index]
        self.driver.switch_to.window(var)
