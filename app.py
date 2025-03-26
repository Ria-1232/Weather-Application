from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

# OpenWeatherMap API Key
API_KEY = "YOUR_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form["city"]
        weather_data = get_weather_data(city)
        if weather_data:
            return render_template("index.html", weather=weather_data, city=city)
        else:
            return render_template("index.html", error="City not found or invalid.")
    return render_template("index.html")

def get_weather_data(city):
    complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == "404":
        return None

    main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    weather_data = {
        "city": city,
        "temperature": main["temp"],
        "description": weather["description"],
        "humidity": main["humidity"],
        "pressure": main["pressure"],
        "wind_speed": wind["speed"],
        "time": time,
    }

    return weather_data

if __name__ == "__main__":
    app.run(debug=True)
