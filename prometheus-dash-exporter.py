### prometheus-dash-exporter,  prometheus exporter for the DASH cryptocurrency
### python3, requires prometheus_client (pip3 install prometheus_client)
### https://github.com/funkestefan/prometheus-dash-exporter

from prometheus_client import start_http_server, Summary, Gauge
import time
import json
import requests

debug = True

url = "https://www.cryptonator.com/api/ticker/dash-eur"
http_port = 9091
headers = { 'User-Agent': 'prometheus-dash-exporter/0.2' }

global_dash_json = {}

def get_dash_json(url):
    try:
        json_request = requests.get(url, headers=headers)
        json_request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        global global_dash_json
        global_dash_json = json_request.json()

def process_request(t):
    get_dash_json(url)
    master_fetcher(global_dash_json)
    time.sleep(t)

def get_dash_value(dash_json_in):
    latest_Value = dash_json_in['ticker']['price']
    return(latest_Value)

def get_dash_change(dash_json_in):
    latest_Change = dash_json_in['ticker']['change']
    return(latest_Change)

def get_dash_timestamp(dash_json_in):
    latest_Timestamp = dash_json_in['timestamp']
    return(latest_Timestamp)

def master_fetcher(dash_json_in):
    g_value.set(get_dash_value(dash_json_in))
    g_change.set(get_dash_change(dash_json_in))
    g_timestamp.set(get_dash_timestamp(dash_json_in))

    if debug:
        print("DEBUG -- Value is set to " + str(get_dash_value(dash_json_in)))
        print("DEBUG -- Change is set to " + str(get_dash_change(dash_json_in)))
        print("DEBUG -- Timestamp is set " + str(get_dash_timestamp(dash_json_in)))

g_value = Gauge('dash_value_in_EUR', 'Dash Value in EUR from https://www.cryptonator.com/api/ticker/dash-eur')
g_change = Gauge('dash_value_change', 'Dash Value changed')
g_timestamp = Gauge('dash_value_timestamp', 'Dash Value from THIS timestamp')

if __name__ == '__main__':
    # Start up the server to expose the metrics
    start_http_server(http_port)

    # grab data and expose values
    while True:
        process_request(60)