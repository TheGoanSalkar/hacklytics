import requests
from time import sleep

API_URL = "https://api-inference.huggingface.co/models/KrishnaSriIpsitMantri/BlipFineTuneHacklytics2024"
headers = {"Authorization": "Bearer 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"}

def run_inference(filename):
    with open(filename, "rb") as f:
        data = f.read()
    done = False
    tries = 0
    while(not done or tries < 10):
        try:
            response = requests.post(API_URL, headers=headers, data=data)
            return response.json()[0]['generated_text']
        except:
            tries += 1
            sleep(1)
    response = requests.post(API_URL, headers=headers, data=data)
    print(response.json())
    return response.json()[0]['generated_text']