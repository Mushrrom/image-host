from flask import Flask

# import routes.index
import routes.image
import routes.api.login
import routes.api.sign_up
import routes.api.upload
import routes.api.image.raw
import routes.api.image.data
import routes.static
app = Flask(__name__)


# app.register_blueprint(routes.index.app)
app.register_blueprint(routes.image.app)
app.register_blueprint(routes.static.app)
app.register_blueprint(routes.api.login.app)
app.register_blueprint(routes.api.sign_up.app)
app.register_blueprint(routes.api.upload.app)
app.register_blueprint(routes.api.image.raw.app)
app.register_blueprint(routes.api.image.data.app)

if __name__ == '__main__':
    app.run(debug=True)  #runs the template/index.html file by default