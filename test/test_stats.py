from math import ceil
from dotenv import load_dotenv
from utils.entities_extraction import entities_extraction
import utils.statistics_analysis as statistics_analysis
import os
import sys
import unittest
import sqlite3
sys.path.append(os.path.join(os.getcwd()))

load_dotenv()

STATS_DB_PATH = os.getenv('STATS_DB_PATH')
stats_tables = statistics_analysis.stats_tables


class StatsTestCase(unittest.TestCase):

    def test_existing_stats_file(self):
        assert statistics_analysis.database_creation() == True

    def test_tables_exists(self):
        statistics_analysis.tables_creation()
        conn = sqlite3.connect(STATS_DB_PATH)
        c = conn.cursor()
        for i in stats_tables.keys():
            #   Get the number of tables with this name
            c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(i))
            assert c.fetchone()[0]==1
                        
        #   Close the connection
        conn.close()
 
    def test_stats_recording(self):
        person = {'full name': 'Joe Biden', 'country of citizenship': 'United States of America', 'occupation': 'politician', 'date of birth': '11/20/1942', 'spouse': 'Neilia Hunter', 'given name': 'Joe', 'place of birth': "St. Mary's Hospital", 'child': 'Beau Biden', 'age': 79}
        

        def load_data():
            """
            Load stats from the database
            """
            conn = sqlite3.connect(STATS_DB_PATH)
            c = conn.cursor()

            data = {}
            for i, j in stats_tables.items():
                if i != "age":
                    c.execute("SELECT occurence FROM {} WHERE value='{}'".format(i, person[j]))
                    res = c.fetchone()
                    res = 0 if res is None else res[0]
                else:
                    c.execute("SELECT value, occurence FROM {}".format(i, person[j]))
                    r_ = c.fetchall()
                    res = 0
                    k = 0
                    if r_ is not None:
                        for j in r_:
                            res += j[0] * j[1]
                            k += j[1]
                        res = res / k
                
                data[i] = res
            conn.close()
            return data


        #   Load stats before request
        old_value = load_data()

        #   Recording of stats
        statistics_analysis.stats_recording(person)

        #   Load stats after request
        new_value = load_data()

        for i in stats_tables:
            if i != "age":
                assert new_value[i] == old_value[i] + 1
            else:
                assert new_value[i] != old_value[i]

    def test_stats_reception(self):
        stats = statistics_analysis.stats_computation()
        expected_result = {
            "persons" : ["Joe Biden"],
            "country_citizenship" : ["United States of America"],
            "occupation" : ["politician"],
            "age" : [79]
        }
        assert stats is not None
        assert type(stats) == dict
        assert set(stats_tables.keys()) == stats.keys()
        for i in stats_tables.keys():
            assert type(stats[i]) == list
            if i != "age":
                assert type(stats[i][0]) == str
            else:
                assert type(stats[i][0]) == int






if __name__ == "__main__":
    unittest.main()

