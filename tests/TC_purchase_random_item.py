from utilities.teststatus import TestStatus
import unittest
from pages.home import Shopping
import pytest
import utilities.custom_logger as cl
import logging

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class PurchaseRandomItem(unittest.TestCase) :
    log = cl.customLogger(logging.DEBUG)

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp) :
        self.lp = Shopping(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.first
    def test_add_item_to_card(self) :
        """
        """
        self.log.info(" * *" * 40)
        self.log.info("**test_Add random selected item to the card** STARTED")
        self.log.info(" * *" * 40)
        self.lp.random_item()
        result = self.lp.verify_item_added()
        self.ts.mark(result, "Selected item Text Verification")
        self.ts.markFinal("test_add_item_to_card : ", result, "Selected item Text Verification")

    @pytest.mark.second
    def test_item_added_to_card(self) :
        """
        """
        self.log.info(" * *" * 40)
        self.log.info("**test_Verify item added to the card** STARTED")
        self.log.info(" * *" * 40)
        self.lp.view_card()
        result = self.lp.verify_card()
        self.ts.mark(result, "Card data Verification")
        self.ts.markFinal("test_item_added_to_card : ", result, "Card data Verification")

    @pytest.mark.last
    def test_place_order(self) :
        """
        """
        self.log.info(" * *" * 40)
        self.log.info("**test_Verify checkout and place order** STARTED")
        self.log.info(" * *" * 40)
        self.lp.checkout()
        result = self.lp.verify_checkout()
        self.ts.mark(result, "Item details Verification")
        self.ts.markFinal("test_item_place_order : ", result, "Item details Verification")
