import pytest

from oscar.test.factories import UserFactory

from packjoy.apps.checkout import forms


pytestmark = pytest.mark.django_db


class TestCheckoutForms:

    def init_submit(self):
        self.user = UserFactory()

    def generate_shipping_address_data(self):
        self.init_submit()
        data = {
            'first_name': 'test1',
            'last_name': 'test2',
            'line1': 'This is the 1st address line',
            'line4': 'The 4th line address',
            'state': 'CV',
            'postcode': '525400',
            'phone_number': '+40740501803',
            'notes': 'Notes for testing',
            'user': self.user
        }
        return data

    def test_shipping_address_form_required_fields(self):
        form = forms.ShippingAddressForm({})
        assert form.is_valid() is False

        self.init_submit()
        data = self.generate_shipping_address_data()
        form = forms.ShippingAddressForm(data)
        print(form.errors)
        assert form.is_valid() is True

        for i in range(len(data)):
            # Looping over the data and removing required fields
            submit_data = list(data.items())
            submit_data.pop(i)
            form = forms.ShippingAddressForm({ key: value for (key, value) in submit_data })
            assert form.is_valid() is False

