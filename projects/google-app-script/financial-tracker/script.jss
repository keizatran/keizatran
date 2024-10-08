// Declaration

const ss = SpreadsheetApp.getActiveSpreadsheet();
const transactionSheet = ss.getSheetByName("Transaction");
const databaseSheet = ss.getSheetByName("Financial Database");
const keywords = [
  "Date",
  "Time",
  "Source",
  "Category",
  "Subcategory",
  "Location",
  "Event/Trip",
  "Is Dating",
];

function findValues() {
  // Dynamically find Values next to the keywords (info of Order)

  // Object to store the values next to each keyword
  const valuesNextToKeywords = {};

  // Loop through each keyword
  for (let i = 0; i < keywords.length; i++) {
    const keyword = keywords[i];

    // Use createTextFinder to find the keyword in the sheet
    const textFinder = transactionSheet.createTextFinder(keyword);
    const keywordCell = textFinder.findNext();

    if (keywordCell) {
      // Get the row and column of the keyword
      const row = keywordCell.getRow();
      const column = keywordCell.getColumn();

      // Get the value in the next cell (same row, next column)
      const nextCellValue = transactionSheet
        .getRange(row, column + 1)
        .getValue();

      // Store the value in the object with the keyword as the key
      valuesNextToKeywords[keyword] = nextCellValue;
    } else {
      // If the keyword is not found, store a null or empty value
      valuesNextToKeywords[keyword] = null;
    }
  }

  // Log the results
  // Logger.log("Values next to keywords: " + JSON.stringify(valuesNextToKeywords));
  return valuesNextToKeywords;
}

const data = findValues();
const itemValueStartRow = transactionSheet
  .createTextFinder("Item List")
  .findNext()
  .getRow();
const billValues = transactionSheet.getDataRange().getValues();

function flattenItemValues() {
  const dataToSave = [];

  for (let i = itemValueStartRow; i < billValues.length; i++) {
    const item = billValues[i][2]; // Item in column C
    const price = billValues[i][3] * 1000; // Price in column D
    const quantity = billValues[i][4]; // Quantity in column E
    const isOnMe = billValues[i][5]; // Is On Me in column F

    if (item && price && quantity) {
      // check if item + price + quantity exist
      dataToSave.push([
        data["Date"],
        data["Time"],
        data["Source"],
        data["Category"],
        data["Subcategory"],
        data["Location"],
        item,
        price,
        quantity,
        data["Event/Trip"],
        isOnMe,
        data["Is Dating"],
      ]);
      // dataToSave.push([...Object.values(data), item, price, quantity, isOnMe]); // Parse all values of data dictionary
    }
  }

  // Logger.log(dataToSave);
  return dataToSave;
}

function pushData() {
  const pasteRange = databaseSheet
    .getRange("A1")
    .getNextDataCell(SpreadsheetApp.Direction.DOWN)
    .getRow();
  const dataToSave = flattenItemValues();

  // Append the flattened data to the Database sheet
  if (dataToSave.length > 0) {
    databaseSheet
      .getRange(pasteRange + 1, 1, dataToSave.length, dataToSave[0].length)
      .setValues(dataToSave);
  }

  // Sort Database after inserting
  databaseSheet.getRange("A2:L").sort([
    { column: 1, ascending: false },
    { column: 2, ascending: false },
  ]);

  Logger.log(pasteRange);
}

function clearUnboldCells() {
  // Get the data range
  const range = transactionSheet.getDataRange();
  const values = range.getValues();
  const fontWeights = range.getFontWeights();

  // Loop through all cells
  for (let row = 0; row < values.length; row++) {
    for (let col = 0; col < values[row].length; col++) {
      const cellFontWeight = fontWeights[row][col];

      // Check if the cell's text is not bold
      if (cellFontWeight !== "bold") {
        // Clear the content of the cell if it is not bold
        transactionSheet.getRange(row + 1, col + 1).clearContent();
      }
    }
  }

  Logger.log("Clearing of unbold cells completed.");
}

/**
 * @customfunction
 */

function GENERATE_SHA_UUID(inputArray) {
  return inputArray.map((row) => {
    if (row === "") return ""; // Skip empty rows
    // Ensure the row is treated as a string, and convert it to a byte array
    const byteArray = Utilities.newBlob(row.toString()).getBytes();
    const hash = Utilities.computeDigest(
      Utilities.DigestAlgorithm.MD5,
      byteArray
    );
    // Convert the byte array to a hexadecimal string
    return hash.map((e) => ("0" + (e & 0xff).toString(16)).slice(-2)).join("");
  });
}
