import pytest

from oscar.test.utils import RequestFactory
from oscar.test.factories import ProductFactory, UserFactory


pytestmark = pytest.mark.django_db


class TestTaxAmounts:

	def init_checkout(self):
		self.product = ProductFactory()
		self.user = UserFactory()

	def test_tax_is_not_known_when_added_product(self):
		self.init_checkout()
		req = RequestFactory().get('/')
		req.basket.add_product(self.product)
		req.basket.add_product(self.product)
		assert req.basket.is_tax_known == False, 'Should be only true at the very end of checkout'

	def test_tax_is_zero_in_basket(self):
		self.init_checkout()
		req = RequestFactory().get('/')
		basket = req.basket
		basket.add_product(self.product)
		for line in basket.all_lines():
			assert line.purchase_info.price.tax is None, 'Should be None for every line in the basket' 