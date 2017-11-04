"""Google Sheet API file"""
import argparse
import os
import httplib2
from oauth2client import client, tools
from oauth2client.file import Storage
from apiclient import discovery
import pandas

REPORT_SID = "1yCXhEcWtFPLQJG-Llfu4zUOSuqDrGsFF_qc5RA18WgY"
INVENTORY_SID = "1xNS1Z2XJRT_tXaiTUgnVRj4mJ2pvLwhs2EQRLejog88"
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

def get_product_info(service):
    """Get product infomations from Google Sheets 'Inventory'"""
    product_info = service.read_range(INVENTORY_SID, "Inventory!A:H")
    return pandas.DataFrame(product_info[1:], columns=product_info[0])


class GService(object):
    """Create a connection to Google Sheets"""
    def __init__(self):
        self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        self.scopes = "https://www.googleapis.com/auth/spreadsheets"
        self.client_secret_file = "../credentials/client_secret.json"
        self.connect()


    def get_credentials(self):
        """..."""
        store = Storage("../credentials/client_sheet.json")
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.scopes)
            flow.user_agent = "SpreadSheet"
            credentials = tools.run_flow(flow, store, self.flags)
        return credentials


    def connect(self):
        """..."""
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build("Sheets", "v4", http=http)


    def clear(self, sid, range_name):
        """Used for clear Google Sheets content. """
        self.service.spreadsheets().values().clear(spreadsheetId=sid, range=range_name, body={}).execute()


    def delete_range(self, sid, sheet_name):
        """Detele rows"""

        def get_sheetId(self, sid, sheet_name):
            """Get sheetID by sheet_name"""

            data = self.service.spreadsheets().get(spreadsheetId=sid).execute()
            return next((item.get('properties').get('sheetId') for item in data.get('sheets') if item.get('properties').get('title') == sheet_name), None)


        sheet_id = get_sheetId(self, sid, sheet_name)
        request = []
        request.append({
            "deleteDimension": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": 100,
                    "endIndex": 10000
                }
            }
        })
        body = {'requests': request}
        self.service.spreadsheets().batchUpdate(spreadsheetId=sid, body=body).execute()




    def read_single_column(self, sid, range_name):
        """Read a single column, return a list"""
        result = self.service.spreadsheets().values().get(spreadsheetId=sid, range=range_name, majorDimension="COLUMNS").execute()
        values = result.get("values", [])
        return values[0] if values else None


    def read_range(self, sid, range_name):
        """..."""
        result = self.service.spreadsheets().values().get(spreadsheetId=sid, range=range_name).execute()
        return result.get("values", [])


    def write_range(self, sid, range_name, values):
        """..."""
        body = {"values": values}
        self.service.spreadsheets().values().update(spreadsheetId=sid, range=range_name, valueInputOption="USER_ENTERED", body=body).execute()

