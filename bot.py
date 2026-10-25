import os
import json
import re
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Environment variables se credentials uthayega
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# Tere private channel ki exact numeric ID
CHANNEL_ID = -1004312648358

async def main():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    
    # Channel ke latest 5 messages scan karenge
    async for message in client.iter_messages(CHANNEL_ID, limit=5):
        if message.text:
            text = message.text
            
            # Agar message mein match se related keywords hain
            if any(k in text.lower() for k in ["vs", "t20", "odi", "match", "india"]):
                lines = text.split("\n")
                match_title = lines[0].strip()
                
                event_streams = []
                
                # Saari lines ko check karenge ki kisme link aur language hai
                for i in range(len(lines)):
                    line = lines[i]
                    urls = re.findall(r'https?://[^\s]+', line)
                    
                    if urls:
                        potential_url = urls[0]
                        # Agar link masked ya star wala nahi hai toh hi lenge
                        if "*" not in potential_url:
                            # Upar wali line ya current line se stream ka naam/language dhoondhenge
                            stream_label = "Live Stream"
                            if i > 0:
                                stream_label = lines[i - 1].strip() # Jaise "HIN - SD" ya "ENG - SD"
                            
                            domain = potential_url.split('/')[2]
                            
                            # Har ek valid stream ko list me add kar denge
                            event_streams.append({
                                "match": f"{match_title} ({stream_label})",
                                "streamUrl": potential_url,
                                "headers": {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                    "Referer": f"https://{domain}/"
                                }
                            })
                
                # Agar ek bhi valid stream mil gayi toh events.json update kar denge
                if event_streams:
                    with open("events.json", "w", encoding="utf-8") as f:
                        json.dump(event_streams, f, indent=4, ensure_ascii=False)
                    
                    print(f"Successfully updated events.json with {len(event_streams)} streams for: {match_title}")
                    break

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
