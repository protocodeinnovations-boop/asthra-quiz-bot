import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://script.google.com/macros/s/AKfycbxBWEHGX_zzsg2oTmImd3z9K7aX9U9KvO72uiAEEgA9bvbk_RP6vdvu80JiREGNMIoD/exec"


async def send_questions():

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found")

    if not CHAT_ID:
        raise ValueError("CHAT_ID not found")

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

            options = [
                str(q["a"]),
                str(q["b"]),
                str(q["c"]),
                str(q["d"])
            ]

            correct_index = ["A", "B", "C", "D"].index(
                str(q["correct"]).strip().upper()
            )

            explanation = str(
                q.get("explanation", "")
            )[:180]

            await bot.send_poll(
                chat_id=CHAT_ID,
                question=f"Q{index}. {q['question']}",
                options=options,
                type="quiz",
                correct_option_id=correct_index,
                explanation=explanation,
                is_anonymous=False
            )

            print(f"✅ Sent Question {index}")

            # Mark as sent
            try:
                mark_response = requests.post(
                    API_URL,
                    data={
                        "row": q["row"]
                    },
                    timeout=10
                )

                print(
                    f"✅ Marked row {q['row']} as sent"
                )

                print(mark_response.text)

            except Exception as mark_error:
                print(
                    f"❌ Mark sent failed: {mark_error}"
                )

            delay = 10

            try:
                if "delay" in q:
                    delay = int(q["delay"])
            except:
                delay = 10

            await asyncio.sleep(delay)

        except Exception as e:
            print(
                f"❌ Error sending Question {index}: {e}"
            )

    print("🎉 Quiz completed!")


if __name__ == "__main__":
    asyncio.run(send_questions())
