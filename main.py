from flask import Flask

import routes.image
import routes.api.user.login
import routes.api.user.sign_up
import routes.api.user.get_images
import routes.api.user.get_collections
import routes.api.upload
import routes.api.image.raw
import routes.api.image.data
import routes.api.image.thumbnail
import routes.static
import routes.api.collection.get_images
import routes.api.collection.add_image
import routes.api.collection.add_user


app = Flask(__name__)


app.register_blueprint(routes.image.app)
app.register_blueprint(routes.static.app)
app.register_blueprint(routes.api.user.login.app)
app.register_blueprint(routes.api.user.sign_up.app)
app.register_blueprint(routes.api.user.get_images.app)
app.register_blueprint(routes.api.user.get_collections.app)
app.register_blueprint(routes.api.upload.app)
app.register_blueprint(routes.api.image.raw.app)
app.register_blueprint(routes.api.image.data.app)
app.register_blueprint(routes.api.image.thumbnail.app)
app.register_blueprint(routes.api.collection.get_images.app)
app.register_blueprint(routes.api.collection.add_image.app)
app.register_blueprint(routes.api.collection.add_user.app)

if __name__ == '__main__':
    app.run(debug=True)  #runs the template/index.html file by default