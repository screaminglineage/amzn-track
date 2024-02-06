#!/bin/bash
# Original version of the script. Incomplete and doesnt really support updating the prices.
# Tracks the price of an Amazon product and notifies when its the lowest

SAVE_PATH="/tmp/amazon-price/"
USER_AGENT="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"

# Shows information about this command
help() {
    echo "usage: amazon-price [-h]"
    echo ""
    echo "Tracks the price of an Amazon product and notifies when its the lowest"
    echo ""
    echo "positional arguments:"
    echo "  link      link to Amazon product page"
    echo ""
    echo "options:"
    echo "  -h, --help  show this help message and exit"
}

# Shows help and exits if the argument is -h
if [[ $1 = -h ]] || [[ $1 = --help ]]; then
    help
    exit 0
fi

# Extract price from given link
extract_price() {
    link="$1"

    curl "$link" --header "$USER_AGENT" --compressed --output tmp.html
    price=$(cat tmp.html \
        | pup 'span[class=a-price-whole] text{}' \
        | head -1
    )
    price=$(tr -d ',' <<< "$price") 

    if [[ "$price" ]]; then
        echo "$price" 
    else
        echo "Error! Couldnt Get Price"
    fi
}

# Compare saved prices and notify when new lowest reached
check_smallest() {
    filepath="$1"
    num="$2"
    new_min=true
    while read -r line; do
        if ((num >= line)); then
            new_min=false
            break
        fi
    done < "$filepath"
    "$new_min" && echo "new lowest"
}

# Save passed in price to the file
# Creates the folder and files if not found
save_price() {
    price="$1"
    product_id="$2"
    filepath="${SAVE_PATH}/${product_id}"
    
    [[ ! -e "$SAVE_PATH" ]] && mkdir -p "$SAVE_PATH"

    if [[ -e "$filepath" ]]; then
        check_smallest "$filepath" "$price"
        echo "$price" >> "$filepath"
    else
        echo "$price" > "$filepath"
    fi
}

main() {
    url="$1"

    # Grabbing product id
    product_id=$(grep -oE "/dp/[0-9a-zA-Z]+" <<< "$url")
    product_id="${product_id#/dp/}"
    product_id="${product_id%/}"
    
    echo "$product_id"
    price=$(extract_price "$1")
    echo "$price"   # Echoes either the price or an error
    [[ "$price" == "Error! Couldnt Get Price" ]] && exit 1
    
    save_price "$price" "$product_id"
}

main "$1"
main "https://www.amazon.in/HP-x765w-32GB-USB-Drive/dp/B01L901UIU?th=1"
main "https://www.amazon.in/Oppo-Bluetooth-Truly-Wireless-Earbuds/dp/B096YBVZP3/ref=sr_1_2?keywords=oppo+enco+buds&qid=1681405983&sr=8-2"


