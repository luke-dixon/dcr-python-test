import json
import urllib.request

from db import Country, Region


class LoadData:
    DATA_FILE = "../data/countries.json"

    def __init__(self):
        # Cache of regions
        self.regions = {}

    def get_raw_data(self):
        data = None
        with open(self.DATA_FILE) as f:
            data = json.load(f)
        return data

    def add_country(self, data):
        region_name = data.get("region", "Unknown")
        region_id = self.get_region_id(region_name)

        country = Country()
        found = country.get_by_name(data["name"])
        if found:
            return
        country.insert(
            data["name"],
            data["alpha2Code"],
            data["alpha3Code"],
            data["population"],
            region_id,
        )
        print(country.data)

    def get_region_id(self, region_name):
        if region_name not in self.regions:
            region = Region()
            region.get_or_create_by_name(region_name)
            self.regions[region.data["name"]] = region.data["id"]
        return self.regions[region_name]

    def run(self):
        data = self.get_raw_data()
        for row in data:
            self.add_country(row)


class LoadDataHTTP(LoadData):
    URL = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def get_raw_data(self):
        # urllib.http.HTTPError for non-200 status codes
        # urllib.error.URLError is raised for connection errors
        response = urllib.request.urlopen(self.URL)
        return json.load(response)


if __name__ == "__main__":
    LoadDataHTTP().run()
