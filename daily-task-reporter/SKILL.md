---
name: daily-task-reporter
description: Tự động trích xuất, sàng lọc và lập báo cáo công việc hàng ngày (Daily Task Report) từ Codex, Antigravity, hoặc file xuất ChatGPT Web của nhân sự (như Thảo), chuẩn form Google Sheet của sếp.
---

# Daily Task Reporter Skill

Skill này chuyên trách tự động quét và lập bảng **Daily Task Log** hàng ngày cho nhân sự SEO / Digital Marketing / Content từ dữ liệu thực tế tại:
- Codex SQLite database: `~/.codex/thread_history_1.sqlite`
- Antigravity transcripts: `~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl`
- File JSON xuất từ ChatGPT Web của nhân sự (Thảo, Content team): `--chatgpt-file <path>`

## Quy tắc BẮT BUỘC (Strict Rules)

1. **Giờ làm việc công ty (Company Work Hours)**:
   - **Bắt đầu từ 09:00 sáng**. Tuyệt đối KHÔNG xếp task trước 09:00.
   - Khung giờ buổi sáng: `09:00-10:30`, `10:30-12:00`.
   - Nghỉ trưa: `12:00-13:30`.
   - Khung giờ buổi chiều: `13:30-15:30`, `15:30-17:30`.

2. **Đánh giá công việc bằng AI thực thụ (Deep AI Evaluation)**:
   - Đọc kỹ nội dung thực tế của các bài viết, kịch bản, đề tài mà nhân sự đã thực hiện với AI.
   - Viết Task Description tự nhiên, chi tiết, chuyên nghiệp, phản ánh đúng chiều sâu công việc (không dùng câu mẫu rập khuôn).

3. **Bộ lọc loại trừ nghiêm ngặt (Blacklist Filters)**:
   - Bỏ qua toàn bộ task cá nhân, chơi game, fix lỗi hệ thống cá nhân.
   - Bỏ qua toàn bộ script cào tải video, khóa học ngoài, cheat xem video.
   - Bỏ qua các trao đổi nội bộ nhạy cảm về ngân sách, hạ CPA.
   - Bỏ qua các thao tác kỹ thuật lặt vặt (độ rộng cột Sheet, copy-paste).

4. **Whitelist Danh mục (Category)**:
   - `Content Creation`, `SEO`, `Social Media`, `Email Marketing`, `Paid Ads`, `Reporting/Analytics`, `Client/Team Meetings`, `Admin/Ops`, `Learning/Training`, `Other`.

5. **Whitelist Growth Driver**:
   - `Traffic Growth`, `Conversion / Sales`, `Retention / Engagement`, `Brand Awareness`, `Skill Building`, `Internal Ops`, `Unclear / Not sure`.

6. **Whitelist Website / Client**:
   - `Hiagency`, `everydayclean`, `Hairfolli`, `Jaesthetic`, `Biabnails`, `sydneygrannyflat`, `sydneyofficeclean`.

7. **Webhook & Google Sheet Destination**:
   - Web App URL: `https://script.google.com/macros/s/AKfycbzZr2gghKYzZ7MhcYuKJloHIPBjbucSKZqhbPOc1Qb7DvgZjlfZogFFPaoo3OWs8hFkDg/exec`
   - Target Tab: `Daily Task Log`

## Cách dùng

1. **Báo cáo task cho người dùng Codex/Antigravity**:
   > "Điền task hôm nay vào sheet"
   Script: `python3 scripts/generate_daily_report.py --push`

2. **Báo cáo task cho nhân sự dùng ChatGPT Web (Thảo)**:
   Khi nhận được file JSON hoặc text xuất từ ChatGPT của Thảo:
   > "Đọc file chatgpt này và điền task hôm nay cho Thảo vào sheet"
   Script: `python3 scripts/generate_daily_report.py --chatgpt-file <path-to-json> --name "Thảo" --role "Content Specialist" --push`
