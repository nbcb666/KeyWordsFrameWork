# -*- coding: utf-8 -*-

from selenium.webdriver.support.ui import WebDriverWait

#获取单个页面元素
def getElement(driver,locateType,locatorExpression):
    try:
        element = WebDriverWait(driver,30).until\
            (lambda x: x.find_element(by = locateType,value= locatorExpression))
        return element
    except Exception,e:
        raise e

#获取多个相同页面元素对象，以list返回
def getElements(driver,locateType,locatorExpression):
    try:
        element = WebDriverWait(driver,30).until\
            (lambda x: x.find_elements(by = locateType,value= locatorExpression))
        return element
    except Exception,e:
        raise e

if __name__ == '__main__':
    from selenium import webdriver

    driver = webdriver.Firefox(executable_path="C:\\wmh\\driver\\geckodriver")
    driver.get("https://www.baidu.com")
    searchBox = getElement(driver,"id","kw")
    print searchBox.tag_name
    aList = getElements(driver,"tag name","a")
    print len(aList)
    driver.quit()