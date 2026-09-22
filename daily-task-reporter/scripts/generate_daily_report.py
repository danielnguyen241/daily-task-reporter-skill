#!/usr/bin/env python3
"""
Daily Task Reporter CLI & Automation Script
Automatically extracts, filters, and synchronizes daily work logs from Codex and Antigravity
to the company master Google Sheet via Google Apps Script Web App.
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

# Master Google Apps Script Web App Endpoint (Pre-authenticated, 0-friction)
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbzZr2gghKYzZ7MhcYuKJloHIPBjbucSKZqhbPOc1Qb7DvgZjlfZogFFPaoo3OWs8hFkDg/exec"

# Master Whitelists
WHITELIST_CLIENTS = [
    "Hiagency",
    "everydayclean",
    "Hairfolli",
    "Jaesthetic",
    "Biabnails",
    "sydneygrannyflat",
    "sydneyofficeclean"
]

WHITELIST_CATEGORIES = [
    "SEO",
    "Paid Ads",
    "Social Media",
    "Email Marketing",
    "Content Creation",
    "Reporting/Analytics",
    "Client/Team Meetings",
    "Admin/Ops",
    "Learning/Training",
    "Other"
]

WHITELIST_GROWTH_DRIVERS = [
    "Traffic Growth",
    "Conversion / Sales",
    "Retention / Engagement",
    "Brand Awareness",
    "Skill Building",
    "Internal Ops",
    "Unclear / Not sure"
]

# Strict blacklist to eliminate personal, training, scraper, or user-excluded tasks
BLACKLIST_PATTERNS = [
    "vanguard",
    "game",
    "whop",
    "video",
    "khóa học",
    "phụ đề",
    "báo cáo chiến dịch",
    "chiến dịch.csv",
    "nguyen hoang tan",
    "cpa mục tiêu",
    "giảm chi phí lại bên adword",
    "campain local",
    "72 lead",
    "tỷ lệ table",
    "copy qua",
    "độ rộng cột",
    "task report",
    "tổng hợp task",
    "sửa lại skill",
    "bỏ cái",
    "cấm từ ddây",
    "m nói ít thôi",
    "codex-clipboard",
    "t k có vi phạm",
    "quyền browser",
    "file pdf á, để t gửi cho anh em",
    "đánh giá thực tế",
    "nhìn theo góc độ của m",
    "tạo thumb feature image",
    "featured image",
    "chuẩn seo (webp"
]

def is_blacklisted(text):
    text_lower = text.lower()
    for pattern in BLACKLIST_PATTERNS:
        if pattern.lower() in text_lower:
            return True
    return False

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
    """Auto-detect user full name from git config or system account."""
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
        'lananh': 'Lan Anh'
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
        
        # Company hours strictly start >= 09:00
        start_hour = max(9, first_dt.hour)
        hour_block = f"{start_hour:02d}:00-{(start_hour + 1):02d}:00"
        
        # Match Client
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
    
    payload = json.dumps({"rows": rows_to_send, "cleanFirstSheetTestRows": True}).encode("utf-8")
    req = urllib.request.Request(WEBAPP_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Generate daily task report from Codex & Antigravity logs.")
    parser.add_argument("--date", type=str, default=None, help="Target date YYYY-MM-DD (defaults to today in VN time)")
    parser.add_argument("--name", type=str, default=None, help="Author name (auto-detected if omitted)")
    parser.add_argument("--role", type=str, default="SEO Specialist", help="Job role title")
    parser.add_argument("--format", type=str, choices=["markdown", "tsv", "json"], default="markdown", help="Output format")
    parser.add_argument("--push", action="store_true", help="Automatically push rows to Google Sheet via Web App")
    args = parser.parse_args()
    
    date_str, start_ms, end_ms, tz_vn = get_day_bounds(args.date)
    author_name = args.name if args.name else detect_user_name()
    
    codex_events = collect_codex_events(start_ms, end_ms, tz_vn)
    ag_events = collect_antigravity_events(date_str, tz_vn)
    
    all_events = codex_events + ag_events
    tasks = group_into_tasks(all_events, date_str, author_name, args.role)
    
    if args.push:
        if tasks:
            res = push_to_sheets(tasks)
            print(f"✅ Đã tự động đẩy {len(tasks)} dòng lên Google Sheet! Kết quả: {res}")
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
