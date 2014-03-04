# next 4 lines are for deployment with Apache WSGI
#import sys, os
#abspath = os.path.dirname(__file__)
#sys.path.append(abspath)
#os.chdir(abspath)
import web
import datetime
from operator import itemgetter, attrgetter

db = web.database(dbn='mysql', user='test', pw='test123', db='budgetbasics')

# including hasattr in global because by default, templates blocks it
globals()['hasattr'] = hasattr
globals()['str'] = str
render = web.template.render('templates/', base='base', globals=globals())

urls = (
    '/', 'index',
    '/expense_form', 'expense_form',
    '/add_expense', 'add_expense'
)

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

# function to get rolling expenses 
        



class index:
    def GET(self):
        var_where = "expenses.type = 'Variable'"
        variable_exp = list(db.select('expenses', where=var_where))
        fixed_where = "expenses.type = 'Fixed'"
        fixed_exp = list(db.select('expenses', where=fixed_where))
        var_chart_list = week_exp_list(variable_exp)
        fix_chart_list = week_exp_list(fixed_exp)
        return render.index(variable_exp, fixed_exp, var_chart_list, fix_chart_list)

class expense_form:
    def GET(self):
        return render.expense_form()

class add_expense:
    def POST(self):
        form = web.input()
        expense = db.insert('expenses', name=form.exp_name, 
            expense_date=form.exp_date, type=form.exp_type, 
            amount=form.exp_amount)
        raise web.seeother('/')

class rolling_expenses:
    def GET(self):
        return "Rolling Expenses"


app = web.application(urls, globals())
# this condition is for testing
if __name__ == "__main__":
    app.run()

# the following lines are for deployment
#app = web.application(urls, globals(), autoreload=False)
#application = app.wsgifunc()
