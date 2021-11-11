from flask.wrappers import Response
import requests,json
from requests.auth  import HTTPBasicAuth
from decouple import config

from flask import Flask,json,request
app = Flask(__name__)

#mpesa details 
consumer_key = config('organization_mpesa_api_key')
consumer_secret = config('organization_mpesa_api_secret')
base_url = config('organization_mpesa_base_url')
organization_shortcode = config('organization_shortcode')
transation_state = config('organization_transation_state')

@app.route('/',methods = ['GET'])
def home():
	return 'Our Mpesa App Home Page'

@app.route('/access_token')
def token():
	'''
	Function that uses the consumer key and consumer secret
	to generate and authorization token for a given MPesa app
	'''
	return ac_token()

def ac_token():
	'''
	Function that fetched authorization token for daraja api
	'''
	mpesa_auth_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
	data = (requests.get(mpesa_auth_url,auth = HTTPBasicAuth(consumer_key,consumer_secret))).json()
	return data['access_token']

#register urls
@app.route('/register_urls')
def register():
	'''
	Function that registers the validation and confirmation urls for an APP
	in MPesa
	'''
	mpesa_endpoint = 'https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl'
	headers = {
		"Authorization": "Bearer %s" % ac_token(),
		"Content-Type": "application/json"
	}

	req_body = {
		"ShortCode":organization_shortcode,
		"ResponseType":transation_state,
		"ConfirmationURL": base_url +"/c2b/confirm",
		"ValidationURL": base_url +"/c2b/validation"
	}

	response_data = requests.post(
		mpesa_endpoint,
		json = req_body,
		headers = headers
	)
	#return the response data
	return response_data.json()


@app.route('/c2b/confirm',methods = ['GET','POST'])
def confirm():
	'''
	This is an endpoint that receives confirmation from 
	Mpesa when a transation is completed successfully
	'''
	#get data
	data = request.get_json()
	#call the payment processing on the recieved data
	payment_status = process_payment(data)
	#return sucess
	return {'status':'Success'}

@app.route('/c2b/validation')
def validate():
	'''
	Function that recives a validation request from mpesa before a
	transaction is completed. A request is only sent to this URL is 
	external validation is activated
	'''
	#we currently have not active external validation hence just pass
	pass
	return {'status':'Success'}

def process_payment(transaction):
	'''
	Function that uses the data from the transaction response i.e confirm
	url to create process payment that can be stored locally
	input: 
		transaction - dict
	output:
		None
	'''
	#get various details
	customer_acc = transaction.get('BillRefNumber')
	customer_phone_num = transaction.get('MSISDN')
	customer_first_name = transaction.get('FirstName')
	customer_middle_name = transaction.get('MiddleName')
	customer_last_name = transaction.get('LastName')
	transaction_amount = transaction.get('TransAmount')
	transaction_id = transaction.get('TransID')
	transaction_type = transaction.get('TransactionType')
	transaction_time = transaction.get('TransTime')
	business_short_code = transaction.get('BusinessShortCode')
	third_party_id = transaction.get('ThirdPartyTransID')
	invoice_number = transaction.get('InvoiceNumber')
	organization_balance = transaction.get('OrgAccountBalance')
	#now create the payment in the system here etc.
	print("*"*80)
	print("processing payments in here")
	print(customer_phone_num)
	print(customer_first_name)
	print(transaction_amount)
	print(transaction_id)


if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0' , port = 3400)
