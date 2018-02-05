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
    print('Signal Received')
    if 'request' in kwargs:
        request = kwargs['request']
        basket = request.basket
        

        for line in basket.lines.all():
            print(line)
            if line.quantity < int(settings.MINIMUM_ORDER_QUANTITY):
                messages.error(request,
                        _('''Something went wrong during your card processing.
                        Please Try again, if the problem persist please,
                        contact our server administrator.'''))
