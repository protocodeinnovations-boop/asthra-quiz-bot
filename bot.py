import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://script.google.com/macros/s/AKfycbxBWEHGX_zzsg2oTmImd3z9K7aX9U9KvO72uiAEEgA9bvbk_RP6vdvu80JiREGNMIoD/exec"

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found in Railway Variables")

    if not CHAT_ID:
        raise ValueError("CHAT_ID not found in Railway Variables")

    bot = Bot(token=BOT_TOKEN)

    response = requests.get(API_URL, allow_redirects=True)

    print("STATUS:", response.status_code)
    print("FINAL URL:", response.url)

    response.raise_for_status()

    questions = response.json()

    if not questions:
        print("No questions pending.")
        return

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
        correct_option_id=["A", "B", "C", "D"].index(q["correct"]),
        explanation=q["explanation"]
    )

    print("Question sent successfully.")

if __name__ == "__main__":
    asyncio.run(main())
