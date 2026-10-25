import os
import json
import re
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

CHANNEL_ID = -1004312648358

async def main():
    print("Initializing Telegram client...")
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    print("Client started successfully!")
    
    print(f"Scanning messages from channel: {CHANNEL_ID}")
    all_event_streams = []
    
    # Ab hum last 15 messages scan karenge taaki saare active matches ke links mil sakein
    async for message in client.iter_messages(CHANNEL_ID, limit=15):
        if message.text:
            text = message.text
            if any(k in text.lower() for k in ["vs", "t20", "odi", "match", "test", "india"]):
                lines = text.split("\n")
                match_title = "Live Match"
                current_label = "Live Stream"
                
                for i in range(len(lines)):
                    line = lines[i].strip()
                    if "vs" in line.lower() and len(line) > 5:
                        match_title = line
                    
                    urls = re.findall(r'https?://[^\s]+', line)
                    if urls:
                        potential_url = urls[0].strip('*')
                        if "t.me" not in potential_url:
                            if i > 0 and not re.findall(r'https?://[^\s]+', lines[i-1]):
                                current_label = lines[i-1].strip()
                            
                            domain = potential_url.split('/')[2]
                            
                            stream_entry = {
                                "match": f"{match_title} ({current_label})",
                                "streamUrl": potential_url,
                                "headers": {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                    "Referer": f"https://{domain}/"
                                }
                            }
                            
                            # Duplicate entries rokne ke liye check karenge
                            if stream_entry not in all_event_streams:
                                all_event_streams.append(stream_entry)
    
    if all_event_streams:
        with open("events.json", "w", encoding="utf-8") as f:
            json.dump(all_event_streams, f, indent=4, ensure_ascii=False)
        print(f"SUCCESS: events.json updated with total {len(all_event_streams)} streams from active matches!")
    else:
        print("No valid streams found in recent messages.")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
