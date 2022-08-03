import time
import json
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

url = "chromedriver.exe"
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.mexc.com/ru-RU/exchange/EVMOS_USDT")

# these vars for check to unique data
const_bought = []
const_sold = []

# make our app cyclic
while True:
    try:
        table_bought = driver.find_element(By.CSS_SELECTOR, ".orderbook_asksWrapper__F6wpm")
        price_bought = table_bought.find_element(By.CLASS_NAME, "orderbook_tableRow__M1cC0")

        table_sold = driver.find_element(By.CSS_SELECTOR, ".orderbook_bids__swekw")
        price_sold = table_sold.find_element(By.CLASS_NAME, "orderbook_tableRow__M1cC0")

        bought = price_bought.text.split("\n")
        sold = price_sold.text.split("\n")

        if const_bought == [] or bought not in const_bought:
            const_bought.append(bought)
            print(f"Цена на продажу: {bought[0]} Количество: {bought[1]} Всего: {bought[2]}")
            new_show = {
                "Cost": bought[0],
                "Vol": bought[1],
                "Amount": bought[2]
            }
            with open("bought_table.json", "a") as file:
                file.write(json.dumps(new_show, ensure_ascii=False,indent=4, separators=(',', ': '), sort_keys=False))

        if const_sold == [] or sold not in const_sold:
            const_sold.append(sold)
            print(f"Цена на покупку: {sold[0]} Количество: {sold[1]} Всего: {sold[2]}")
            new_show = {
                "Cost": sold[0],
                "Vol": sold[1],
                "Amount": sold[2]
            }
            with open("sold_table.json", "a") as file:
                file.write(json.dumps(new_show, ensure_ascii=False, indent=4, separators=(',', ': ')))

        time.sleep(2)

    except NoSuchElementException:
        pass
    except StaleElementReferenceException:
        pass
        # these problems can be because site is dynamic
