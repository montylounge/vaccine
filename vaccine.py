#!/usr/bin/env python3
from time import sleep
from datetime import datetime
from pprint import pprint

from pyzipcode import ZipCodeDatabase
import requests

STATE = "CO"
URL = f"https://www.vaccinespotter.org/api/v0/states/{STATE}.json"
MYZIP = 80111


def _get_close_zips(zipcode=MYZIP):
    zcdb = ZipCodeDatabase()
    return {
        int(z.zip)
        for z in zcdb.get_zipcodes_around_radius(zipcode, 25)
        if z
    }

def scrape():
    close_zips = _get_close_zips()
    print(close_zips)

    while True:
        print(f'{"-" * 20} {datetime.now().isoformat()}')
        try:
            d = requests.get(URL).json()
        except Exception as exc:
            print(exc)
        else:
            zips_found = set()
            for feature in d["features"]:
                prop = feature["properties"]
                if prop["appointments_available"]:
                    #['id', 'url', 'city', 'name', 'state', 'address', 'provider', 'time_zone', 'postal_code', 'appointments', 'provider_brand', 'carries_vaccine', 'provider_brand_name', 'provider_location_id', 'appointments_available', 'appointments_last_fetched'] 
                    zipcode = int(prop.get("postal_code", 0))
                    if zipcode in close_zips:
                        pprint(prop)
                    zips_found.add(zipcode)
            print(sorted(zips_found))
        sleep(300)


if __name__ == '__main__':
    scrape()
