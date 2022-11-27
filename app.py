from flask import render_template
import connexion

import sqlalchemy
from secret import db

engine = sqlalchemy.engine.create_engine(
    "mysql://root:cueva128rata@localhost:3306")


app = connexion.App(__name__, specification_dir="./specifications")  # app = Flask(__name__)
app.add_api("swagger.yml")


debug = True


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=debug)
