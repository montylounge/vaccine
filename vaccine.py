#!/usr/bin/env python3

#['id', 'url', 'city', 'name', 'state', 'address', 'provider', 'time_zone', 'postal_code', 'appointments', 'provider_brand', 'carries_vaccine', 'provider_brand_name', 'provider_location_id', 'appointments_available', 'appointments_last_fetched']
from time import sleep
from datetime import datetime
from pprint import pprint

from pyzipcode import ZipCodeDatabase
import requests

STATE = "CO"
MYZIP = 80111


def _get_close_zips(zipcode=MYZIP):
    zcdb = ZipCodeDatabase()
    return {int(z.zip) for z in zcdb.get_zipcodes_around_radius(zipcode, 25)}

def scrape():
    close_zips = _get_close_zips()
    print(f"zip codes considered close: {sorted(close_zips)}")

    url = f"https://www.vaccinespotter.org/api/v0/states/{STATE}.json"
    while True:
        print(f"{'-' * 20} {datetime.now().isoformat()}")
        try:
            d = requests.get(url).json()
        except Exception as exc:
            print(exc)
        else:
            prop_iter = (feature["properties"] for feature in d["features"])
            available = [(prop, int(prop.get("postal_code", 0))) for prop in prop_iter if prop["appointments_available"]]
            for prop, zipcode in available:
                if zipcode in close_zips:
                    pprint(prop)
            zips_found = {zipcode for _, zipcode in available if zipcode not in close_zips}
            print(f"Appointments found in: {sorted(zips_found)}")
        sleep(300)


if __name__ == '__main__':
    scrape()
