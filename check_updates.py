import requests
import datetime
import time
from google_play_scraper import app as android_app

apps = {
    "Facebook":  {"ios": "284882215", "android": "com.facebook.katana"},
    "Instagram": {"ios": "389801252", "android": "com.instagram.android"},
    "WhatsApp":  {"ios": "310633997", "android": "com.whatsapp"},
    "Telegram":  {"ios": "686449807", "android": "org.telegram.messenger"},
    "Snapchat":  {"ios": "447134409", "android": "com.snapchat.android"}
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"# 📱 Global OS & App Security Tracker")
print(f"**Audit Date:** {datetime.date.today()}\n")
print("## ⚙️ 1. Core Operating Systems")
print("| System | Status | Security Notes |\n| :--- | :--- | :--- |\n| Apple iOS | 🟢 Active | *Check Settings.* |\n| Google Android | 🟢 Active | *Check Settings.* |\n")
print("## 📲 2. Application Updates & Vulnerability Status")
print("| Application | Platform | Version | Release Date | Risk Level | Fixes & Full Release Notes |")
print("| :--- | :--- | :--- | :--- | :--- | :--- |")

for name, ids in apps.items():
    # --- Apple iOS Check ---
    ios_row = f"| {name} | iOS | N/A | N/A | ⚠️ Unknown | Connection busy. |"
    try:
        # NEW URL: Added 'country=us' to make the search more specific/stable
        ios_url = f"https://itunes.apple.com/lookup?id={ids['ios']}&country=us&entity=software"
        res = requests.get(ios_url, headers=headers, timeout=20).json()
        if res['results']:
            data = res['results'][0]
            ver, dt = data['version'], data['currentVersionReleaseDate'][:10]
            notes = data.get('releaseNotes', 'Security improvements.').replace('\n', '<br>').replace('|', ' ')
            risk = "🟢 Low" if "2026" in dt else "🔴 High"
            ios_row = f"| {name} | iOS | {ver} | {dt} | {risk} | {i_notes} |"
    except:
        pass
    print(ios_row)

    # --- Android Check ---
    try:
        and_data = android_app(ids['android'])
        a_ver = and_data.get('version', 'Varies')
        a_updated = and_data.get('updated')
        a_date = datetime.datetime.fromtimestamp(a_updated).strftime('%Y-%m-%d') if isinstance(a_updated, int) else str(a_updated)[:10]
        a_notes = and_data.get('recentChanges', 'Security improvements.').replace('\n', '<br>').replace('|', ' ')
        a_risk = "🟢 Low" if "2026" in a_date else "🔴 High"
        print(f"| {name} | Android | {a_ver} | {a_date} | {a_risk} | {a_notes} |")
    except:
        print(f"| {name} | Android | Error | N/A | ⚠️ Unknown | Connection busy. |")

print("\n---\n*Generated every 24 hours.*")
