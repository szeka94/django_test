from decimal import Decimal as D

def apply_to(submission):
	rate = D('0.00')
	for line in submission['basket'].all_lines():
		line_tax = calculate_tax(
			line.line_price_excl_tax_incl_discounts, rate)
		unit_tax = (line_tax / line.quantity).quantize(D('0.01'))
		line.purchase_info.price.tax = unit_tax

	# Note, we change the submission in place - we don't need to
	# return anything from this function

	# THIS SHIT SHOULD BE FIXED
	shipping_method = submission['shipping_method']
	# if not shipping_method.name == 'Free shipping':
	# 	shipping_method.tax = calculate_tax(
	# 		shipping_method.charge_incl_tax, rate)
	# Hardcpde shipping_method attribute to the submissing to
	# calculate non-tax price again
	shipping_method.excl_tax = D('0.00')
	shipping_method.incl_tax = D('0.00')
	shipping_method.is_tax_known = True

def calculate_tax(price, rate):
	tax = price * rate
	return tax.quantize(D('0.01'))