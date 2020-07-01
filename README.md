# prometheus-dash-exporter 

Prometheus exporter for the DASH cryptocurrency using https://www.cryptonator.com/

This is a simple server that scrapes DASH value in EUR from the cryptonator.com API.
POC project to get me started with python3.

## Requirements
prometheus_client (pip3 install prometheus_client)

## Config values
http_port = tcp/listener, default: 9091

### Exported metrics
- dash_value_in_EUR
- dash_value_change
- dash_value_timestamp

## License

MIT License, Copyright (c) 2020
[Stefan Funke](https://itgaertner.net)
