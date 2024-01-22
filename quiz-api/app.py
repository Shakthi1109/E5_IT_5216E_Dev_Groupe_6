from flask import Flask
from flask_cors import CORS

from database_utils import generate_structure
from dependencies import get_db_connection
from routers.admin import admin_page
from routers.users import user_page

app = Flask(__name__)
CORS(app)

app.register_blueprint(admin_page)
app.register_blueprint(user_page)


@app.before_first_request
def setup_db():
    generate_structure(get_db_connection())


@app.route('/')
def main():
    return "Hello world!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
