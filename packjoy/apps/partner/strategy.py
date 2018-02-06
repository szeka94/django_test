from decimal import Decimal as D

from oscar.apps.partner.strategy import UseFirstStockRecord, StockRequired, FixedRateTax, Structured, Selector
from oscar.apps.partner.prices import FixedPrice as OscarFixedPrice
from oscar.core.loading import get_class


Unavailable = get_class('partner.availability', 'Unavailable')
UnavailablePrice = get_class('partner.prices', 'Unavailable')


class FixedPrice(OscarFixedPrice):
    # @property
    # def incl_tax(self):
    # 	'''
    # 	Overwriting this to show the excl prices
    # 	'''
    # 	return self.excl_tax
    show_tax_price = False
    @property
    def effective_price(self):
        return self.excl_tax


class Selector(Selector):

    def strategy(self, request=None, user=None, **kwargs):
        return RomanianEclTVA(request=request)


class RomanianEclTVA(UseFirstStockRecord, StockRequired, FixedRateTax, Structured):
    rate = D('0.00') # no better idea for now

    def pricing_policy(self, product, stockrecord):
        if not stockrecord or stockrecord.price_excl_tax is None:
            return UnavailablePrice()
        rate = self.get_rate(product, stockrecord)
        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price_excl_tax * rate).quantize(exponent)
        return FixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax,
            tax=tax)

