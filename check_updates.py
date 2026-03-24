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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def assess_risk(notes):
    notes_lower = notes.lower()
    critical_keywords = ["critical", "urgent", "vulnerability", "exploit", "cve", "security patch", "remote code execution"]
    security_keywords = ["security", "patch", "fixes security", "vulnerability fixed"]
    bug_keywords = ["bug", "crash", "stability", "performance", "minor fix", "improvement"]

    if any(k in notes_lower for k in critical_keywords):
        return "🔴 High"
    elif any(k in notes_lower for k in security_keywords):
        return "🟢 Low"
    elif any(k in notes_lower for k in bug_keywords):
        return "🟡 Medium"
    else:
        return "🟡 Medium"

print(f"# 📱 Global OS & App Security Tracker")
print(f"**Audit Date:** {datetime.date.today()}\n")
print("## ⚙️ 1. Core Operating Systems\n| System | Status | Security Notes |\n| :--- | :--- | :--- |\n| Apple iOS | 🟢 Active | *Check Settings > General > Software Update.* |\n| Google Android | 🟢 Active | *Check Settings > Security & Privacy.* |\n")
print("## 📲 2. Application Updates & Vulnerability Status")
print("| Application | Platform | Version | Release Date | Risk Level | Fixes & Full Release Notes |")
print("| :--- | :--- | :--- | :--- | :--- | :--- |")

for name, ids in apps.items():
    ios_success = False
    try:
        time.sleep(2)
        ios_url = f"https://itunes.apple.com/lookup?id={ids['ios']}&country=us&entity=software"
        response = requests.get(ios_url, headers=headers, timeout=15).json()
        if response['results']:
            data = response['results'][0]
            ver = data.get('version', 'N/A')
            dt_raw = data.get('currentVersionReleaseDate', '')
            notes = data.get('releaseNotes', 'Security improvements.').replace('\n', '<br>').replace('|', ' ')
            try:
                dt_obj = datetime.datetime.fromisoformat(dt_raw.replace('Z', '+00:00'))
                dt = dt_obj.strftime('%Y-%m-%d')
            except:
                dt = dt_raw[:10]

            risk = assess_risk(notes)
            print(f"| {name} | iOS | {ver} | {dt} | {risk} | {notes} |")
            ios_success = True
    except:
        pass

    if not ios_success:
        print(f"| {name} | iOS | N/A | N/A | ⚠️ Unknown | Could not fetch data. |")

    try:
        and_data = android_app(ids['android'])
        a_ver = and_data.get('version', 'Varies')
        a_notes = and_data.get('recentChanges', 'Security improvements.').replace('\n', '<br>').replace('|', ' ')
        a_updated = and_data.get('updated', '')

        try:
            if isinstance(a_updated, int):
                a_date = datetime.datetime.fromtimestamp(a_updated).strftime('%Y-%m-%d')
            else:
                a_date = datetime.datetime.strptime(a_updated, "%B %d, %Y").strftime('%Y-%m-%d')
        except:
            a_date = str(a_updated)[:10]

        a_risk = assess_risk(a_notes)
        print(f"| {name} | Android | {a_ver} | {a_date} | {a_risk} | {a_notes} |")
    except:
        print(f"| {name} | Android | Error | N/A | ⚠️ Unknown | Could not reach Google Play. |")

print("\n---\n*This report is automatically generated every 24 hours.*")
