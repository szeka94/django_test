import pprint
import hashlib

from django.shortcuts import redirect
from django.conf import settings

from oscar.apps.checkout.views import ShippingMethodView as OscarShippingMethodView, \
                                        PaymentDetailsView as OscarPaymentDetailsView

pp = pprint.PrettyPrinter(indent=4)


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
        pp.pprint(dir((context['basket'])))
        context['submit'] = self.collect_submit_data()
        return context

    @staticmethod
    def collect_submit_data():
        submit = {
            'url' : settings.CHECKOUT_SUBMIT_URL,
            'account_number' : settings.CHECKOUT_ACCOUNT_NUMBER,
        }
        return submit

    def handle_payment(self, order_number, order_total, **payment_kwargs):
        print('At this point, should be valid')

class ReturnCheckoutView(PaymentDetailsView):

    def get(self, request, *args, **kwargs):
        if request.GET.get('action') == 'place_order':
            data = dict()
            data['order_number'] = request.GET.get('order_number')
            data['total'] = request.GET.get('total')
            data['key'] = request.GET.get('key')
            return self.handle_place_order_submission(resp=data)
        return redirect('checkout:preview')

    def handle_place_order_submission(self, resp):

        """
        Handle a request to place an order.
        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.
        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """
        print(self.is_valid_payment_response(order_number=resp['order_number'], total=resp['total'],
                                             key=resp['key']))
        return self.submit(**self.build_submission())

    @staticmethod
    def is_valid_payment_response(secret_word='MGIwNmZjOTUtYzk4ZS00MzA0LThmMTMtZTg1ZDQwNzRkYTVh',
                                     seller_id='901369605', order_number='', total='', key=''):
        word = secret_word + seller_id + order_number + total
        new_key = hashlib.md5()
        new_key.update(word.encode('utf8'))
        return key == new_key

