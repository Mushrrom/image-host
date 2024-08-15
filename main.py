from flask import Flask

import routes.index
import routes.api.login
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.register_blueprint(routes.index.app)
app.register_blueprint(routes.api.login.app)

if __name__ == '__main__':
    app.run(debug=True)  #runs the template/index.html file by default