#import all needed libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

#chrome as main webdriver, also set to not close after opening (detach)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

#create 3 empty lists where data will be stored
data1 = []
data2 = []
data3 = []

#opening website using Selenium
driver.get(f"https://finance.yahoo.com/most-active?count=25&offset=0")
time.sleep(2)

#bypassing cookies window
reject = driver.find_element(By.CLASS_NAME, "btn.secondary.reject-all")
reject.click()

#cycle through website so .py can scrape all stocks listed there
while True:
    #finding requested elemenets by css_selector/class_name
    symbol = driver.find_elements(By.CSS_SELECTOR, '[data-test="quoteLink"].Fw\(600\).C\(\$linkColor\)')
    name = driver.find_elements(By.CLASS_NAME, "Va\(m\).Ta\(start\).Px\(10px\).Fz\(s\)")
    price = driver.find_elements(By.CSS_SELECTOR, '[data-field="regularMarketPrice"][data-test="colorChange"]')

    #getting texts from all 3 elemenets lists .py found
    for i in symbol:
        data1.append(i.text)

    for i in name:
        x = i.text.strip()
        data2.append(x)

    for i in price:
        data3.append(i.text)
    next = driver.find_element(By.XPATH, '//span[contains(text(), "Next")]')

    #if there is no more stocks, close webdriver
    try:
        next.click()
        time.sleep(2)
    except:
        driver.quit()
        break

#turn 3 data lists into one dictionary
datas = {
    "Symbol":data1,
    "Name":data2,
    "Price":data3
}

#turn dictionary into df using Pandas, turn df into csv using Pandas
df = pd.DataFrame(datas)
df.to_csv('stocks.csv', index=False, encoding='utf-8-sig')