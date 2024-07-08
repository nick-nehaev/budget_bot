import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import datetime
import json
from aiogram.filters import *
from aiogram.enums import ParseMode
import kb

API_TOKEN = '5599967571:AAF_oNvUK3Ks66EZ0ZVPYEgiDRMcATkK3Xs'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class botstate(StatesGroup):
    menu = State()
    spd = State()
    spd_change = State()
    payments = State()
    payments_add_year = State()
    payments_add_month = State()
    payments_add_day = State()
    payments_amount = State()
    payments_amount_plus = State()
    payments_amount_minus = State()
    payments_delete = State()
    onspot = State()
    onspot_plus = State()
    onspot_minus = State()
    regular = State()
    regular_add = State()
    regular_amount = State()
    regular_amount_plus = State()
    regular_amount_minus = State()
    regular_delete = State()
    notifications = State()
    notifications_hours = State()
    notifications_minutes = State()
    graph_start = State()
    graph_end = State()

user_data = {}

def load_user_data():
    global user_data
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}

def save_user_data(id):
    user_data[str(id)]['payments'] = sorted(user_data[str(id)]['payments'], key=lambda x: (x['year'], x['month'], x['day'], x['amount']))
    user_data[str(id)]['regular'] = sorted(user_data[str(id)]['regular'], key=lambda x: (x['day'], x['amount']))
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

load_user_data()

def init_user(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            'balance': 0,
            'spd': 0,
            'payments': [],
            'regular': [],
            'notifications':["","off"]
        }
        save_user_data(user_id)

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    init_user(message.from_user.id)
    await message.answer(
        "Welcome to the Budget Bot! You can use the following commands:\n(распишу)",
        reply_markup=kb.main)
    await state.set_state(botstate.menu)
    #await bot.send_message(chat_id=message.from_user.id, text="Select an action:", reply_markup=keyboard_main)

@dp.message(StateFilter(None))
async def no_state(message: Message):
    await message.answer(f"Looks like I was restarted...\n\n"
                     "/start - to wake the bot up")
    
