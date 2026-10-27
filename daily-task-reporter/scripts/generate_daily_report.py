#!/usr/bin/env python3
"""
Daily Task Reporter CLI & Automation Script
Supports:
1. Codex & Antigravity SQLite/JSONL local logs
2. ChatGPT Web JSON export files (for Content/Marketing team like Thảo)
3. Direct 1-click sync to HiAgency Google Sheet via Google Apps Script Web App
"""

import os
import sys
import json
import sqlite3
import datetime
import argparse
import glob
import subprocess
import getpass
import urllib.request

# Master Defaults (can be customized via config.json or environment variables)
DEFAULT_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbzZr2gghKYzZ7MhcYuKJloHIPBjbucSKZqhbPOc1Qb7DvgZjlfZogFFPaoo3OWs8hFkDg/exec"

DEFAULT_CLIENTS = [
    "Hiagency",
    "everydayclean",
    "Hairfolli",
    "Jaesthetic",
    "Biabnails",
    "sydneygrannyflat",
    "sydneyofficeclean"
]

DEFAULT_CATEGORIES = [
    "Content Creation",
    "SEO",
    "Social Media",
    "Email Marketing",
    "Paid Ads",
    "Reporting/Analytics",
    "Client/Team Meetings",
    "Admin/Ops",
    "Learning/Training",
    "Other"
]

DEFAULT_GROWTH_DRIVERS = [
    "Traffic Growth",
    "Conversion / Sales",
    "Retention / Engagement",
    "Brand Awareness",
    "Skill Building",
    "Internal Ops",
    "Unclear / Not sure"
]

def load_config(custom_path=None):
    """
    Load configuration from:
    1. custom_path if provided
    2. ./config.json (current working directory)
    3. config.json in script or repository root
    4. ~/.config/daily-task-reporter/config.json
    5. Fallback to defaults and environment variables
    """
    candidates = []
    if custom_path:
        candidates.append(custom_path)
    candidates.append(os.path.join(os.getcwd(), "config.json"))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(script_dir, "config.json"))
    candidates.append(os.path.join(script_dir, "..", "config.json"))
    candidates.append(os.path.join(script_dir, "..", "..", "config.json"))
    candidates.append(os.path.expanduser("~/.config/daily-task-reporter/config.json"))

    cfg = {}
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    break
            except Exception:
                pass

    webapp_url = os.environ.get("DAILY_TASK_WEBAPP_URL") or cfg.get("webapp_url") or DEFAULT_WEBAPP_URL
    clients = cfg.get("clients") or DEFAULT_CLIENTS
    categories = cfg.get("categories") or DEFAULT_CATEGORIES
    growth_drivers = cfg.get("growth_drivers") or DEFAULT_GROWTH_DRIVERS
    
    return {
        "webapp_url": webapp_url,
        "clients": clients,
        "categories": categories,
        "growth_drivers": growth_drivers,
        "target_sheet_tab": cfg.get("target_sheet_tab", "Daily Task Log")
    }

CONFIG = load_config()
WEBAPP_URL = CONFIG["webapp_url"]
WHITELIST_CLIENTS = CONFIG["clients"]
WHITELIST_CATEGORIES = CONFIG["categories"]
WHITELIST_GROWTH_DRIVERS = CONFIG["growth_drivers"]

BLACKLIST_PATTERNS = [
    "vanguard", "game", "whop", "video đó sẽ tính", "tự động tải",
    "khóa học", "phụ đề", "báo cáo chiến dịch", "chiến dịch.csv",
    "nguyen hoang tan", "cpa mục tiêu", "giảm chi phí lại bên adword",
    "campain local", "72 lead", "tỷ lệ table", "độ rộng cột",
    "task report", "tổng hợp task", "sửa lại skill", "bỏ cái",
    "cấm từ ddây", "m nói ít thôi", "codex-clipboard"
]

def is_blacklisted(text):
    lower = text.lower()
    return any(p in lower for p in BLACKLIST_PATTERNS)

def get_vietnam_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))

def get_day_bounds(date_str=None):
    tz_vn = datetime.timezone(datetime.timedelta(hours=7))
    if not date_str:
        now_vn = get_vietnam_now()
        date_str = now_vn.strftime("%Y-%m-%d")
    
    parts = [int(p) for p in date_str.split("-")]
    start_dt = datetime.datetime(parts[0], parts[1], parts[2], 0, 0, 0, tzinfo=tz_vn)
    end_dt = datetime.datetime(parts[0], parts[1], parts[2], 23, 59, 59, 999999, tzinfo=tz_vn)
    
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)
    return date_str, start_ms, end_ms, tz_vn

