from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import selenium
import time, datetime
from icecream import ic

class Element:
    class ElementNotFetchableError(Exception):
        def __init__(self, *args):
            super().__init__(args)

        def __str__(self):
            return 'The element is not fetchable.'

    class FetchFailureError(Exception):
        def __init__(self, name, *args):
            super().__init__(args)
            self.name = name

        def __str__(self):
            return f'An attempt to fetch the {self.name} element failed.'

    def __init__(self, driver, name, method, selector, delay=30, element=None, optional=False):
        self.driver = driver
        self.name = name
        self.method = method
        self.selector = selector
        self.element = element
        self.optional = optional
        if not element:
            self.fetch(delay=delay)

    def fetch(self, delay=10, elapsed=0, clickable=True):
        if not self.method:
            raise self.ElementNotFetchableError()

        start = time.perf_counter()  # Initialize start here

        by = {
            "ID": By.ID,
            "XPATH": By.XPATH,
            "CSS_SELECTOR": By.CSS_SELECTOR,
        }.get(self.method, By.XPATH)

        ec = EC.element_to_be_clickable if clickable else EC.presence_of_element_located

        try:
            self.element = WebDriverWait(self.driver, delay).until(ec((by, self.selector)))
        except (TimeoutException, NoSuchElementException) as e:
            if self.optional:
                self.element = None  # If element is optional, do not raise an exception
            else:
                raise self.FetchFailureError(self.name)
        except selenium.common.exceptions.StaleElementReferenceException as e:
            if elapsed < delay:
                time.sleep(0.1)
                elapsed += time.perf_counter() - start  # Now start is defined
                self.fetch(delay=delay, elapsed=elapsed, clickable=clickable)
            else:
                if not self.optional:
                    raise self.FetchFailureError(self.name)
                
    def click(self, delay=15, elapsed=0):
        start = time.perf_counter()
        try:
            self.element.click()
            return True
        except selenium.common.exceptions.ElementClickInterceptedException:
            elapsed = elapsed + time.perf_counter()-start
            if elapsed < delay:
                time.sleep(0.1)
                ic("click intercepted", elapsed, delay)
                return self.click(delay, elapsed)
            else:
                f"Element click was intercepted for more than {delay} seconds"
                return False
        except selenium.common.exceptions.StaleElementReferenceException:
            elapsed = elapsed + time.perf_counter()-start
            if elapsed < delay:
                time.sleep(0.1)
                try:
                    self.fetch()
                    return self.click(delay, elapsed)
                except self.ElementNotFetchableError as e:
                    print(str(e))
                    return False

            else:
                f"Element reference was stale for more than {delay} seconds"
                return False
        except selenium.common.exceptions.ElementNotInteractableException:
            elapsed = elapsed + time.perf_counter()-start
            if elapsed < delay:
                time.sleep(0.1)
                ic("NotInteractable", elapsed, delay)
                return self.click(delay, elapsed)
            else:
                f"Element click was not interactable for more than {delay} seconds"
                return False
        except selenium.common.exceptions.WebDriverException:
            elapsed = elapsed + time.perf_counter()-start
            if elapsed < delay:
                time.sleep(0.1)
                ic("Unknown web driver error", elapsed, delay)
                return self.click(delay, elapsed)
            else:
                f"Unkown web driver error for more than {delay} seconds"
                return False


    def send_keys(self, text):
        return self.element.send_keys(text)

    def get_attribute(self, text):
        return self.element.get_attribute(text)

    @property
    def innerText(self):
        return self.element.get_attribute("innerText")

    @property
    def text(self):
        return self.element.text

    def find_element(self, by, selector, optional=False):
        try:
            elem = self.element.find_element(by, selector)
            new_selector = (self.selector + selector[1:]) if self.selector else None
            new_method = self.method if new_selector else None
            name = self.name + "+" + selector
            new_elem = Element(self.driver, name, self.method, new_selector, element=elem)
            return new_elem
        except selenium.common.exceptions.StaleElementReferenceException:
            if not optional:
                self.fetch()
                self.find_element(by, selector)
            else:
                raise NoSuchElementException()

    def find_elements(self, by, selector):
        elems = self.element.find_elements(by, selector)
        name = self.name + "+" + selector
        new_elems = [Element(self.driver, name, method=None, selector=None, element=i) for i in elems]                     
        return new_elems