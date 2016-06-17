from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

myCSVFile = open("output.csv", "w")
myCSVFile.write("")
myCSVFile.close()

productsList=[]
START_FROM=0
EMAIL='rossbob304@gmail.com'    #Your email and pass to kroger.com
PASS='ross12345'

def writeToCSV():
    global productsList
    myCSVFile = open("output.csv", "a")     #output csv file is in the same folder where script
    writer=csv.writer(myCSVFile)
    for item in productsList:
        writer.writerow(item)
    productsList=[]
    myCSVFile.close()

chrome_path=("chromedriver.exe")        #path to chromedriver. By default it us in the script foldr.
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_path,chrome_options=chromeOptions)     #starting Chrome with disabled images
driver.get("https://www.kroger.com/onlineshopping/signin")
time.sleep(1)
driver.find_element_by_id("signIn").click()
driver.find_element_by_id('signin-drawer-email-address').send_keys(EMAIL)
driver.find_element_by_id('signin-drawer-password').send_keys(PASS)
driver.find_element_by_id("signin-drawer-submit").click()       #loging in to website
time.sleep(5)
driver.find_element_by_class_name("pickup-store-result-preferred-button").click()
driver.find_element_by_id("departmentsButton").click()
htmlFile = BeautifulSoup(driver.page_source, "html.parser")
categoryLinks=htmlFile.find_all("a",{"class": "menuLink"})
categoryLinks.pop(0)
categoryLinks.pop(21)
categoryLinks.pop(41)
for link in categoryLinks:
    while True:
        driver.get(link.attrs['href']+"#facet:&productBeginIndex:%s&orderBy:0&pageView:grid&minPrice:&maxPrice:&pageSize:&"%START_FROM)   #opening catalog page and scraping product links
        time.sleep(5)
        htmlFile = BeautifulSoup(driver.page_source, "html.parser")
        products = htmlFile.find_all("div", {"class": "product_name"})
        if(len(products)==1):
            START_FROM=0
            break
        for item in products:       #script goes to item page and scraps data
            try:
                driver.get(item.contents[1].attrs['href'])
                prodName=driver.find_element_by_class_name('main_header').text
                prodSKU=driver.find_element_by_class_name('sku').text
                prodPrice=driver.find_element_by_class_name('price').text
                prodUOM=driver.find_element_by_class_name('product_uom').text
                prodCategory=link.contents[0].contents[0]
                productsList.append([prodCategory,prodName,prodSKU,prodPrice,prodUOM])
            except:
                continue
        writeToCSV()        #each 60 product writes to CSV file
        START_FROM+=60
driver.close()