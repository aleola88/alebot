import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def add_habit(user_id, name, days, time):
    data = {
        "user_id": str(user_id),
        "name": name,
        "days": days,
        "time": time
    }
    res = requests.post(f"{SUPABASE_URL}/rest/v1/habits", headers=headers, json=data)
    return res.status_code == 201

def get_today_habits(user_id, weekday):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/habits?user_id=eq.{user_id}", headers=headers)
    if res.status_code == 200:
        habits = res.json()
        return [h for h in habits if weekday in h['days']]
    return []
