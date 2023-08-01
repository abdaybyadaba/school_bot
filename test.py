from dotenv import load_dotenv
import os
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, executor, types, filters
from parse import term_reader
from dbmanager import Database


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # удержание страницы открытой
#options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
#options.add_argument('--disable-dev-shm-usage')

bw = webdriver.Chrome(options=options)
