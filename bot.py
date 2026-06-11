import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://script.google.com/macros/s/AKfycbxBWEHGX_zzsg2oTmImd3z9K7aX9U9KvO72uiAEEgA9bvbk_RP6vdvu80JiREGNMIoD/exec"

QUESTION_DELAY = 30  # seconds between questions


async def send_questions():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found in Railway Variables")

    if not CHAT_ID:
        raise ValueError("CHAT_ID not found in Railway Variables")

    bot = Bot(token=BOT_TOKEN)

    print("Fetching questions from Google Sheets...")

    response = requests.get(API_URL)
    response.raise_for_status()

    questions = response.json()

    if not questions:
        print("No questions found.")
        return

    print(f"Found {len(questions)} questions")

    for index, q in enumerate(questions, start=1):
        try:
            correct_index = ["A", "B", "C", "D"].index(
                q["correct"].strip().upper()
            )

            await bot.send_poll(
                chat_id=CHAT_ID,
                question=f"Q{index}. {q['question']}",
                options=[
                    q["a"],
                    q["b"],
                    q["c"],
                    q["d"]
                ],
                type="quiz",
                correct_option_id=correct_index,
                explanation=q.get("explanation", "")
            )

            print(f"✅ Sent Question {index}")

            if index < len(questions):
                await asyncio.sleep(QUESTION_DELAY)

        except Exception as e:
            print(f"❌ Error sending Question {index}: {e}")

    print("🎉 Quiz completed!")


if __name__ == "__main__":
    asyncio.run(send_questions())

# Mark as sent in Google Sheet
requests.post(
    API_URL,
    params={"row": q["row"]}
)

print(f"✅ Marked row {q['row']} as sent")
