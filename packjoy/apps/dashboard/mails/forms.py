from django import forms
from django.utils.translation import ugettext_lazy as _


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
								label=_('Email address/list name'),
								help_text=_('Please enter the email address'
											' or the name of the email list.'))
	# a checkbox to check if the recipient is a list of emails
	is_email_list = forms.NullBooleanField(label=_('Is email list?'),
										   help_text=_('Check this if should search'
									   			       ' for the email list.'))
