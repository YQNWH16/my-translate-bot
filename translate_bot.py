import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# ၁။ Render Port Error အတွက် ဖြေရှင်းချက် (မရှိမဖြစ်ပါရမည့်အပိုင်း)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is Alive')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"Dummy server started on port {port}")
    server.serve_forever()

# Thread ဖြင့် Web Server ကို နှိုးထားခြင်း
threading.Thread(target=run_web_server, daemon=True).start()

DetectorFactory.seed = 0

# API Keys
api_id = 35148850
api_hash = '3426b7d98ab6a3599cd5b28925d1fcdd'
bot_token = '8608923887:AAGuIfjHMNwLFkG0ecRzFqaQ6zb9bLzGg1M'

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# ဘာသာပြန်စနစ်များ
to_my = GoogleTranslator(source='auto', target='my')
to_en = GoogleTranslator(source='auto', target='en')
to_es = GoogleTranslator(source='auto', target='es')
to_zh = GoogleTranslator(source='auto', target='zh-CN')

print("Bot is running on Render with Port Fix and Chinese support...")

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_msg = "သင့်အနေနှင့် ကျွန်ုပ်ရဲ့ စကားပြန် Bot ကို စတင်အသုံးပြုသည့်အခါ တစ်မိနစ်ခန့်စောင့်ပါ။ တစ်မိနစ်ခန့်စောင့်ပြီးပါက ဆက်လက်အသုံးပြုနိုင်ပါပြီ။"
    await event.reply(welcome_msg)

@client.on(events.NewMessage)
async def handle_message(event):
    if event.is_private and not event.raw_text.startswith('/start'):
        text = event.raw_text
        if text and len(text.strip()) > 0:
            try:
                try:
                    detected_lang = detect(text)
                except:
                    detected_lang = "unknown"
                
                results = []
                if not (detected_lang.startswith('my') or any('\u1000' <= c <= '\u109f' for c in text)):
                    results.append(f"🇲🇲 **Myanmar:**\n{to_my.translate(text)}")
                if not detected_lang.startswith('en'):
                    results.append(f"🇺🇸 **English:**\n{to_en.translate(text)}")
                if not detected_lang.startswith('es'):
                    results.append(f"🇪🇸 **Spanish:**\n{to_es.translate(text)}")
                if not detected_lang.startswith('zh'):
                    results.append(f"🇨🇳 **Chinese:**\n{to_zh.translate(text)}")

                reply_message = "\n\n".join(results)
                if reply_message:
                    await event.reply(reply_message)
            except Exception as e:
                print(f"Error: {e}")

client.run_until_disconnected()
