// HiAgency ChatGPT Daily Task Reporter - Content Script
(function() {
  'use strict';

  const WEBAPP_URL = 'https://script.google.com/macros/s/AKfycbzZr2gghKYzZ7MhcYuKJloHIPBjbucSKZqhbPOc1Qb7DvgZjlfZogFFPaoo3OWs8hFkDg/exec';
  const SHEET_URL = 'https://docs.google.com/spreadsheets/d/1jjlsI9Wd6HdF97S4uDm1nFlRR7FlMd2RuKX1mZjz7JA/edit?gid=356470169#gid=356470169';

  const WHITELIST_CLIENTS = [
    'Hiagency',
    'everydayclean',
    'Hairfolli',
    'Jaesthetic',
    'Biabnails',
    'sydneygrannyflat',
    'sydneyofficeclean'
  ];

  const WHITELIST_CATEGORIES = [
    'Content Creation',
    'SEO',
    'Social Media',
    'Email Marketing',
    'Paid Ads',
    'Reporting/Analytics',
    'Client/Team Meetings',
    'Admin/Ops',
    'Learning/Training',
    'Other'
  ];

  const WHITELIST_GROWTH_DRIVERS = [
    'Traffic Growth',
    'Conversion / Sales',
    'Retention / Engagement',
    'Brand Awareness',
    'Skill Building',
    'Internal Ops',
    'Unclear / Not sure'
  ];

  const BLACKLIST_WORDS = [
    'chào bạn', 'hello', 'hi', 'bạn là ai', 'thời tiết', 'game', 'vanguard',
    'dịch giúp', 'dịch câu này', 'công thức nấu', 'code python lặt vặt'
  ];

  // Inject Floating Button
  function injectFloatingButton() {
    if (document.getElementById('hiagency-reporter-btn')) return;

    const btn = document.createElement('button');
    btn.id = 'hiagency-reporter-btn';
    btn.innerHTML = '📊 <span>Báo Cáo Task Hôm Nay</span>';
    btn.title = 'Tự động quét lịch sử chat hôm nay và đẩy vào Google Sheet';
    btn.addEventListener('click', handleReporterClick);
    document.body.appendChild(btn);
  }

  // Get Today's Date String in Vietnam Time (UTC+7)
  function getVietnamTodayStr() {
    const now = new Date();
    const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000);
    const vnTime = new Date(utcTime + (3600000 * 7));
    const year = vnTime.getFullYear();
    const month = String(vnTime.getMonth() + 1).padStart(2, '0');
    const day = String(vnTime.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  // Handle Button Click
  async function handleReporterClick() {
    const btn = document.getElementById('hiagency-reporter-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ <span>Đang quét chat hôm nay...</span>';
    btn.disabled = true;

    try {
      const tasks = await extractTodayTasks();
      btn.innerHTML = originalText;
      btn.disabled = false;

      if (!tasks || tasks.length === 0) {
        alert('⚠️ Không tìm thấy đoạn chat công việc hợp lệ nào của ngày hôm nay để báo cáo.');
        return;
      }

      showPreviewModal(tasks);
    } catch (err) {
      console.error('Lỗi khi quét chat:', err);
      btn.innerHTML = originalText;
      btn.disabled = false;
      alert('Có lỗi khi quét chat: ' + (err.message || err));
    }
  }

  // Extraction Engine
  async function extractTodayTasks() {
    const todayStr = getVietnamTodayStr();
    let authHeader = {};
    let userName = 'Thao';
    let userRole = 'Content Specialist';

    // 1. Get User Session & Token
    try {
      const sessionRes = await fetch('/api/auth/session', { credentials: 'include' });
      if (sessionRes.ok) {
        const session = await sessionRes.json();
        if (session.accessToken) {
          authHeader = { 'Authorization': `Bearer ${session.accessToken}` };
        }
        if (session.user && session.user.name) {
          userName = session.user.name.split(' ')[0] || session.user.name;
        }
      }
    } catch (e) {
      console.warn('Cannot fetch session, using cookie auth fallback');
    }

    // Try reading saved user config
    if (chrome && chrome.storage && chrome.storage.local) {
      const saved = await chrome.storage.local.get(['userName', 'userRole']);
      if (saved.userName) userName = saved.userName;
      if (saved.userRole) userRole = saved.userRole;
    }

    // 2. Fetch Conversations List
    let convList = [];
    try {
      const convRes = await fetch('/backend-api/conversations?offset=0&limit=28&order=updated', {
        headers: authHeader,
        credentials: 'include'
      });
      if (convRes.ok) {
        const data = await convRes.json();
        convList = data.items || [];
      }
    } catch (e) {
      console.warn('Cannot fetch conversations API, trying DOM fallback:', e);
    }

    // Filter conversations updated today
    let todayConvs = [];
    for (const c of convList) {
      if (!c.update_time) continue;
      const updateDate = new Date(c.update_time);
      const utcTime = updateDate.getTime() + (updateDate.getTimezoneOffset() * 60000);
      const vnDate = new Date(utcTime + (3600000 * 7));
      const cDateStr = `${vnDate.getFullYear()}-${String(vnDate.getMonth() + 1).padStart(2, '0')}-${String(vnDate.getDate()).padStart(2, '0')}`;
      if (cDateStr === todayStr) {
        todayConvs.push(c);
      }
    }

    // Fallback: If API returned empty, scrape sidebar DOM
    if (todayConvs.length === 0) {
      todayConvs = scrapeSidebarTodayChats();
    }

    if (todayConvs.length === 0) {
      return [];
    }

    // Standard Office Hour Blocks starting strictly >= 09:00
    const standardBlocks = [
      '09:00-10:30',
      '10:30-12:00',
      '13:30-15:30',
      '15:30-17:30',
      '17:30-18:30'
    ];

    const tasks = [];
    let blockIndex = 0;

    for (const item of todayConvs) {
      let promptSnippet = '';

      // Try fetching conversation details if ID is available
      if (item.id && authHeader.Authorization) {
        try {
          const detailRes = await fetch(`/backend-api/conversation/${item.id}`, {
            headers: authHeader,
            credentials: 'include'
          });
          if (detailRes.ok) {
            const detail = await detailRes.json();
            promptSnippet = extractUserPromptsFromMapping(detail.mapping);
          }
        } catch (e) {
          // ignore error
        }
      }

      const combinedText = `${item.title || ''} ${promptSnippet}`.trim();
      if (!combinedText || isBlacklisted(combinedText)) {
        continue;
      }

      // Classify Client
      let matchedClient = 'Hiagency';
      const textLower = combinedText.toLowerCase();
      for (const cl of WHITELIST_CLIENTS) {
        if (textLower.includes(cl.toLowerCase())) {
          matchedClient = cl;
          break;
        }
      }
      if (matchedClient === 'Hiagency') {
        if (textLower.includes('vệ sinh') || textLower.includes('cleaning') || textLower.includes('lau dọn')) {
          matchedClient = 'everydayclean';
        } else if (textLower.includes('tóc') || textLower.includes('hair') || textLower.includes('folli')) {
          matchedClient = 'Hairfolli';
        } else if (textLower.includes('thẩm mỹ') || textLower.includes('filler') || textLower.includes('botox') || textLower.includes('jaesthetic')) {
          matchedClient = 'Jaesthetic';
        } else if (textLower.includes('nail') || textLower.includes('móng') || textLower.includes('biab')) {
          matchedClient = 'Biabnails';
        } else if (textLower.includes('granny flat') || textLower.includes('xây dựng')) {
          matchedClient = 'sydneygrannyflat';
        } else if (textLower.includes('office clean') || textLower.includes('văn phòng')) {
          matchedClient = 'sydneyofficeclean';
        }
      }

      // Classify Category
      let matchedCategory = 'Content Creation';
      if (textLower.includes('seo') || textLower.includes('từ khóa') || textLower.includes('keyword') || textLower.includes('cluster') || textLower.includes('backlink')) {
        matchedCategory = 'SEO';
      } else if (textLower.includes('facebook') || textLower.includes('tiktok') || textLower.includes('instagram') || textLower.includes('reels') || textLower.includes('social') || textLower.includes('fanpage')) {
        matchedCategory = 'Social Media';
      } else if (textLower.includes('email') || textLower.includes('newsletter')) {
        matchedCategory = 'Email Marketing';
      } else if (textLower.includes('ads') || textLower.includes('quảng cáo') || textLower.includes('cpa') || textLower.includes('camp')) {
        matchedCategory = 'Paid Ads';
      } else if (textLower.includes('báo cáo') || textLower.includes('report') || textLower.includes('analytics') || textLower.includes('audit')) {
        matchedCategory = 'Reporting/Analytics';
      }

      // Classify Growth Driver
      let matchedDriver = 'Traffic Growth';
      if (matchedCategory === 'Paid Ads') {
        matchedDriver = 'Conversion / Sales';
      } else if (matchedCategory === 'Social Media') {
        matchedDriver = 'Brand Awareness';
      } else if (matchedCategory === 'Email Marketing') {
        matchedDriver = 'Retention / Engagement';
      }

      // Clean task description
      let titleClean = item.title || 'Triển khai công việc nội dung';
      let desc = `Thực hiện soạn thảo và tối ưu nội dung: "${titleClean}" cho khách hàng ${matchedClient}.`;
      if (matchedCategory === 'SEO') {
        desc = `Nghiên cứu và tối ưu SEO nội dung: "${titleClean}" cho ${matchedClient}.`;
      } else if (matchedCategory === 'Social Media') {
        desc = `Sáng tạo kịch bản/nội dung bài đăng Social Media: "${titleClean}" cho ${matchedClient}.`;
      }

      const hourBlock = standardBlocks[blockIndex % standardBlocks.length];
      blockIndex++;

      tasks.push({
        date: todayStr,
        week: 'Week 1',
        name: userName,
        role: userRole,
        hourBlock: hourBlock,
        taskDesc: desc,
        category: matchedCategory,
        client: matchedClient,
        growthDriver: matchedDriver,
        deepWork: 90,
        notes: 'Đã hoàn thành bản thảo'
      });
    }

    return tasks;
  }

  function extractUserPromptsFromMapping(mapping) {
    if (!mapping) return '';
    const prompts = [];
    for (const key in mapping) {
      const node = mapping[key];
      if (node.message && node.message.author && node.message.author.role === 'user') {
        const parts = node.message.content?.parts || [];
        for (const p of parts) {
          if (typeof p === 'string') prompts.push(p);
        }
      }
    }
    return prompts.join(' ').substring(0, 300);
  }

  function scrapeSidebarTodayChats() {
    const list = [];
    const chatLinks = document.querySelectorAll('nav a[href^="/c/"]');
    chatLinks.forEach(a => {
      const title = a.textContent?.trim();
      const href = a.getAttribute('href');
      const id = href ? href.replace('/c/', '') : '';
      if (title && id) {
        list.push({ id, title });
      }
    });
    return list.slice(0, 5); // Take top recent
  }

  function isBlacklisted(text) {
    const lower = text.toLowerCase();
    return BLACKLIST_WORDS.some(w => lower.includes(w));
  }

  // Render Interactive Preview Modal
  function showPreviewModal(tasks) {
    const existing = document.getElementById('hiagency-modal-overlay');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.id = 'hiagency-modal-overlay';

    overlay.innerHTML = `
      <div class="hiagency-modal">
        <div class="hiagency-modal-header">
          <div class="hiagency-modal-title">
            <span>📊</span>
            <span>HiAgency Daily Task Reporter (Hôm nay: ${tasks[0].date})</span>
          </div>
          <button class="hiagency-close-btn" id="hiagency-close-btn">&times;</button>
        </div>
        <div class="hiagency-modal-body">
          <div id="hiagency-toast-container"></div>
          <div class="hiagency-user-inputs">
            <div class="hiagency-input-group">
              <label>Họ và Tên:</label>
              <input type="text" id="hiagency-input-name" value="${tasks[0].name}">
            </div>
            <div class="hiagency-input-group">
              <label>Chức Danh (Role):</label>
              <input type="text" id="hiagency-input-role" value="${tasks[0].role}">
            </div>
          </div>
          <div class="hiagency-table-container">
            <table class="hiagency-tasks-table" id="hiagency-tasks-table">
              <thead>
                <tr>
                  <th>Khung Giờ</th>
                  <th>Mô Tả Công Việc (Task Description)</th>
                  <th>Category</th>
                  <th>Website / Client</th>
                  <th>Growth Driver</th>
                  <th>Deep-Work %</th>
                  <th>Ghi Chú</th>
                  <th>Xóa</th>
                </tr>
              </thead>
              <tbody>
                ${tasks.map((t, idx) => `
                  <tr data-index="${idx}">
                    <td><input type="text" class="task-hour" value="${t.hourBlock}" style="width:90px;"></td>
                    <td><input type="text" class="task-desc" value="${t.taskDesc}"></td>
                    <td>
                      <select class="task-cat">
                        ${WHITELIST_CATEGORIES.map(c => `<option value="${c}" ${c === t.category ? 'selected' : ''}>${c}</option>`).join('')}
                      </select>
                    </td>
                    <td>
                      <select class="task-client">
                        ${WHITELIST_CLIENTS.map(cl => `<option value="${cl}" ${cl === t.client ? 'selected' : ''}>${cl}</option>`).join('')}
                      </select>
                    </td>
                    <td>
                      <select class="task-driver">
                        ${WHITELIST_GROWTH_DRIVERS.map(d => `<option value="${d}" ${d === t.growthDriver ? 'selected' : ''}>${d}</option>`).join('')}
                      </select>
                    </td>
                    <td><input type="number" class="task-quality" value="${t.deepWork}" style="width:60px;"></td>
                    <td><input type="text" class="task-notes" value="${t.notes}" style="width:120px;"></td>
                    <td><button class="hiagency-del-btn" data-del="${idx}">🗑️</button></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
        <div class="hiagency-modal-footer">
          <a href="${SHEET_URL}" target="_blank" class="hiagency-sheet-link">🔗 Mở Google Sheet Daily Task Log</a>
          <div class="hiagency-actions">
            <button class="hiagency-btn-secondary" id="hiagency-cancel-btn">Hủy Bỏ</button>
            <button class="hiagency-btn-primary" id="hiagency-submit-btn">🚀 Bắn Lên Google Sheet</button>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    // Event Listeners
    document.getElementById('hiagency-close-btn').onclick = () => overlay.remove();
    document.getElementById('hiagency-cancel-btn').onclick = () => overlay.remove();

    // Delete Row
    overlay.querySelectorAll('.hiagency-del-btn').forEach(btn => {
      btn.onclick = (e) => {
        const tr = e.target.closest('tr');
        if (tr) tr.remove();
      };
    });

    // Submit Action
    document.getElementById('hiagency-submit-btn').onclick = async () => {
      const submitBtn = document.getElementById('hiagency-submit-btn');
      submitBtn.innerHTML = '⏳ Đang bắn lên Sheet...';
      submitBtn.disabled = true;

      const authorName = document.getElementById('hiagency-input-name').value.trim() || 'Thao';
      const authorRole = document.getElementById('hiagency-input-role').value.trim() || 'Content Specialist';

      // Save user preferences
      if (chrome && chrome.storage && chrome.storage.local) {
        chrome.storage.local.set({ userName: authorName, userRole: authorRole });
      }

      const tableRows = overlay.querySelectorAll('#hiagency-tasks-table tbody tr');
      const rowsToSend = [];

      tableRows.forEach(tr => {
        const hour = tr.querySelector('.task-hour').value.trim();
        const desc = tr.querySelector('.task-desc').value.trim();
        const cat = tr.querySelector('.task-cat').value;
        const client = tr.querySelector('.task-client').value;
        const driver = tr.querySelector('.task-driver').value;
        const quality = parseInt(tr.querySelector('.task-quality').value, 10) || 90;
        const notes = tr.querySelector('.task-notes').value.trim();

        if (desc) {
          rowsToSend.push([
            tasks[0].date,
            'Week 1',
            authorName,
            authorRole,
            hour,
            desc,
            cat,
            client,
            driver,
            quality,
            notes
          ]);
        }
      });

      if (rowsToSend.length === 0) {
        alert('Không có dòng task nào để gửi.');
        submitBtn.innerHTML = '🚀 Bắn Lên Google Sheet';
        submitBtn.disabled = false;
        return;
      }

      try {
        const res = await fetch(WEBAPP_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ rows: rowsToSend, cleanFirstSheetTestRows: false })
        });
        const result = await res.json();

        if (result.status === 'success') {
          const toastContainer = document.getElementById('hiagency-toast-container');
          toastContainer.innerHTML = `
            <div class="hiagency-toast success">
              ✅ Đã điền thành công ${rowsToSend.length} task vào tab Daily Task Log trên Google Sheet!
            </div>
          `;
          submitBtn.innerHTML = '✅ Đã Bắn Thành Công';
          setTimeout(() => {
            overlay.remove();
          }, 3500);
        } else {
          throw new Error(result.message || 'Lỗi từ Google Apps Script');
        }
      } catch (err) {
        console.error('Lỗi khi gửi Google Sheet:', err);
        const toastContainer = document.getElementById('hiagency-toast-container');
        toastContainer.innerHTML = `
          <div class="hiagency-toast error">
            ❌ Lỗi khi gửi dữ liệu: ${err.message}
          </div>
        `;
        submitBtn.innerHTML = '🚀 Bắn Lên Google Sheet';
        submitBtn.disabled = false;
      }
    };
  }

  // Periodic check to inject button if page navigates
  setInterval(injectFloatingButton, 1500);
  injectFloatingButton();

})();
