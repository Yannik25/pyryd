# This Python file uses the following encoding: utf-8
import requests
import json
import uuid
import datetime

RYD_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def ryd_time(s: str):
    return datetime.datetime.strptime(s, RYD_DATETIME_FORMAT)

# Dict for refactoring entries of the returned data to
# a value and a unit
REFACTOR_DICT = {
    "fuel_type": (lambda x: x["fuelType"], None),
    "examination_date": (lambda x: ryd_time(x["examinationDate"]), None),
    "last_fuel_top_up": (lambda x: ryd_time(x["lastFuelTopUpTimestamp"]), None),
    "battery_voltage": (lambda x: float(x["batteryLevelMV"])/1000, "V"),
    "battery_percentage": (lambda x: float(x["batteryLevelPercent"]), "%"),
    "battery_health": (lambda x: str(x["batteryHealth"]), None),
    "overall_distance": (lambda x: int(x["carOdometer"]["distanceM"])/1000, "km"),
    "fuel_level": (lambda x: float(x["level"]["OBD_FUELLEVEL"]["l"]), "l"),
    "fuel_percent": (lambda x: float(x["level"]["OBD_FUELLEVEL"]["percent"]), "%"),

}

class Ryd(object):
    def __init__(
        self,
        ryd_api_server: str,
        user_email: str,
        user_passwd: str,
        ryd_app_version="2.52.4(201008000)",
        client_device_version="9.0.0",
        client_device_resolution="2960x1440",
        client_device_id="SM-G960F",
        client_device_type="Android",
        think_properties="curLocation,parkingLocation,carOdometer,estimates,reportedFuelTotal,fuel",
        think_properties_ignore="recurrences,openDtcs,score",
        ryd_app_locale="de-de",
        ryd_app_internal_name="TankTaler",
    ):
        self._ryd_api_server = ryd_api_server
        self._user_email = user_email
        self._user_passwd = user_passwd
        self._ryd_app_version = ryd_app_version
        self._client_device_version = client_device_version
        self._client_device_resolution = client_device_resolution
        self._client_device_id = client_device_id
        self._client_device_type = client_device_type
        self._think_properties = think_properties
        self._think_properties_ignore = think_properties_ignore
        self._ryd_app_locale = ryd_app_locale
        self._ryd_app_internal_name = ryd_app_internal_name
        self._raw_data = {}
        self._ryd_app_platform = "{} [{},{},{}]".format(
            client_device_type,
            client_device_id,
            client_device_version,
            client_device_resolution,
        )
        self._ryd_app_user_agent = "{}/{}({};{} {})".format(
            ryd_app_internal_name,
            ryd_app_version,
            client_device_id,
            client_device_type,
            client_device_version,
        )
        self._headers = {
            "x-txn-platform": self._ryd_app_platform,
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": str(0),
            "x-txn-app-version": ryd_app_version,
            "User-agent": self._ryd_app_user_agent,
            "X-Txn-Request-Id": str(uuid.uuid4()),
            "X-Txn-Locale": ryd_app_locale,
            "Content-Type": "application/json; charset=utf-8",
        }
        self._data = json.dumps({"email": user_email, "password": user_passwd})

    def fetch(self):
        response = requests.post(
            "{}/auth%2Flogin%2Flocal".format(self._ryd_api_server),
            data=self._data,
            headers=self._headers,
            timeout=2000,
        )
        json_object = response.json()

        ryd_auth_token = json_object["auth_token"]
        rydid = json_object["things"][0]["id"]

        response = requests.get(
            "{}/things/{}/status?auth_token={}".format(
                self._ryd_api_server,
                rydid,
                ryd_auth_token,
            ),
            headers=self._headers,
            timeout=2000,
        )
        json_data = response.json()

        self._raw_data = json_data["data"]
        self._ref_data = self._refactored_data(self._raw_data)

    @staticmethod
    def _refactored_data(data: dict):
        """ Returns a refactored version of the raw data returned by fetching """
        result = {}
        for key, (val, uni) in REFACTOR_DICT.items():
            try:
                result[key] = {"value": val(data), "unit": uni}
            except (KeyError, TypeError):
                continue
        return result

    def refactored_data(self):
        return self._ref_data

    def raw_data(self):
        return self._raw_data
