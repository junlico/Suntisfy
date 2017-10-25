"""Daily Report file"""
import gs_connect
import pandas
import thread
import time

INVENTORY_SID = "1_3ajuJe5OTPCpzeqJfs_UIbS6q_40Ux9-don-2Kkssk"
REPORT_SID = "1yCXhEcWtFPLQJG-Llfu4zUOSuqDrGsFF_qc5RA18WgY"

def sales_rep_sid():
    """Spreadsheets ID for sales representatives"""
    return [
        "12N8uSPwhfgTGQnnENm3NFtweuaguLmHKxfE7ogjbwzE",
        "1JD5uhCuZOECpdnM4w10iwo2CiY89G17Dqv2QBoXlCPo",
        "1ndoKxpMEtZmBNKTQMkX_vSzMTNhwJ3jAkfFI3mUAooM"
    ]

def uploading_ads():
    """..."""
