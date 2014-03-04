import datetime
from operator import itemgetter, attrgetter


class ChartExpense:
    def __init__(self, day=1, month=1, year=1, amount=0):
        self.day = day
        self.month = month
        self.year = year
        self.this_day = datetime.date(year=year, month=month, day=day)
        self.amount = amount

def daily_exp_list(expenses, term="month"):
    exp_list = []
    # initialize list
    today = datetime.date.today()
    for i in range(0, 31):
        new_day = today - datetime.timedelta(days=i)
        new_exp = ChartExpense(new_day.day, new_day.month, new_day.year)
        exp_list.append(new_exp)
    # fill values
    for expense in expenses:
        if term == "month":
            if (today - expense.expense_date).days < 31 and (today - expense.expense_date).days >= 0:
                for some_day in exp_list:
                    if some_day.this_day == expense.expense_date:
                        some_day.amount += expense.amount
    exp_list = sorted(exp_list, key=attrgetter('year', 'month', 'day'))
    return exp_list

def rolling_exp_list(expenses, term="month"):
    exp_list = []
    expenses = sorted(expenses, key=attrgetter('expense_date'))
    total = 0
    # initialize list
    today = datetime.date.today()
    for i in range(0, 31):
        new_day = today - datetime.timedelta(days=i)
        new_exp = ChartExpense(new_day.day, new_day.month, new_day.year)
        exp_list.append(new_exp)
    # fill values
    for expense in expenses:
        if term == "month":
            if (today - expense.expense_date).days < 31 and (today - expense.expense_date).days >= 0:
                total += expense.amount
                for some_day in exp_list:
                    if some_day.this_day == expense.expense_date:
                        some_day.amount = total
    exp_list = sorted(exp_list, key=attrgetter('year', 'month', 'day'))
    # for empty days, fill with previous day value
    old_value = 0
    for some_day in exp_list:
        if some_day.amount == 0:
            some_day.amount = old_value
        else:
            old_value = some_day.amount
    return exp_list
