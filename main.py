from flask import Flask
from pages.upload import upload
from pages.view import viewimg
from pages.funstuff import funstuff
from pages.delete import delete
from pages.public import public

from pages.account.create import create
from pages.account.getconfig import getconfig

app = Flask(__name__)
app.register_blueprint(upload)
app.register_blueprint(viewimg)
app.register_blueprint(funstuff)
app.register_blueprint(delete)
app.register_blueprint(public)
app.register_blueprint(create)
app.register_blueprint(getconfig)




# For hosting on the server
if __name__ == "__main__":
        app.run()
