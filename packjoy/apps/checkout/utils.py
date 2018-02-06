from django.conf import settings
from django.contrib import messages
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from oscar.core.loading import get_class
from oscar.apps.checkout.signals import start_checkout


InvalidBasketLineError = get_class('basket.models', 'InvalidBasketLineError')


@receiver(signal=start_checkout)
def handle_line_save(**kwargs):
    '''
    Setting up a listener to force the user to order a minimum quantity
    ak. the MINIMUM_ORDER_QUANTITY variable from the setting file
    '''
    if 'request' in kwargs:
        request = kwargs['request']
        basket = request.basket
        for line in basket.lines.all():
            if line.quantity < int(settings.MINIMUM_ORDER_QUANTITY):
                messages.warning(request,
                        _('''Please don\'t forget, 
                            that our minimum order quantity 
                            per product is: {} pieces.'''.format(
                                settings.MINIMUM_ORDER_QUANTITY)))
                raise InvalidBasketLineError('Invalid Basket Line Error')