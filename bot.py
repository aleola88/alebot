from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)
from db import add_habit, get_today_habits
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

TOKEN = os.getenv("8424750554:AAGhsvOwcRRDKUMMXnYAjtPLrnf5VeWpz_w")

# States for conversation
ASK_NAME, ASK_DAYS, ASK_TIME = range(3)
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola, soy tu Habit Tracker. Usa /add para agregar un nuevo hábito.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 ¿Cuál es el nombre del hábito?")
    return ASK_NAME

async def ask_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id] = {"name": update.message.text}
    await update.message.reply_text("📅 ¿Qué días? (Ej: lunes,martes,viernes)")
    return ASK_DAYS

async def ask_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id]["days"] = update.message.text.lower().replace(" ", "").split(",")
    await update.message.reply_text("⏰ ¿A qué hora? (Ej: 18:00)")
    return ASK_TIME

async def save_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    time = update.message.text
    habit = user_sessions[user_id]
    habit["time"] = time
    add_habit(user_id, habit["name"], habit["days"], time)
    await update.message.reply_text(f"✅ Hábito '{habit['name']}' agregado.")
    return ConversationHandler.END

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weekday = datetime.now().strftime('%A').lower()
    habits = get_today_habits(update.effective_user.id, weekday)
    if habits:
        text = "\n".join([f"📝 {h['name']} a las {h['time']}" for h in habits])
        await update.message.reply_text(f"📋 Tus hábitos de hoy:\n{text}")
    else:
        await update.message.reply_text("🎉 No tienes hábitos para hoy.")

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_days)],
        ASK_DAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_time)],
        ASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_habit)],
    },
    fallbacks=[]
)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
app.add_handler(CommandHandler("today", today))

# Scheduler (ver siguiente paso)
from scheduler import schedule_jobs
schedule_jobs(app)

app.run_polling()
