import pytest
from mixer.backend.django import mixer

from django.urls import reverse

from oscar.test.utils import RequestFactory
from oscar.test.factories import ProductFactory, UserFactory
from oscar.core.loading import get_class

from packjoy.apps.checkout import views

IndexView = get_class('checkout.views', 'IndexView')


pytestmark = pytest.mark.django_db


class TestCheckoutView:

    def init_checkout(self):
        self.product = ProductFactory()
        self.user = UserFactory()

    def test_anonymous_user_no_basket(self):
        req = RequestFactory().get('/')
        resp = views.ShippingMethodView.as_view()(req)
        assert resp.status_code == 302
        assert resp.url == reverse('basket:summary'), 'Should be redirected to the basket page'

    def test_logged_in_user_no_basket(self):
        self.init_checkout()
        req = RequestFactory().get('/')
        req.user = self.user
        resp = views.ShippingMethodView.as_view()(req)
        assert resp.status_code == 302
        assert resp.url == reverse('basket:summary'), 'Should be redirected to the basket page'

    def test_anon_user_login_redirect(self):
        self.init_checkout()
        req = RequestFactory().get('/')
        req.basket.add_product(self.product)
        resp = IndexView.as_view()(req)
        assert resp.status_code == 200, 'Should be logged in to checkout'

    def test_user_can_go_to_shipping_address_page(self):
        self.init_checkout()
        req = RequestFactory().get('/')
        req.user = self.user
        req.basket.add_product(self.product)
        resp = views.ShippingAddressView.as_view()(req)
        assert resp.status_code == 200




