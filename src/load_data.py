import argparse
import json
import urllib.request

from db import Country, CountryTopLevelDomain, Region


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

    def add_country(self, data, update=False):
        region_name = data.get("region", "Unknown")
        region_id = self.get_region_id(region_name)

        country = Country()
        found = country.get_by_name(data["name"])
        if found and not update:
            return

        if found:
            country.update(
                data["name"],
                data["alpha2Code"],
                data["alpha3Code"],
                data["population"],
                region_id,
                data["capital"],
            )
            self.update_top_level_domains(country.data["id"], data)
        else:
            country.insert(
                data["name"],
                data["alpha2Code"],
                data["alpha3Code"],
                data["population"],
                region_id,
                data["capital"],
            )
            self.add_top_level_domains(country.data["id"], data)

        print(country.data)

    def add_top_level_domains(self, country_id, data):
        for name in data["topLevelDomain"]:
            top_level_domain = CountryTopLevelDomain()
            top_level_domain.insert(country_id, name)

    def update_top_level_domains(self, country_id, data):
        CountryTopLevelDomain.clear_for_country(country_id)
        self.add_top_level_domains(country_id, data)

    def get_region_id(self, region_name):
        if region_name not in self.regions:
            region = Region()
            region.get_or_create_by_name(region_name)
            self.regions[region.data["name"]] = region.data["id"]
        return self.regions[region_name]

    def run(self, update=False):
        data = self.get_raw_data()
        for row in data:
            self.add_country(row, update=update)


class LoadDataHTTP(LoadData):
    URL = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def get_raw_data(self):
        # urllib.http.HTTPError for non-200 status codes
        # urllib.error.URLError is raised for connection errors
        response = urllib.request.urlopen(self.URL)
        return json.load(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="load_data",
        description="Loads the data into the database",
    )
    parser.add_argument("-u", "--update", action="store_true")
    parser.add_argument("-f", "--file", action="store_true")
    args = parser.parse_args()
    if args.file:
        LoadData().run(update=args.update)
    else:
        LoadDataHTTP().run(update=args.update)
