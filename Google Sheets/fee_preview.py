"""
Fee Preview
Need Down load 'REPORTS - Fulfillment - Fee Preview'
file in 'Downloads' directory
"""
import os
import re
# import datetime
from gs_connect import DOWNLOAD_DIR, REPORT_SID
from gs_connect import get_product_info, GService
import pandas

def get_fee_preview_file(file_list):
    """Get latest fee preview file in 'Downloads' Folder."""
    selected_list = sorted([f for f in file_list if re.match(r"\d+.txt", f)], reverse=True)
    if selected_list:
        for report in selected_list:
            df_header = pandas.read_csv(os.path.join(DOWNLOAD_DIR, report), sep="\t", encoding="ISO-8859-1", nrows=1)
            if df_header.columns.tolist()[19] == "estimated-referral-fee-per-unit":
                return report


def get_prev_fee_preview_data(service):
    """Get previous fee preview data from Google Sheets 'Report'. """
    prev_updates = service.read_range(REPORT_SID, "Fee_Preview!A:F")
    return pandas.DataFrame(prev_updates[1:], columns=prev_updates[0])

'''
def update_fee_preview(service, file_name, product_info_df):
    """..."""
    use_cols = ["asin", "sales-price", "estimated-referral-fee-per-unit", "expected-fulfillment-fee-per-unit"]
    rename = {"estimated-referral-fee-per-unit":"referral", "expected-fulfillment-fee-per-unit":"fulfillment"}
    curr_df = pandas.read_csv(os.path.join(DOWNLOAD_DIR, file_name), sep="\t", encoding="ISO-8859-1", usecols=use_cols).rename(columns=rename)

    prev_updates = service.read_range(REPORT_SID, "Product_Info!A:F")
    prev_df = pandas.DataFrame(prev_updates[1:], columns=prev_updates[0])
    prev_df = pandas.merge(product_info_df.loc[:, ["SID", "ASIN"]], prev_df, how="left", on=["SID", "ASIN"])
    upload_df = pandas.merge(prev_df, curr_df, how="left", left_on=["ASIN"], right_on=["asin"])
    upload_df.loc[pandas.notnull(upload_df["sales-price"]), "Current Price"] = upload_df["sales-price"]
    upload_df.loc[pandas.notnull(upload_df["fulfillment"]), "Fulfillment"] = upload_df["fulfillment"]
    upload_df.loc[pandas.notnull(upload_df["sales-price"]), "Referral %"] = (upload_df["referral"] / upload_df["sales-price"]).round(2)
    upload_df.loc[pandas.notnull(upload_df["sales-price"]), "Update Date"] = datetime.datetime.now().strftime("%m/%d/%Y")
    upload_df = upload_df.loc[:, "SID":"Update Date"].fillna("")
    service.clear(REPORT_SID, "Product_Info!A:F")
    upload_values = [upload_df.columns.tolist()] + upload_df.values.tolist()
    print("Updating Product_Info...")
    service.write_range(REPORT_SID, "Product_Info!A:F", upload_values)
    service.write_range(REPORT_SID, "Product_Info!G1", [[datetime.datetime.now().strftime("%m/%d/%Y")]])
'''

if __name__ == "__main__":
    SERVICE = GService()
    FILE_LIST = os.listdir(DOWNLOAD_DIR)
    print(get_fee_preview_file(FILE_LIST))
    # update_fee_preview(service, file_name)