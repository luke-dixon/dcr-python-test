from db import DBO


class CreateDB(DBO):
    CREATE_REGIONS = """
        CREATE TABLE IF NOT EXISTS region (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );"""

    CREATE_COUNTRY = """
        CREATE TABLE IF NOT EXISTS country (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            alpha2Code TEXT,
            alpha3Code TEXT,
            population INTEGER,
            region_id INTEGER,
            capital TEXT,
            FOREIGN KEY (region_id) REFERENCES region(id)
        );"""

    CREATE_COUNTRY_TOP_LEVEL_DOMAINS = """
        CREATE TABLE IF NOT EXISTS country_top_level_domain_name (
            id INTEGER PRIMARY KEY,
            country_id INTEGER,
            name TEXT,
            FOREIGN KEY (country_id) REFERENCES country(id)
        );"""

    def run(self):
        self.cursor.execute(self.CREATE_REGIONS)
        self.cursor.execute(self.CREATE_COUNTRY)
        self.cursor.execute(self.CREATE_COUNTRY_TOP_LEVEL_DOMAINS)


if __name__ == "__main__":
    CreateDB().run()
