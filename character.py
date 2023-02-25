from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

# URL to scrape
characters_url = "https://wiki.hoyolab.com/pc/genshin/aggregate/character"
character_url = "https://wiki.hoyolab.com/pc/genshin/entry/3336"
char_url = "https://wiki.hoyolab.com/pc/genshin/entry/"
chars_id = []

# XML path to scrape
char = '//*[@id="__layout"]/main/main/section/div[3]/div/article'
char_name = '[3]/div[2]/span'
char_profile = '[3]/div[1]/div/img[2]'

# Use a headless browser to load the page
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.get(characters_url)

# Wait for the element to appear
wait = WebDriverWait(driver, 5)

# Click any border of the page to load the content
# element = wait.until(EC.presence_of_element_located((By.XPATH, char)))

# Extract the complete HTML content
html_content = driver.page_source


def character(chari_id, i):
    w = WebDriverWait(driver, 7)
    driver.get(char_url + chari_id)

    if i == 0:
        w.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.guide-edit-close')))
        driver.find_element(By.CSS_SELECTOR, '.guide-edit-close').click()

    w.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="1_baseInfo"]/div/div[2]/div[1]/div[2]/div[1]/div/div/p')))

    char_j = []
    name = ""

    # Simulate scrolling down the page to load the content
    scroll_pause = 2
    l_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == l_height:
            break
        l_height = new_height

    # General
    name_path = '//*[@id="1_baseInfo"]/div/div[2]/div[1]/div[2]/div[1]/div/div/p'
    description_path = '//*[@id="__layout"]/main/div/div[2]/div[2]/div[1]/div/div[4]/div/div[1]/div/div/p'

    d1 = '//*[@id="__layout"]/main/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[1]'
    d2 = '//*[@id="__layout"]/main/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[2]'
    d3 = '//*[@id="__layout"]/main/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[3]'
    d4 = '//*[@id="__layout"]/main/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[4]'
    d5 = '//*[@id="__layout"]/main/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[5]'

    # Attributes
    constellation_path = '//*[@id="1_baseInfo"]/div/div[2]/div[3]/div[2]/div[1]/div/div/p'
    vision_path = '//*[@id="1_baseInfo"]/div/div[2]/div[5]/div[2]/div[1]/div/div/p'
    birthday_path = '//*[@id="1_baseInfo"]/div/div[2]/div[2]/div[2]/div[1]/div/div/p'
    title_path = '//*[@id="1_baseInfo"]/div/div[2]/div[4]/div[2]/div[1]/div/div/p'
    affiliation_path = '//*[@id="1_baseInfo"]/div/div[2]/div[6]/div[2]/div[1]/div/div/p'

    # Stats

    # Gallery
    avatar_path = '//*[@id="3_gallery_character"]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/img'
    card_path = '//*[@id="3_gallery_character"]/div/div[2]/div[2]/div[2]/img'

    weapon = "unknown"
    region = "unknown"
    rarity = "unknown"
    bonus_multiplier = "unknown"
    c_element = "unknown"

    # Get general data
    def get_data_type(data_path):
        try:
            d = driver.find_element(By.XPATH, data_path).text
            if d == "Anemo" or d == "Cryo" or d == "Dendro" or d == "Electro" or d == "Geo" or d == "Hydro" or d == "Pyro":
                return [d, "element"]
            elif d == "Mondstadt" or d == "Liyue" or d == "Inazuma City" or d == "Sumeru" or d == "Dragonspine" or d == "Teyvat" or d == "Inazuma" or d == "Liyue Harbor" or d == "Mondstadt Harbor" or d == "Mondstadt" or d == "Liyue" or d == "Inazuma City" or d == "Sumeru" or d == "Dragonspine" or d == "Teyvat":
                return [d, "region"]
            elif d == "5-Star" or d == "4-Star":
                return [d, "rarity"]
            elif d == "Sword" or d == "Claymore" or d == "Polearm" or d == "Bow" or d == "Catalyst":
                return [d, "weapon"]
            else:
                return [d, "bonus_multiplier"]
        except:
            return ["unknown", "unknown"]

    data1 = get_data_type(d1)
    data2 = get_data_type(d2)
    data3 = get_data_type(d3)
    data4 = get_data_type(d4)
    data5 = get_data_type(d5)

    if data1[1] == "region":
        region = data1[0]
    elif data1[1] == "rarity":
        rarity = data1[0]
    elif data1[1] == "bonus_multiplier":
        bonus_multiplier = data1[0]
    elif data1[1] == "weapon":
        weapon = data1[0]
    elif data1[1] == "element":
        c_element = data1[0]

    if data2[1] == "region":
        region = data2[0]
    elif data2[1] == "rarity":
        rarity = data2[0]
    elif data2[1] == "bonus_multiplier":
        bonus_multiplier = data2[0]
    elif data2[1] == "weapon":
        weapon = data2[0]
    elif data2[1] == "element":
        c_element = data2[0]

    if data3[1] == "region":
        region = data3[0]
    elif data3[1] == "rarity":
        rarity = data3[0]
    elif data3[1] == "bonus_multiplier":
        bonus_multiplier = data3[0]
    elif data3[1] == "weapon":
        weapon = data3[0]
    elif data3[1] == "element":
        c_element = data3[0]

    if data4[1] == "region":
        region = data4[0]
    elif data4[1] == "rarity":
        rarity = data4[0]
    elif data4[1] == "bonus_multiplier":
        bonus_multiplier = data4[0]
    elif data4[1] == "weapon":
        weapon = data4[0]
    elif data4[1] == "element":
        c_element = data4[0]

    if data5[1] == "region":
        region = data5[0]
    elif data5[1] == "rarity":
        rarity = data5[0]
    elif data5[1] == "bonus_multiplier":
        bonus_multiplier = data5[0]
    elif data5[1] == "weapon":
        weapon = data5[0]
    elif data5[1] == "element":
        c_element = data5[0]

    card = "unknown"

    try:
        card = driver.find_element(By.XPATH, card_path).get_attribute("src")
    except:
        pass

    char_j.append({
        "name": driver.find_element(By.XPATH, name_path).text,
        "description": driver.find_element(By.XPATH, description_path).text,
        "element": c_element,
        "weapon": weapon,

        "Attributes": {
            "region": region,
            "rarity": rarity,
            "bonus_multiplier": bonus_multiplier,
            "constellation": driver.find_element(By.XPATH, constellation_path).text,
            "vision": driver.find_element(By.XPATH, vision_path).text,
            "birthday": driver.find_element(By.XPATH, birthday_path).text,
            "title": driver.find_element(By.XPATH, title_path).text,
            "affiliation": driver.find_element(By.XPATH, affiliation_path).text
        },

        "Gallery": {
            "avatar": driver.find_element(By.XPATH, avatar_path).get_attribute('src'),
            "card": card
        }
    })

    name = char_j[0]["name"]

    with open(name + '.json', 'w') as outfile:
        json.dump(char_j, outfile, indent=4)


character(str(3336), 0)

# Close the browser
driver.quit()
