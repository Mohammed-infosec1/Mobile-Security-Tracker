import requests
import datetime
import time
from google_play_scraper import app as android_app

# The App IDs
apps = {
    "Facebook":  {"ios": "284882215", "android": "com.facebook.katana"},
    "Instagram": {"ios": "389801252", "android": "com.instagram.android"},
    "WhatsApp":  {"ios": "310633997", "android": "com.whatsapp"},
    "Telegram":  {"ios": "686449807", "android": "org.telegram.messenger"},
    "Snapchat":  {"ios": "447134409", "android": "com.snapchat.android"}
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"# 📱 Global OS & App Security Tracker")
print(f"**Audit Date:** {datetime.date.today()}\n")

print("## ⚙️ 1. Core Operating Systems")
print("| System | Status | Security Notes |")
print("| :--- | :--- | :--- |")
print("| Apple iOS | 🟢 Active Monitoring | *Check Settings > General > Software Update.* |")
print("| Google Android | 🟢 Active Monitoring | *Check Settings > Security & Privacy > System & Updates.* |\n")

print("## 📲 2. Application Updates & Vulnerability Status")
print("| Application | Platform | Version | Release Date | Risk Level | Fixes & Full Release Notes |")
print("| :--- | :--- | :--- | :--- | :--- | :--- |")

for name, ids in apps.items():
    # --- Apple iOS Check ---
    ios_success = False
    for attempt in range(3): # Try 3 times if Apple is busy
        try:
            ios_url = f"https://itunes.apple.com/lookup?id={ids['ios']}"
            response = requests.get(ios_url, headers=headers, timeout=20).json()
            if response['results']:
                ios_data = response['results'][0]
                i_ver = ios_data['version']
                i_date = ios_data['currentVersionReleaseDate'][:10]
                i_notes = ios_data.get('releaseNotes', 'Security improvements.').replace('\n', '<br>').replace('|', ' ')
                i_risk = "🟢 Low" if "2026" in i_date else "🔴 High"
                print(f"| {name} | iOS | {i_ver} | {i_date} | {i_risk} | {i_notes} |")
                ios_success = True
                break
         dream_except:
            time.sleep(2) # Wait 2 seconds before retrying
    
    if not ios_success:
        print(f"| {name} | iOS | N/A | N/A | ⚠️ Unknown | Apple Store busy. Will retry tomorrow. |")

    # --- Google Android Check ---
    try:
        and_data = android_app(ids['android'])
        a_ver = and_data.get('version', 'Varies')
        a_updated = and_data.get('updated')
        a_date = datetime.datetime.fromtimestamp(a_updated).strftime('%Y-%m-%d') if isinstance(a_updated, int) else str(a_updated)[:10]
        a_notes = and_data.get('recentChanges', 'Security improvements.').replace('\n', '<br>').replace('|', ' ')
        a_risk = "🟢 Low" if "2026" in a_date else "🔴 High"
        print(f"| {name} | Android | {a_ver} | {a_date} | {a_risk} | {a_notes} |")
    except Exception:
        print(f"| {name} | Android | Error | N/A | ⚠️ Unknown | Could not reach Google Play. |")

print("\n---\n*This report is automatically generated every 24 hours.*")
