import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import dotenv_values
from settings import *


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # удержание страницы открытой
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--disable-dev-shm-usage')

bw = webdriver.Chrome(options=options)
time.sleep(5)
bw.get("https://login.school.mosreg.ru/login/?ReturnUrl=https%3A%2F%2Fschool.mosreg.ru%2Fuserfeed")
time.sleep(5)
print("1", bw)
print(bw.page_source, bw.current_url)
bw.get("https://login.school.mosreg.ru/login/?ReturnUrl=https%3A%2F%2Fschool.mosreg.ru%2Fuserfeed")
print("1", bw)
print(bw.page_source, bw.current_url)
log = bw.find_element(By.CLASS_NAME, "mosreg-login-block__content").find_element(By.NAME, "mosreg-login-form")
print("2", bw, log)
log.send_keys("spd")
