# next 4 lines are for deployment with Apache WSGI
#import sys, os
#abspath = os.path.dirname(__file__)
#sys.path.append(abspath)
#os.chdir(abspath)
import web
import datetime
from operator import itemgetter, attrgetter
from budget_functions import *

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


class index:
    def GET(self):
        var_where = "expenses.type = 'Variable'"
        variable_exp = list(db.select('expenses', where=var_where))
        fixed_where = "expenses.type = 'Fixed'"
        fixed_exp = list(db.select('expenses', where=fixed_where))
        var_chart_list = rolling_exp_list(variable_exp)
        fix_chart_list = rolling_exp_list(fixed_exp)
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
