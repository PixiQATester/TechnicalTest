"""
@package utilities
CheckPoint class implementation
It provides functionality to assert the result
"""
import logging
from traceback import print_stack
import utilities.custom_logger as cl
from base.selenium_driver import SeleniumDriver


class TestStatus(SeleniumDriver) :
    log = cl.customLogger(logging.INFO)

    def __init__(self, driver) :
        """
        Inits CheckPoint class
        """
        super(TestStatus, self).__init__(driver)
        self.resultList = []

    def setResult(self, result, resultMessage) :
        try :
            if result is not None :
                if result :
                    self.resultList.append("PASS")
                    self.log.info("### VERIFICATION SUCCESSFUL : " + resultMessage)
                else :
                    self.resultList.append("FAIL")
                    self.log.error("### VERIFICATION FAILED : " + resultMessage)
                    self.screenShot(resultMessage)
            else :
                self.resultList.append("FAIL")
                self.log.error("### VERIFICATION FAILED : " + resultMessage)
                self.screenShot(resultMessage)
        except :
            self.resultList.append("FAIL")
            self.log.error("### Exception Occurred !!!")
            self.screenShot(resultMessage)
            print_stack()

    def mark(self, result, resultMessage) :
        """
        Mark the result of the verification point in a test case
        """
        self.setResult(result, resultMessage)

    def markFinal(self, testName, result, resultMessage) :
        """
        Mark the final result of the verification point in a test case
        This needs to be called at least once in a test case
        This should be final test status of the test case
        """
        self.setResult(result, resultMessage)

        if "FAIL" in self.resultList :
            self.log.error(testName + " ### XXX FAILED XXX ### ")
            self.resultList.clear()
            assert False
        else :
            self.log.info(testName + " ### XXX SUCCESSFUL XXX ### ")
            self.resultList.clear()
            assert True
