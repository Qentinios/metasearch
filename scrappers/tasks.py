from scrappers.sites.olx import olx_add_offers, olx_get_offers, olx_get_response
from scrappers.sites.otodom import otodom_get_response, otodom_get_offers, otodom_add_offers
from website.models import OfferWebsite, Offer


class Search:
    type = None
    website = None
    area_min = None
    area_max = None
    rooms = None
    price_min = None
    price_max = None
    city = None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __init__(self, data, *args, **kwargs):
        for key, value in data.items():
            self.__setitem__(key, value)

    def search(self):
        if self.website:
            sites = [self.website.name]
        else:
            sites = OfferWebsite.objects.values_list('name', flat=True)

        if 'Otodom.pl' in sites:
            response = otodom_get_response(type=self.type, area_min=self.area_min, area_max=self.area_max,
                                           rooms=self.rooms, price_min=self.price_min, price_max=self.price_max,
                                           city=self.city)
            offers = otodom_get_offers(response)
            print(len(offers))
            otodom_add_offers(self.type, self.city, offers)

        if 'Olx.pl' in sites:
            response = olx_get_response(type=self.type, area_min=self.area_min, area_max=self.area_max,
                                        rooms=self.rooms, price_min=self.price_min, price_max=self.price_max,
                                        city=self.city)
            offers = olx_get_offers(response)
            print(len(offers))
            olx_add_offers(self.type, self.city, offers)

        offers = Offer.objects.filter(type=self.type).select_related('city')
        if self.city:
            offers = offers.filter(city=self.city)
        if self.price_min:
            offers = offers.filter(price__gte=self.price_min)
        if self.price_max:
            offers = offers.filter(price__lte=self.price_max)
        if self.rooms:
            offers = offers.filter(rooms__exact=self.rooms)
        if self.area_min:
            offers = offers.filter(area__gte=self.area_min)
        if self.area_max:
            offers = offers.filter(area__lte=self.area_max)

        return offers.order_by('-price')