@dp.message(botstate.menu, F.text == "spd")
async def menu_spd(message: Message, state: FSMContext):
    spd = user_data[str(message.from_user.id)]['spd']
    await message.answer(f"Current spd = {spd}\n\nspd options:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.spd)
    await state.set_state(botstate.spd)

@dp.message(botstate.spd, F.text == "change")
async def spd_change(message: Message, state: FSMContext):
    await message.answer("Enter the daily spending (spd).",
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(botstate.spd_change)

@dp.message(botstate.spd, F.text == "back to menu")
async def spd_tomenu(message: Message, state: FSMContext):
    await message.answer("Menu:",
                        reply_markup=kb.main)
    await state.set_state(botstate.menu)

@dp.message(botstate.spd)
async def spd_error(message: Message, state: FSMContext):
    await message.answer("Invalid input",
                        reply_markup=kb.spd)
    await state.set_state(botstate.spd)

@dp.message(botstate.spd_change)
async def spd_change_setvalue(message: Message, state: FSMContext):
    try:
        spd = float(message.text)
        user_data[str(message.from_user.id)]['spd'] = spd
        save_user_data(message.from_user.id)
        await message.answer(f"Daily spending (spd) set to {spd}", reply_markup=kb.main)
        await state.set_state(botstate.menu)
    except ValueError:
        await message.answer("Please enter a valid number.")
        await state.set_state(botstate.spd_change)

@dp.message(botstate.menu, F.text == "payments")
async def menu_payments(message: Message, state: FSMContext):
    await message.answer(f"Payments options:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.payments)
    await state.set_state(botstate.payments)

@dp.message(botstate.payments, F.text == "add")
async def payments_add_year(message: Message, state: FSMContext):
    await message.answer(f"Please select a year for your payments/income.",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.year)
    await state.set_state(botstate.payments_add_year)

@dp.message(botstate.payments_add_year, F.text.in_([str(i) for i in range(2022, 2027)]))
async def payments_add_year_success(message: Message, state: FSMContext):
    year = int(message.text)
    await state.update_data(year=year)
    await message.answer(f"Please select a month for your payments/income.",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.month)
    await state.set_state(botstate.payments_add_month)

@dp.message(botstate.payments_add_year)
async def payments_add_year_error(message: Message, state: FSMContext):
    await message.answer(f"Invalid input",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.year)
    await state.set_state(botstate.payments_add_year)

@dp.message(botstate.payments_add_month, F.text.in_(kb.months_list))
async def payments_add_month_success(message: Message, state: FSMContext):
    month = message.text
    month_int = kb.months_list.index(month)+1
    await state.update_data(month=month_int)
    data = await state.get_data()
    year = data['year']
    await message.answer(f"Please select a day for your payments/income.",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.monthdays(month, year))
    await state.set_state(botstate.payments_add_day)

@dp.message(botstate.payments_add_month)
async def payments_add_month_error(message: Message, state: FSMContext):
    await message.answer(f"Invalid input",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.month)
    await state.set_state(botstate.payments_add_month)

@dp.message(botstate.payments_add_day, F.text.in_([str(i) for i in range(1, 32)]))
async def payments_add_day_success(message: Message, state: FSMContext):
    data = await state.get_data()
    month, year = data['month'], data['year']
    day = int(message.text)
    try:
        if day not in kb.day_list(month, year):
            await message.answer("Enter a valid day.",
                                parse_mode=ParseMode.HTML,
                                reply_markup=kb.monthdays(month, year))
            await state.set_state(botstate.payments_add_day)
        else:
            await state.update_data(day=day)
            await message.answer("Plus or Minus?",
                                parse_mode=ParseMode.HTML,
                                reply_markup=kb.plus_minus)
            await state.set_state(botstate.payments_amount)
    except ValueError:
        await message.answer("Enter a valid day.",
                            parse_mode=ParseMode.HTML,
                            reply_markup=kb.monthdays(month, year))
        await state.set_state(botstate.payments_amount_plus)


@dp.message(botstate.payments_add_day)
async def payments_add_day_error(message: Message, state: FSMContext):
    data = await state.get_data()
    month, year = data['month'], data['year']
    await message.answer(f"Invalid input",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.monthdays(month, year))
    await state.set_state(botstate.payments_add_day)

@dp.message(botstate.payments_amount, F.text == "+")
async def payments_add_value_plus(message: Message, state: FSMContext):
    await message.answer(f"Enter value:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(botstate.payments_amount_plus)

@dp.message(botstate.payments_amount, F.text == "-")
async def payments_add_value_minus(message: Message, state: FSMContext):
    await message.answer(f"Enter value:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(botstate.payments_amount_minus)

@dp.message(botstate.payments_amount, F.text == "back to menu")
async def payments_add_value_tomenu(message: Message, state: FSMContext):
    await message.answer(f"Menu:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.main)
    await state.set_state(botstate.menu)

@dp.message(botstate.payments_amount)
async def payments_add_value_error(message: Message, state: FSMContext):
    await message.answer(f"Invalid input",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.plus_minus)
    await state.set_state(botstate.payments_amount)

@dp.message(botstate.payments_amount_plus)
async def payments_add_value_plus_success(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)
        data = await state.get_data()
        year, month, day = data['year'], data['month'], data['day']
        user_data[str(message.from_user.id)]['payments'].append({
            'year': year, 'month': month, 'day': day, 'amount': amount
        })
        save_user_data(message.from_user.id)
        await message.answer(f"{day}/{month}/{year}:    {amount} was added.", reply_markup=kb.payments)
        await state.set_state(botstate.payments)
    except ValueError:
        await message.answer("Please enter a valid number.")
        await state.set_state(botstate.payments_amount_plus)

@dp.message(botstate.payments_amount_minus)
async def payments_add_value_minus_success(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)*-1
        data = await state.get_data()
        year, month, day = data['year'], data['month'], data['day']
        user_data[str(message.from_user.id)]['payments'].append({
            'year': year, 'month': month, 'day': day, 'amount': amount
        })
        save_user_data(message.from_user.id)
        await message.answer(f"{day}/{month}/{year}:    {amount} was added.", reply_markup=kb.payments)
        await state.set_state(botstate.payments)
    except ValueError:
        await message.answer("Please enter a valid number.")
        await state.set_state(botstate.payments_amount_minus)

@dp.message(botstate.payments, F.text == "show all") # теоретически сюда лучше добавить выбор промежутка времени
async def payments_showall(message: Message, state: FSMContext):
    payment_list = ""
    payments = user_data[str(message.from_user.id)]['payments']
    if payments == []:
        await message.answer(f"No payments to show",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.payments)
        await state.set_state(botstate.payments)
    else:
        for payment in payments:
            year = payment['year']
            month = payment['month']
            day = payment['day']
            amount = payment['amount']
            payment_list += f"{day}/{month}/{year}:    {amount}\n"
        await message.answer(f"{payment_list}",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.payments)
        await state.set_state(botstate.payments)

@dp.message(botstate.payments, F.text == "delete")
async def payments_delete(message: Message, state: FSMContext):
    if user_data[str(message.from_user.id)]['payments'] == []:
        await message.answer(f"No payments to delete",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.payments)
        await state.set_state(botstate.payments)
    else:
        await message.answer(f"Choose payment to delete",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.paymentsdel(user_data[str(message.from_user.id)]['payments']))
        await state.set_state(botstate.payments_delete)

@dp.message(botstate.payments_delete)
async def payments_delete_success(message: Message, state: FSMContext):
    payment = message.text
    if payment not in kb.payment_list(user_data[str(message.from_user.id)]['payments']):
        await message.answer(f"Choose valid payment to delete",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.paymentsdel(user_data[str(message.from_user.id)]['payments']))
        await state.set_state(botstate.payments_delete)
    else: 
        split_payment = payment.split("/")
        split_year_amount = split_payment[2].split(":    ")
        new_list = user_data[str(message.from_user.id)]['payments']
        delete_condition = {"day":int(split_payment[0]),
                            "month":int(split_payment[1]),
                            "year":int(split_year_amount[0]),
                            "amount":float(split_year_amount[1])}
        new_list = [i for i in new_list if i != delete_condition]
        user_data[str(message.from_user.id)]['payments'] = new_list
        save_user_data(message.from_user.id)
        await message.answer(f"{payment}\nwas deleted",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.payments)
        await state.set_state(botstate.payments)

@dp.message(botstate.payments, F.text == "back to menu")
async def payments_tomenu(message: Message, state: FSMContext):
    await message.answer("Menu:",
                        reply_markup=kb.main)
    await state.set_state(botstate.menu)

@dp.message(botstate.menu, F.text == "onspot")
async def menu_onspot(message: Message, state: FSMContext):
    await message.answer(f"Ok",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.plus_minus)
    await state.set_state(botstate.onspot)

@dp.message(botstate.onspot, F.text == "+")
async def onspot_plus(message: Message, state: FSMContext):
    await message.answer(f"Enter value:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(botstate.onspot_plus)

@dp.message(botstate.onspot, F.text == "-")
async def onspot_minus(message: Message, state: FSMContext):
    await message.answer(f"Enter value:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(botstate.onspot_minus)

@dp.message(botstate.onspot, F.text == "back to menu")
async def onspot_tomenu(message: Message, state: FSMContext):
    await message.answer(f"Menu:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.main)
    await state.set_state(botstate.menu)

@dp.message(botstate.onspot)
async def onspot_error(message: Message, state: FSMContext):
    await message.answer(f"Invalid input",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.plus_minus)
    await state.set_state(botstate.onspot)

@dp.message(botstate.onspot_plus)
async def onspot_plus_success(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)
        year, month, day = kb.today()
        user_data[str(message.from_user.id)]['payments'].append({
            'year': year, 'month': month, 'day': day, 'amount': amount
        })
        save_user_data(message.from_user.id)
        await message.answer(f"{day}/{month}/{year}:    {amount}",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.main)
        await state.set_state(botstate.menu)
    except ValueError:
        await message.answer("Please enter a valid number.")
        await state.set_state(botstate.onspot_plus)
    
@dp.message(botstate.onspot_minus)
async def onspot_minus_success(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)*-1
        year, month, day = kb.today()
        user_data[str(message.from_user.id)]['payments'].append({
            'year': year, 'month': month, 'day': day, 'amount': amount
        })
        save_user_data(message.from_user.id)
        await message.answer(f"{day}/{month}/{year}:    {amount}",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.main)
        await state.set_state(botstate.menu)
    except ValueError:
        await message.answer("Please enter a valid number.")
        await state.set_state(botstate.onspot_plus)

@dp.message(botstate.menu, F.text == "regular")
async def menu_regular(message: Message, state: FSMContext):
    await message.answer(f"Regular options:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.regular)
    await state.set_state(botstate.regular)

@dp.message(botstate.regular, F.text == "add")
async def regular_add(message: Message, state: FSMContext):
    await message.answer(f"Please select a day for your regular payments/income.",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.alldays())
    await state.set_state(botstate.regular_add)

@dp.message(botstate.regular_add, F.text.in_([str(i) for i in range(1, 32)]))
async def regular_add_day(message: Message, state: FSMContext):
    day = int(message.text)
    try:
        await state.update_data(rday=day)
        await message.answer("Plus or Minus?",
                            parse_mode=ParseMode.HTML,
                            reply_markup=kb.plus_minus)
        await state.set_state(botstate.regular_amount)
    except ValueError:
        await message.answer("Enter a valid day.",
                            parse_mode=ParseMode.HTML,
                            reply_markup=kb.alldays())
        await state.set_state(botstate.regular_add)

@dp.message(botstate.regular_add)
async def regular_add_error(message: Message, state: FSMContext):
    await message.answer(f"Invalid input",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.alldays())
    await state.set_state(botstate.regular_add)

@dp.message(botstate.regular_amount, F.text == "+")
async def regular_add_value_plus(message: Message, state: FSMContext):
    await message.answer(f"Enter value:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(botstate.regular_amount_plus)

@dp.message(botstate.regular_amount, F.text == "-")
async def regular_add_value_minus(message: Message, state: FSMContext):
    await message.answer(f"Enter value:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(botstate.regular_amount_minus)

@dp.message(botstate.regular_amount, F.text == "back to menu")
async def regular_add_value_tomenu(message: Message, state: FSMContext):
    await message.answer(f"Menu:",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.main)
    await state.set_state(botstate.menu)

@dp.message(botstate.regular_amount)
async def regular_add_value_error(message: Message, state: FSMContext):
    await message.answer(f"Invalid input",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.plus_minus)
    await state.set_state(botstate.regular_amount)

@dp.message(botstate.regular_amount_plus)
async def regular_add_value_plus_success(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)
        data = await state.get_data()
        day = data['rday']
        user_data[str(message.from_user.id)]['regular'].append({
            'day': day, 'amount': amount})
        save_user_data(message.from_user.id)
        await message.answer(f"Every month on {day} day {amount} wil be added.", reply_markup=kb.regular)
        await state.set_state(botstate.regular)
    except ValueError:
        await message.answer("Please enter a valid number.")
        await state.set_state(botstate.regular_amount_plus)

@dp.message(botstate.regular_amount_minus)
async def regular_add_value_minus_success(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)*-1
        data = await state.get_data()
        day = data['rday']
        user_data[str(message.from_user.id)]['regular'].append({
            'day': day, 'amount': amount})
        save_user_data(message.from_user.id)
        await message.answer(f"Every month on {day} day {amount*-1} wil be deducted.", reply_markup=kb.regular)
        await state.set_state(botstate.regular)
    except ValueError:
        await message.answer("Please enter a valid number.")
        await state.set_state(botstate.regular_amount_minus)

@dp.message(botstate.regular, F.text == "show all") # теоретически сюда лучше добавить выбор промежутка времени
async def regular_showall(message: Message, state: FSMContext):
    regular_list = ""
    regulars = user_data[str(message.from_user.id)]['regular']
    if regulars == []:
        await message.answer(f"No regular transactions to show",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.regular)
        await state.set_state(botstate.regular)
    else:
        for regular in regulars:
            day = regular['day']
            amount = regular['amount']
            regular_list += f"{day}:    {amount}\n"
        await message.answer(f"Day     amount\n{regular_list}",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.regular)
        await state.set_state(botstate.regular)

@dp.message(botstate.regular, F.text == "delete")
async def regular_delete(message: Message, state: FSMContext):
    if user_data[str(message.from_user.id)]['regular'] == []:
        await message.answer(f"No regular transactions to delete",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.regular)
        await state.set_state(botstate.regular)
    else:
        await message.answer(f"Choose regular transaction to delete",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.regulardel(user_data[str(message.from_user.id)]['regular']))
        await state.set_state(botstate.regular_delete)

@dp.message(botstate.regular_delete)
async def regular_delete_success(message: Message, state: FSMContext):
    regular = message.text
    if regular not in kb.regular_list(user_data[str(message.from_user.id)]['regular']):
        await message.answer(f"Choose valid regular transaction to delete",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.regulardel(user_data[str(message.from_user.id)]['regular']))
        await state.set_state(botstate.regular_delete)
    else: 
        split_regular = regular.split(":    ")
        new_list = user_data[str(message.from_user.id)]['regular']
        delete_condition = {"day":int(split_regular[0]),
                            "amount":float(split_regular[1])}
        new_list = [i for i in new_list if i != delete_condition]
        user_data[str(message.from_user.id)]['regular'] = new_list
        save_user_data(message.from_user.id)
        await message.answer(f"{regular}\nwas deleted",
                        parse_mode=ParseMode.HTML,
                        reply_markup=kb.regular)
        await state.set_state(botstate.regular)

@dp.message(botstate.regular, F.text == "back to menu")
async def regular_tomenu(message: Message, state: FSMContext):
    await message.answer("Menu:",
                        reply_markup=kb.main)
    await state.set_state(botstate.menu)

@dp.message(botstate.menu, F.text == "notifications")
async def menu_notifications(message: Message, state: FSMContext):
    time = user_data[str(message.from_user.id)]['notifications'][0]
    onoff = user_data[str(message.from_user.id)]['notifications'][1]
    if onoff == "off":
        await message.answer(f"Notifications are {onoff}",
                        reply_markup=kb.notifications)
    else:
        await message.answer(f"Notifications are {onoff} at {time} every day",
                        reply_markup=kb.notifications)
    await state.set_state(botstate.notifications)

@dp.message(botstate.notifications, F.text == "change time")
async def notifications_changetime(message: Message, state: FSMContext):
    await message.answer("Choose hour:",
                        reply_markup=kb.hours())
    await state.set_state(botstate.notifications_hours)

@dp.message(botstate.notifications_hours, F.text.in_(kb.hours_list))
async def notifications_changetime_hours_success(message: Message, state: FSMContext):
    hour = message.text
    await state.update_data(hour=hour)
    await message.answer("Choose minutes:",
                        reply_markup=kb.minutes)
    await state.set_state(botstate.notifications_minutes)

@dp.message(botstate.notifications_hours)
async def notifications_changetime_hours_error(message: Message, state: FSMContext):
    await message.answer("Invalid input",
                        reply_markup=kb.hours())
    await state.set_state(botstate.notifications_hours)

@dp.message(botstate.notifications_minutes, F.text.in_(kb.minutes_list))
async def notifications_changetime_minutes_success(message: Message, state: FSMContext):
    minutes = message.text
    data = await state.get_data()
    hour = data['hour']
    time = str(hour+minutes)
    user_data[str(message.from_user.id)]['notifications'][0] = time
    save_user_data(message.from_user.id)
    await message.answer(f"You will recieve notifications every day at {time}",
                        reply_markup=kb.notifications)
    await state.set_state(botstate.notifications)

@dp.message(botstate.notifications_minutes)
async def notifications_changetime_minutes_error(message: Message, state: FSMContext):
    await message.answer("Invalid input",
                        reply_markup=kb.minutes)
    await state.set_state(botstate.notifications_minutes)




@dp.message(botstate.notifications, F.text == "on/off")
async def notifications_onoff(message: Message, state: FSMContext):
    onoff = user_data[str(message.from_user.id)]['notifications'][1]
    if onoff == "off":
        time = user_data[str(message.from_user.id)]['notifications'][0]
        onoff = "on"
        await message.answer(f"Notifications every day at {time} are on",
                        reply_markup=kb.notifications)
    else:
        onoff = "off"
        await message.answer("Notifications are off",
                        reply_markup=kb.notifications)
    user_data[str(message.from_user.id)]['notifications'][1] = onoff
    save_user_data(message.from_user.id)
    await state.set_state(botstate.notifications)

@dp.message(botstate.notifications, F.text == "back to menu")
async def notifications_tomenu(message: Message, state: FSMContext):
    await message.answer("Menu:",
                        reply_markup=kb.main)
    await state.set_state(botstate.menu)

@dp.message(botstate.notifications)
async def notifications_tomenu(message: Message, state: FSMContext):
    await message.answer("Invalid input",
                        reply_markup=kb.notifications)
    await state.set_state(botstate.notifications)

@dp.message(botstate.menu, F.text == "graph")
async def menu_graph(message: Message, state: FSMContext):
    await message.answer("Choose start month:",
                        reply_markup=kb.graph_month(last=True))
    await state.set_state(botstate.graph_start)

@dp.message(botstate.graph_start)
async def graph_start(message: Message, state: FSMContext):
    month_str = message.text
    try:
        month_int = kb.graph_month_test(last=True,month_str=month_str)
        if month_int != 0:
            await state.update_data(graph_start=month_int)
            await message.answer("Choose end month:",
                            reply_markup=kb.graph_month(last=False))
            await state.set_state(botstate.graph_end)
        else:
            await message.answer("Choose only from these options:",
                            reply_markup=kb.graph_month(last=True))
            await state.set_state(botstate.graph_start)
    except ValueError:
        await message.answer("Invalid input")
        await state.set_state(botstate.graph_start)

@dp.message(botstate.graph_end)
async def graph_end(message: Message, state: FSMContext):
    month_str = message.text
    try:
        month_int = kb.graph_month_test(last=False,month_str=month_str)
        if month_int != 0:
            data = await state.get_data()
            graph_start = data['graph_start']
            graph_end = month_int
            date_start = kb.month_to_date(last=True, month_int=graph_start, first_day=True)
            date_end = kb.month_to_date(last=False, month_int=graph_end, first_day=False)
            #рисуем график
            spd = user_data[str(message.from_user.id)]['spd']
            regular = user_data[str(message.from_user.id)]['regular']
            payments = user_data[str(message.from_user.id)]['payments']
            kb.create_balance_graph(spd,regular,payments,date_start,date_end)
            image = FSInputFile("balance_chart.png")
            await message.answer_photo(image)
            await message.answer(f"Menu:",
                            reply_markup=kb.main)
            await state.set_state(botstate.menu)
        else:
            await message.answer("Choose only from these options:",
                            reply_markup=kb.graph_month(last=False))
            await state.set_state(botstate.graph_end)
    except ValueError:
        await message.answer("Invalid input")
        await state.set_state(botstate.graph_end)

async def check_regular_payments():
    while True:
        now = datetime.datetime.now()
        target_time = now.replace(hour=9, minute=00, second=0, microsecond=0)
        if now > target_time:
            target_time += datetime.timedelta(days=1)
        sleep_duration = (target_time - now).total_seconds()
        await asyncio.sleep(sleep_duration)
        load_user_data()
        for user_id in user_data.keys():
            user_id_str = str(user_id)
            regular = user_data[user_id_str].get('regular', [])
            payments = user_data[user_id_str].get('payments', [])
            updated_payments, new_payments = kb.regular_to_payments(regular, payments)
            user_data[user_id_str]['payments'] = updated_payments
            for payment in new_payments:
                amount = payment['amount']
                if amount < 0:
                    message = f"Regular payment of {amount} was deducted"
                else:
                    message = f"Regular income of {amount} was added"
                await bot.send_message(chat_id=user_id, text=message)
            save_user_data(user_id)

        await asyncio.sleep(1)

async def send_daily_notifications():
    while True:
        now = datetime.datetime.now()
        for user_id in user_data.keys():
            user_id_str = str(user_id)
            notifications = user_data[user_id_str].get('notifications', [])
            notification_time_str = notifications[0]
            notifications_enabled = notifications[1] == "on"
            if notifications_enabled:
                notification_time = datetime.datetime.strptime(notification_time_str, "%H:%M").time()
                target_time = now.replace(hour=notification_time.hour, minute=notification_time.minute, second=0, microsecond=0)
                if now > target_time:
                    target_time += datetime.timedelta(days=1)
                sleep_duration = (target_time - now).total_seconds()
                await asyncio.sleep(sleep_duration)
                today = datetime.datetime.today()
                daily_spending = sum(payment['amount'] for payment in user_data[user_id_str]['payments'] if payment['year'] == today.year and payment['month'] == today.month and payment['day'] == today.day)
                spd = user_data[user_id_str]['spd']
                balance = sum(
                    payment['amount']
                    for payment in user_data[user_id_str]['payments']
                    if datetime.datetime(int(payment['year']), int(payment['month']), int(payment['day'])) <= today)
                message = (
                    f"Current balance: {balance}\n"
                    f"Today's spending: {daily_spending}\n"
                    f"Your spd: {spd}")
                await bot.send_message(chat_id=user_id, text=message)
        await asyncio.sleep(60)

async def main(bot):
    asyncio.create_task(check_regular_payments())
    asyncio.create_task(send_daily_notifications())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main(bot))











