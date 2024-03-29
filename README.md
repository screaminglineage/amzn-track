# amzn-track

Scrapes prices of products on Amazon and saves them to a local file for tracking. The prices can be updated and a notification is sent if the new price is lower. 

## Requirements
- [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/) 
- [`libnotify`](https://gitlab.gnome.org/GNOME/libnotify) (Required for `notify-send`)

## Usage

```console
usage: amzn-track.py [-h] [-u] [url ...]

Save prices of an item from Amazon and update if required

positional arguments:
  url           product URL to save

options:
  -h, --help    show this help message and exit
  -u, --update  update all saved prices
  -l, --list    list all saved items
```

