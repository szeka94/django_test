from django import forms
from django.utils.translation import ugettext_lazy as _
# for some reason this isn't working
# I have to import the Product model directly
# from the oscar libary
# from oscar.core.loading import get_model
from oscar.apps.catalogue.models import Product

class EmailSenderForm(forms.Form):
	CAMPAIGN_TYPES = [
		('back_in_stock', 'Back In Stock'),
		('new_arrivals', 'New Arrivals'),
		('price_decrease', 'Price Decrease'),
		('welcome', 'Welcome Email'),
	]

	# This is the name of the template
	# which will be sent
	campaign_type = forms.ChoiceField(widget=forms.Select(),
									  choices=CAMPAIGN_TYPES,
									  label=_('Campaign Type'),
									  help_text=_('Please select the'
												  ' campaign type you'
												  ' would like to send.'))
	# the email address of the recipient
	# or the name of the mailing list
	recipient = forms.CharField(max_length=256,
								min_length=6,
								widget=forms.Textarea,
								label=_('Email address/list name'),
								help_text=_('Please enter the email address'
											' or the name of the email list.'))
	# TODO: do some research and refactor the products field
	# below to use a for loop instead hardcoding each one
	product_1 = forms.ModelChoiceField(queryset=Product.objects.all(),
									   label=_('Product 1'),
									   required=False,)
	product_2 = forms.ModelChoiceField(queryset=Product.objects.all(),
									   label=_('Product 2'),
									   required=False,)
	product_3 = forms.ModelChoiceField(queryset=Product.objects.all(),
									   label=_('Product 3'),
									   required=False,)
	product_4 = forms.ModelChoiceField(queryset=Product.objects.all(),
									   label=_('Product 4'),
									   required=False,)
	product_5 = forms.ModelChoiceField(queryset=Product.objects.all(),
									   label=_('Product 5'),
									   required=False,)
	product_6 = forms.ModelChoiceField(queryset=Product.objects.all(),
									   label=_('Product 6'),
									   required=False,)
