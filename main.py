from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

data1 = []
data2 = []
data3 = []

driver.get(f"https://finance.yahoo.com/most-active?count=25&offset=0")
time.sleep(2)

reject = driver.find_element(By.CLASS_NAME, "btn.secondary.reject-all")
reject.click()

while True:
    symbol = driver.find_elements(By.CSS_SELECTOR, '[data-test="quoteLink"].Fw\(600\).C\(\$linkColor\)')
    name = driver.find_elements(By.CLASS_NAME, "Va\(m\).Ta\(start\).Px\(10px\).Fz\(s\)")
    price = driver.find_elements(By.CSS_SELECTOR, '[data-field="regularMarketPrice"][data-test="colorChange"]')

    for i in symbol:
        data1.append(i.text)

    for i in name:
        x = i.text.strip()
        data2.append(x)

    for i in price:
        data3.append(i.text)
    next = driver.find_element(By.XPATH, '//span[contains(text(), "Next")]')

    try:
        next.click()
        time.sleep(2)
    except:
        driver.quit()
        break

datas = {
    "Symbol":data1,
    "Name":data2,
    "Price":data3
}

df = pd.DataFrame(datas)
df.to_csv('stocks.csv', index=False, encoding='utf-8-sig')