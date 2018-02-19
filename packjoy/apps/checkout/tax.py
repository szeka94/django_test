from decimal import Decimal as D


def apply_to(submission):
	'''
	Hardcoded 0 tax for b2b sales. Maybe it should be changed 
	in the future, when we have different (b2b, b2c) clients
	'''
	tax_rate = D('0.00')

	basket = submission['basket']
	for line in basket.all_lines():
		line_tax = calculate_tax(
			line.line_price_excl_tax_incl_discounts, tax_rate)
		unit_tax = (line_tax / line.quantity).quantize(D('0.01'))
		line.purchase_info.price.tax = unit_tax

	# should calculate also the shipping chare
	# with 0 tax. This might be changed in the future
	submission['basket'] = basket
	return submission

	# import ipdb; ipdb.set_trace()


def calculate_tax(price, rate):
	tax = price * rate
	return tax.quantize(D('0.01'))