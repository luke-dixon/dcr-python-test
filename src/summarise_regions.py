"""
Print out a summary of each region with the region name, number of
countries and total population as JSON.
"""
import json

from db import Region, DBO


class SummariseRegionsDBO(Region):
    @classmethod
    def summarise(cls):
        dbo = DBO()
        select_statement = """
            SELECT
                r.name,
                COUNT(c.id) AS number_countries,
                SUM(c.population) AS total_population
            FROM country c JOIN region r ON c.region_id = r.id
            GROUP BY r.id
            ORDER BY r.name;
            """
        dbo.cursor.execute((select_statement))
        headers = [header[0] for header in dbo.cursor.description]

        for row in dbo.cursor.fetchall():
            obj = cls()
            obj.data = {k: v for k, v in zip(headers, row)}
            yield obj


class SummariseRegions:
    def run(self):
        print(
            json.dumps(
                {"regions": [r.data for r in SummariseRegionsDBO.summarise()]},
                indent=4,
            )
        )


if __name__ == "__main__":
    SummariseRegions().run()
