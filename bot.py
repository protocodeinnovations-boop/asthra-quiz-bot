import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("8539465341:AAF3GakskKFGxT5hWQV1pIQgnx5-XF0IqH0")
CHAT_ID = os.getenv("1001234567890")

API_URL = "https://script.google.com/macros/s/AKfycbxBWEHGX_zzsg2oTmImd3z9K7aX9U9KvO72uiAEEgA9bvbk_RP6vdvu80JiREGNMIoD/exec"

async def main():
    bot = Bot(token=8539465341:AAF3GakskKFGxT5hWQV1pIQgnx5-XF0IqH0)

    response = requests.get(API_URL, allow_redirects=True)

    print("STATUS:", response.status_code)
    print("URL:", response.url)
    print("TEXT:", response.text[:1000])

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
        correct_option_id=["A", "B", "C", "D"].index(q["correct"])
    )

    await bot.send_message(
        chat_id=,1001234567890
        text=f"📘 Explanation:\n{q['explanation']}"
    )

if __name__ == "__main__":
    asyncio.run(main())
