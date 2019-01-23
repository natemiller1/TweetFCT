import harmony_connect_client
from __future__ import print_function
import time
import harmony_connect_client
from harmony_connect_client.rest import ApiException
from pprint import pprint

configuration = harmony_connect_client.Configuration()
# Configure API key authorization: AppId
configuration.api_key['app_id'] = 'YOUR_API_KEY'
# Configure API key authorization: AppKey
configuration.api_key['app_key'] = 'YOUR_API_KEY'

# create an instance of the API class
api_instance = harmony_connect_client.ChainsApi(harmony_connect_client.ApiClient(configuration))
chain_id = 285904 # str | Chain identifier

try:
    # Get Chain Info
    api_response = api_instance.get_chain_by_id(chain_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChainsApi->get_chain_by_id: %s\n" % e)
