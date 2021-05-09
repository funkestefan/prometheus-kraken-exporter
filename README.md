# prometheus-kraken-exporter 

Prometheus exporter for cryptocurrency using the [Kraken](https://www.kraken.com/) API.

This is a simple server that scrapes values in EUR from the kraken.com API.
POC project to get me started with python3.

## Requirements
prometheus_client (pip3 install prometheus_client)

## Config values
- http_port = tcp/listener, default: 9091
- interval = refresh values every x seconds, default 60

## prometheus example config
```yaml
  - job_name: 'kraken'
    scrape_interval: 60s
    static_configs:
            - targets: ['localhost:9091']
```

## License

MIT License, Copyright (c) 2020
[Stefan Funke](https://itgaertner.net)
