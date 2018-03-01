from decimal import Decimal as D

from oscar.apps.partner.strategy import UseFirstStockRecord, StockRequired, DeferredTax, Structured
from oscar.apps.partner.strategy import Default, Selector
from oscar.apps.partner.prices import FixedPrice as OscarFixedPrice
from oscar.core.loading import get_class


Unavailable = get_class('partner.availability', 'Unavailable')
UnavailablePrice = get_class('partner.prices', 'Unavailable')


class FixedPrice(OscarFixedPrice):
    # @property
    # def incl_tax(self):
    #   '''
    #   Overwriting this to show the excl prices
    #   '''
    #   return self.excl_tax

    @property
    def effective_price(self):
        return self.excl_tax

    @property
    def is_tax_known(self):
        return self.tax is not None



class Selector(Selector):

    def strategy(self, request=None, user=None, **kwargs):
        return RomanianEclTVA(request=request)


class RomanianEclTVA(UseFirstStockRecord, StockRequired, DeferredTax, Structured):

   def pricing_policy(self, product, stockrecord):
        # Check stockrecord has the appropriate data
        if not stockrecord or stockrecord.price_excl_tax is None:
            return UnavailablePrice()
        return FixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax )


