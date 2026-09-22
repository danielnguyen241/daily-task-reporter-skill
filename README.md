# Daily Task Reporter Skill

**Tự động đọc toàn bộ cuộc trò chuyện trong ngày của Codex & Antigravity → Lọc sạch task rác/cá nhân → Bắn thẳng vào Google Sheet Daily Task Log của Sếp chỉ với 1 click.**

Sẵn sàng 100% data credential và Webhook Google Apps Script tích hợp sẵn. Thành viên trong team chỉ cần cài đặt là chạy ngay lập tức, không cần cấu hình Google API, OAuth hay token phức tạp.

---

## ⚡ Cài đặt 1-Click cho Team (One-Line Install)

Mở terminal trên macOS và chạy lệnh sau:

```bash
curl -fsSL https://raw.githubusercontent.com/danielnguyen241/daily-task-reporter-skill/main/install.sh | bash
```

*Lệnh trên sẽ tự động cài skill vào cả **Google Antigravity** (`~/.gemini/config/skills/`) và **OpenAI Codex** (`~/.codex/skills/`).*

---

## 🚀 Cách sử dụng hàng ngày

Sau khi cài đặt xong, cuối mỗi ngày bạn chỉ cần mở Codex hoặc Antigravity lên và nhắn một câu:

### Cách 1: Tự động đẩy thẳng vào Google Sheet (Khuyên dùng)
> **"Điền task hôm nay vào sheet"**

AI sẽ tự động:
1. Đọc database cục bộ của Codex & Antigravity trong ngày.
2. Lọc bỏ toàn bộ việc cá nhân, chơi game, tải khóa học ngoài, trao đổi nội bộ nhạy cảm.
3. Chia khung giờ hợp lý bắt đầu từ **09:00 sáng**.
4. Khớp đúng **Category**, **Website/Client** và **Growth Driver** theo chuẩn công ty.
5. Gọi Webhook đẩy thẳng các hàng dữ liệu vào tab `Daily Task Log` trên file Google Sheet mà không bao giờ ghi đè lên hàng của đồng nghiệp.

### Cách 2: Xem trước bảng báo cáo trong chat
> **"Làm task report hôm nay"**

AI sẽ xuất ra bảng Markdown gọn gàng để bạn xem trước hoặc copy thủ công nếu muốn.

---

## 📋 Danh mục và Quy tắc chuẩn hóa

### 1. Giờ làm việc:
* Bắt đầu từ **09:00 sáng**. Không xếp task trước 09:00.
* Khung giờ sáng: `09:00-10:30`, `10:30-12:00`.
* Khung giờ chiều: `13:30-15:30`, `15:30-17:30`.

### 2. Whitelist Categories:
* `SEO`, `Paid Ads`, `Social Media`, `Email Marketing`, `Content Creation`, `Reporting/Analytics`, `Client/Team Meetings`, `Admin/Ops`, `Learning/Training`, `Other`.

### 3. Whitelist Growth Drivers:
* `Traffic Growth`, `Conversion / Sales`, `Retention / Engagement`, `Brand Awareness`, `Skill Building`, `Internal Ops`, `Unclear / Not sure`.

### 4. Whitelist Websites / Clients:
* `Hiagency`, `everydayclean`, `Hairfolli`, `Jaesthetic`, `Biabnails`, `sydneygrannyflat`, `sydneyofficeclean`.

---

## 🔗 Liên kết hệ thống
* **Google Sheet Báo cáo**: [Task report - Daily Task Log](https://docs.google.com/spreadsheets/d/1jjlsI9Wd6HdF97S4uDm1nFlRR7FlMd2RuKX1mZjz7JA/edit?gid=356470169#gid=356470169)
* **Webhook Web App**: `https://script.google.com/macros/s/AKfycbzZr2gghKYzZ7MhcYuKJloHIPBjbucSKZqhbPOc1Qb7DvgZjlfZogFFPaoo3OWs8hFkDg/exec`

---
© 2026 HiAgency Team.
