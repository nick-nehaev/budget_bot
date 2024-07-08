from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, FSInputFile, Message
import calendar
import datetime
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

kb_main = [
    [KeyboardButton(text="onspot")],
    [KeyboardButton(text="payments")],
    [KeyboardButton(text="spd")],
    [KeyboardButton(text="graph")],
    [KeyboardButton(text="regular")],
    [KeyboardButton(text="notifications")]
]
main = ReplyKeyboardMarkup(keyboard=kb_main, resize_keyboard=True, input_field_placeholder="Select an action")

kb_spd = [
    [KeyboardButton(text="change")],
    [KeyboardButton(text="back to menu")]
]
spd = ReplyKeyboardMarkup(keyboard=kb_spd, resize_keyboard=True, input_field_placeholder="Select an action")

kb_payments = [
    [KeyboardButton(text="add")],
    [KeyboardButton(text="show all")],
    [KeyboardButton(text="delete")],
    [KeyboardButton(text="back to menu")]
]
payments = ReplyKeyboardMarkup(keyboard=kb_payments, resize_keyboard=True, input_field_placeholder="Select an action")

kb_year = [
    [KeyboardButton(text="2026")],
    [KeyboardButton(text="2025")],
    [KeyboardButton(text="2024")],
    [KeyboardButton(text="2023")],
    [KeyboardButton(text="2022")],
]
year = ReplyKeyboardMarkup(keyboard=kb_year, resize_keyboard=True, input_field_placeholder="Select year")

kb_month = [
    [KeyboardButton(text="January")],
    [KeyboardButton(text="February")],
    [KeyboardButton(text="March")],
    [KeyboardButton(text="April")],
    [KeyboardButton(text="May")],
    [KeyboardButton(text="June")],
    [KeyboardButton(text="July")],
    [KeyboardButton(text="August")],
    [KeyboardButton(text="September")],
    [KeyboardButton(text="October")],
    [KeyboardButton(text="November")],
    [KeyboardButton(text="December")],
]
month = ReplyKeyboardMarkup(keyboard=kb_month, resize_keyboard=True, input_field_placeholder="Select month")


text_calendar = calendar.TextCalendar()
def monthdays(month, year):
    month_dict = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
    if type(month) is str:
        month_num = month_dict[month]
    else: month_num = int(month)
    year = int(year)
    kb_day = []
    for day in text_calendar.itermonthdays(year, month_num):
        if day != 0:
            kb_day.append([KeyboardButton(text=f"{day}")])
    day = ReplyKeyboardMarkup(keyboard=kb_day, resize_keyboard=True, input_field_placeholder="Select day")
    return day

months_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

def day_list(month, year):
    year = int(year)
    month = int(month)
    days = []
    for day in text_calendar.itermonthdays(year, month):
        if day != 0:
            days.append(day)
    return days

def paymentsdel(payments):
    kb_payment = []
    for payment in payments:
        year = payment['year']
        month = payment['month']
        day = payment['day']
        amount = payment['amount']
        kb_payment.append([KeyboardButton(text=f"{day}/{month}/{year}:    {amount}\n")])
    payment = ReplyKeyboardMarkup(keyboard=kb_payment, resize_keyboard=True, input_field_placeholder="Select day")
    return payment

def payment_list(payments):
    payment_list = []
    for payment in payments:
        year = payment['year']
        month = payment['month']
        day = payment['day']
        amount = payment['amount']
        payment_list.append(f"{day}/{month}/{year}:    {amount}")
    return payment_list

kb_plus_minus = [
    [KeyboardButton(text="+")],
    [KeyboardButton(text="-")],
    [KeyboardButton(text="back to menu")]
]
plus_minus = ReplyKeyboardMarkup(keyboard=kb_plus_minus, resize_keyboard=True, input_field_placeholder="Select an action")

def today():
    today = str(date.today())
    today = today.split("-")
    year = int(today[0])
    month = int(today[1])
    day = int(today[2])
    return year, month, day

