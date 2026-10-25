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
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    
    async for message in client.iter_messages(CHANNEL_ID, limit=5):
        if message.text:
            text = message.text
            
            # Match related keywords check karenge
            if any(k in text.lower() for k in ["vs", "t20", "odi", "match", "test", "india"]):
                lines = text.split("\n")
                match_title = "Live Match"
                
                event_streams = []
                current_label = "Live Stream"
                
                for i in range(len(lines)):
                    line = lines[i].strip()
                    
                    # Agar line me 'vs' hai toh wo match title ho sakta hai
                    if "vs" in line.lower() and len(line) > 5:
                        match_title = line
                        continue
                    
                    # Links dhundhenge
                    urls = re.findall(r'https?://[^\s]+', line)
                    if urls:
                        potential_url = urls[0]
                        if "*" not in potential_url and "t.me" not in potential_url:
                            # Link se pehle wali line ko label bana lenge (jaise ENG - SD)
                            if i > 0 and not re.findall(r'https?://[^\s]+', lines[i-1]):
                                current_label = lines[i-1].strip()
                            
                            domain = potential_url.split('/')[2]
                            
                            event_streams.append({
                                "match": f"{match_title} ({current_label})",
                                "streamUrl": potential_url,
                                "headers": {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                    "Referer": f"https://{domain}/"
                                }
                            })
                
                if event_streams:
                    with open("events.json", "w", encoding="utf-8") as f:
                        json.dump(event_streams, f, indent=4, ensure_ascii=False)
                    
                    print(f"Successfully updated events.json with {len(event_streams)} streams!")
                    break

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
