import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import dotenv_values
from settings import *

#from pyvirtualdisplay import Display

SCHOLL_PAGE = "https://login.school.mosreg.ru/login/?ReturnUrl=https%3A%2F%2Fschool.mosreg.ru%2Fuserfeed"
# переменные и хром
auth_config = dotenv_values(".env")



def open_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # удержание страницы открытой
    # options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


def open_marks_tables(driver):  # осуществляет переход к таблицам
    driver.find_element(By.CLASS_NAME, "mosreg-login-form__submit").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "login-notification_link-container").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "clear").find_elements(By.TAG_NAME, "ul"
                        )[1].find_elements(By.TAG_NAME, "li")[2].click()
    driver.find_element(By.CLASS_NAME, "pB").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "tabs").find_elements(By.TAG_NAME, "li")[3].click()


def authorization(driver, login, password):
    print(driver.current_url)
    print("1st action")
    driver.find_element(By.NAME, "login").send_keys(login)
    print("2nd action")
    driver.find_element(By.NAME, "password").send_keys(password)


def change_date_format(date_str):
    day = "0" + date_str[1] if len(date_str[1]) < 2 else date_str[1]
    return date_str[3] + ".{}".format(months[date_str[2]]) + "." + day


def write_subject_row(row):
    marks = []
    for mark in [mark for mark in row.find_elements(By.TAG_NAME, "span")]:
        mark_title = mark.get_attribute("title")
        if mark_title and "не учит" not in mark_title:
            marks.append(int(mark.text))
    if marks:
        return round(sum(marks) / len(marks), 2)
    return 0


def term_reader(actual_term, log, passw):
    #display = Display(visible=0, size=(800, 600))
    #display.start()

    browser = open_browser()
    browser.get(SCHOLL_PAGE)
    print(browser.current_url)
    # print(browser.page_source)

    time.sleep(6)
    print("1st phase")
    authorization(browser, log, passw)
    print("2nd phase")
    open_marks_tables(browser)
    term_stat = subjects_structure
    browser.find_element(By.CLASS_NAME, "switch").find_elements(By.TAG_NAME, "li")[actual_term].click()
    # переход на страницу триместра
    for subject_row in browser.find_element(By.ID, "journal").find_elements(By.TAG_NAME, "tr")[2:]:
        subject_name = subject_row.find_element(By.CLASS_NAME, "s2").find_element(By.CLASS_NAME, "u").text
        term_stat[subject_name] = [(write_subject_row(subject_row))]
    browser.close()
    #display.stop()
    return term_stat

