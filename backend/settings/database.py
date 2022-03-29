import os
from mysql import connector
from mysql.connector import errorcode

# Connect to the MySQL database by using .yml and .env files

try:
    DB = connector.connect(host=os.environ.get("MYSQL_HOST"),
                           user=os.environ.get("MYSQL_USER"),
                           port=3306,
                           passwd=os.environ.get("MYSQL_PASSWORD"),
                           database=os.environ.get("MYSQL_DATABASE"))

    print("Connection to the database has been established!")

except connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(f"MySQL error: {e.errno} - User or password wrong")
    if e.errno == errorcode.ER_BAD_DB_ERROR:
        print(f"MySQL error:{e.errno} - Database does not exist")
    if e.errno == 2005:
        print(f"MySQL error:{e.errno} - Unkown server host")

    raise Exception(e)
