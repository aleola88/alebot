from apscheduler.schedulers.background import BackgroundScheduler
from db import get_today_habits
from datetime import datetime

def schedule_jobs(app):
    scheduler = BackgroundScheduler()

    def morning_summary():
        now = datetime.now()
        weekday = now.strftime('%A').lower()
        users = [12345678]  # TODO: puedes mantener lista de usuarios únicos en una tabla
        for uid in users:
            habits = get_today_habits(uid, weekday)
            if habits:
                text = "\n".join([f"📝 {h['name']} a las {h['time']}" for h in habits])
                app.bot.send_message(chat_id=uid, text=f"☀️ Buenos días. Hoy tienes:\n{text}")

    scheduler.add_job(morning_summary, 'cron', hour=8, minute=0)  # 08:00 am
    scheduler.start()
