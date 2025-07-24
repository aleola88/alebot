import requests

SUPABASE_URL = "https://uunagymkizpspxfdmfbu.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1bmFneW1raXpwc3B4ZmRtZmJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMzODY3NjksImV4cCI6MjA2ODk2Mjc2OX0.d_j7ln82zF3ey9vllU1irzZ5pBBSeXoc0P2Cs63qVBs"

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