def detect_user_name():
    try:
        git_name = subprocess.check_output(['git', 'config', 'user.name'], text=True).strip()
        if git_name and git_name.lower() not in ['github actions', 'root']:
            return git_name
    except Exception:
        pass
    
    username = getpass.getuser()
    mapping = {
        'DatNguyenaddmin': 'Dat Nguyen',
        'datnguyen': 'Dat Nguyen',
        'jayden': 'Jayden',
        'tungvu': 'Tung Vu',
        'lananh': 'Lan Anh',
        'thao': 'Thao',
        'thaonguyen': 'Thao Nguyen'
    }
    return mapping.get(username, username.replace('_', ' ').title())

def collect_codex_events(start_ms, end_ms, tz_vn):
    db_path = os.path.expanduser("~/.codex/thread_history_1.sqlite")
    if not os.path.exists(db_path):
        return []
    
    events = []
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        rows = c.execute("""
            SELECT thread_id, created_at_ms, item_json 
            FROM thread_items 
            WHERE item_type = 'userMessage' 
              AND created_at_ms >= ? 
              AND created_at_ms <= ?
            ORDER BY created_at_ms ASC
        """, (start_ms, end_ms)).fetchall()
        
        for tid, ts_ms, ij in rows:
            try:
                data = json.loads(ij)
                text_parts = [p.get("text", "") for p in data.get("content", []) if p.get("type") == "text"]
                full_text = " ".join(" ".join(text_parts).split())
                if not full_text or is_blacklisted(full_text):
                    continue
                
                dt = datetime.datetime.fromtimestamp(ts_ms / 1000, tz=tz_vn)
                events.append({
                    "source": "Codex",
                    "thread_id": tid,
                    "dt": dt,
                    "text": full_text
                })
            except Exception:
                pass
        conn.close()
    except Exception as e:
        sys.stderr.write(f"Error reading Codex: {e}\n")
    return events

def collect_antigravity_events(date_str, tz_vn):
    transcripts = glob.glob(os.path.expanduser("~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl"))
    events = []
    for tp in transcripts:
        cid = tp.split("/")[-4]
        try:
            with open(tp, "r", encoding="utf-8") as f:
                for line in f:
                    d = json.loads(line)
                    if d.get("type") == "USER_INPUT":
                        ct = d.get("created_at")
                        if ct:
                            dt = datetime.datetime.fromisoformat(ct).astimezone(tz_vn)
                            if dt.strftime("%Y-%m-%d") == date_str:
                                txt = d.get("content", "").replace("<USER_REQUEST>", "").replace("</USER_REQUEST>", "").strip()
                                full_text = " ".join(txt.split())
                                if not full_text or is_blacklisted(full_text):
                                    continue
                                events.append({
                                    "source": "Antigravity",
                                    "thread_id": cid,
                                    "dt": dt,
                                    "text": full_text
                                })
        except Exception:
            pass
    return events

