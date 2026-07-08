import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("FIREWORKS_API_KEY")
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

url = "https://api.fireworks.ai/inference/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_moisture_status(ndwi):
    if ndwi < -0.1:
        return "SEVERELY DRY - irrigate immediately"
    elif ndwi < 0.1:
        return "DRY - irrigation needed soon"
    elif ndwi < 0.3:
        return "MODERATE - monitor closely"
    else:
        return "ADEQUATE - no immediate action needed"

def get_weather(district):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={district},Haryana,IN&appid={weather_api_key}&units=metric"
    response = requests.get(weather_url)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        rain = "rain expected" if 'rain' in data else "no rain expected"
        return f"Temperature: {temp}°C, Humidity: {humidity}%, {rain}"
    else:
        return "Weather data unavailable"

def get_crop_advisory(crop, district, ndvi, ndwi, farmer_query):
    prompt = f"""You are an expert agricultural advisor for Indian farmers.

Farmer details:
- Crop: {crop}
- District: {district}, Haryana
- Satellite NDVI value: {ndvi} (0-1 scale, below 0.3 means stressed crop)
- Satellite NDWI value: {ndwi}
- Moisture status: {get_moisture_status(ndwi)}
- Current weather: {get_weather(district)}
- Farmer's question: {farmer_query}

Respond with ONLY the final 3 bullet points below. Do NOT show your reasoning, analysis, or thought process. Do NOT include any text before or after the 3 bullets.

Format exactly like this:
1. Problem: [one sentence]
2. Immediate action: [one sentence]
3. Watch for (next 7 days): [one sentence]"""

    payload = {
        "model": "accounts/fireworks/models/glm-5p2",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1200
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result

# Test case 1: Water-stressed wheat
print("### TEST 1: Water-stressed wheat ###")
result1 = get_crop_advisory(
    crop="Wheat",
    district="Karnal",
    ndvi=0.3,
    ndwi=-0.2,
    farmer_query="My wheat leaves are turning yellow"
)
print(result1['choices'][0]['message']['content'])
print("\n")

# Test case 2: Healthy rice, farmer just checking in
print("### TEST 2: Healthy rice crop ###")
result2 = get_crop_advisory(
    crop="Rice",
    district="Kaithal",
    ndvi=0.7,
    ndwi=0.4,
    farmer_query="Is my crop okay? When should I irrigate next?"
)
print(result2['choices'][0]['message']['content'])
print("\n")

# Test case 3: Mustard with unknown pest issue
print("### TEST 3: Mustard with pest concern ###")
result3 = get_crop_advisory(
    crop="Mustard",
    district="Jind",
    ndvi=0.45,
    ndwi=0.1,
    farmer_query="I see small insects on my mustard leaves, what should I do?"
)
print(result3['choices'][0]['message']['content'])