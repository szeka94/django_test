from django.test import TestCase
from django.urls import reverse

# from packjoy.packjoy.apps.checkout import views


class AuthorModelTest(TestCase):

    def setUp(self):
        pass

    def test_no_basket_shipping_method_view(self):
        response = self.client.get(reverse('checkout:shipping-address'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('basket:summary'))

    def test_no_basket_user_address_view(self):
        response = self.client.get(reverse('checkout:payment-method'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('basket:summary'))

    def test_no_basket_payment_details_view(self):
        response = self.client.get(reverse('checkout:payment-details'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('basket:summary'))
