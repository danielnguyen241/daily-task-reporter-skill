# 📊 HiAgency Daily Task Reporter

**Hệ sinh thái tự động hoá báo cáo công việc hàng ngày (Daily Task Log) cho toàn bộ nhân sự HiAgency.**

Giải pháp hỗ trợ 100% tất cả các đối tượng nhân sự trong công ty:
1. **Nhân sự Kỹ thuật / SEO dùng Codex hoặc Google Antigravity**: Tự động đọc database SQLite cục bộ, đồng bộ qua dòng lệnh / chat prompt.
2. **Nhân sự Content / Social Media dùng ChatGPT trên Trình Duyệt Web (như Thảo)**: Tự động quét lịch sử chat của mục *Today* trên `chatgpt.com` qua Chrome Extension và bắn thẳng vào Google Sheet chỉ với 1 click!

---

## 🎯 Chọn Cách Cài Đặt Phù Hợp

### 🟢 DÀNH CHO NHÂN SỰ DÙNG CHATGPT TRÊN WEB (Thảo, Content, Social...)
*Dành cho các bạn làm việc trực tiếp trên trình duyệt `https://chatgpt.com/*`

#### Bước 1: Tải tiện ích về máy
👉 **[Tải file hiagency-chatgpt-task-reporter.zip tại đây](https://github.com/danielnguyen241/daily-task-reporter-skill/raw/main/dist/hiagency-chatgpt-task-reporter.zip)**
*(Sau khi tải về, bấm chuột phải giải nén ra một thư mục)*.

#### Bước 2: Cài vào Google Chrome (Mất 10 giây)
1. Mở Chrome, gõ vào thanh địa chỉ: `chrome://extensions` (và bấm Enter).
2. Bật công tắc **Chế độ dành cho nhà phát triển (Developer mode)** ở góc trên bên phải.
3. Bấm nút **Tải tiện ích đã giải nén (Load unpacked)** ở góc trên bên trái > Chọn thư mục vừa giải nén.

#### Bước 3: Cách dùng hàng ngày
* Mở trang **https://chatgpt.com** làm việc bình thường.
* Cuối ngày (tầm 17h00 - 17h30), ở góc dưới bên phải màn hình ChatGPT sẽ luôn có nút:
  👉 **[ 📊 Báo Cáo Task Hôm Nay ]**
* Bấm vào nút đó:
  1. Tiện ích sẽ tự động đọc các đoạn chat Thảo đã làm hôm nay.
  2. Tự lọc bỏ chat linh tinh, bóc tách công việc thành từng block từ **09:00 sáng**.
  3. Khớp đúng khách hàng (*Everydayclean, Hiagency, Hairfolli, Jaesthetic, Biabnails...*).
  4. Hiện bảng xem trước để bạn kiểm tra hoặc sửa tên nếu muốn.
  5. Bấm nút **"🚀 Bắn Lên Google Sheet"** là dữ liệu tự động bay thẳng vào Sheet công ty, không bao giờ ghi đè lên dòng của người khác!

---

### 🔵 DÀNH CHO NHÂN SỰ DÙNG CODEX / ANTIGRAVITY (SEO, Dev, Ads...)
*Dành cho nhân sự làm việc trên terminal hoặc môi trường IDE*

#### Cài đặt 1 dòng lệnh (One-line Install):
Mở Terminal trên máy Mac và dán lệnh sau:

```bash
curl -fsSL https://raw.githubusercontent.com/danielnguyen241/daily-task-reporter-skill/main/install.sh | bash
```

#### Cách dùng cuối ngày:
Chỉ cần mở chat Codex hoặc Antigravity và gõ:
> **"Điền task hôm nay vào sheet"**

AI sẽ tự quét lịch sử hội thoại thật, nhận diện Tên nhân sự, chia khung giờ từ 09:00 và bắn thẳng vào Google Sheet.

---

## 📋 Quy Chuẩn Báo Cáo Công Ty Đã Khóa Cứng

1. **Giờ làm việc**: Bắt đầu từ **09:00 sáng**.
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
