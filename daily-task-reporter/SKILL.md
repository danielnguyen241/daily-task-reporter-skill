---
name: daily-task-reporter
description: Autonomous Daily Task Reporter for Codex & Antigravity. Automatically extracts and categorizes daily engineering/marketing tasks from agent activity logs and ChatGPT Web exports, syncing to any Google Sheet via customizable config.
---

# Universal Daily Task Reporter Skill

This skill scans and generates a structured **Daily Task Log** for developers, SEO specialists, and marketing teams from primary observable agent activity:
- Codex SQLite database: `~/.codex/thread_history_1.sqlite`
- Antigravity transcripts: `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl`
- ChatGPT Web JSON exports: `--chatgpt-file <path>`

---

## ⚙️ Configuration & Customization

The skill supports fully customized clients, categories, work hours, and Google Sheet destinations via `config.json` (or `~/.config/daily-task-reporter/config.json`):

1. **Target Google Sheet Web App**: Set `webapp_url` in `config.json` or through environment variable `DAILY_TASK_WEBAPP_URL`.
2. **Custom Clients / Projects**: Define your project/client whitelist in `config.json["clients"]`.
3. **Custom Categories & KPIs**: Define `config.json["categories"]` and `config.json["growth_drivers"]`.
4. **Custom Work Schedule**: Configure morning/afternoon hour blocks in `config.json["work_hours"]`.

---

## 📋 Strict Operational Rules

1. **Work Hours Alignment**: Tasks are structured within professional hour blocks (`09:00-10:30`, `10:30-12:00`, `13:30-15:30`, `15:30-17:30`).
2. **Deep Work Artifact Evaluation**: Tasks are synthesized from actual code commits, article drafts, and architectural outputs rather than generic placeholder summaries.
3. **Privacy & Noise Filtering**: Automatically drops personal browsing, games, video downloaders, and trivial terminal commands.

---

## 🚀 Execution Commands

1. **Self-Report for Codex / Antigravity User**:
   ```bash
   python3 scripts/generate_daily_report.py --push
   ```
2. **Team Report from ChatGPT Web Export**:
   ```bash
   python3 scripts/generate_daily_report.py --chatgpt-file <path-to-json> --name "Name" --role "Role" --push
   ```
