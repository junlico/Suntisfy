"""
Search Term Report
Need Down load 'Report - Advertising Report - Search Term Report'
Multiple files in 'Downloads' directory
"""
import os
import re
import datetime
import pandas
import gs_connect


#Spreadsheets ID for sales representatives
SALES_REP_SID = [
    "1azL-wYpM9kax1vnDkrt3MLjCCL6w53aXF7NFhH3bi5A"
]

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

def get_report_file_list():
    """Get list of search term report files in Downloads Folder."""
    file_list = os.listdir(DOWNLOAD_DIR)
    report_pattern = r"search-term-report-\d{4}-\d{2}-\d{2}-\d+.txt"
    return sorted([f for f in file_list if re.match(report_pattern, f)], reverse=True)


def get_df(file):
    """Get DataFrame from file"""
    use_cols = [
        "Campaign Name", "Ad Group Name",
        "Customer Search Term", "Keyword", "Match Type",
        "First Day of Impression", "Last Day of Impression",
        "Impressions", "Clicks", "Total Spend",
        "Same SKU units Ordered within 1-week of click", "Other SKU units Ordered within 1-week of click",
        "Same SKU units Product Sales within 1-week of click", "Other SKU units Product Sales within 1-week of click"
    ]

    rename = {
        "Customer Search Term":"Search Term",
        "First Day of Impression":"From",
        "Last Day of Impression":"To",
        "Average CPC":"CPC",
        "Total Spend": "Ads Cost",
        "Same SKU units Product Sales within 1-week of click":"Same Sales",
        "Same SKU units Ordered within 1-week of click":"Same Transactions",
        "Other SKU units Ordered within 1-week of click":"Other Transactions",
        "Other SKU units Product Sales within 1-week of click":"Other Sales"
    }
    return pandas.read_csv(os.path.join(DOWNLOAD_DIR, file), sep="\t", usecols=use_cols).rename(columns=rename)


def get_daily_df(report_file_list):
    """..."""
    def get_date(file_name):
        """Get date from file name"""
        return datetime.datetime(*map(int, [file_name[19:23], file_name[24:26], file_name[27:29]]))


    assert (report_file_list), "No Search Term Report in 'Downloads' Folder."
    report_iter = iter(report_file_list)
    curr_report = next(report_iter)
    curr_df = get_df(curr_report)
    curr_date = curr_df["To"].max()
    index = ["Campaign Name", "Ad Group Name", "Keyword", "Match Type", "Search Term", "From"]
    print(curr_date)


    for report in report_iter:
        print("yes")

if __name__ == "__main__":
    fl = get_report_file_list()
    get_daily_df(fl)