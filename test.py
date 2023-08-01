import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import dotenv_values
from settings import *


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # удержание страницы открытой
#options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
#options.add_argument('--disable-dev-shm-usage')

bw = webdriver.Chrome(options=options)
print(bw)