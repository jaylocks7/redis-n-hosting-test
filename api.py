import requests
import dotenv
import os
import redis
import json
from flask import Flask, jsonify, send_file
from flask_cors import CORS

dotenv.load_dotenv()
api_key = os.getenv("RAPIDAPI-KEY")

app = Flask(__name__)
CORS(app)

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(redis_url, decode_responses=True)

headers = {
    'Content-Type': 'application/json',
    "x-rapidapi-host": "nba-api-free-data.p.rapidapi.com",
    "x-rapidapi-key": api_key
}

VALID_REGIONS = {"atlantic", "central", "southeast", "northwest", "pacific", "southwest"}

def build_url(region):
    return f"https://nba-api-free-data.p.rapidapi.com/nba-{region}-team-list"

def get_with_cache(url, ttl=3600):
    cached: str | None = r.get(url)  # type: ignore[assignment]
    if cached:
        print("cache hit")
        return json.loads(cached)

    print("cache miss")
    response = requests.get(url, headers=headers)
    data = response.json()
    r.set(url, json.dumps(data), ex=ttl)
    return data

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/teams/<region>")
def get_teams(region):
    if region not in VALID_REGIONS:
        return jsonify({"error": "Invalid region"}), 400

    url = build_url(region)
    data = get_with_cache(url)
    print(data)
    return data

if __name__ == "__main__":
    app.run(debug=True)
