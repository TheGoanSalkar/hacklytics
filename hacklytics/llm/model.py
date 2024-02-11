import requests

API_URL = "https://api-inference.huggingface.co/models/KrishnaSriIpsitMantri/BlipFineTuneHacklytics2024"
headers = {"Authorization": "Bearer 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"}

def run_inference(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    print(response.json())
    return response.json()[0]['generated_text']