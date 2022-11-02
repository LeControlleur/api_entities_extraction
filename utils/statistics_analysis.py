from datetime import datetime
from datetime import date
import os
import json
import sqlite3
from dotenv import load_dotenv

load_dotenv()
STATS_DB_PATH = os.getenv('STATS_DB_PATH')

#   For support, 
stats_tables = {
    "persons" : "full name",
    "country_citizenship" : "country of citizenship",
    "occupation" : "occupation",
    "age" : "age"
}

def database_creation():
    if not os.path.exists(STATS_DB_PATH):
        sqlite3.connect(STATS_DB_PATH)
    return True


def tables_creation():
    conn = sqlite3.connect(STATS_DB_PATH)
    c = conn.cursor()
    #   Creation of each table based on the stats_tables list
    for i in stats_tables.keys():
        if i != "age":
            c.execute("""
                CREATE TABLE IF NOT EXISTS {}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value TEXT NOT NULL,
                    occurence INTEGER NOT NULL DEFAULT 1
                )
            """.format(i)
            )
        else :
            c.execute("""
                CREATE TABLE IF NOT EXISTS {}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value INT NOT NULL,
                    occurence INTEGER NOT NULL DEFAULT 1
                )
            """.format(i)
            )
    conn.commit()
    conn.close()
    
def age_calculator(birth_date : str, death_date : str) -> int:
    """
    Return the age of a person as int using the dates or birth and now is this person is still alive or the date of death if the person is dead.
    """
    
    end_date = date.today() if death_date == "" else datetime.strptime(death_date, "%m/%d/%Y")
    birth_date = datetime.strptime(birth_date, "%m/%d/%Y")
    age = end_date.year - birth_date.year - ((end_date.month, end_date.day) < (birth_date.month, birth_date.day))

    return age

def stats_recording(dataToRecord : dict):
    """
    Records the stats into the stats JSON file
    """
    conn = sqlite3.connect(STATS_DB_PATH)
    c = conn.cursor()
    print(dataToRecord)
    #   Creation of each table based on the stats_tables list
    for i, j in stats_tables.items():
        try :
            req = """
            SELECT occurence FROM {0} WHERE value = "{1}"
            """.format(i, dataToRecord[j])
            c.execute(req)
            res = c.fetchone()
            nbre_occ = 1
            if res is not None and len(res) > 0:
                nbre_occ += res[0] 
                req = """
                UPDATE {0}
                SET occurence = {1} WHERE value = """.format(i, nbre_occ)
                req += """ "{}" """.format(dataToRecord[j]) if i != "age" else """ {} """.format(dataToRecord[j])
            else:
                req = " INSERT INTO {0} (value, occurence)".format(i)
                req += """ VALUES ( "{0}", {1} ) """.format(dataToRecord[j], nbre_occ) if i != "age" else """ VALUES ( {0}, {1} ) """.format(dataToRecord[j], nbre_occ)

            print(req)
            c.execute(req)

        except KeyError:
            print("Error")
            continue

    conn.commit()
    conn.close()

def stats_computation():
    """
    Function use for computing stats
    """
    conn = sqlite3.connect(STATS_DB_PATH)
    c = conn.cursor()

    stats = {}
    for i in stats_tables.keys():
        req = "SELECT value, occurence FROM {0} ORDER BY occurence DESC LIMIT 5".format(i)
        c.execute(req)
        res = c.fetchall()
        stats[i] = []
        if res is not None:
            stats[i] = [k[0] for k in res]

    return stats

