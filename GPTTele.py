from telethon import TelegramClient, events
import requests
import json

# بيانات تيليجرام من my.telegram.org
api_id = 29387102       # ← استبدله بـ API ID
api_hash = 'd45744dd07ce19c3aaaaa4f8bdf9623a'  # ← استبدله بـ API Hash
phone = '+9647718589875'  # ← رقمك مع رمز الدولة

# API Key من OpenRouter
openrouter_api_key = "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"

# إعداد تيليجرام
client = TelegramClient('ai_chat_session', api_id, api_hash)

# دالة توليد الرد من OpenRouter
def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  # تقدر تغيّر إلى deepseek-ai/deepseek-chat
        "messages": [
            {"role": "system", "content": "انت مساعد ذكي و اسمك هو سجاد وكل ما هو عليك المساعده في اي شيء وتعامل مثل الشخص الحقيقي جد الحلول عند وصف المشاكل وتصرف كأنك شخص حقيقي "},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        res_json = response.json()
        return res_json["choices"][0]["message"]["content"]
    except Exception as e:
        return "ما قدرت أرد، صار خطأ من الذكاء الاصطناعي."

# التعامل مع الرسائل الخاصة
@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    if event.is_private:
        sender = await event.get_sender()
        name = sender.first_name or "حبيبي "
        msg = event.raw_text

        full_prompt = f"{name} سألك: {msg}\nرد عليه باللهجة العراقية."
        reply = ask_openrouter(full_prompt)
        await event.reply(reply)

async def main():
    await client.start()  # ← هذا يتعامل مع تسجيل الدخول التلقائي

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input("أدخل كود التحقق: ")
        await client.sign_in(phone, code)

    print("تم تسجيل الدخول!")

client.loop.run_until_complete(main())

# تشغيل البوت
with client:
    print("البوت شغال، انتظر الرسائل...")
    client.run_until_disconnected()