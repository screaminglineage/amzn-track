#!/usr/bin/env python

import requests
import subprocess
import argparse
import json
from bs4 import BeautifulSoup

# Top level domain can be changed below
TOP_LEVEL_DOMAIN = "in"
AMAZON_PREFIX = f"https://www.amazon.{TOP_LEVEL_DOMAIN}"

# Available parsers: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
# 'html.parser' is a built-in python alternative to 'lxml' albeit slightly slower
HTML_PARSER = "lxml"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.bbc.com/news/entertainment-arts-64759120",
}


def get_html(url: str, headers=headers) -> str:
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error: Failed to get http response")
        return ""

    return response.text


def get_name(html_doc: str, parser=HTML_PARSER):
    json_index = html_doc.find("jQuery.parseJSON('")
    if not json_index:
        print("Error: Could not get name")
        return ""
    start = html_doc.find("{", json_index)
    end = html_doc.find("');", start)

    try:
        json_data = json.loads(html_doc[start:end])
    except json.decoder.JSONDecodeError:
        print("Error: Could not get name")
        return ""

    if not json_data.get("title"):
        print("Error: Could not get name")
        return ""

    return BeautifulSoup(json_data["title"], parser).text


def price_get(html_doc: str, parser=HTML_PARSER):
    soup = BeautifulSoup(html_doc, parser)

    # handle out of stock
    if soup.find("div", id="outOfStock"):
        return -1

    # couldnt get price
    price_span = soup.find("span", class_="a-price-whole")
    if not price_span:
        return None

    return int(price_span.text.replace(",", "").removesuffix("."))


def url_to_id(url) -> str:
    if not url.startswith(AMAZON_PREFIX):
        return ""

    product_id = url.split("/dp/")[-1]
    if not product_id:
        return ""

    return product_id.removesuffix("/")


def products_add(urls: list[str], filepath="amazon-prices.json"):
    products = []
    for url in urls:
        prod_id = url_to_id(url)
        if not prod_id:
            print(f"Invalid URL/ID: `{url}`")
            continue

        html_doc = get_html(url)
        if not html_doc:
            print(f"Failed to get HTML for: `{url}`")
            continue

        # parse price
        price = price_get(html_doc)
        if not price:
            print(f"Failed to get price for: `{url}`")
            continue
        elif price == -1:
            print(f"Item currently out of stock: `{url}`")

        # parse name
        name = get_name(html_doc)
        if not name:
            print(f"Failed to get name for `{url}`. Falling back to title in URL.")
            name = url.removeprefix(f"{AMAZON_PREFIX}/").split("/")[0]

        print(f" - Adding {name}")
        products.append({"id": prod_id, "name": name, "price": price})

    with open(filepath, "w") as file:
        json.dump(products, file)


def products_get(filepath="amazon-prices.json") -> list[dict]:
    with open(filepath, "r") as file:
        return json.load(file)


def products_update(filepath="amazon-prices.json"):
    products = products_get(filepath)

    for product in products:
        url = f"{AMAZON_PREFIX}/dp/{product['id']}"
        new_price = price_get(get_html(url))
        if new_price != -1 and new_price < product["price"]:
            print(f"New low for item: {product['name']}")
            subprocess.run(
                [
                    "notify-send",
                    "--app-name",
                    "amazon-price",
                    f"New Low for Item: {new_price}",
                    product["name"],
                ]
            )
        product["price"] = new_price

    with open(filepath, "w") as file:
        json.dump(products, file)


# Argparse Options
def cli_parser():
    parser = argparse.ArgumentParser(
        description="Save prices of an item from Amazon and update if required"
    )

    # Gets Command Line Arguments
    parser.add_argument(
        "urls", type=str, metavar="url", nargs="*", help="product URL to save"
    )

    parser.add_argument(
        "-u", "--update", action="store_true", help="update all saved prices"
    )
    return parser


def main():
    parser = cli_parser()
    args = parser.parse_args()

    if not (args.urls or args.update):
        parser.print_help()
        return

    if args.urls:
        print("Adding Items")
        products_add(args.urls)
        print("Items Added")

    if args.update:
        products_update()


if __name__ == "__main__":
    main()