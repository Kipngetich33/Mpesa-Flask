from decouple import config

API_USERNAME = config('organization_mpesa_api_key')
API_KEY = config('organization_mpesa_api_secret')

print(API_USERNAME)