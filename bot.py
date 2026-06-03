if not CHAT_ID:
    raise ValueError("CHAT_ID not found in Railway Variables")

bot = Bot(token=BOT_TOKEN)

response = requests.get(API_URL, allow_redirects=True)

print("STATUS:", response.status_code)
print("URL:", response.url)
print("TEXT:", response.text[:1000])

response.raise_for_status()

questions = response.json()

if not questions:
    raise ValueError("No questions returned from API")

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
    chat_id=CHAT_ID,
    text=f"📘 Explanation:\n{q['explanation']}"
)
