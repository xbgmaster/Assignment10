import random, requests, os
from dotenv import load_dotenv
from datetime import datetime
from django.shortcuts import render
from .forms import ContinentForm
from pymongo import MongoClient
 
load_dotenv()
 
MONGO_URI = 'mongodb://3.236.244.253:27017'
client = MongoClient(MONGO_URI)
db = client.geodata
 
OPENWEATHERMAP_API_KEY = 'e2c15f906c20e4c38967f552199fcf6c'
 
def continent_view(request):
    if request.method == 'POST':
        form = ContinentForm(request.POST)
        if form.is_valid():
            continent = form.cleaned_data['continent']
            response = requests.get(f"https://restcountries.com/v3.1/region/{continent}")
            countries = random.sample(response.json(), 5)
            results = []
            for c in countries:
                capital = c.get("capital", [""])[0]
                name = c.get("name", {}).get("common", "")
                pop = c.get("population", 0)
                try:
                    weather = requests.get(
                        f"https://api.openweathermap.org/data/2.5/weather",
                        params={"q": capital, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"}
                    ).json()

                    if weather.get("cod") == 200:
                        temp = weather['main']['temp']
                        desc = weather['weather'][0]['description']
                    else:
                        temp, desc = None, weather.get("message", "Not found")
                except:
                    temp, desc = None, "Not found"
 
                results.append({
                    "country": name,
                    "capital": capital,
                    "population": pop,
                    "temperature_celsius": temp,
                    "weather_description": desc
                })
 
            record = {
                "continent": continent,
                "search_timestamp": datetime.utcnow().isoformat(),
                "results": results
            }
            db.searches.insert_one(record)
            return render(request, "search_results.html", {"results": results})
    else:
        form = ContinentForm()
    return render(request, "continent_form.html", {"form": form})
 
def history_view(request):
    history = list(db.searches.find().sort("search_timestamp", -1))
    return render(request, "history.html", {"history": history})
