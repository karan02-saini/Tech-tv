import urllib.request
import json
import re

M3U_SOURCE_URL = "https://iptv-org.github.io/iptv/countries/in.m3u"
JSON_FILE_PATH = "channels.json"

def parse_m3u_to_json(m3u_content):
    channels = []
    current_channel = {}
    
    lines = m3u_content.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            current_channel = {}
            
            
            parts = line.split(',')
            if len(parts) > 1:
                name = parts[-1].strip()
                current_channel["name"] = name
               
                channel_id = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
                current_channel["id"] = channel_id if channel_id else "channel_id"
            else:
                current_channel["name"] = "Unknown Channel"
                current_channel["id"] = "unknown"
                
            group_match = re.search(r'group-title="([^"]*)"', line)
            current_channel["category"] = group_match.group(1) if group_match else "General"
                
            lang_match = re.search(r'tvg-chno="([^"]*)"', line) 
            current_channel["language"] = "Hindi"
                
            logo_match = re.search(r'tvg-logo="([^"]*)"', line)
            current_channel["logo"] = logo_match.group(1) if logo_match else ""
                
        elif line and not line.startswith("#"):
            current_channel["streamUrl"] = line
            
            if "name" in current_channel and "streamUrl" in current_channel:
                channels.append(current_channel)
                
    return channels

def update_json():
    try:
        print("Fetching M3U playlist from source...")
        req = urllib.request.Request(
            M3U_SOURCE_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            m3u_data = response.read().decode('utf-8', errors='ignore')
            
        print("Parsing and formatting to match exact JSON structure...")
        channels_list = parse_m3u_to_json(m3u_data)
        
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(channels_list, f, indent=4)
            
        print(f"Successfully updated channels.json with {len(channels_list)} channels!")
    except Exception as e:
        print(f"Error updating channels: {e}")

if __name__ == "__main__":
    update_json()
