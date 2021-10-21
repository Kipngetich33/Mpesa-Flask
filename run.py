from flask.wrappers import Response
import requests,json
from requests.auth  import HTTPBasicAuth

from flask import Flask,json,request
app = Flask(__name__)


#mpesa details 
consumer_key = 'mR0ImhjJEcC0cVefGItVsZOjVi926cfw'
consumer_secret = 'ZKSVFJqJs3InB03s'
base_url = "http://102.135.170.111:3400/"

@app.route('/',methods = ['GET'])
def home():
	return 'Hello World'

@app.route('/access_token')
def token():
	return ac_token()

#register urls
@app.route('/register_urls')
def register():
	print("*"*80)
	print("register")
	mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
	headers = {
		"Authorization": "Bearer %s" % ac_token(),
		"Content-Type": "application/json"
	}

	req_body = {
			"ShortCode":"600980",
			"ResponseType":"Completed",
			"ConfirmationURL": base_url +"c2b/confirm",
			"ValidationURL": base_url +"c2b/validation"
	}

	print(req_body)

	response_data = requests.post(
		mpesa_endpoint,
		json = req_body,
		headers = headers
	)
	print(response_data)
	print(response_data.headers)
	print(response_data.text)
	return response_data.json()


@app.route('/c2b/confirm',methods = ['GET','POST'])
def confirm():
	print("*"*80)
	print("trying to confim")
	#get data
	data = request.get_json()
	print(data)
	# # write to file
	# file = open('confirm.json','a')
	# file.write(data)
	# file.close()
	return json.jsonify({'status':'Success'})

@app.route('/c2b/validation')
def validate():
	pass
	# #get data
	# data = requests.get_json()
	# # write to file
	# file = open('confirm.json','a')
	# file.write(data)
	# file.close()

def ac_token():
	mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
	data = (requests.get(mpesa_auth_url,auth = HTTPBasicAuth(consumer_key,consumer_secret))).json()
	return data['access_token']


if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0' , port = 3400)
