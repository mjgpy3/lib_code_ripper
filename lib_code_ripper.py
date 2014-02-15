#!/usr/bin/env python

DEBUG = True

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    driver = webdriver.PhantomJS() if not DEBUG else webdriver.Firefox()

    driver.get("http://catalog.loc.gov/")
    search_box = driver.find_element_by_name("Search_Arg")
    search_box.send_keys("foobar")
    search_box.send_keys(Keys.RETURN)
