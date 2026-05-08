from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

# API Keys (သင့်ရဲ့ Keys တွေအတိုင်း ထည့်ထားပါတယ်)
api_id = 35148850
api_hash = '3426b7d98ab6a3599cd5b28925d1fcdd'
bot_token = '8608923887:AAGuIfjHMNwLFkG0ecRzFqaQ6zb9bLzGg1M'

# Render ပေါ်မှာ Proxy မလိုဘဲ တိုက်ရိုက်ချိတ်ဆက်ခြင်း
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

to_my = GoogleTranslator(source='auto', target='my')
to_en = GoogleTranslator(source='auto', target='en')
to_es = GoogleTranslator(source='auto', target='es')

print("Bot is running on Render...")

@client.on(events.NewMessage)
async def handle_message(event):
    if event.is_private:
        text = event.raw_text
        if text and len(text.strip()) > 0:
            try:
                try:
                    detected_lang = detect(text)
                except:
                    detected_lang = "unknown"
                
                results = []
                # မြန်မာစာ မဟုတ်ရင် မြန်မာပြန်မယ်
                if not (detected_lang.startswith('my') or any('\u1000' <= c <= '\u109f' for c in text)):
                    results.append(f"🇲🇲 **Myanmar:**\n{to_my.translate(text)}")
                
                # အင်္ဂလိပ်စာ မဟုတ်ရင် အင်္ဂလိပ်ပြန်မယ်
                if not detected_lang.startswith('en'):
                    results.append(f"🇺🇸 **English:**\n{to_en.translate(text)}")
                
                # စပိန်စာ မဟုတ်ရင် စပိန်ပြန်မယ်
                if not detected_lang.startswith('es'):
                    results.append(f"🇪🇸 **Spanish:**\n{to_es.translate(text)}")

                reply_message = "\n\n".join(results)
                if reply_message:
                    await event.reply(reply_message)
            except Exception as e:
                print(f"Error: {e}")

client.run_until_disconnected()
