import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://script.google.com/macros/s/AKfycbxBWEHGX_zzsg2oTmImd3z9K7aX9U9KvO72uiAEEgA9bvbk_RP6vdvu80JiREGNMIoD/exec"

async def main():
    bot = Bot(token=BOT_TOKEN)

    response = requests.get(API_URL)
    questions = response.json()

    q = questions[0]

    await bot.send_poll(
        chat_id=CHAT_ID,
        question=q["question"],
        options=[
            q["a"],
            q["b"],
            q["c"],
            q["d"]
        ],
        type="quiz",
        correct_option_id=["A","B","C","D"].index(q["correct"])
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"📘 Explanation:\n{q['explanation']}"
    )

if __name__ == "__main__":
    asyncio.run(main())
