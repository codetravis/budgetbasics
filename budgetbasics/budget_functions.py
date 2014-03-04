import datetime
from operator import itemgetter, attrgetter


class ChartExpense:
    def __init__(self, day=1, month=1, year=1, amount=0):
        self.day = day
        self.month = month
        self.year = year
        self.this_day = datetime.date(year=year, month=month, day=day)
        self.amount = amount

def week_exp_list(expenses, term="week"):
    exp_list = []
    # initialize list
    today = datetime.date.today()
    for i in range(0, 31):
        new_day = today - datetime.timedelta(days=i)
        new_exp = ChartExpense(new_day.day, new_day.month, new_day.year)
        exp_list.append(new_exp)
    # fill values
    for expense in expenses:
        if term == "week":
            if (today - expense.expense_date).days < 31 and (today - expense.expense_date).days >= 0:
                for some_day in exp_list:
                    if some_day.this_day == expense.expense_date:
                        some_day.amount += expense.amount
    exp_list = sorted(exp_list, key=attrgetter('year', 'month', 'day'))
    return exp_list

