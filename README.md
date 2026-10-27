# 📊 Universal Daily Task Reporter

**Autonomous Daily Task Extraction, Deep AI Evaluation & 1-Click Sync to Google Sheets for Codex, Antigravity, and Marketing Teams.**

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Codex%20%7C%20Antigravity%20%7C%20ChatGPT-brightgreen.svg)](#)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](#)

---

## 🌟 Overview

The **Universal Daily Task Reporter** automates the tedious end-of-day task reporting process for agencies, remote teams, and solo builders. It bridges the gap between technical teams using local AI agents and creative/content teams using Web chat interfaces:

1. **For Technical / Dev / SEO Staff (Codex / Antigravity)**: Automatically scans local agent execution histories (`~/.codex/thread_history_1.sqlite` and `~/.gemini/antigravity/brain/`), filters out trivial commands and personal browsing, groups tasks into structured time blocks, and pushes them directly to Google Sheets.
2. **For Content / Creative / Marketing Staff (ChatGPT Web)**: A 1-click **Chrome Bookmarklet** extracts the day's chats into a clean JSON export. When handed to the AI agent, it parses real work artifacts and auto-logs them with human-quality task descriptions.

---

## 🚀 Quick Setup (2 Minutes)

### Step 1: Set Up Your Free Google Sheet Backend

1. Create a new Google Sheet (or open an existing team task tracker).
2. Create a sheet tab named **`Daily Task Log`** with the following header row:
   ```text
   Date | Week | Name | Role | Hour Block | Task Description | Category | Website / Client | Growth Driver | Quality / Deep-Work % | Notes / Blockers
   ```
3. In Google Sheets, click **Extensions** → **Apps Script**.
4. Replace all code in the script editor with the contents of [`daily-task-reporter/Code.gs`](daily-task-reporter/Code.gs).
5. Click **Deploy** → **New deployment**:
   - Select type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
6. Copy the generated **Web App URL** (`https://script.google.com/macros/s/.../exec`).

---

### Step 2: Configure Your Settings

Copy `config.example.json` to `config.json`:

```bash
cp config.example.json config.json
```

Edit `config.json` with your Web App URL and custom client/category lists:

```json
{
  "webapp_url": "https://script.google.com/macros/s/YOUR_APPS_SCRIPT_ID/exec",
  "target_sheet_tab": "Daily Task Log",
  "timezone_offset_hours": 7,
  "work_hours": {
    "start": "09:00",
    "lunch_start": "12:00",
    "lunch_end": "13:30",
    "end": "17:30"
  },
  "clients": [
    "Internal Ops",
    "Project Alpha",
    "Client Beta",
    "Open Source"
  ],
  "categories": [
    "Content Creation",
    "SEO / AEO",
    "Software Development",
    "Social Media",
    "Paid Ads",
    "Reporting / Analytics",
    "Client / Team Meetings",
    "Admin / Ops",
    "Learning / Research",
    "Other"
  ],
  "growth_drivers": [
    "Traffic Growth",
    "Conversion / Sales",
    "Retention / Engagement",
    "Brand Awareness",
    "Skill Building",
    "Internal Ops",
    "General Delivery"
  ]
}
```

> **Tip:** You can also configure the URL via environment variable:  
> `export DAILY_TASK_WEBAPP_URL="https://script.google.com/macros/s/.../exec"`

---

## 💻 Usage

### 1. For Codex & Antigravity Users

Run the CLI command directly or prompt your AI agent:

```bash
# Preview today's tasks in Markdown table
python3 daily-task-reporter/scripts/generate_daily_report.py

# Push today's tasks directly to your Google Sheet
python3 daily-task-reporter/scripts/generate_daily_report.py --push

# Report for a specific date or custom author
python3 daily-task-reporter/scripts/generate_daily_report.py --date 2026-10-27 --name "Alex" --role "Fullstack Engineer" --push
```

Or simply chat in your agent interface:
> *"Điền task hôm nay vào sheet"* / *"Log today's tasks to Google Sheet"*

---

### 2. For Non-Technical Team Members (ChatGPT Web)

1. Open [`bookmarklet.html`](bookmarklet.html) in Chrome.
2. Drag the green **"📥 Xuất Chat Hôm Nay"** button onto your Chrome **Bookmarks Bar**.
3. At the end of the day on `https://chatgpt.com`, click the bookmarklet. It downloads a clean `chatgpt_today_YYYY-MM-DD.json`.
4. Provide the file to your agent:
   ```bash
   python3 daily-task-reporter/scripts/generate_daily_report.py --chatgpt-file ~/Downloads/chatgpt_today_2026-10-27.json --name "Sarah" --role "Content Specialist" --push
   ```

---

## 🛡️ Built-in Noise & Privacy Filters

The reporter automatically filters out:
- Irrelevant personal commands, games, and video streaming scripts.
- Trivial technical micro-actions (formatting, copy-paste, terminal exits).
- Sensitive internal token or budget calculations.

---

## 📄 License

MIT License. Built with ❤️ for the open-source developer & digital marketing community.
