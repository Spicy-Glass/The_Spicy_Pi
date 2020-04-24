import requests
import json
import Pi
import time



API_ENDPOINT = "https://deployment-test-5tfsskgkda-uc.a.run.app/"
def set_val(vehicle_id, key, new_val, sender, token, subkey=None):
    payload = {'vehicle_id':vehicle_id, 'key':key, 'new_val':new_val, 'sender':sender, 'token':token, 'subkey':subkey}
    r = requests.post(url = API_ENDPOINT + "set_val", json=payload)
    #r = requests.post(url = API_ENDPOINT + "500",json = payload)
    print(r)
    if str(r) == "<Response [200]>":
        print("The call is working perfectly")
    else:
        print("There was an error",str(r))
        Pi.light_dic["spicylight2"] = True
        time.sleep(6)
        print("hello after 6 sec sleep")
        Pi.light_dic["spicylight2"] = False
        print("light should be off now")

    return r
    
def get_vehicle_data(vehicle_id):
    payload = {'vehicle_id':vehicle_id}
    r = requests.post(url = API_ENDPOINT + "get_vehicle_data", json=payload)
    # print(r)
    return r