regular = payments

def alldays():
    kb_alldays = []
    for i in range(1,32):
        kb_alldays.append([KeyboardButton(text=f"{i}")])
    alldays = ReplyKeyboardMarkup(keyboard=kb_alldays, resize_keyboard=True, input_field_placeholder="Select day")
    return alldays

def regulardel(regulars):
    kb_regular = []
    for regular in regulars:
        day = regular['day']
        amount = regular['amount']
        kb_regular.append([KeyboardButton(text=f"{day}:    {amount}\n")])
    regular = ReplyKeyboardMarkup(keyboard=kb_regular, resize_keyboard=True, input_field_placeholder="Select day")
    return regular

def regular_list(regulars):
    regular_list = []
    for regular in regulars:
        day = regular['day']
        amount = regular['amount']
        regular_list.append(f"{day}:    {amount}")
    return regular_list

def adjust_day(year, month, day):
    last_day_of_month = calendar.monthrange(year, month)[1]
    if day > last_day_of_month:
        day = last_day_of_month
    return day

def regular_to_payments(regular, payments):
    current_date = datetime.datetime.now()
    new_payments = []
    for reg in regular:
        day = reg['day']
        amount = reg['amount']
        next_payment_date = current_date.replace(day=adjust_day(current_date.year, current_date.month, day))
        if next_payment_date == current_date:
            new_payment = {
                "year": next_payment_date.year,
                "month": next_payment_date.month,
                "day": next_payment_date.day,
                "amount": amount}
            if new_payment not in payments:
                payments.append(new_payment)
                new_payments.append(new_payment)
    return payments, new_payments

kb_notifications = [
    [KeyboardButton(text="on/off")],
    [KeyboardButton(text="change time")],
    [KeyboardButton(text="back to menu")]
]
notifications = ReplyKeyboardMarkup(keyboard=kb_notifications, resize_keyboard=True, input_field_placeholder="Select an action")

def hours():
    kb_hours = []
    for hour in range(0,24):
        if len(str(hour)) == 1:
            hour = "0"+str(hour)
        kb_hours.append([KeyboardButton(text=f"{hour}:")])
    hours = ReplyKeyboardMarkup(keyboard=kb_hours, resize_keyboard=True, input_field_placeholder="Select an hour")
    return hours
hours_list = ["00:","01:","02:","03:","04:","05:","06:","07:","08:","09:","10:","11:","12:","13:","14:","15:","16:","17:","18:","19:","20:","21:","22:","23:"]

minutes_list = ["00","05","10","15","20","25","30","35","40","45","50","55"]
kb_minutes = []
for minute in minutes_list:
    kb_minutes.append([KeyboardButton(text=f"{minute}")])
minutes = ReplyKeyboardMarkup(keyboard=kb_minutes, resize_keyboard=True, input_field_placeholder="Select minutes")

def last_six_months():
    today = datetime.datetime.today()
    current_month = today.month
    months = []
    months.append(current_month)
    for i in range(1, 6):
        prev_month = (current_month - i) % 12
        if prev_month == 0:
            prev_month = 12
        months.insert(0, prev_month)
    return months

def next_six_months():
    today = datetime.datetime.today()
    current_month = today.month
    months = []
    months.append(current_month)
    for i in range(1, 6):
        next_month = (current_month + i - 1) % 12 + 1
        months.append(next_month)
    return months

def graph_month(last):
    months_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
    kb_graph_month = []
    if last == True:
        months = last_six_months()
    else: 
        months = next_six_months()
    for i in months:
        month_str = months_list[i-1]
        kb_graph_month.append([KeyboardButton(text=f"{month_str}")])
    graph_month = ReplyKeyboardMarkup(keyboard=kb_graph_month, resize_keyboard=True, input_field_placeholder="Select month")
    return graph_month

