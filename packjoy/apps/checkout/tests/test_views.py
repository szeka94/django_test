import pytest
from mixer.backend.django import mixer

from django.urls import reverse

from oscar.test.utils import RequestFactory
from oscar.test.factories import ProductFactory
from oscar.core.loading import get_class

from packjoy.apps.checkout import views

IndexView = get_class('checkout.views', 'IndexView')


pytestmark = pytest.mark.django_db


class TestShippingMethodView:

	def init_checkout(self):
		self.create_user()
		self.product = ProductFactory()

	def create_user(self):
		self.user = mixer.blend('auth.User')

	def test_anonymous_user_no_basket(self):
		req = RequestFactory().get('/')
		resp = views.ShippingMethodView.as_view()(req)
		assert resp.status_code == 302
		assert resp.url == reverse('basket:summary'), 'Should be redirected to the basket page'

	def test_logged_in_user_no_basket(self):
		req = RequestFactory().get('/')
		req.user = self.create_user()
		resp = views.ShippingMethodView.as_view()(req)
		assert resp.status_code == 302
		assert resp.url == reverse('basket:summary'), 'Should be redirected to the basket page'

	def test_anon_user_login_redirect(self):
		self.init_checkout()
		req = RequestFactory().get('/')
		req.basket.add_product(self.product)
		resp = IndexView.as_view()(req)
		print(req)
		print(resp)
		assert resp.status_code == 302, 'Should be redirected to login page'
