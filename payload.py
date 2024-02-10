from faker import Faker
import random
import requests
import json
from datetime import datetime
from time import sleep
import requests
from pprint import pprint
from time import perf_counter

fake = Faker()


# Function to generate a fake product
def generate_fake_product():
    categories = ['Clothing', 'Electronics', 'Home & Garden', 'Books', 'Toys & Games']
    product = {
        "item_id": fake.random_int(min=1, max=1000),
        "name": fake.word(),
        "price": round(random.uniform(5.0, 200.0), 2),
        "category": random.choice(categories)
    }
    return product


# Function to generate a random purchase payload
def generate_purchase_payload():
    number_of_items = random.randint(1, 3)
    purchased_items = [generate_fake_product() for _ in range(number_of_items)]
    total_price = sum(item["price"] for item in purchased_items)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23]

    markets = ["Nokora", "Spari", "Zgapari", "Ori Nabiji", "Ioli", "Smarti", "Magniti", "Libre", "Gvirila", "Fresko", "Karfuri", "Agrohabi", "Evroprodukti", "Madagoni"]
    cities = ["Tbilisi", "Khashuri", "Berlin", "Zestaponi", "Wasington_DC"]

    return {
        "report": {
            "email": fake.email(),
            "sms": fake.phone_number()
        },
        "timestamp": now,
        "store_name": random.choice(markets),
        "user_location": random.choice(cities),
        "customer_id": fake.random_int(min=1000, max=5000),
        "items": purchased_items,
        "total_price": total_price
    }


# Function to send the payload to an API
def send_payload(api_url, payload):
    response = requests.post(api_url, json=payload)
    return response.status_code, response.text


# Main function to generate and send multiple payloads
def main(api_url, num_payloads):
    for _ in range(num_payloads):
        payload = generate_purchase_payload()
        payload = json.dumps(payload, indent=4)

       
        # Sending the POST request
        response = requests.post(url, data=payload)

        #Checking the response status code
        
        if response.status_code == 200:
            print("POST request was successful!")
            pprint(response.text)
        else:
            print("POST request failed with status code:", response.status_code)
        
        sleep(1)
        




number_of_payloads = 1000  # Number of payloads to generate and send

url = 'http://[::1]:8001/orders'
t = perf_counter()

main(url, number_of_payloads)

print(perf_counter() - t)