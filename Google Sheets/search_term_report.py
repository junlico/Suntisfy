"""
Search Term Report
Need Down load 'Report - Advertising Report - Search Term Report 
Multiple files in 'Downloads' directory
"""
import pandas
import gs_connect
import os
import re
import datetime
import itertools

def sales_rep_sid():
    """Spreadsheets ID for sales representatives"""
    return [
        "1azL-wYpM9kax1vnDkrt3MLjCCL6w53aXF7NFhH3bi5A"
    ]

def get_search_term_report():
    """..."""
    file_list = os.listdir(os.path.join(os.path.expanduser("~"), "Downloads"))
    report_pattern = r"search-term-report-\d{4}-\d{2}-\d{2}-\d+.txt"
    return sorted([f for f in file_list if re.match(report_pattern, f)], reverse=True)

def get_daily_df(report_list):
    """..."""
    def get_date(file_name):
        return datetime.datetime(*map(int, [file_name[19:23], file_name[24:26], file_name[27:29]]))

    report_iter = iter(report_list)
    print(next(report_iter))
    
    for i in report_iter:
        print("yes", i)
        

if __name__ == "__main__":
    fl = get_search_term_report()
    get_daily_df(fl)