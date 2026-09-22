function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var data = JSON.parse(e.postData.contents);
    
    // Tìm đúng tab "Daily Task Log"
    var sheet = ss.getSheetByName("Daily Task Log") || ss.getSheetByName("Task report") || ss.getActiveSheet();
    
    // Tự động xóa dòng test lỡ vào nhầm tab đầu tiên
    if (data.cleanFirstSheetTestRows) {
      var firstSheet = ss.getSheets()[0];
      var lastR = firstSheet.getLastRow();
      if (lastR >= 4 && firstSheet.getName() !== "Daily Task Log") {
        firstSheet.deleteRows(lastR - 3, 4);
      }
    }
    
    var rows = data.rows || [];
    for (var i = 0; i < rows.length; i++) {
      sheet.appendRow(rows[i]);
    }
    return ContentService.createTextOutput(JSON.stringify({ status: "success", count: rows.length }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
