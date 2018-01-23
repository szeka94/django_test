from django.shortcuts import redirect
from django.conf import settings

from oscar.apps.checkout.views import ShippingMethodView as OscarShippingMethodView, \
                                        PaymentDetailsView as OscarPaymentDetailsView


class ShippingMethodView(OscarShippingMethodView):

    def get_success_response(self):
        '''
        Overriding the default behaviour in order
        to skip the `select payment-method` view
        and go directly to the pre
        '''
        return redirect('checkout:preview')


class PaymentDetailsView(OscarPaymentDetailsView):

    def get_context_data(self, **kwargs):
        context = super(PaymentDetailsView, self).get_context_data(**kwargs)
        submit = {
            'url' : settings.CHECKOUT_SUBMIT_URL,
        }
        context['submit'] = submit
        return context
