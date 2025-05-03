from aiogram import types
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

async def equity_handler(message: types.Message):
    try:
        df = pd.read_csv("trades.csv", parse_dates=["timestamp"])
        df.sort_values("timestamp", inplace=True)
        df["equity"] = df["pnl"].cumsum()

        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["equity"], label="Equity Curve")
        plt.xlabel("Time")
        plt.ylabel("Equity")
        plt.title("Agentic RAG Equity Curve")
        plt.grid(True)
        plt.legend()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        await message.answer_photo(photo=buf, caption="📈 Equity Curve")
        buf.close()
        plt.close()

    except Exception as e:
        await message.answer(f"Ошибка построения equity: {e}")