def parse_chatgpt_file(file_path, date_str, author_name, role_name):
    if not os.path.exists(file_path):
        print(f"❌ Không tìm thấy file: {file_path}")
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Lỗi đọc file JSON: {e}")
        return []
    
    items = data if isinstance(data, list) else [data]
    tasks = []
    standard_blocks = [
        "09:00-10:30",
        "10:30-12:00",
        "13:30-15:30",
        "15:30-17:30",
        "17:30-18:30"
    ]
    
    for idx, item in enumerate(items):
        title = item.get("title", "")
        # Extract user prompts
        prompts = []
        mapping = item.get("mapping", {})
        for k, node in mapping.items():
            msg = node.get("message", {})
            if msg and msg.get("author", {}).get("role") == "user":
                parts = msg.get("content", {}).get("parts", [])
                for p in parts:
                    if isinstance(p, str):
                        prompts.append(p.strip())
        
        full_text = f"{title} {' '.join(prompts)}".strip()
        if not full_text or is_blacklisted(full_text):
            continue
        
        text_lower = full_text.lower()
        
        # Match Client
        client = "Hiagency"
        for cl in WHITELIST_CLIENTS:
            if cl.lower() in text_lower:
                client = cl
                break
        if client == "Hiagency":
            if any(w in text_lower for w in ["vệ sinh", "giặt thảm", "lau dọn", "cleaning"]):
                client = "everydayclean"
            elif any(w in text_lower for w in ["tóc", "rụng tóc", "hair", "folli"]):
                client = "Hairfolli"
            elif any(w in text_lower for w in ["thẩm mỹ", "filler", "botox", "jaesthetic"]):
                client = "Jaesthetic"
            elif any(w in text_lower for w in ["nail", "móng", "biab"]):
                client = "Biabnails"
            elif any(w in text_lower for w in ["granny flat", "xây dựng"]):
                client = "sydneygrannyflat"
            elif any(w in text_lower for w in ["office clean", "văn phòng"]):
                client = "sydneyofficeclean"
        
        # Match Category
        category = "Content Creation"
        if any(w in text_lower for w in ["seo", "từ khóa", "keyword", "cluster"]):
            category = "SEO"
        elif any(w in text_lower for w in ["facebook", "tiktok", "instagram", "reels", "social", "fanpage"]):
            category = "Social Media"
        elif any(w in text_lower for w in ["email", "newsletter"]):
            category = "Email Marketing"
        elif any(w in text_lower for w in ["ads", "quảng cáo", "campaign", "cpa"]):
            category = "Paid Ads"
        elif any(w in text_lower for w in ["báo cáo", "report", "analytics"]):
            category = "Reporting/Analytics"
        
        # Match Growth Driver
        driver = "Traffic Growth"
        if category == "Social Media":
            driver = "Brand Awareness"
        elif category == "Email Marketing":
            driver = "Retention / Engagement"
        elif category == "Paid Ads":
            driver = "Conversion / Sales"
        
        # Natural task description
        clean_title = title if title else "Soạn thảo nội dung"
        if category == "Content Creation":
            desc = f"Nghiên cứu tài liệu và soạn thảo bài viết hoàn chỉnh: \"{clean_title}\" cho khách hàng {client}."
        elif category == "Social Media":
            desc = f"Sáng tạo kịch bản video và biên soạn các bài đăng Social Media: \"{clean_title}\" cho {client}."
        elif category == "SEO":
            desc = f"Nghiên cứu bộ từ khóa và xây dựng nội dung chuẩn SEO: \"{clean_title}\" cho {client}."
        else:
            desc = f"Triển khai công việc {category}: \"{clean_title}\" cho khách hàng {client}."
            
        hour_block = standard_blocks[idx % len(standard_blocks)]
        tasks.append({
            "date": date_str,
            "week": "Week 1",
            "name": author_name,
            "role": role_name,
            "hour_block": hour_block,
            "task_desc": desc,
            "category": category,
            "client": client,
            "growth_driver": driver,
            "deep_work": 90,
            "notes": "Đã hoàn thành bản thảo"
        })
        
    return tasks

def group_into_tasks(events, date_str, author_name, role_name):
    if not events:
        return []
    
    events.sort(key=lambda x: x["dt"])
    
    groups = {}
    for ev in events:
        key = f"{ev['source']}_{ev['thread_id']}"
        if key not in groups:
            groups[key] = []
        groups[key].append(ev)
        
    tasks = []
    for key, ev_list in groups.items():
        first_dt = ev_list[0]["dt"]
        all_text = " ".join([e["text"] for e in ev_list])
        
        start_hour = max(9, first_dt.hour)
        hour_block = f"{start_hour:02d}:00-{(start_hour + 1):02d}:00"
        
        client = "Hiagency"
        for cl in WHITELIST_CLIENTS:
            if cl.lower() in all_text.lower():
                client = cl
                break
        
        category = "SEO"
        growth_driver = "Traffic Growth"
        task_desc = ""
        notes = "Chiến dịch phân phối ổn định"
        deep_work = 90
        
        if "jaesthetic" in all_text.lower() or "morning review" in all_text.lower():
            client = "Jaesthetic"
            category = "Paid Ads"
            growth_driver = "Traffic Growth"
            task_desc = "Audit hiệu suất Google Ads J.Aesthetic; trích xuất snapshot Looker Studio và kiểm tra phân phối search terms."
            notes = "Chiến dịch phân phối ổn định"
            deep_work = 90
        elif "topical cluster" in all_text.lower() or "research từ khóa" in all_text.lower() or "shopify" in all_text.lower() or "global" in all_text.lower():
            client = "Hiagency"
            category = "SEO"
            growth_driver = "Traffic Growth"
            task_desc = "Nghiên cứu cụm chủ đề Topical Cluster SEO cho Hiagency; rà soát cấu trúc nội dung, đối chiếu chống cannibalization với bài cũ; lọc từ khóa có search volume Global."
            notes = "Ưu tiên search volume Global để mở rộng traffic"
            deep_work = 95
        else:
            continue
            
        tasks.append({
            "date": date_str,
            "week": "Week 1",
            "name": author_name,
            "role": role_name,
            "hour_block": hour_block,
            "task_desc": task_desc,
            "category": category,
            "client": client,
            "growth_driver": growth_driver,
            "deep_work": deep_work,
            "notes": notes
        })
        
    tasks.sort(key=lambda x: x["hour_block"])
    return tasks

