import web


db = web.database(dbn='mysql', user='test', pw='test123', db='budgetbasics')
globals = {'hasattr': hasattr}

render = web.template.render('templates/', base='base', globals=globals)

urls = (
    '/', 'index',
    '/expense_form', 'expense_form',
    '/add_expense', 'add_expense'
)

app = web.application(urls, locals())


class index:
    def GET(self):
        var_where = "expenses.type = 'Variable'"
        variable_exp = list(db.select('expenses', where=var_where))
        fixed_where = "expenses.type = 'Fixed'"
        fixed_exp = list(db.select('expenses', where=fixed_where))
         
        return render.index(variable_exp, fixed_exp)

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

if __name__ == "__main__":
    app.run()
