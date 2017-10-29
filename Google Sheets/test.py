from gs_connect import GService
import pandas


SERVICE = GService()
weekly_list = SERVICE.read_range("1xE4C9pSfhxdhOZ_152S5PuXi31UTwjMVHEMQZByR0hk", "Weekly!A:P")

df = pandas.DataFrame(weekly_list[1:], columns=weekly_list[0])

print(df)
