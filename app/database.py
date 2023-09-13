import pymysql
import pymysql.cursors
import sys
import requests
import csv
import io
import urllib3
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASS, GOOGLE_FILE_ID, GOOGLE_URL_CSV

"""Disable ssl warninngs"""
urllib3.disable_warnings()

def google_data():
    """Pull data from google file"""
    try:
        lines = []
        url = GOOGLE_URL_CSV.format(GOOGLE_FILE_ID)
        r = requests.get(url, verify=False)
        data = {}
        cols = []
        sio = io.StringIO( r.content.decode('utf-8'), newline=None)
        reader = csv.reader(sio, dialect=csv.excel)
        rownum = 0
        return reader
    except:
        print("Ошибка получения google данных")

def open_connection():
    """Connect to MySQL Database."""
    global conn
    try:
        conn = pymysql.connect(
               host=MYSQL_HOST,
               user=MYSQL_USER,
               password=MYSQL_PASS,
               db=MYSQL_DB,
               autocommit=True,
               )
    except pymysql.Error as error:
        print("Ошибка соединения с Mysql", error)
        #sys.exit()
    finally:
        print("Соединение с Mysql установлено")

def insert_main_data(sql_data, tableName):
    """Execute SQL query."""
    global conn
    try:
        google_data()
        open_connection()
        with conn.cursor() as cur:
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

            cur.execute(sql_drop)
            print('Table {} удалена'.format(tableName))

            cur.execute(sql_create_table)
            print('Table {} создана'.format(tableName))

            for i in sql_data:
                cur.execute(sql_insert_statement, i)

            cur.execute('SELECT COUNT(*) FROM {}'.format(tableName))
            rowCount = cur.fetchone()[0]

            print('Table {} обновлена'.format(tableName))
            print(tableName, 'Добавлено строк:', rowCount)

            conn.commit()
            cur.close()
    except pymysql.Error as error:
        print("Ошибка: ", error)
    finally:
        if conn:
           conn.close()
           conn = None
           print("Соединение с Mysql закрыто")

def view_data_db(tableName):
    """Execute SQL query."""
    global conn
    try:
        open_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM {}'.format(tableName))
            rowCount = cur.fetchall()
            for row in rowCount:
                print (row[0], row[1])

            conn.commit()
            cur.close()
    except pymysql.Error as error:
        print("Ошибка: ", error)
    finally:
        if conn:
           conn.close()
           conn = None
           print("Соединение с Mysql закрыто")

def view_all_content(tableName):
    """Execute SQL query."""
    global conn
    try:
        open_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM {}'.format(tableName))
            content = cur.fetchall()
            conn.commit()
            cur.close()
        return content
    except pymysql.Error as error:
        print("Ошибка: ", error)
    finally:
        if conn:
           conn.close()
           conn = None
           print("Соединение с Mysql закрыто")

def view_all_fields(tableName):
    """Execute SQL query."""
    global conn
    try:
        open_connection()
        with conn.cursor() as cur:
            cur.execute('SHOW FIELDS FROM {}'.format(tableName))
            fields = cur.fetchall()
            fields = [l[0] for l in fields]
            conn.commit()
            cur.close()
        return fields
    except pymysql.Error as error:
        print("Ошибка: ", error)
    finally:
        if conn:
           conn.close()
           conn = None
           print("Соединение с Mysql закрыто")


def select_content(tableName, search):
    """Execute SQL query."""
    global conn
    try:
        open_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {0} WHERE Name LIKE '%{1}%' OR Price LIKE '%{1}%'".format(tableName, search))
            content = cur.fetchall()
            conn.commit()
            cur.close()
        return content
    except pymysql.Error as error:
        print("Ошибка: ", error)
    finally:
        if conn:
           conn.close()
           conn = None
           print("Соединение с Mysql закрыто")


def count_data(tableName):
    """Execute SQL query."""
    global conn
    try:
        open_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM {}'.format(tableName))
            rowCount = cur.fetchone()[0]
            conn.commit()
            cur.close()
        return rowCount
    except pymysql.Error as error:
        print("Ошибка: ", error)
    finally:
        if conn:
           conn.close()
           conn = None
           print("Соединение с Mysql закрыто")
