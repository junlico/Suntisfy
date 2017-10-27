"""
Search Term Report
Need Down load 'Report - Advertising Report - Search Term Report'
Multiple files in 'Downloads' directory
"""
import os
import re
import pandas
import gs_connect
import threading

#Spreadsheets ID for sales representatives
SALES_REP_SID = [
    
]

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

def get_report_file_list():
    """Get list of search term report files in Downloads Folder."""
    days = 7    #get one week date
    file_list = os.listdir(DOWNLOAD_DIR)
    report_pattern = r"search-term-report-\d{4}-\d{2}-\d{2}-\d+.txt"
    report_file_list = sorted([f for f in file_list if re.match(report_pattern, f)], reverse=True)
    return report_file_list[:days]


def read_df_and_date(file):
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

    index = ["Campaign Name", "Ad Group Name", "Keyword", "Match Type", "Search Term", "From"]

    ads_df = pandas.read_csv(os.path.join(DOWNLOAD_DIR, file), sep="\t", encoding="ISO-8859-1", usecols=use_cols).rename(columns=rename)
    to_date = ads_df["To"].max()
    ads_df = ads_df.loc[ads_df["To"] == to_date].set_index(index)
    del ads_df["To"]
    return ads_df, to_date


def get_daily_and_weekly_df(report_file_list):
    """..."""

    def calculate_df(dataframe):
        """Calculte CPC, ACos and reorder the header"""
        dataframe.loc[dataframe["Clicks"] <= 0,"CPC"] = 0
        dataframe.loc[dataframe["Clicks"] > 0, "CPC"] = (dataframe["Ads Cost"] / dataframe["Clicks"]).round(2)
        dataframe.loc[(dataframe["Same Sales"] + dataframe["Other Sales"]) <= 0,"ACoS"] = 0
        dataframe.loc[(dataframe["Same Sales"] + dataframe["Other Sales"]) > 0, "ACoS"] = (dataframe["Ads Cost"] / (dataframe["Same Sales"] + dataframe["Other Sales"])).round(2)
        reorder = [
            "Campaign Name", "Ad Group Name", "Keyword", "Match Type", "Search Term", "From", "To",
            "Impressions", "Clicks", "Ads Cost", "CPC", "ACoS",
            "Same Transactions", "Same Sales", "Other Transactions", "Other Sales"
        ]
        return dataframe.loc[:, reorder]


    assert (report_file_list), "No Search Term Report in 'Downloads' Folder."

    df_list = []
    report_iter = iter(report_file_list)
    curr_df, curr_date = read_df_and_date(next(report_iter))
    to_date = curr_date
    
    daily_df = curr_df.reset_index()
    daily_df = daily_df.loc[daily_df["From"] == curr_date]

    if not daily_df.empty:
        daily_df["To"] = curr_date
        df_list.append(calculate_df(daily_df))

    for report in report_iter:
        prev_df, prev_date = read_df_and_date(report)
        daily_df = curr_df.sub(prev_df).dropna().reset_index()
        
        if not daily_df.empty:
            daily_df["From"] = prev_date
            daily_df["To"] = curr_date
            daily_df = daily_df.loc[daily_df["Impressions"] > 0]
            df_list.append(calculate_df(daily_df))
        
        curr_df, curr_date = prev_df, prev_date

    daily_df = pandas.concat(df_list)
    #Calculte weekly_df by sum daily_df
    weekly_df = daily_df.drop(["From", "To", "CPC", "ACoS"], axis=1).groupby(["Campaign Name", "Ad Group Name", "Keyword", "Match Type", "Search Term"]).sum().reset_index()
    weekly_df["From"] = curr_date
    weekly_df["To"] = to_date

    return daily_df, calculate_df(weekly_df)
    

def upload_ads(service, sid, daily_df, weekly_df):
    """Get campaign list from 'sid' Settings tab, and uploads data for these compaign."""
    campaign_list = service.read_single_column(sid, "Settings!A2:A")
    if campaign_list:
        upload_daily = daily_df.loc[daily_df["Campaign Name"].isin(campaign_list)]
        upload_weekly = weekly_df.loc[weekly_df["Campaign Name"].isin(campaign_list)]
        print("Uploading %s ..." % sid)
        if not upload_daily.empty:
            try:
                service.write_range(sid, "Daily!A:P", [upload_daily.columns.tolist()] + upload_daily.values.tolist())
                print("    Uploading Daily successfully")
            except Exception:
                print(Exception)

        if not upload_weekly.empty:
            try:
                service.write_range(sid, "Weekly!A:P", [upload_weekly.columns.tolist()] + upload_weekly.values.tolist())
                print("    Uploading Weekly successfully")
            except Exception:
                print(Exception)


def search_term_report(service):
    """Main function of 'Search Term Report'"""
    daily_df, weekly_df = get_daily_and_weekly_df(get_report_file_list())

    for sid in SALES_REP_SID:
        upload_ads(service, sid, daily_df, weekly_df)


if __name__ == "__main__":
    service = gs_connect.GService()   
    search_term_report(service)
