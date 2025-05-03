import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram import F
import asyncio
import pandas as pd

from handlers.report_handler import get_last_signals
from handlers.winrate_handler import calculate_winrate
from handlers.pnl_handler import calculate_pnl
from handlers.equity_handler import generate_equity_plot
from handlers.heatmap_handler import generate_heatmap
from handlers.daily_report_handler import generate_daily_report
from handlers.equity_live_handler import generate_equity_live
from handlers.autostop_handler import check_autostop

import subprocess

API_TOKEN = '7947328586:AAGhTyJ8bSMU0BrfcXrIPx9SFocZJk9u5WQ'

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="📊 Report"), KeyboardButton(text="📈 Winrate")],
        [KeyboardButton(text="💰 PnL"), KeyboardButton(text="📉 Equity Curve")],
        [KeyboardButton(text="🧮 Summary"), KeyboardButton(text="🗺 Heatmap")],
        [KeyboardButton(text="📅 Daily Report"), KeyboardButton(text="📡 Equity Live")],
        [KeyboardButton(text="🛑 Autostop"), KeyboardButton(text="📤 Feedback")]
    ])
    await message.answer("🚀 Quant bot online.\nChoose an action:", reply_markup=kb)

@dp.message(F.text == "📊 Report")
async def report_handler_func(message: types.Message):
    try:
        lines = get_last_signals()
        report_text = "\n".join(lines)
        await message.answer(f"📊 Last Signals:\n{report_text}")
    except Exception as e:
        await message.answer(f"❌ Error in report: {e}")

@dp.message(F.text == "📈 Winrate")
async def winrate_handler_func(message: types.Message):
    try:
        winrate = calculate_winrate()
        await message.answer(f"📈 Winrate: {winrate}%")
    except Exception as e:
        await message.answer(f"❌ Error in winrate: {e}")

@dp.message(F.text == "💰 PnL")
async def pnl_handler_func(message: types.Message):
    try:
        total = calculate_pnl()
        total = float(total)
        await message.answer(f"💰 Total PnL: ${total:.2f}")
    except Exception:
        await message.answer(f"💰 Total PnL: {total}")

@dp.message(F.text == "📉 Equity Curve")
async def equity_handler_func(message: types.Message):
    try:
        photo_path = generate_equity_plot()
        with open(photo_path, "rb") as photo:
            await message.answer_photo(photo)
    except Exception as e:
        await message.answer(f"❌ Error in equity curve: {e}")

@dp.message(F.text == "🧮 Summary")
async def summary_handler(message: types.Message):
    try:
        df = pd.read_csv("trades.csv")
        winrate = (df["pnl"] > 0).mean() * 100
        expectancy = df["pnl"].mean()
        profit_factor = df[df["pnl"] > 0]["pnl"].sum() / abs(df[df["pnl"] < 0]["pnl"].sum())
        msg = (
            f"🧮 <b>Summary Metrics</b>:\n"
            f"• Total Trades: {len(df)}\n"
            f"• Winrate: {winrate:.2f}%\n"
            f"• Expectancy: {expectancy:.2f} $/trade\n"
            f"• Profit Factor: {profit_factor:.2f}\n"
        )
        await message.answer(msg)
    except Exception as e:
        await message.answer(f"❌ Error in summary: {e}")

@dp.message(F.text == "🗺 Heatmap")
async def heatmap_handler(message: types.Message):
    try:
        photo_path = generate_heatmap()
        with open(photo_path, "rb") as photo:
            await message.answer_photo(photo, caption="🗺 Heatmap of PnL by Symbol")
    except Exception as e:
        await message.answer(f"❌ Error in heatmap: {e}")

@dp.message(F.text == "📅 Daily Report")
async def daily_handler(message: types.Message):
    try:
        report = generate_daily_report()
        await message.answer(report)
    except Exception as e:
        await message.answer(f"❌ Error in daily report: {e}")

@dp.message(F.text == "📡 Equity Live")
async def equity_live_handler(message: types.Message):
    try:
        photo_path = generate_equity_live()
        with open(photo_path, "rb") as photo:
            await message.answer_photo(photo, caption="📡 Live Equity Curve")
    except Exception as e:
        await message.answer(f"❌ Error in equity live: {e}")

@dp.message(F.text == "🛑 Autostop")
async def autostop_handler(message: types.Message):
    try:
        result = check_autostop()
        await message.answer(result)
    except Exception as e:
        await message.answer(f"❌ Autostop error: {e}")

@dp.message(F.text == "📤 Feedback")
async def feedback_handler(message: types.Message):
    try:
        result = subprocess.run(["python3", "feedback_tracker.py"], capture_output=True, text=True)
        await message.answer(f"📤 Feedback:\n{result.stdout[-400:]}")
    except Exception as e:
        await message.answer(f"❌ Feedback error: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
