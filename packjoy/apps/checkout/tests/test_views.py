import pytest
from mixer.backend.django import mixer

from django.urls import reverse

from oscar.test.utils import RequestFactory

from packjoy.apps.checkout import views


pytestmark = pytest.mark.django_db


class TestShippingMethodView:
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