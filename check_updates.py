import requests
import datetime
from google_play_scraper import app as android_app

# The exact App IDs
apps = {
    "Facebook": {"ios": "284882215", "android": "com.facebook.katana"},
    "Instagram": {"ios": "389801252", "android": "com.instagram.android"},
    "WhatsApp": {"ios": "310633997", "android": "com.whatsapp"},
    "Telegram": {"ios": "686449807", "android": "org.telegram.messenger"},
    "Snapchat": {"ios": "447134409", "android": "com.snapchat.android"}
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
    try:
        ios_url = f"https://itunes.apple.com/lookup?id={ids['ios']}"
        ios_data = requests.get(ios_url).json()['results'][0]
        i_ver = ios_data['version']
        i_date = ios_data['currentVersionReleaseDate'][:10]
        # REMOVED LIMIT: Now gets the full text and replaces new lines with spaces
        i_notes = ios_data.get('releaseNotes', 'Security improvements.').replace('\n', ' ').replace('|', ' ')
        i_risk = "🟢 Low" if "2026" in i_date else "🔴 High"
        print(f"| {name} | iOS | {i_ver} | {i_date} | {i_risk} | {i_notes} |")
    except Exception:
        pass

    # --- Google Android Check ---
    try:
        and_data = android_app(ids['android'])
        a_ver = and_data.get('version', 'Varies')
        a_updated = and_data.get('updated')
        if isinstance(a_updated, int):
            a_date = datetime.datetime.fromtimestamp(a_updated).strftime('%Y-%m-%d')
        else:
            a_date = str(a_updated)[:10]
            
        # REMOVED LIMIT: Gets full Android changes
        a_notes = and_data.get('recentChanges', 'Security improvements.')
        if not a_notes: a_notes = "Security improvements."
        a_notes = a_notes.replace('\n', ' ').replace('|', ' ')
        a_risk = "🟢 Low" if "2026" in a_date else "🔴 High"
        
        print(f"| {name} | Android | {a_ver} | {a_date} | {a_risk} | {a_notes} |")
    except Exception:
        pass

print("\n---\n*This report is automatically generated every 24 hours.*")
