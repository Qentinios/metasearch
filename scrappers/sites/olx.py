from datetime import datetime

import requests
import unidecode
from bs4 import BeautifulSoup

from scrappers.helpers import extract_number_from_string
from website.models import Offer, OfferWebsite


def olx_get_response(type, area_min, area_max, rooms, price_min, price_max, city):
    url = 'https://www.olx.pl/nieruchomosci/'
    params = {}

    if type:
        if type == Offer.TYPES.house:
            url += 'domy/'
        elif type == Offer.TYPES.flat:
            url += 'mieszkania/'
        elif type == Offer.TYPES.rent:
            url += 'mieszkania/wynajem/'
        elif type == Offer.TYPES.plot:
            url += 'dzialki/'

    if city:
        city_name = unidecode.unidecode(city.name.lower())
        url += city_name + '/'

    if price_min:
        params["search[filter_float_price:from]"] = price_min

    if price_max:
        params["search[filter_float_price:to]"] = price_max

    if area_min:
        params["search[filter_float_m:from]"] = area_min

    if area_max:
        params["search[filter_float_m:to]"] = area_max

    if rooms and type != Offer.TYPES.plot:
        if rooms == 1:
            value = "one"
        elif rooms == 2:
            value = "two"
        elif rooms == 3:
            value = "three"
        else:
            value = "four"

        params["search[filter_enum_rooms][0]"] = value

    response = requests.get(url, params)

    return response.content


def olx_get_offers(response):
    offers = []

    soup = BeautifulSoup(response, 'html.parser')

    for offer in soup.find_all('td', class_="offer"):
        a = offer.find('a', class_="detailsLink")
        address = offer.find('i', {"data-icon": "location-filled"}).parent.find(text=True)

        if a:
            link = a['href']

            # skip external offers
            if not link.startswith('https://www.olx.pl'):
                continue

            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.find('h1', {'data-cy': 'ad_title'}).find(text=True)
            price = soup.find('div', id='baxter-under-price').findPrevious('h3').find(text=True)
            price = extract_number_from_string(price)
            area = None
            rooms = None

            for attribute in soup.find_all('li'):
                if attribute.text.startswith('Powierzchnia'):
                    area = attribute.find(text=True)
                    area = extract_number_from_string(area)
                if attribute.text.startswith('Liczba pokoi'):
                    rooms = attribute.find(text=True)

                    if rooms == 'Liczba pokoi: Kawalerka':
                        rooms = 1
                    else:
                        rooms = extract_number_from_string(rooms)

            offers.append({'title': title, 'price': price, 'area': area, 'rooms': rooms, 'address': address,
                           'link': link})

    return offers


def olx_add_offers(type, city, offers):
    website = OfferWebsite.objects.get(name='Olx.pl')

    for offer in offers:
        offer_obj = Offer.objects.filter(type=type, city=city, website=website, link=offer.get('link'))

        if offer_obj.exists():
            offer_obj = offer_obj.get()
            properties = ['title', 'price', 'area', 'rooms', 'address']

            for prop in properties:
                modified = False
                new_value = offer.get(prop)
                old_value = getattr(offer_obj, prop)

                if old_value != new_value:
                    modified = True
                    setattr(offer_obj, prop, new_value)

                if modified:
                    offer_obj.modified = datetime.now()
                    offer_obj.save()
        else:
            Offer.objects.create(type=type, city=city, website=website, title=offer.get('title'), price=offer.get('price'),
                                 area=offer.get('area'), rooms=offer.get('rooms'), address=offer.get('address'),
                                 link=offer.get('link'))

