from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import math
from re import search
from time import sleep



def calc(x):
  return str(math.log(abs(12*math.sin(int(x)))))

browser = webdriver.Chrome()

browser.get("http://suninjuly.github.io/explicit_wait2.html")

# говорим Selenium проверять в течение 5 секунд, пока кнопка не станет кликабельной
wait = WebDriverWait(browser, 12).until(
        EC.text_to_be_present_in_element((By.ID, "price"), '$100')
    )
if wait:
    print('Цена 100$ найдена')
button = browser.find_element(By.ID, "book")
button.click()

x = browser.find_element(By.CSS_SELECTOR, "#input_value").text
y = calc(x)
input1 = browser.find_element(By.CSS_SELECTOR, "input[id='answer']")
input1.send_keys(y)
submit = browser.find_element(By.ID, "solve")
submit.click()
alert = browser.switch_to.alert
alert_text = alert.text
match = search('\d+[.]\d+', alert_text)
if match:
    print('Введите этот номер', match[0], sep='\n')
sleep(5)
