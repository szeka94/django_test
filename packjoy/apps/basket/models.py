from django.utils.translation import ugettext as _

from oscar.apps.basket.models import *  # noqa isort:skip
from oscar.apps.basket.models import Basket as OscarBasket


class Basket(OscarBasket):

    def is_quantity_allowed(self, qty):
        """
        Test whether the passed quantity of items can be added to the basket
        """
        # We enforce a max threshold to prevent a DOS attack via the offers
        # system.
        basket_threshold = settings.OSCAR_MAX_BASKET_QUANTITY_THRESHOLD
        if basket_threshold:
            total_basket_quantity = self.num_items
            max_allowed = basket_threshold - total_basket_quantity
            if qty > max_allowed:
                return False, _(
                    "Due to technical limitations we are not able "
                    "to ship more than %(threshold)d items in one order.") \
                       % {'threshold': basket_threshold}
        return True, None
