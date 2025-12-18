from flask import Flask
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Moscow"
CITY_DISPLAY_NAME = "Москва"

@app.route("/")
def weather():
    if not API_KEY:
        return "Ошибка: переменная окружения WEATHER_API_KEY не задана", 500

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "main" not in data:
            return f"Ошибка от погодного сервиса: {data.get('message', 'unknown')}", 502

        temperature = data["main"]["temp"]

    except Exception as e:
        return f"Ошибка при получении данных о погоде: {e}", 502

    return f"Текущая температура в г. {CITY_DISPLAY_NAME}: {temperature} °C"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
