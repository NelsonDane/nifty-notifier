# Nifty Notifier
# A script to monitor Nifty Gateway for new drops

import requests
from datetime import datetime
import os
from time import sleep
from dotenv import load_dotenv

# Global Variables
URL = "https://api.niftygateway.com"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " \
                "AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/90.0.4430.212 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT,
    "authority": "api.niftygateway.com",
    "accept": "application/json, text/plain, */*",
    "origin": "https://niftygateway.com",
    "referer": "https://niftygateway.com/",
}
ARTIST_ID = "1158839" # Starbucks Corporation

load_dotenv()
if os.getenv("DISCORD_WEBHOOK") is None:
    print("No Discord Webhook found in .env")
    exit(1)
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def make_request(url, endpoint):
    try:
        response = requests.get(url + endpoint, headers=HEADERS)
        return response
    except Exception as e:
        print(e)
        return None


def get_new_collections():
    endpoint = f"/market/all-data/?page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%22exclude_types%22:[%22withdrawals%22],%22artist_filter%22:{ARTIST_ID}%7D"
    response = make_request(URL, endpoint)
    if response is None:
        return None
    else:
        response = response.json()["data"]["results"]
        return response


def print_nifty(collection):
    nifty_type = collection["Type"]
    print("=====================================")
    print("Found new Nifty!")
    print(f"Type: {nifty_type}")
    if nifty_type != "nifty_transfer":
        print(f"Price: ${round(int(collection['OfferAmountInCents'])/100, 2)}")
    print(f"Link: https://niftygateway.com/marketplace/collection/{collection['UnmintedNiftyObj']['niftyContractAddress']}/1")
    print(f"Image: {collection['UnmintedNiftyObj']['niftyDisplayImage']}")
    print("=====================================")


def notify_discord(collection):
    nifty_type = collection["Type"]
    if nifty_type == "nifty_transfer":
        return
    else:
        price = round(int(collection['OfferAmountInCents'])/100, 2)
        image = collection['UnmintedNiftyObj']['niftyDisplayImage']
        link = f"https://niftygateway.com/marketplace/collection/{collection['UnmintedNiftyObj']['niftyContractAddress']}/1"
        data = {
            "content": f"New Nifty! {nifty_type} for ${price}!\n{link}",
            "embeds": [
                {
                    "image": {
                        "url": image
                    }
                }
            ]
        }
        response = requests.post(DISCORD_WEBHOOK, json=data)


def print_and_notify(collection):
    print_nifty(collection)
    notify_discord(collection)


if __name__ == "__main__":
    try:
        print("Starting Nifty Notifier...")
        first_run = True
        previous_collections = []
        while True:
            collections = get_new_collections()
            if collections is None:
                print("Error getting collections")
                continue
            if first_run:
                print(f"Found {len(collections)} collections")
                previous_collections = collections
                first_run = False
                continue
            for col in collections:
                if col not in previous_collections:
                    print_and_notify(col)
            previous_collections = collections
            print(f"Nothing new found at {datetime.now()}")
            sleep(5)
    except KeyboardInterrupt:
        print("Exiting Nifty Notifier...")
        exit(0)
