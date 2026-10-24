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
                
                hindi_url = None
                
                for line in lines:
                    # Sirf HIN / Hindi waali line filter karenge
                    if any(h in line.lower() for h in ["hin", "hindi"]):
                        urls = re.findall(r'https?://[^\s]+', line)
                        if urls:
                            potential_url = urls[0]
                            # Yahan check laga diya ki URL mein '*' nahi hona chahiye
                            if "*" not in potential_url:
                                hindi_url = potential_url
                                break
                
                # Agar valid Hindi link mila (bina star wala) toh events.json update karenge
                if hindi_url:
                    domain = hindi_url.split('/')[2]
                    
                    event_data = [
                        {
                            "match": match_title,
                            "streamUrl": hindi_url,
                            "headers": {
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                "Referer": f"https://{domain}/"
                            }
                        }
                    ]
                    
                    with open("events.json", "w", encoding="utf-8") as f:
                        json.dump(event_data, f, indent=4, ensure_ascii=False)
                    
                    print(f"Successfully updated events.json for: {match_title}")
                    break

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
