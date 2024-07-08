# budget_bot
Simple yet powerful telegram bot for budget tracking

A few days ago I sat and calculated in my head my upcoming expenses that I would incur during my vacation. Taking into account all income/expenses, counting long-term expenses, etc. always drove me crazy. I thought it would be nice to have a lightweight app that would allow me to record my expenses on the go and also quickly predict my balance in 1, 3 or 6 months.

To do this, I decided to use the functionality of telegram bots. What you can find in this repository is the first fully working version of the bot. When writing the bot, I followed my own application requirements. I hate using what the app stores offer. First of all, because to collect full statistics and make all your payments you need to log into a separate application every day. In addition, not all of them have the functionality that I would like to have.

## Bot functionality

- the ability to enter data on expenses/income for any day 
- a separate opportunity to make expenses “on the go”, they are immediately recorded on the day
- the ability to specify "spd" - expenditure per day, an approximate arbitrary number for calculations
- the ability to add regular payments, which, upon reaching a certain date, will be included in expenses/income
- setting up daily reminders about daily expenses and balance status
- the cherry on the cake is the ability to create graphs that take into account all entries made about income/expenses in the past and future, as well as all regular payments and 'spd'

## Usage
copy files main.py and kb.py to the same directory and add your bot API to the main.py file. That's all :)

## P.S.
I strongly welcome any additions or changes to the code. The first version of the application I downloaded is still far from ideal
