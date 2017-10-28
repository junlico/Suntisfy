"""
Search Term Report
Need Down load 'Reports - Advertising Report - Search Term Report'
Multiple files in 'Downloads' directory
"""
import os
import re
import pandas
from gs_connect import DOWNLOAD_DIR
from gs_connect import GService


#Spreadsheets ID for sales representatives
SALES_REP_SID = [
    "1xE4C9pSfhxdhOZ_152S5PuXi31UTwjMVHEMQZByR0hk"
]


def get_report_file_list():
    """Get list of search term report files in Downloads Folder."""
    days = 7    #get one week data
    file_list = os.listdir(DOWNLOAD_DIR)
    report_pattern = r"search-term-report-\d{4}-\d{2}-\d{2}-\d+.txt"
    report_file_list = sorted([f for f in file_list if re.match(report_pattern, f)], reverse=True)
    return report_file_list[:days]

def read_report(file):
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
    print(to_date)
    return ads_df, to_date


def get_df(report_file_list):
    """..."""

    def calculate_df(dataframe):
        """Calculte CPC, ACos and reorder the header"""
        dataframe.loc[dataframe["Clicks"] <= 0, "CPC"] = 0
        dataframe.loc[dataframe["Clicks"] > 0, "CPC"] = (dataframe["Ads Cost"] / dataframe["Clicks"]).round(2)
        dataframe.loc[(dataframe["Same Sales"] + dataframe["Other Sales"]) <= 0, "ACoS"] = 0
        dataframe.loc[(dataframe["Same Sales"] + dataframe["Other Sales"]) > 0, "ACoS"] = (dataframe["Ads Cost"] / (dataframe["Same Sales"] + dataframe["Other Sales"])).round(2)
        reorder = [
            "Campaign Name", "Ad Group Name", "Keyword", "Match Type", "Search Term", "From", "To",
            "Impressions", "Clicks", "Ads Cost", "CPC", "ACoS",
            "Same Transactions", "Same Sales", "Other Transactions", "Other Sales"
        ]
        return dataframe.loc[:, reorder]


    def get_weekly_df(daily_df, from_date, to_date):
        """Calculte weekly_df by sum daily_df"""
        weekly_df = daily_df.drop(["From", "To", "CPC", "ACoS"], axis=1).groupby(["Campaign Name", "Ad Group Name", "Keyword", "Match Type", "Search Term"]).sum().reset_index()
        weekly_df["From"] = from_date
        weekly_df["To"] = to_date
        return calculate_df(weekly_df)


    if not report_file_list:
        print("No Search Term Reports in 'Downloads' Folder.")
    else:
        df_list = []
        curr_df, curr_date = read_report(report_file_list[0])
        to_date = curr_date

        daily_df = curr_df.reset_index()
        daily_df = daily_df.loc[daily_df["From"] == curr_date]

        if not daily_df.empty:
            daily_df["To"] = curr_date
            df_list.append(calculate_df(daily_df))

        for report in report_file_list[1:]:
            prev_df, prev_date = read_report(report)
            daily_df = curr_df.sub(prev_df).dropna().reset_index()

            if not daily_df.empty:
                daily_df["From"] = prev_date
                daily_df["To"] = curr_date
                daily_df = daily_df.loc[daily_df["Impressions"] > 0]
                df_list.append(calculate_df(daily_df))

            curr_df, curr_date = prev_df, prev_date

        daily_df = pandas.concat(df_list)
        weekly_df = get_weekly_df(daily_df, curr_date, to_date)

        return daily_df, weekly_df


def search_term_report(service):
    """
    Main function of 'Search Term Report'
    Get campaign list from 'sid' Settings tab, and uploads data for these compaign.
    """

    daily_df, weekly_df = get_df(get_report_file_list())
    for sid in SALES_REP_SID:
        campaign_list = service.read_single_column(sid, "Settings!A2:A")

        if campaign_list:
            upload_daily = daily_df.loc[daily_df["Campaign Name"].isin(campaign_list)]
            upload_weekly = weekly_df.loc[weekly_df["Campaign Name"].isin(campaign_list)]
            print("Uploading %s ..." % sid)
            if not upload_daily.empty:
                try:
                    service.clear(sid, "Daily!A:P")
                    service.write_range(sid, "Daily!A:P", [upload_daily.columns.tolist()] + upload_daily.values.tolist())
                    print("    Uploading Daily successfully")
                except Exception:
                    print(Exception)

            if not upload_weekly.empty:
                try:
                    service.clear(sid, "Weekly!A:P")
                    service.write_range(sid, "Weekly!A:P", [upload_weekly.columns.tolist()] + upload_weekly.values.tolist())
                    print("    Uploading Weekly successfully")
                except Exception:
                    print(Exception)



if __name__ == "__main__":
    SERVICE = GService()
    search_term_report(SERVICE)
