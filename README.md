# 📊 HiAgency Daily Task Reporter

**Hệ sinh thái tự động hoá báo cáo công việc hàng ngày (Daily Task Log) cho toàn bộ nhân sự HiAgency.**

Hỗ trợ 2 luồng công việc tối ưu cho từng nhóm nhân sự:
1. **Dành cho nhân sự Kỹ thuật / SEO (Dùng Codex hoặc Antigravity)**: Tự động đọc database SQLite cục bộ, đồng bộ qua dòng lệnh / chat prompt.
2. **Dành cho nhân sự Content / Marketing (Dùng ChatGPT trên Web như Thảo)**: 1-Click xuất toàn bộ lịch sử chat trong ngày ra file → Đưa vào Codex/Antigravity để AI đánh giá sâu sắc nội dung và tự động bắn vào Google Sheet!

---

## 🟢 1. DÀNH CHO NHÂN SỰ DÙNG CHATGPT TRÊN WEB (Thảo, Content, Social...)

Không cần cài extension phức tạp, chỉ cần dùng nút **Bookmarklet 1-Click**:

### Bước 1: Thêm nút vào trình duyệt Chrome
1. Tải hoặc mở file [`bookmarklet.html`](https://raw.githubusercontent.com/danielnguyen241/daily-task-reporter-skill/main/bookmarklet.html) trên trình duyệt Chrome.
2. Dùng chuột **kéo nút màu xanh "📥 Xuất Chat Hôm Nay" thả lên thanh Dấu trang (Bookmarks bar)** của Chrome.

### Bước 2: Cách dùng cuối mỗi ngày (Mất 3 giây)
1. Đang ở tab **https://chatgpt.com** (trong Project hoặc trang chat làm việc của bạn).
2. Bấm vào nút **"📥 Xuất Chat Hôm Nay"** trên thanh Bookmark.
3. Trình duyệt sẽ tự động tải về file `chatgpt_today_YYYY-MM-DD.json` vào thư mục **Downloads**.
4. Bạn chỉ cần gửi file đó vào nhóm chat (hoặc kéo vào Codex/Antigravity), AI sẽ tự động đọc từng bài viết, phân tích sâu sắc công việc và bắn thẳng vào Google Sheet cho sếp!

---

## 🔵 2. DÀNH CHO NHÂN SỰ DÙNG CODEX / ANTIGRAVITY (SEO, Dev, Ads...)

### Cài đặt 1 dòng lệnh (One-line Install):
Mở Terminal trên máy Mac và dán lệnh sau chạy 1 lần duy nhất:

```bash
curl -fsSL https://raw.githubusercontent.com/danielnguyen241/daily-task-reporter-skill/main/install.sh | bash
```

### Cách dùng cuối ngày:
* **Tự báo cáo cho chính mình**:
  > "Điền task hôm nay vào sheet"
* **Báo cáo hộ cho Thảo từ file ChatGPT**:
  > "Đọc file chatgpt này và điền task hôm nay cho Thảo vào sheet"

---

## 📋 Quy Chuẩn Báo Cáo Đã Khóa Cứng

1. **Giờ làm việc**: Bắt đầu từ **09:00 sáng**. Không xếp task trước 09:00.
   - Buổi sáng: `09:00-10:30`, `10:30-12:00`.
   - Buổi chiều: `13:30-15:30`, `15:30-17:30`.
2. **Whitelist Danh Mục (Category)**:
   - `Content Creation`, `SEO`, `Social Media`, `Email Marketing`, `Paid Ads`, `Reporting/Analytics`, `Client/Team Meetings`, `Admin/Ops`, `Learning/Training`, `Other`.
3. **Whitelist Mục Tiêu Tăng Trưởng (Growth Driver)**:
   - `Traffic Growth`, `Conversion / Sales`, `Retention / Engagement`, `Brand Awareness`, `Skill Building`, `Internal Ops`, `Unclear / Not sure`.
4. **Whitelist Khách Hàng / Website**:
   - `Hiagency`, `everydayclean`, `Hairfolli`, `Jaesthetic`, `Biabnails`, `sydneygrannyflat`, `sydneyofficeclean`.

---

## 🔗 Tài Nguyên Hệ Thống
* **File Báo Cáo**: [Task report - Daily Task Log (Google Sheet)](https://docs.google.com/spreadsheets/d/1jjlsI9Wd6HdF97S4uDm1nFlRR7FlMd2RuKX1mZjz7JA/edit?gid=356470169#gid=356470169)
* **Webhook Endpoint**: `https://script.google.com/macros/s/AKfycbzZr2gghKYzZ7MhcYuKJloHIPBjbucSKZqhbPOc1Qb7DvgZjlfZogFFPaoo3OWs8hFkDg/exec`

---
© 2026 HiAgency Team.
