"""Google Sheet API file"""
import argparse
import httplib2
from oauth2client import client, tools
from oauth2client.file import Storage
from apiclient import discovery

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

if __name__ == "__main__":
    SERVICE = GService()
    SID = "1xNS1Z2XJRT_tXaiTUgnVRj4mJ2pvLwhs2EQRLejog88"
    print(SERVICE.read_range(SID, "Inventory!A:C"))
