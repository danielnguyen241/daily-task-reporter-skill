---
name: daily-task-reporter
description: Tự động trích xuất, sàng lọc và lập báo cáo công việc hàng ngày (Daily Task Report) từ cơ sở dữ liệu hội thoại thực tế của Codex và Antigravity, chuẩn form Google Sheet của sếp. Tích hợp sẵn Webhook tự động bắn thẳng vào Google Sheet 1-click.
---

# Daily Task Reporter Skill

Skill này chuyên trách tự động quét và lập bảng **Daily Task Log** hàng ngày cho nhân sự SEO / Digital Marketing từ dữ liệu thực tế tại:
- Codex SQLite database: `~/.codex/thread_history_1.sqlite`
- Antigravity transcripts: `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl`

## Quy tắc BẮT BUỘC (Strict Rules)

1. **Giờ làm việc công ty (Company Work Hours)**:
   - **Bắt đầu từ 09:00 sáng**. Tuyệt đối KHÔNG xếp task trước 09:00 (kể cả bot chạy lúc 7h-8h sáng thì quy về block bắt đầu từ 09:00).
   - Khung giờ buổi sáng: `09:00-10:30`, `10:30-12:00` (hoặc các block 1 tiếng từ 09:00).
   - Nghỉ trưa: `12:00-13:30`.
   - Khung giờ buổi chiều: `13:30-15:30`, `15:30-17:30`.

2. **Tuyệt đối KHÔNG tự bịa / lấp liếm task (Zero Hallucination / Zero Padding)**:
   - Chỉ ghi nhận những việc thực sự diễn ra trong ngày theo log `created_at_ms` của tin nhắn người dùng.
   - Cấm lấy nhầm phiên làm việc của các ngày trước.

3. **Bộ lọc loại trừ nghiêm ngặt (Blacklist Filters)**:
   - Bỏ qua toàn bộ task cá nhân, chơi game, fix lỗi hệ thống cá nhân.
   - Bỏ qua toàn bộ script cào tải video, khóa học ngoài, cheat xem video (Whop, YouTube...).
   - Bỏ qua các trao đổi nội bộ nhạy cảm về ngân sách, hạ CPA, thảo luận team.
   - Bỏ qua các thao tác kỹ thuật lặt vặt (độ rộng cột Sheet, copy-paste).
   - Bỏ qua các đoạn chat meta về làm task report, chỉnh sửa skill.

4. **Whitelist Danh mục (Bắt buộc chọn đúng 1 trong các giá trị sau)**:
   - `SEO`
   - `Paid Ads`
   - `Social Media`
   - `Email Marketing`
   - `Content Creation`
   - `Reporting/Analytics`
   - `Client/Team Meetings`
   - `Admin/Ops`
   - `Learning/Training`
   - `Other`

5. **Whitelist Growth Driver (Bắt buộc chọn đúng 1 trong các giá trị sau)**:
   - `Traffic Growth`
   - `Conversion / Sales`
   - `Retention / Engagement`
   - `Brand Awareness`
   - `Skill Building`
   - `Internal Ops`
   - `Unclear / Not sure`

6. **Whitelist Website / Client (Bắt buộc chọn đúng 1 trong các site sau)**:
   - `Hiagency`
   - `everydayclean`
   - `Hairfolli`
   - `Jaesthetic`
   - `Biabnails`
   - `sydneygrannyflat`
   - `sydneyofficeclean`

7. **Webhook & Google Sheet Destination**:
   - Web App URL: `https://script.google.com/macros/s/AKfycbzZr2gghKYzZ7MhcYuKJloHIPBjbucSKZqhbPOc1Qb7DvgZjlfZogFFPaoo3OWs8hFkDg/exec`
   - Google Sheet: `https://docs.google.com/spreadsheets/d/1jjlsI9Wd6HdF97S4uDm1nFlRR7FlMd2RuKX1mZjz7JA/edit?gid=356470169#gid=356470169`
   - Target Tab: `Daily Task Log`

## Cách dùng

1. **Xem bảng báo cáo trong chat**:
   > "Tổng hợp task hôm nay" hoặc "Làm task report"

2. **Tự động bắn dữ liệu thẳng vào Google Sheet**:
   > "Điền task hôm nay vào sheet"
   Agent sẽ chạy lệnh: `python3 scripts/generate_daily_report.py --push`
