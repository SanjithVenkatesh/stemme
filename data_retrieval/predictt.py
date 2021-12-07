import requests
import json
import mysql.connector
from mysql.connector import errorcode

database_config =  {
  'user': 'sanjith',
  'password': 'sanjith',
  'host': '127.0.0.1',
  'database': 'predictt',
  'raise_on_warnings': True
}

add_market_query = "INSERT INTO markets values ('%s', '%s', '%s', '%s', '%s', '%s', '%s');"
add_contract_query = "INSERT INTO contracts VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "

check_market_query = "SELECT * from markets where ID = '%s';"
check_contracts_query = "SELECT * from contracts where ID = '%s';"


update_contracts_query_starter = "UPDATE contracts set "

"""
Import all of the data into the local MySQL database
Params: JSON object containing all information
Returns: None
"""
def import_data(market_info):
    try:
        cnx = mysql.connector.connect(**database_config)
        cur = cnx.cursor()
        for market in market_info["markets"]:
            market_id = market["id"]
            cur.execute(check_market_query, (market_id,))
            market_exists = True if cur.rowcount > 0 else False
            if market_exists:
                # Update row
                update_market_query_starter = "UPDATE markets set "
                for key, value in market.items():
                    if key != "id":
                        update_market_query_starter += str(key) + " \'" + str(value) + "\', "
                update_market_query = update_market_query_starter[:-1]
                update_market_query += "WHERE id = " + str(market_id) + ";"
                cur.execute(update_market_query)
            else:
                # Insert new row
                new_info = (market_id, market["name"], market["shortName"], market["image"], market["url"], market["timeStamp"], market["status"])
                cur.execute(add_market_query, new_info)
            for contract in market["contracts"]:
                cur.execute(check_contracts_query, contract["id"])
                contract_exists = True if cur.rowcount > 0 else False
                if contract_exists:
                    # Update the contract information
                    pass
                else:
                    pass
        """
        Effectively do the following for each market:
        1. Check if the market is already in the table. This should be done by running a select on the id and seeing anything is returned.
        2. If market is already there, simply do an update on all of the values
        3. If market is not there, run the insert query and add it there
        4. Perform the same operations on the contracts.
        """
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

"""
Extract all of the data from the predictt website and return a json object with the information
Params: None
Returns: JSON object with all market information
"""
def extract_data():
    data = requests.get("https://www.predictit.org/api/marketdata/all/")
    j = json.loads(data.text)
    first_market = j["markets"][0]
    print(json.dumps(first_market, indent=4, sort_keys=True))
    return j

if __name__ == "__main__":
    import_data(market_info=None)