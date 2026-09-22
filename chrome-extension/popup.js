document.addEventListener('DOMContentLoaded', async () => {
  const SHEET_URL = 'https://docs.google.com/spreadsheets/d/1jjlsI9Wd6HdF97S4uDm1nFlRR7FlMd2RuKX1mZjz7JA/edit?gid=356470169#gid=356470169';
  const nameInput = document.getElementById('userName');
  const roleInput = document.getElementById('userRole');
  const saveBtn = document.getElementById('saveBtn');
  const openChatGptBtn = document.getElementById('openChatGptBtn');
  const openSheetBtn = document.getElementById('openSheetBtn');

  // Load saved config
  const data = await chrome.storage.local.get(['userName', 'userRole']);
  nameInput.value = data.userName || 'Thao';
  roleInput.value = data.userRole || 'Content Specialist';

  // Save config
  saveBtn.addEventListener('click', async () => {
    await chrome.storage.local.set({
      userName: nameInput.value.trim() || 'Thao',
      userRole: roleInput.value.trim() || 'Content Specialist'
    });
    saveBtn.innerText = '✅ Đã Lưu!';
    setTimeout(() => { saveBtn.innerText = '💾 Lưu Cấu Hình'; }, 1500);
  });

  // Open ChatGPT
  openChatGptBtn.addEventListener('click', () => {
    chrome.tabs.create({ url: 'https://chatgpt.com/' });
  });

  // Open Sheet
  openSheetBtn.addEventListener('click', () => {
    chrome.tabs.create({ url: SHEET_URL });
  });
});
