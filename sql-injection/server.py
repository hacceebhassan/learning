from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
import sys
import os
import psycopg2
from datetime import datetime, timezone

# Configuration loading
from config import load_configs, get

load_configs(os.getenv("APP_CONFIG", "resources/config.ini"))

# Setup logging
logging_handler = logging.StreamHandler(sys.stdout)
logging_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
)
logging.getLogger().addHandler(logging_handler)
logging.getLogger().setLevel("INFO")

# App configs
app = Flask(__name__, template_folder="resources/template")
CORS(app)
app.debug = True

# Error handling
class CustomError(Exception):
    def __init__(self, message, status, exception=None):
        Exception.__init__(self)
        self.message = message
        self.status = status
        if exception is not None:
            logging.info(exception)

    def to_dict(self):
        rv = dict()
        rv["message"] = self.message
        rv["status"] = self.status
        return rv


@app.errorhandler(CustomError)
def handle_custom_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    return response


def getConn():
    return psycopg2.connect(
        host=get("DB_HOST"),
        port=get("DB_PORT"),
        database=get("DB_NAME"),
        user=get("DB_USER"),
        password=get("DB_PSW"),
    )


@app.route("/sql-injection", methods=["GET", "POST"])
def sql_injection():
    try:

        conn = getConn()
        cur = conn.cursor()

        if request.method != 'POST':
            sql = (
                "SELECT * FROM "
                + get("DB_NAME")
            )
            cur.execute(sql,)
        else:
            username = request.get_json(force=True)['username']
            #original 
            # sql = (
            #     "SELECT * FROM "
            #     + get("DB_NAME") + " WHERE username ='" + username + "'"
            # )

            # sql = (
            #     "SELECT * FROM " + 
            #     get("DB_NAME") + " WHERE username ='%s'", (username)
            # )
                
                

            # print(sql)

            cur.execute("SELECT * FROM " + get("DB_NAME") + " WHERE username =%s", (username, ))

        users = cur.fetchall()

        logging.info("USERS: " + str(users))
        results=[]
        for user in users:
            _, name, surname, username, __ = user

            results.append({
                'name': name,
                'surname': surname,
                'username': username
            })

        print(results)
        conn.commit()
        cur.close()
        conn.close()

        return render_template(
            "results.html",
            results=results,
        )

    except Exception as e:
        raise CustomError("Cannot get data from backup table", status=500, exception=e)


if __name__ == "__main__":
    app.run(host=get("SERVER_HOST"), port=get("SERVER_PORT"))