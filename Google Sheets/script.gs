/*
Google Sheet Script
*/
function onEdit() {
  var sht = SpreadsheetApp.getActiveSheet(),
      sht_name = sht.getName();

  var aCell = sht.getActiveCell(),
      value = aCell.getValue(),
      aCol = aCell.getColumn(),
      aRow = aCell.getRow();

  if (sht_name == "Negative Kewords" && aRow != 1 && value) {
    if (aCol == 4) {
      setNegInfo(sht, aRow);
    } else if (aCol == 5) {
      setNote(sht, aRow, value);
    }
  }
}


function setNegInfo(sht, aRow) {
  var PDT = Utilities.formatDate(new Date(), "America/Los_Angeles", "MM/dd/yyyy"),
      sht_weekly_view = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Weekly_View"),
      info = sht_weekly_view.getRange("C1:C2").getValues(),
      campaign = info[0][0],
      group = info[1][0];

  sht.getRange(aRow, 1, 1, 3).setValues([[PDT, campaign, group]]);
}


function setNote(sht, aRow, value) {


  var sht_weekly = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Weekly"),
      data_weekly = sht_weekly.getDataRange().getValues();

  var info = sht.getRange(aRow, 2, 1, 3).getValues();

  var array_weekly_note = [];
  var start, row, len = data_weekly.length;

  var note = (value.indexOf("AM") > -1) ? "AM" : "Negative";
  var match_type = (value.indexOf("EXACT") > -1) ? true : false;
  Logger.log(note);

  for (row = 1; row < len; row++) {
    if (data_weekly[row][0] == info[0][0] && data_weekly[row][1] == info[0][1]) {
      start = row;
      break;
    }
  }

  if (start) {
    if (match_type) {//EXACT
      for (row = start; row < len; row++) {
        if (data_weekly[row][0] == info[0][0] && data_weekly[row][1] == info[0][1]) {
          if (data_weekly[row][4] == info[0][2]) {
            array_weekly_note.push([note]);
          } else array_weekly_note.push([data_weekly[row][16]?data_weekly[row][16]: ""]);
        } else break;
      }
      sht_weekly.getRange(start+1, 17, array_weekly_note.length, 1).setValues(array_weekly_note);
    } else {
      for (row = start; row < len; row++) {
        if (data_weekly[row][0] == info[0][0] && data_weekly[row][1] == info[0][1]) {
          if (data_weekly[row][4].indexOf(info[0][2]) > -1) {
            array_weekly_note.push([note]);
          } else array_weekly_note.push([data_weekly[row][16]?data_weekly[row][16]: ""]);
        } else break;
      }
      sht_weekly.getRange(start+1, 17, array_weekly_note.length, 1).setValues(array_weekly_note);
    }
  }
}
