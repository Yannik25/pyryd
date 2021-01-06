# This Python file uses the following encoding: utf-8
import requests
import json
import uuid

data = json.dumps({"email":"customemail","password":"verysecretpassword!"})
# copied from https://github.com/NemoN/ioBroker.ryd/blob/master/io-package.json
ryd_api_server = 'url'
ryd_app_version = "2.52.4(201008000)"
client_device_version = "9.0.0"
client_device_resolution = "2960x1440"
client_device_id = "SM-G960F"
client_device_type = "Android"
think_properties = "curLocation,parkingLocation,carOdometer,estimates,reportedFuelTotal,fuel"
think_properties_ignore = "recurrences,openDtcs,score"
ryd_app_locale = "de-de"
ryd_app_internal_name = "TankTaler"
ryd_app_platform = "{} [{},{},{}]".format(
    client_device_type, client_device_id, client_device_version, client_device_resolution
)
ryd_app_user_agent = "{}/{}({};{} {})".format(
    ryd_app_internal_name, ryd_app_version, client_device_id, client_device_type, client_device_version
)
headers = {
    'x-txn-platform': ryd_app_platform,
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': str(0),
    'x-txn-app-version': ryd_app_version,
    'User-agent': ryd_app_user_agent,
    'X-Txn-Request-Id': str(uuid.uuid4()),
    'X-Txn-Locale': ryd_app_locale,
    'Content-Type': 'application/json; charset=utf-8',
}

response = requests.post(ryd_api_server+"/auth%2Flogin%2Flocal", data=data,
                         headers=headers, timeout=2000)
json_object = json.loads(response.text)

ryd_auth_token=json_object["auth_token"]
rydid = json_object["things"][0]["id"]

response = requests.get(ryd_api_server + "/things/" + rydid + "/status?auth_token=" + ryd_auth_token,
                         headers=headers, timeout=2000) 
json_data = json.loads(response.text)
data=json_data["data"]
fuel=data["fuelType"]
license_plate=data["licensePlate"]
battery_mvoltage=data["batteryLevelMV"]
battery_percentage=data["batteryLevelPercent"]
print(fuel)
print(license_plate)
print(battery_mvoltage)
print(battery_percentage)