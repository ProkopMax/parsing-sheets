import requests
import csv
import io
import urllib3
from settings import HEADERS_USER_AGENT, HEADERS_DNT, HEADERS_ACCEPT, HEADERS_ACCEPT_CHARSET, HEADERS_ACCEPT_ENCODING, HEADERS_ACCEPT_LANGUAGE, GOOGLE_FILE_ID, GOOGLE_URL_CSV

# Disable ssl warninngs
urllib3.disable_warnings()

# Pull data from google file
def get_data():
    #headers={"User-Agent": HEADERS_USER_AGENT, "DNT": HEADERS_DNT, "Accept": HEADERS_ACCEPT, "Accept-Charset": HEADERS_ACCEPT_CHARSET, "Accept-Encoding": HEADERS_ACCEPT_ENCODING, "Accept-Language": HEADERS_ACCEPT_LANGUAGE}
    lines = []
    url = GOOGLE_URL_CSV.format(GOOGLE_FILE_ID)
    r = requests.get(url, verify=False)
    data = {}
    cols = []
    sio = io.StringIO( r.content.decode('utf-8'), newline=None)
    reader = csv.reader(sio, dialect=csv.excel)
    rownum = 0
    return reader
