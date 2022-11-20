import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os
from itertools import combinations
from collections import Counter

# importing / reading csv file
# tsk_mstr = pd.read_csv('./Sales_Data/Sales_April_2019.csv')
# creating a dataframe
# tsk_df = pd.DataFrame(tsk_mstr)
# fetching the list of sales data csv files
# sales_data_files = os.listdir("./Sales_Data")
# creating an empty df
# all_months_df = pd.DataFrame()
# for files in sales_data_files:
# tsk_mstr = pd.read_csv('./Sales_Data/'+files)
# all_months_df = pd.concat([all_months_df,tsk_mstr])

# creating a csv files from dataframes
# all_months_df.to_csv("./all_month_data.csv",index=false)

tsk_mstr = pd.read_csv("./all_month_data.csv")
all_months_data = pd.DataFrame(tsk_mstr)
# renaming column names

# tsk_mstr_df["Order Date"] = pd.to_datetime(tsk_mstr_df["Order Date"],format='%Y_%m_%d %H:%M')

# Augment data with additional columns
all_months_data['Month'] = all_months_data['Order Date'].str[0:2]

# Dropping rows having NaN values

all_months_data.dropna(inplace=True)



all_months_data = all_months_data[all_months_data['Order Date'].str[:2]!='Or']

# Converting Month column dtype ton int64
all_months_data['Month'] = all_months_data['Month'].astype('int64')
all_months_data['Price Each'] = all_months_data['Price Each'].astype('float64')
all_months_data['Quantity Ordered'] = all_months_data['Quantity Ordered'].astype('int64')

month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Calculates total sales in each month

# def total_sales_in_month(month,data):
#     temp_df = data[data['Month']==month]
#     net_sales = 0
#     for qty,price in zip(temp_df['Quantity Ordered'],data['Price Each']):
#         x += qty
#         y += price
#         net_sales += qty*price
#     return net_sales

# Prints Total sales of each month and returns a list of sales each month 

# def sales_each_month():
#     sales_each_month = []
#     for _ in range(1,13):
#         print("Net Sales in {}: \u20B9{:,}".format(month[_-1],total_sales_in_month(_,all_months_data)))
#         sales_each_month.append(total_sales_in_month(_,all_months_data))
#     return sales_each_month

# returns best sales amount and month

# def best_sales_in_all_months():
#     best_sales_amount = max(sales_each_month())
#     for x,_ in zip(month,sales_each_month()): 
#         if _==best_sales_amount: best_sales_month = x  
#     result = [best_sales_month,best_sales_amount]
#     return result

# print(f"Best Sales is \u20B9{best_sales_in_all_months()[1]} in the month of {best_sales_in_all_months()[0]}")

# Inserting sales column adjacent to price each 

all_months_data.insert(
    loc=4,
    column='Sales',
    value=all_months_data['Quantity Ordered']*all_months_data['Price Each']
)

# Visulaising Sales data 

results = all_months_data.groupby('Purchase Address').sum()
# ax = plt.figure(figsize=(15,6))
# plt.bar(month,results['Sales'],color='green')
# plt.xlabel("Months")
# plt.ylabel("Sales In Each Month($)")
# plt.title("SALES CHART (2019)")
# plt.show()

# Question:: which city had the highest number of sales

# creating a function to get city name
def get_city(address):
    return address.split(',')[1]

# creating a function ito get state name
def get_state(address):
    return address.split(',')[2].split(' ')[1]

# adding a city column
    
all_months_data['City'] = all_months_data['Purchase Address'].apply(lambda x:f"{get_city(x)} ({get_state(x)})")

city_data = all_months_data.groupby('City').sum()

# city_name = all_months_data['City'].unique()

# city_name = [city for city,_ in all_months_data.groupby('City')]

# Plotting Sales Chart By Each City

# ax = plt.figure(figsize=(10,10))
# plt.bar(city_name,city_data['Sales'],color='green',width=0.3)
# plt.xlabel("Cities")
# plt.xticks(rotation=45)
# plt.ylabel("Sales In Each City($)")
# plt.title("SALES CHART By CITY (2019)")
# plt.show()

def get_time(datetime):
    return datetime.split(' ')[1]

all_months_data['Order Date'] = pd.to_datetime(all_months_data['Order Date'])
all_months_data['Order Hour'] = all_months_data['Order Date'].dt.hour
# order_time_data = all_months_data.groupby('Order Hour').sum()
# hour = [hour for hour,_ in all_months_data.groupby('Order Hour')]

# Plotting Order Chart 

# ax = plt.figure(figsize=(10,10))
# plt.plot(hour,all_months_data.groupby(['Order Hour']).count(),color='green')

# plt.plot(hour,all_months_data.groupby(['Order Hour']).count().to_numpy())
# plt.xlabel("Time(Hours)")
# plt.xticks(hour,rotation=45)
# plt.ylabel("Orders In Each City")
# plt.title("SALES CHART By CITY (2019)")
# plt.grid()
# plt.show()



product_data = all_months_data[all_months_data['Order ID'].duplicated(keep=False)]
print(product_data.head(20))
product_data['Grouped'] = product_data.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
product_data = product_data[['Order ID','Grouped']].drop_duplicates()


count = Counter()

for row in product_data['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))

print(count.most_common(10))