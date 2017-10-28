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

  if (sht_name == "Negative Kewords" && aRow != 1 && aCol == 4) {
    if (value == "") {
      var info = sht.getRange("C1:C2").getValues();

    } else {
      var sht_weekly_view = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Weekly_View");
      var info = sht_weekly_view.getRange("C1:C2").getValues();
      var campaign = info[0][0],
          group = info[1][0];
    }
    sht.getRange(aRow, 1).setValue("YES");
  }
//    if (!isblank) {
//      setNegativePage(sht, aRow);
//    } else {
//
//    }
//
//  }

}




function setNegativePage(sht, aRow, neg_key, clear) {
//  var PDT = Utilities.formatDate(new Date(), "America/Los_Angeles", "M/dd/yyyy");
//  var weekly_view_sht = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Weekly_View");
//  var weekly_view_info = weekly_view_sht.getRange("C1:C2").getValues();
//  var campaign = weekly_view_info[0][0];
//  var group = weekly_view_info[1][0];
//  sht.getRange(aRow, 1, 1, 3).setValues([[PDT, campaign, group]]);



  function test(num) {
    return 2 * num;
  }

  dd = test(5);
  Logger.log(dd);

}