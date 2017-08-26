#Written by Jose Estrada

import requests
from bs4 import BeautifulSoup as bs
import timeit

session = requests.session()

url = input('Enter the URL for the desired shoe : ')

def add_to_cart(url):
	global session
	print ('Checking for sizes instock...')
	endpoint = url
	response = session.get(endpoint)

	soup = bs(response.text, 'html.parser')
	div = soup.find("div", {"class": "box_wrapper"})
	all_sizes = div.find_all("a")
	
	
	sizes_instock = []	
	for size in all_sizes:
		if "piunavailable" not in size["class"]:
			size_id = size['id']
			sizes_instock.append(size_id.split("_")[1])
			print (sizes_instock)
			
	size_chosen = input('From the list, enter the desired PID: ')
	cart_endpoint = 'http://www.jimmyjazz.com/cart-request/cart/add/%s/1'%(size_chosen)
	print ('Attempting to add ' + size_chosen + ': ' + cart_endpoint)
	cart_response = session.get(cart_endpoint)
	
	return '"success":1' in cart_response.text


def checkout():
	global session
	print('Checking Out...')
	checkout_endpoint = 'https://www.jimmyjazz.com/cart/checkout'
	checkout_endpoint_response = session.get(checkout_endpoint)
	soup = bs(checkout_endpoint_response.text, 'html.parser')
	
	inputs = soup.find_all('input',{'name':'form_build_id'})
	form_build_id = inputs[1]["value"]

	endpoint1 = 'https://www.jimmyjazz.com/cart/checkout'

#Enter your info
	payload1 =   [

	  ('billing_email', ''),
	  ('billing_email_confirm', ''),
	  ('billing_phone', ''),
	  ('email_opt_in', '1'),
	  ('shipping_first_name', ''),
	  ('shipping_last_name', ''),
	  ('shipping_address1', ''), #House street only
	  ('shipping_address2', ''), #House digit only
	  ('shipping_city', ''),
	  ('shipping_state', ''),
	  ('shipping_zip', ''),
	  ('shipping_method', '1'),
	  ('billing_first_name', ''),
	  ('billing_last_name', ''),
	  ('billing_country', 'US'),
	  ('billing_address1', ''),
	  ('billing_address2', ''),
	  ('billing_city', ''),
	  ('billing_state', ''),
	  ('billing_zip', ''),
	  ('cc_type', 'Visa'),
	  ('cc_number', ''),
	  ('cc_exp_month', ''),
	  ('cc_exp_year', ''),
	  ('cc_cvv', ''),
	  ('gc_num', ''),
	  ('form_build_id', form_build_id),
	  ('form_id', 'cart_checkout_form'),

	]

	
	response1 = session.post(endpoint1, data=payload1)
	
	response2 = session.get('https://www.jimmyjazz.com/cart/confirm')
	soup = bs(response2.text, 'html.parser')
	form_id = soup.find('input', {'name': 'form_build_id'})['id']
	payload2 = {
		'form_build_id': form_build_id,
		'form_id': 'cart_confirm_form'
	}
	response3 = session.post('https://www.jimmyjazz.com/cart/confirm', data=payload2)
	try:
		soup = bs(response3.text, 'html.parser')
		error = soup.find('div', {'class': 'messages error'}).text
		print(error)
	except:
		print('Checkout was successful!')


start = timeit.default_timer()
if add_to_cart():
	checkout()
else:
	print('Size not available')
stop = timeit.default_timer()
print(stop - start)
