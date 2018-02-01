from django.test import TestCase
from django.urls import reverse

from packjoy.tests.factories import ProductFactory, UserFactory


class CheckoutViewTest(TestCase):

    def setUp(self):
        self.product = ProductFactory()
        self.user = UserFactory()
        # self.pdp = reverse('catalogue:detail', kwargs={'pk': self.product.id,
        #                                                 'product_slug': self.product.slug, })
        self.address_page = reverse('checkout:shipping-address')

    def init_checkout(self):
        # Ensure that user have one item in the basket
        product_url = reverse('basket:add', kwargs={'pk': self.product.id})
        self.client.post(product_url, {'quantity': 1}, format='json')

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

    def test_anon_user_is_redirected_to_checkout_index(self):
        self.client.force_login(user=self.user)
        self.init_checkout()
        response = self.client.get(self.address_page)
        self.assertEqual(response.url, reverse('checkout:index'))

    def test_user_can_go_to_shipping_address_page(self):
        self.init_checkout()

