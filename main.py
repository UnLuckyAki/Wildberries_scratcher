from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import requests
from selenium.webdriver.chrome.options import Options
from os import mkdir, startfile


print('''
░██╗░░░░░░░██╗██████╗░  ░██████╗░█████╗░██████╗░░█████╗░████████╗░█████╗░██╗░░██╗███████╗██████╗░
░██║░░██╗░░██║██╔══██╗  ██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║░░██║██╔════╝██╔══██╗
░╚██╗████╗██╔╝██████╦╝  ╚█████╗░██║░░╚═╝██████╔╝███████║░░░██║░░░██║░░╚═╝███████║█████╗░░██████╔╝
░░████╔═████║░██╔══██╗  ░╚═══██╗██║░░██╗██╔══██╗██╔══██║░░░██║░░░██║░░██╗██╔══██║██╔══╝░░██╔══██╗
░░╚██╔╝░╚██╔╝░██████╦╝  ██████╔╝╚█████╔╝██║░░██║██║░░██║░░░██║░░░╚█████╔╝██║░░██║███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚═════╝░  ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝''')
print('''Wildberries scratcher by Lucky Aki
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
''')


def scratch_proc(text_nums):
    #text_nums = input("Код товара: ")
    if len(text_nums) != 8 or text_nums.isalpha():
        print('Неверный ввод! Только артикул, например: 12345678')
        return 0

    mkdir(text_nums)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"https://www.wildberries.ru/catalog/{text_nums}/detail.aspx")
    html = driver.find_element(By.TAG_NAME,'html')
    time.sleep(0.5)
    html.send_keys(Keys.END)
    time.sleep(0.5)
    html.send_keys(Keys.END)
    wait = WebDriverWait(driver, 0.5)
    try:
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.popup__btn-main.j-confirm")))
        element.click()
    except:
        pass
    source_data = driver.page_source

    soup = BeautifulSoup(source_data, "html.parser")
    photo_tags = soup.find_all('img', alt='photo')
    n = 0
    for image in photo_tags:
        n+=1
        cut_link = image['src']
        link = cut_link[:len(cut_link)-6]
        img_data = requests.get(f'https:{link}fs.jpg').content
        with open(f'{text_nums}/{n}.jpg', 'wb') as handler:
            handler.write(img_data)
    startfile(text_nums)

while True:
    scratch_proc(text_nums = input('\033[91m' + "Артикул: " + '\033[0m'))
