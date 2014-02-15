#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

DEBUG = True
DILBERT_BOOK = "HD31 .A294 1996"

class LibOfCongBookRetriever:
    def __init__(self, driver):
        self.driver = driver

    def rows_to_py_object(self, rows):
        py_object = {}
        for row in rows:
            td_elements = row.find_elements_by_tag_name("td")
            th_elements = row.find_elements_by_tag_name("th")

            if len(th_elements) == 0 or len(td_elements) == 0: continue
            if len(td_elements[0].text) == 0: continue
            key, value = th_elements[0].text, td_elements[0].text

            if key not in py_object:
                py_object[key] = value

        return py_object

    def get_book_by_call_number(self, call_number):
        self.driver.get("http://catalog.loc.gov/")
        search_box = self.driver.find_element_by_name("Search_Arg")
        search_box.send_keys(call_number)
        search_box.send_keys(Keys.RETURN)

        table = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form[1]/table/tbody")))

        # Check to make sure that the books was found
        try:
            self.driver.find_element_by_class_name("nohits")
            return None
        except:
            pass

        rows = table.find_elements_by_tag_name("tr")
        return self.rows_to_py_object(rows)

if __name__ == '__main__':
    driver = webdriver.PhantomJS() if not DEBUG else webdriver.Firefox()

    retriever = LibOfCongBookRetriever(driver)
    print retriever.get_book_by_call_number(DILBERT_BOOK)
    driver.close()
