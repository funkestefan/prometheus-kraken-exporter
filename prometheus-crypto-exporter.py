#!/usr/bin/env python3

# prometheus-crypto-exporter,  prometheus exporter for cryptocurrency
# python3, requires prometheus_client (pip3 install prometheus_client)
# https://github.com/funkestefan/prometheus-crypto-exporter
#
## kraken
## a = ask array(<price>, <whole lot volume>, <lot volume>)
## b = bid array(<price>, <whole lot volume>, <lot volume>)
## c = last trade closed array(<price>, <lot volume>)
## v = volume array(<today>, <last 24 hours>)
## p = volume weighted average price array(<today>, <last 24 hours>)
## t = number of trades array(<today>, <last 24 hours>)
## l = low array(<today>, <last 24 hours>)
## h = high array(<today>, <last 24 hours>)
## o = today’s opening price

from prometheus_client import start_http_server, Summary, Gauge
import time
import json
import requests

debug = False

http_port = 9091
interval = 60

data_url = "https://api.kraken.com/0/public/Ticker?pair=dasheur,bateur,xdgeur,etheur,xmreur"

currencies = {
    "dash": "dasheur",
    "bat": "bateur",
    "doge": "xdgeur",
    "eth": "xethzeur",
    "xmr": "xxmrzeur"
}

headers = { 'User-Agent': 'prometheus-crypto-kraken-exporter/1.0' }

def get_json_from_provider():
    try:
        json_request = requests.get(data_url, headers=headers)
        json_request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        return(json_request.json())

def get_value(json_values, crypto_name):
    identifier = currencies[crypto_name]
    fixed_identifier = identifier.upper()   ## currency identifier in json from kraken is uppercase
    latest_value = json_values['result'][fixed_identifier]['c'][0]
    return(latest_value)

def process_request(t):
    json_values = get_json_from_provider()
    g_value_dash.set(get_value(json_values, "dash"))
    g_value_bat.set(get_value(json_values, "bat"))
    g_value_doge.set(get_value(json_values, "doge"))
    g_value_eth.set(get_value(json_values, "eth"))
    g_value_xmr.set(get_value(json_values, "xmr"))

    if debug:
        print("New run:")
        print("DEBUG -- DASH Value is set to " + get_value(json_values, "dash"))
        print("DEBUG -- BAT Value is set to " + get_value(json_values, "bat"))
        print("DEBUG -- Doge Value is set to " + get_value(json_values, "doge"))        
        print("DEBUG -- Ethereum Value is set to " + get_value(json_values, "eth"))
        print("DEBUG -- Monero Value is set to " + get_value(json_values, "xmr"))

    time.sleep(t)

g_value_dash = Gauge('dash_value_in_EUR', 'Dash Value in EUR from KRAKEN')
g_value_bat = Gauge('bat_value_in_EUR', 'BAT Value in EUR from KRAKEN')
g_value_doge = Gauge('doge_value_in_EUR', 'Doge Value in EUR from KRAKEN')
g_value_eth = Gauge('eth_value_in_EUR', 'Ethereum Value in EUR from KRAKEN')
g_value_xmr = Gauge('xmr_value_in_EUR', 'Monero Value in EUR from KRAKEN')

if __name__ == '__main__':
    # Start up the server to expose the metrics
    print("--- Starting the crypto exporter")
    start_http_server(http_port)

    # grab data and expose values
    while True:
        process_request(interval)