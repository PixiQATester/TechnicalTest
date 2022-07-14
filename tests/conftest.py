import datetime
import pytest
from base.webdriverfactory import WebDriverFactory
import utilities.custom_logger as cl
import logging
import os
import glob
from data import testable_application_url, dir_path  # Used to run login setup fixture

log = cl.customLogger(logging.DEBUG)


@pytest.fixture()
def setUp() :
    # log.info("Running method level setUp")
    yield
    print("Running method level tearDown")


@pytest.fixture(scope="class")
def oneTimeSetUp(request, browser) :
    global driver
    print("Running one time setUp")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()
    if request.cls is not None :
        request.cls.driver = driver
    yield driver
    print("Running one time tearDown")


def pytest_addoption(parser) :
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")


@pytest.fixture(scope="session")
def browser(request) :
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def osType(request) :
    return request.config.getoption("--osType")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screen_file = ''
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    setattr(report, "duration_formatter", "%H:%M:%S.%f")
    global screenshot_dir, page
    screenshot_dir = dir_path + "output\\screenshots"
    if report.when == "call":
        # always add url and browser to the html report :
        if item.funcargs['browser'] is not None :
            browser = item.funcargs['browser']
        else :
            browser = "chrome"
        extra.append(pytest_html.extras.url(testable_application_url, name="URL"))
        extra.append(pytest_html.extras.url(browser, name="Browser"))

        if report.failed and "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir.mkdir(exist_ok=True)
            page.screenshot(path=screenshot_dir)
        xfail = hasattr(report, "wasxfail")

        if (report.skipped and xfail) or (report.failed and not xfail):
            list_of_files = glob.glob(
                dir_path + "output\\screenshots\\*")  # * means all if need specific format then *.csv
            screen_file = max(list_of_files, key=os.path.getctime)
            extra.append(pytest_html.extras.png(screen_file))
            extra.append(pytest_html.extras.url(screenshot_dir, name="Screenshots"))

        report.extra = extra


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure the report file and folder location"""

    path = dir_path+"output\\HTML-Reports\\"
    if not os.path.exists(path) :
        os.makedirs(path)

    file_name = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".html"

    moduli = config.option.file_or_dir

    if moduli is not None:
        for modulo in moduli:
            if modulo is not None and ".py" in modulo:
                name_modulo = modulo.split("/").pop()[:-3]
                file_name = name_modulo+" "+file_name

    config.option.htmlpath = path + file_name
