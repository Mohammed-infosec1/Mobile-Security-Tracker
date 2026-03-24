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

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def assess_risk(notes):
    notes_lower = notes.lower()
    critical_keywords = ["critical", "urgent", "vulnerability", "exploit", "cve", "remote code execution"]
    security_keywords = ["security", "patch", "fix"]
    bug_keywords = ["bug", "crash", "stability", "performance", "improvement"]

    if any(k in notes_lower for k in critical_keywords):
        return "🔴 High"
    elif any(k in notes_lower for k in security_keywords):
        return "🟢 Low"
    elif any(k in notes_lower for k in bug_keywords):
        return "🟡 Medium"
    else:
        return "🟡 Medium"

def fetch_ios_data(app_id):
    url = f"https://itunes.apple.com/lookup?id={app_id}&country=us"

    for _ in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data_json = response.json()
                if data_json.get("resultCount", 0) > 0:
                    return data_json["results"][0]
        except:
            time.sleep(2)
    return None

print(f"# 📱 Global OS & App Security Tracker")
print(f"**Audit Date:** {datetime.date.today()}\n")

print("## ⚙️ 1. Core Operating Systems")
print("| System | Status | Security Notes |")
print("| :--- | :--- | :--- |")
print("| Apple iOS | 🟢 Active | *Check Settings > General > Software Update.* |")
print("| Google Android | 🟢 Active | *Check Settings > Security & Privacy.* |\n")

print("## 📲 2. Application Updates & Vulnerability Status")
print("| Application | Platform | Version | Release Date | Risk Level | Fixes & Full Release Notes |")
print("| :--- | :--- | :--- | :--- | :--- | :--- |")

for name, ids in apps.items():

    ios_data = fetch_ios_data(ids["ios"])

    if ios_data:
        ver = ios_data.get("version", "N/A")
        dt_raw = ios_data.get("currentVersionReleaseDate", "")
        notes = ios_data.get("releaseNotes", "No details provided.").replace("\n", "<br>").replace("|", " ")

        try:
            dt_obj = datetime.datetime.fromisoformat(dt_raw.replace("Z", "+00:00"))
            dt = dt_obj.strftime("%Y-%m-%d")
        except:
            dt = dt_raw[:10]

        risk = assess_risk(notes)
        print(f"| {name} | iOS | {ver} | {dt} | {risk} | {notes} |")
    else:
        print(f"| {name} | iOS | Unknown | Unknown | ⚠️ Unknown | App Store data not available. |")

    try:
        and_data = android_app(ids["android"])
        a_ver = and_data.get("version", "Varies")
        a_notes = and_data.get("recentChanges", "No details provided.").replace("\n", "<br>").replace("|", " ")

        a_updated = and_data.get("updated", "")
        try:
            if isinstance(a_updated, int):
                a_date = datetime.datetime.fromtimestamp(a_updated).strftime("%Y-%m-%d")
            else:
                a_date = datetime.datetime.strptime(a_updated, "%B %d, %Y").strftime("%Y-%m-%d")
        except:
            a_date = str(a_updated)[:10]

        a_risk = assess_risk(a_notes)
        print(f"| {name} | Android | {a_ver} | {a_date} | {a_risk} | {a_notes} |")
    except:
        print(f"| {name} | Android | Error | N/A | ⚠️ Unknown | Could not reach Google Play. |")

print("\n---\n*This report is automatically generated every 24 hours.*")
