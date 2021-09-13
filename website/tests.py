from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from website.models import Offer, OfferCity, OfferWebsite


class ViewsTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_view(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_view(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # logout response is redirect

    def test_offer_details_view(self):
        city = OfferCity.objects.create(name="testcity")
        website = OfferWebsite.objects.create(name="testwebsite")
        offer = Offer.objects.create(title="testoffer", city=city, address="testaddress",
                                     type=Offer.TYPES.flat, website=website, area=40, rooms=3,
                                     price=200000, link='http://linktooffer.com')

        response = self.client.get(reverse("offer-details", kwargs={'pk': offer.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