def push_to_sheets(tasks):
    rows_to_send = []
    for t in tasks:
        rows_to_send.append([
            t['date'],
            t['week'],
            t['name'],
            t['role'],
            t['hour_block'],
            t['task_desc'],
            t['category'],
            t['client'],
            t['growth_driver'],
            t['deep_work'],
            t['notes']
        ])
    
    payload = json.dumps({"rows": rows_to_send, "cleanFirstSheetTestRows": False}).encode("utf-8")
    req = urllib.request.Request(WEBAPP_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    global WEBAPP_URL, WHITELIST_CLIENTS, WHITELIST_CATEGORIES, WHITELIST_GROWTH_DRIVERS
    parser = argparse.ArgumentParser(description="Generate daily task report from Codex & Antigravity logs or ChatGPT export.")
    parser.add_argument("--date", type=str, default=None, help="Target date YYYY-MM-DD")
    parser.add_argument("--name", type=str, default=None, help="Author name")
    parser.add_argument("--role", type=str, default=None, help="Job role title")
    parser.add_argument("--chatgpt-file", type=str, default=None, help="Path to ChatGPT JSON export file")
    parser.add_argument("--config", type=str, default=None, help="Path to custom config.json")
    parser.add_argument("--webapp-url", type=str, default=None, help="Override Google Apps Script Web App URL")
    parser.add_argument("--format", type=str, choices=["markdown", "tsv", "json"], default="markdown")
    parser.add_argument("--push", action="store_true", help="Push rows to Google Sheet via Web App")
    args = parser.parse_args()
    
    if args.config or args.webapp_url:
        cfg = load_config(args.config)
        if args.webapp_url:
            cfg["webapp_url"] = args.webapp_url
        WEBAPP_URL = cfg["webapp_url"]
        WHITELIST_CLIENTS = cfg["clients"]
        WHITELIST_CATEGORIES = cfg["categories"]
        WHITELIST_GROWTH_DRIVERS = cfg["growth_drivers"]
    
    date_str, start_ms, end_ms, tz_vn = get_day_bounds(args.date)
    
    if args.chatgpt_file:
        author_name = args.name if args.name else "Thao"
        author_role = args.role if args.role else "Content Specialist"
        tasks = parse_chatgpt_file(args.chatgpt_file, date_str, author_name, author_role)
    else:
        author_name = args.name if args.name else detect_user_name()
        author_role = args.role if args.role else "SEO Specialist"
        codex_events = collect_codex_events(start_ms, end_ms, tz_vn)
        ag_events = collect_antigravity_events(date_str, tz_vn)
        all_events = codex_events + ag_events
        tasks = group_into_tasks(all_events, date_str, author_name, author_role)
    
    if args.push:
        if tasks:
            res = push_to_sheets(tasks)
            print(f"✅ Đã tự động đẩy {len(tasks)} dòng của [{author_name}] lên Google Sheet! Kết quả: {res}")
        else:
            print("⚠️ Không có task hợp lệ nào để đẩy lên Google Sheet.")
    
    if args.format == "markdown":
        if not tasks:
            print("Không tìm thấy task hợp lệ nào trong ngày.")
            return
        
        print("| Date | Week | Name | Role | Hour Block | Task Description | Category | Website / Client | Growth Driver (which KPI does this move?) | Quality / Deep-Work % (0-100, self-rated) | Notes / Blockers |")
        print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |")
        for t in tasks:
            print(f"| `{t['date']}` | {t['week']} | {t['name']} | {t['role']} | {t['hour_block']} | {t['task_desc']} | {t['category']} | {t['client']} | {t['growth_driver']} | {t['deep_work']} | {t['notes']} |")
    elif args.format == "tsv":
        headers = ["Date", "Week", "Name", "Role", "Hour Block", "Task Description", "Category", "Website / Client", "Growth Driver", "Quality", "Notes"]
        print("\t".join(headers))
        for t in tasks:
            row = [t['date'], t['week'], t['name'], t['role'], t['hour_block'], t['task_desc'], t['category'], t['client'], t['growth_driver'], str(t['deep_work']), t['notes']]
            print("\t".join(row))
    elif args.format == "json":
        print(json.dumps(tasks, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
