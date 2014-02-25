import web


db = web.database(dbn='mysql', user='test', pw='test123', db='budgetbasics')

render = web.template.render('templates/')



urls = (
    '/', 'index',
    '/add_expense', 'add_expense'
)

app = web.application(urls, globals())


class index:
    def GET(self):
        return render.index()

class add_expense:
    def GET(self):
        pass
    def POST(self):
        pass

if __name__ == "__main__":
    app.run()
