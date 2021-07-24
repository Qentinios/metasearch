import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from scrappers.helpers import extract_number_from_string
from website.models import Offer, OfferWebsite


def otodom_get_response(type, area_min, area_max, rooms, price_min, price_max, city):
    driver = webdriver.Chrome()
    driver.get("https://www.otodom.pl/")
    wait = WebDriverWait(driver, 10)

    # accept Cookies
    wait.until(presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
    time.sleep(3)

    if type:
        wait.until(presence_of_element_located((By.ID, "downshift-1-toggle-button"))).click()
        if type == Offer.TYPES.flat:
            wait.until(presence_of_element_located(
                (By.XPATH, "//div[@id='downshift-1-menu']//li[contains(text(), 'Mieszkania')]"))).click()
        elif type == Offer.TYPES.house:
            wait.until(presence_of_element_located(
                (By.XPATH, "//div[@id='downshift-1-menu']//li[contains(text(), 'Domy')]"))).click()
        elif type == Offer.TYPES.plot:
            wait.until(presence_of_element_located(
                (By.XPATH, "//div[@id='downshift-1-menu']//li[contains(text(), 'Działki')]"))).click()
        elif type == Offer.TYPES.rent:
            wait.until(presence_of_element_located(
                (By.XPATH, "//div[@id='downshift-1-menu']//li[contains(text(), 'wszystkie')]"))).click()
            driver.find_element_by_id('downshift-2-toggle-button').click()
            wait.until(presence_of_element_located((By.ID, "downshift-2-item-1"))).click()

    if city:
        wait.until(presence_of_element_located((By.ID, "downshift-0-label"))).click()
        elem = wait.until(presence_of_element_located((By.CLASS_NAME, "css-asxees"))).find_element_by_id("downshift-0-input")
        elem.clear()
        elem.send_keys(city.name)

        wait.until(presence_of_element_located((By.ID, "downshift-0-item-0"))).click()

    driver.find_element_by_id('WidgetSearchFieldContainer').find_element_by_xpath('//button[@type="submit"]').click()

    if price_min and price_max:
        elem = wait.until(presence_of_element_located((By.ID, "priceMin")))
        elem.send_keys(price_min)

        elem = wait.until(presence_of_element_located((By.ID, "priceMax")))
        elem.send_keys(price_max)

    if area_min and area_max:
        elem = wait.until(presence_of_element_located((By.ID, "areaMin")))
        elem.send_keys(area_min)

        elem = wait.until(presence_of_element_located((By.ID, "areaMax")))
        elem.send_keys(area_max)

    if rooms and type != Offer.TYPES.plot:
        wait.until(presence_of_element_located(
            (By.ID, "roomsNumber"))).click()

        if rooms > 10:
            wait.until(presence_of_element_located(
                (By.ID, "dropdown-checkbox-roomsNumber-MORE"))).click()
        else:
            um2words = {1: 'ONE', 2: 'TWO', 3: 'THREE', 4: 'FOUR', 5: 'FIVE',
                        6: 'SIX', 7: 'SEVEN', 8: 'EIGHT', 9: 'NINE', 10: 'TEN'}
            wait.until(presence_of_element_located(
                (By.XPATH, "//label[@for='dropdown-checkbox-roomsNumber-{}']".format(um2words.get(rooms))))).click()

    driver.find_element_by_id('search-form-submit').click()

    html = wait.until(presence_of_element_located((By.XPATH, '//div[@role="main"]'))).get_attribute('innerHTML')

    return html


def otodom_get_offers(response):
    offers = []

    soup = BeautifulSoup(response, 'html.parser')

    for offer in soup.find_all('a', {'data-cy': 'listing-item-link'}):
        title = offer.find('h3', {'data-cy': 'listing-item-title'}).find(text=True)

        paragraphs = offer.find_all('p')

        address = paragraphs[0].find('span').find(text=True)
        price = paragraphs[1].find(text=True)
        if price == 'Zapytaj o cenę':
            continue
        price = extract_number_from_string(price)

        spans = paragraphs[2].find_all('span')
        rooms = spans[0].find(text=True)
        rooms = extract_number_from_string(rooms)
        area = spans[1].find(text=True)

        n = ''
        for char in area:
            if not char.isdecimal():
                break
            n += char
        area = n

        offers.append({'title': title, 'price': price, 'area': area, 'rooms': rooms, 'address': address})

    return offers


def otodom_add_offers(type, city, offers):
    website = OfferWebsite.objects.get(name='Otodom.pl')

    for offer in offers:
        offer_obj, created = Offer.objects\
            .get_or_create(type=type, city=city, website=website, title=offer.get('title'), price=offer.get('price'),
                           area=offer.get('area'), rooms=offer.get('rooms'), address=offer.get('address'))
