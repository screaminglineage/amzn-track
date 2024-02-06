# Amazon Price Tracker

Scrapes prices of products on Amazon and saves them to a local file. The prices can later be compared to see if they have gone down

## Usage

### Linux 

```console
amazon-price.py [options]
```

### Windows

```console
py amazon-price.py [options]
```

## Help

```console
usage: amazon-price [-h] [-u] [url ...]

Save prices of an item from Amazon and update if required

positional arguments:
  url           product URL to save

options:
  -h, --help    show this help message and exit
  -u, --update  update all saved prices
```
