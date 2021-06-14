from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


def scan_otodom(type, area_min, area_max, rooms, price_min, price_max, city):
    driver = webdriver.Chrome()
    driver.get("https://www.otodom.pl/")
    wait = WebDriverWait(driver, 10)

    wait.until(presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
    wait.until(presence_of_element_located((By.ID, "downshift-1-toggle-button"))).click()
    wait.until(presence_of_element_located((By.XPATH, "//div[@id='downshift-1-menu']//li[contains(text(), 'Domy')]"))).click()

    if city:
        driver.find_element_by_id("downshift-0-label").click()
        elem = wait.until(presence_of_element_located((By.CLASS_NAME, "css-asxees"))).find_element_by_id("downshift-0-input")
        elem.clear()
        elem.send_keys(city.name)

        wait.until(presence_of_element_located((By.ID, "downshift-0-item-0"))).click()

