***Technical test Project***
==================

## Technical test Project

This is a test automation project for the application "https://shop.demoqa.com/" based on **Selenium framework** with **Python** language. The collection of tests contains : 

* Random selection of an article with random color and size
* Check if the selected data are correct
* Enter random user card details
* Check all data

## Project Structure

Here you can find a short description of main directories, and it's content :

* base - contains all common functions 
* pages - there are sets of method for each test step
* tests - there are sets of tests for the required functionalities
* reports - tests reports, report.log and screenshots will be saved in this directory
* utils - this directory contains files responsible for configuration
* Other important files are located directly in the main project file (as data.py, fake_data.json)

## Project Features

* Framework follows Page Object Model (POM)
* Data-driven tests - in those tests the option of loading data from a json file has been implemented
* Logger has been implemented in each step of test cases, e.g.
* The ability to easily generate legible and attractive test reports using the pytest-html plugin (for more look Generate Test Report section below)
* Tests can be run on popular browsers - Chrome and Firefox, opera, edge are preconfigured in WebDriverFactory class and both can be selected before running tests.

## Getting started

Just download the project or clone repository. You need to install packages using pip according to requirements.txt file.
Run the command below in terminal:

```
$ pip install -r requirements.txt
```

## Run Automated Tests

An html-report will be generated automatically for each test executed

You just need to choose the "TC_purchase_random_item.py" from "tests" directory and click "Run test" green arrow.
Or, you can run test from terminal using the command below : 

```
$ pytest TC_purchase_random_item.py 

```
We can also select browser, select visibility (headless option) and other options from the command line.

## Generate Test Report

The configuration of the automatic generation of test reports is realized in the tests/conftes.py file.

The html report will contain status of the executed tests, test environment, test steps log, test duration ,the browser in which the test is performed and a screenshot in failure