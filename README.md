# Amazon Price Tracker

Scrapes prices of products on Amazon and saves them to a local file for tracking. The prices can be updated and a notification is sent if the new price is lower.
## Usage

```console
usage: amazon-price [-h] [-u] [url ...]

Save prices of an item from Amazon and update if required

positional arguments:
  url           product URL to save

options:
  -h, --help    show this help message and exit
  -u, --update  update all saved prices
```
