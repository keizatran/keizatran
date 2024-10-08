function onEdit(e) {
  const sheet = e.range.getSheet();

  // Check if the edit was made in the "Gym Tracker" sheet
  if (sheet.getName() !== "Gym Tracker") {
    return; // Exit if the sheet is not "Gym Tracker"
  }

  // Check if the edit was made within the range C:G
  const editedColumn = e.range.getColumn();
  if (editedColumn < 3 || editedColumn > 7) {
    return; // Exit if the edit is outside of the range C:G
  }

  // Call the sorting function if conditions are met
  sortByColumns();
}

function sortByColumns() {
  const sheet =
    SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Gym Tracker");
  const range = sheet.getRange("C:G");

  // Sort by Column C (Descending) and Column G (Ascending)
  range.sort([
    { column: 3, ascending: false },
    { column: 7, ascending: true },
  ]);
}

function insertValues() {
  const sheet =
    SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Gym Tracker");

  // Get the last row of the sheet
  const lastRow = sheet.getLastRow();
  const startRow = lastRow + 1;
  const times = lastRow + 7; // input 7 values
  const range = sheet.getRange("C" + startRow + ":C" + times); // lấy last row + số value cần input

  Logger.log(lastRow);
  Logger.log(range.getA1Notation());
  range.setValue(
    Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd")
  );
  sortByColumns();
}
