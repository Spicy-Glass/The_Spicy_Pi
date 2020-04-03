import requests
import json


def set_val(vehicle_id, key, new_val, sender, token, subkey=None):
    payload = {'vehicle_id':vehicle_id, 'key':key, 'new_val':new_val, 'sender':sender, 'token':token, 'subkey':subkey}
    r = requests.post(url = API_ENDPOINT + "set_val", json=payload)
    # print(r)
    return r
    
def get_vehicle_data(vehicle_id):
    payload = {'vehicle_id':vehicle_id}
    r = requests.post(url = API_ENDPOINT + "get_vehicle_data", json=payload)
    # print(r)
    return r