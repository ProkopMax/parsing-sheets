import requests
import csv
import io
import urllib3
import mysql.connector
from mysql.connector import Error
from os import environ

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Disable ssl warninngs
urllib3.disable_warnings()

# Test connection to mysql database 
try:
    connection = mysql.connector.connect (host= "byte-mysql", user = environ.get('MYSQL_USER'), password = environ.get('MYSQL_PASSWORD'), database = environ.get('MYSQL_DATABASE'))
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print(bcolors.OKGREEN + "Your connected to database: ", record)

except Error as e:
    print(bcolors.FAIL + "Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

# Pull data from google doc
headers={}
headers["User-Agent"]= "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0 Chrome/43.0.2357.134 Safari/537.36"
headers["DNT"]= "1"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
headers["Accept-Charset"] = "utf-8"
headers["Accept-Encoding"] = "deflate"
headers["Accept-Language"]= "ru;q=0.7"
lines = []
file_id="1psvvO5eftQYu4ktZ9g8pc70Owy_NPTPGdeuXvt363_0"
url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(file_id)
r = requests.get(url, verify=False)
data = {}
cols = []
sio = io.StringIO( r.content.decode('utf-8'), newline=None)
reader = csv.reader(sio, dialect=csv.excel)
rownum = 0

# for row in reader:
#     print(bcolors.OKBLUE + bcolors.UNDERLINE + row[0] + bcolors.ENDC, bcolors.OKCYAN + bcolors.BOLD+ row[1] + bcolors.ENDC)

# Create table byte2 and insert data from google doc
def WriteToMySQLTable(sql_data, tableName):
    try:
        connection = mysql.connector.connect (host= "byte-mysql", user = environ.get('MYSQL_USER'), password = environ.get('MYSQL_PASSWORD'), database = environ.get('MYSQL_DATABASE'))

        sql_drop = " DROP TABLE IF EXISTS {} ".format(tableName)

        sql_create_table = """CREATE TABLE {}( 
            id bigint(20) NOT NULL AUTO_INCREMENT,
            Name CHAR(255) NOT NULL CHECK (Name <> ''),
            Price int(9) NOT NULL CHECK (Price > '32'),            
            PRIMARY KEY (id)
            )""".format(tableName)
 
        sql_insert_statement = """INSERT IGNORE INTO {}( 
            Name,
            Price )           
            VALUES ( %s,%s)""".format(tableName)
        
        cursor = connection.cursor()

        cursor.execute(sql_drop)
        print(bcolors.OKCYAN + 'Table {} has been dropped'.format(tableName) + bcolors.ENDC)

        cursor.execute(sql_create_table)
        print(bcolors.OKCYAN + 'Table {} has been created'.format(tableName) + bcolors.ENDC)

        for i in sql_data:
            cursor.execute(sql_insert_statement, i)
        connection.commit()
        print(bcolors.OKCYAN + 'Table {} successfully updated'.format(tableName) + bcolors.ENDC)

    except mysql.connector.Error as error :
        connection.rollback()
        print(bcolors.FAIL + "Error: {}. Table {} not updated!".format(error, tableName))
    
    finally:
        cursor.execute('SELECT COUNT(*) FROM {}'.format(tableName))
        rowCount = cursor.fetchone()[0]
        print(tableName, 'row count:', rowCount)

        if connection.is_connected():
            cursor.close()
            connection.close()
            print(bcolors.UNDERLINE + "MySQL connection is closed.")

WriteToMySQLTable(reader, 'byte2')

# Update byte3 only change data from tabels byte1 and byte2
def ChangeToMySQLTable(tableName):
    try:
        connection = mysql.connector.connect (host= "byte-mysql", user = environ.get('MYSQL_USER'), password = environ.get('MYSQL_PASSWORD'), database = environ.get('MYSQL_DATABASE'))

        # sql_drop = " DROP TABLE IF EXISTS {} ".format(tableName)

        # sql_create_table = """CREATE TABLE {}( 
        #     id bigint(20) NOT NULL AUTO_INCREMENT,
        #     Name CHAR(255) NOT NULL CHECK (Name <> ''),
        #     Price int(9) NOT NULL CHECK (Price > '32'),            
        #     PRIMARY KEY (id)
        #     )""".format(tableName)
 
        # sql_insert_statement = """INSERT INTO {}( 
        #     Name,
        #     Price )           
        #     VALUES ( %s,%s )""".format(tableName)
        sql_replace_statement = """REPLACE INTO {}( 
             Name,
             Price )           
             VALUES ( %s,%s )""".format(tableName)

        
        sql_select_change = "SELECT Name,Price FROM ( SELECT Name,Price FROM byte1 UNION ALL SELECT Name,Price FROM byte2 ) tbl GROUP BY Name,Price HAVING COUNT(*) = 1 ORDER BY Price "

        cursor = connection.cursor()

        # cursor.execute(sql_drop)
        # print(bcolors.OKCYAN + 'Table {} has been dropped'.format(tableName) + bcolors.ENDC)

        # cursor.execute(sql_create_table)
        # print(bcolors.OKCYAN + 'Table {} has been created'.format(tableName) + bcolors.ENDC)

        cursor.execute(sql_select_change)
        records = cursor.fetchall()
        for record in records:
            cursor.execute(sql_replace_statement, record)             
                                
        connection.commit()
        print(bcolors.OKCYAN + 'Table {} successfully updated'.format(tableName) + bcolors.ENDC)
        
    except mysql.connector.Error as error :
        connection.rollback()
        print(bcolors.FAIL + "Error: {}. Table {} not updated!".format(error, tableName))
    
    finally:
        cursor.execute('SELECT COUNT(*) FROM {}'.format(tableName))
        rowCount = cursor.fetchone()[0]
        print(tableName, 'row count:', rowCount)

        if connection.is_connected():
            cursor.close()
            connection.close()
            print(bcolors.UNDERLINE + "MySQL connection is closed.")

ChangeToMySQLTable('byte3')

def SyncMySQLTable(tableName):
    try:
        connection = mysql.connector.connect (host= "byte-mysql", user = environ.get('MYSQL_USER'), password = environ.get('MYSQL_PASSWORD'), database = environ.get('MYSQL_DATABASE'))

        sql_drop = " DROP TABLE IF EXISTS {} ".format(tableName)

        sql_create_table = """CREATE TABLE {}( 
            id bigint(20) NOT NULL AUTO_INCREMENT,
            Name CHAR(255) NOT NULL CHECK (Name <> ''),
            Price int(9) NOT NULL CHECK (Price > '32'),            
            PRIMARY KEY (id)
            )""".format(tableName)
 
        sql_insert_statement = """INSERT INTO {} SELECT * FROM byte2""".format(tableName)

        # sql_replace_statement = """REPLACE INTO {}( 
        #      Name,
        #      Price )           
        #      VALUES ( %s,%s )""".format(tableName)

        
        # sql_select_change = "SELECT COUNT(*) FROM ( SELECT Name,Price FROM byte1 UNION ALL SELECT Name,Price FROM byte2 ) tbl GROUP BY Name,Price HAVING COUNT(*) = 1"

        cursor = connection.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM ( SELECT Name,Price FROM byte1 UNION ALL SELECT Name,Price FROM byte2 ) tbl GROUP BY Name,Price HAVING COUNT(*) = 1')
        records = cursor.fetchall()
        print('records:', records)
        # if records != 0:
        #     cursor.execute(sql_drop)
        #     print(bcolors.OKCYAN + 'Table {} has been dropped'.format(tableName) + bcolors.ENDC)

        #     cursor.execute(sql_create_table)
        #     print(bcolors.OKCYAN + 'Table {} has been created'.format(tableName) + bcolors.ENDC)
 
        #     cursor.execute(sql_insert_statement)
        
        # records = cursor.fetchall()
        # for record in records:
        #     cursor.execute(sql_replace_statement, record)             
                                
        connection.commit()
        print(bcolors.OKCYAN + 'Table {} successfully updated'.format(tableName) + bcolors.ENDC)           

    except mysql.connector.Error as error :
        connection.rollback()
        print(bcolors.FAIL + "Error: {}. Table {} not updated!".format(error, tableName))
    
    finally:
        cursor.execute('SELECT COUNT(*) FROM {}'.format(tableName))
        rowCount = cursor.fetchone()[0]
        print(tableName, 'row count:', rowCount)

        if connection.is_connected():
            cursor.close()
            connection.close()
            print(bcolors.UNDERLINE + "MySQL connection is closed.")

SyncMySQLTable('byte1')