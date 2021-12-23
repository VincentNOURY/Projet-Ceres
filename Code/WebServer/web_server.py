"""Initialise a webserver for the Ceres-Project"""

import json
import flask


app = flask.Flask(__name__)
app.secret_key = "mykey"

def read_config():

    """
    Description : Reads the json config file and return it's data

    Args : None

    Return : a dictionnary containing the configs
    """

    with open("Config/config.json", 'r', encoding = "utf-8") as file:
        data = json.load(file)
    return data

@app.route("/", methods = ["POST", "GET"])
@app.route("/home", methods = ["GET"])
def home():

    """
    Description : home page of the website

    Location :  /
                /home
    """

    return flask.render_template("index.html")

@app.route("/capteurs", methods = ["POST", "GET"])
def capteurs():

    """
    Description : Sets the capteur's info

    Location : /capteurs

    POST : Writes to Capteurs info/Capteurs.json file

    GET : Displays the page to set the info
    """

    if flask.request.method == "POST":
        with open("Capteurs info/Capteurs.json", 'r', encoding = "utf-8") as file:
            data = json.load(file)
        data2 = {}
        data2[flask.request.form["ID"]] = flask.request.form
        for key,value in data2.items():
            if value != "":
                data[key] = value
        print(data)
        with open("Capteurs info/Capteurs.json", 'w', encoding = "utf-8") as file:
            file.write(json.dumps(data))
        return flask.redirect(flask.url_for('view'))
    if flask.request.method == "GET":
        return flask.render_template('capteurs.html')
    print("Unauthorised")
    return flask.render_template(flask.url_for("home"))

@app.route("/view", methods = ["GET"])
def view():

    """
    Description : Displays the capteur's info

    Location : /view

    GET : Reads the Capteurs info/Capteurs.json file to display it on the /capteurs page
    """

    with open("Capteurs info/Capteurs.json", 'r', encoding = "utf-8") as file:
        data = json.load(file)
    for key in data.keys():
        flask.flash(f"ID capteur : {data[key]['ID']}")
        flask.flash(f"Temperature : {data[key]['temp']}")
        flask.flash(f"Humidite : {data[key]['humidity']}")
    return flask.render_template("view.html")

@app.route("/config", methods = ["GET", "POST"])
def config_page():

    """
    Description : Displays the config info

    Location : /config

    POST : Sets the config

    GET : Reads the Config/Config.json file to display it
    """

    if flask.request.method == "GET":
        config = read_config()
        for key in config.keys():
            flask.flash([f"{key.replace('_', ' ').capitalize()} : ", key, config[key]])
        return flask.render_template("config.html")
    if flask.request.method == "POST":
        config = read_config()
        print(flask.request.form)
        for key in flask.request.form.keys():
            if flask.request.form[key] != "":
                config[key] = flask.request.form[key]
        with open("Config/config.json", 'w', encoding = "utf-8") as file:
            file.write(json.dumps(config))
        return flask.redirect(flask.url_for("config_page"))
    print("Unauthorised")
    return flask.render_template(flask.url_for("home"))


def start():
    app.run()

if __name__ == '__main__':
    start()