def graph_month_test(last,month_str):
    month_dict = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
    if last == True:
        months = last_six_months()
    else: 
        months = next_six_months()
    if int(month_dict[month_str]) in months:
        return int(month_dict[month_str])
    else:
        return 0
    
def month_to_date(last, month_int, first_day):
    today = datetime.datetime.today()
    current_month = today.month
    current_year = today.year
    if last:
        if month_int > current_month:
            year = current_year - 1
        else:
            year = current_year
    else:
        if month_int < current_month:
            year = current_year + 1
        else:
            year = current_year
    if first_day:
        return datetime.datetime(year, month_int, 1)
    else:
        last_day = calendar.monthrange(year, month_int)[1]
        return datetime.datetime(year, month_int, last_day)

def create_balance_graph(spd,regular,payments,date_start,date_end):
    payments = sorted(payments, key=lambda x: (x['year'], x['month'], x['day'], x['amount']))
    start_balance = sum(
        payment['amount']
        for payment in payments
        if datetime.datetime(payment['year'], payment['month'], payment['day']) < date_start)
    payments = pd.DataFrame(payment
        for payment in payments
        if date_start <= datetime.datetime(payment['year'], payment['month'], payment['day']) <= date_end)
    payments['date'] = pd.to_datetime(payments[['year', 'month', 'day']])
    payments = payments.groupby('date', as_index=False)['amount'].sum()
    date_range = pd.date_range(start=date_start, end=date_end)
    df_buffer = pd.DataFrame({'date': date_range})
    df_buffer['amount'] = start_balance
    result = pd.merge(df_buffer, payments, on='date', how='left', suffixes=('_df', '_df2'))
    result.fillna({'amount_df2':0}, inplace=True)
    result['last_day_of_month'] = result['date'].apply(lambda x: x.replace(day=calendar.monthrange(x.year, x.month)[1]))
    result['regular'] = float(0)
    result['payment'] = float(0)
    result['spd'] = -spd
    for payment in regular:
        for index, row in result.iterrows():
            day = row['date'].day
            if result.at[index, 'payment'] == 0 and result.at[index, 'amount_df2'] != 0 and result.at[index, 'regular'] == 0:
                result.at[index, 'payment'] = result.at[index, 'amount_df2']
            if day == payment['day']:
                result.at[index, 'amount_df2'] += payment['amount']
                result.at[index, 'regular'] += payment['amount']
            elif payment['day'] > calendar.monthrange(row['date'].year, row['date'].month)[1] and day == calendar.monthrange(row['date'].year, row['date'].month)[1]:
                last_day_index = result.index[result['date'] == row['last_day_of_month']][0]
                result.at[last_day_index, 'amount_df2'] += payment['amount']
                result.at[index, 'regular'] = payment['amount']
    #print(result)
    for i in range(len(result)):
        if result.at[i, 'amount_df2'] != 0 and i != 0:
            result.at[i, 'amount_df'] = float(result.at[i - 1, 'amount_df']) + float(result.at[i, 'amount_df2'])
        elif i > 0:
            result.at[i, 'amount_df'] = float(result.at[i - 1, 'amount_df'])
        result.at[i, 'amount_df'] -= spd
    result.drop(columns=['last_day_of_month'], inplace=True)
    result.rename(columns={'amount_df': 'balance'}, inplace=True)
    result.rename(columns={'amount_df2': 'all_payments'}, inplace=True)

    #result['date'] = result['date'].astype(str)
    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid",context="notebook")
    #fig, ax1 = plt.subplots(figsize=(14, 7))
    #ax2 = ax1.twinx()
    sns.lineplot(data=result, x='date', y='balance', marker="o")#, palette='tab10',hue='regular')
    #sns.barplot(ax=ax1,data=result[result["all_payments"]!=0], x='date', y="all_payments", hue='all_payments', palette="coolwarm")
    plt.title('Balance')
    plt.xlabel('')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('balance_chart.png')
    plt.close()

    #return result