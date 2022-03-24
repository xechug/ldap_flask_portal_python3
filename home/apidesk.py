# Python version - 3.8
# This script requires requests module installed in python.
import requests
import json

url_request = ""
url_workstation= ""
headers = {"authtoken": ""}

def view_all_requests(user_query):
    input_data = '''{
            "list_info": {
                "row_count": 20,
                "start_index": 1,
                "sort_field": "subject",
                "sort_order": "asc",
                "get_total_count": true,
                "search_fields": {
                    "requester.name": "'''+user_query+'''",
                    "status.name": "01 - Abierta"
                }
            }
        }'''
    params = {'input_data': input_data}
    response = requests.get(url_request, headers=headers, params=params, verify=False)
    view_all_requests_json = json.loads(response.text)

    return view_all_requests_json

    #for i in view_all_requests_json['requests']:
        #if i['requester']['name'] == user_query:
        #return i['id']

def view_asset(apidesk_sama):
    input_data = '''{
        "list_info": {
            "row_count": 1,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "asc",
            "get_total_count": true,
     "search_fields": {
                        "name": "'''+apidesk_sama+'''.contoso"

                    }
        }
    }'''
    params = {'input_data': input_data}
    response = requests.get(url_workstation, headers=headers, params=params, verify=False)
    view_workstation = json.loads(response.text)

    return view_workstation