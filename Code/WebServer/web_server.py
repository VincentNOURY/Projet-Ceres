"""Initialise a webserver for the Ceres-Project"""

#from Capteur.Tout_en_un import arroser
import flask
import json
from logs import log


app = flask.Flask(__name__)
app.secret_key = "mykey"
ARROSAGE_TIMEOUT = 120

def read_config():

    """
    Description : Reads the json config file and return it's data

    Args : None

    Return : a dictionnary containing the configs
    """

    with open("WebServer/Config/config.json", 'r', encoding = "utf-8") as file:
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

    return flask.render_template("accueil.html")

@app.route("/pluie.json", methods = ["GET"])
def pluie():
    return flask.render_template("pluie.json")

@app.route("/temperature.json", methods = ["GET"])
def temperature():
    return flask.render_template("temperature.json")

@app.route("/capteurs", methods = ["POST", "GET"])
def capteurs():

    """
    Description : Sets the capteur's info

    Location : /capteurs

    POST : Writes to Capteurs info/Capteurs.json file

    GET : Displays the page to set the info
    """

    if flask.request.method == "POST":
        log('debug', 'post used')
        with open("WebServer/Capteurs info/Capteurs.json", 'r', encoding = "utf-8") as file:
            data = json.load(file)
        data2 = {}
        data2[flask.request.form["ID"]] = flask.request.form
        for key,value in data2.items():
            if value != "":
                data[key] = value
        log('debug', data)
        with open("WebServer/Capteurs info/Capteurs.json", 'w', encoding = "utf-8") as file:
            file.write(json.dumps(data))
        return flask.redirect(flask.url_for('view'))
    if flask.request.method == "GET":
        return flask.render_template('capteurs.html')
    log('error', "Unauthorised")
    return flask.render_template(flask.url_for("home"))

@app.route("/view", methods = ["GET"])
def view():

    """
    Description : Displays the capteur's info

    Location : /view

    GET : Reads the Capteurs info/Capteurs.json file to display it on the /capteurs page
    """

    with open("WebServer/Capteurs info/Capteurs.json", 'r', encoding = "utf-8") as file:
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
            log('debug', [f"{key.replace('_', ' ').capitalize()} : ", key, config[key]])
            flask.flash([f"{key.replace('_', ' ').capitalize()} : ", key, config[key]])
        return flask.render_template("config.html")
    if flask.request.method == "POST":
        config = read_config()
        log('debug', flask.request.form)
        for key in flask.request.form.keys():
            if flask.request.form[key] != "":
                config[key] = flask.request.form[key]
        with open("WebServer/Config/config.json", 'w', encoding = "utf-8") as file:
            file.write(json.dumps(config))
        return flask.redirect(flask.url_for("config_page"))
    log('error', "Unauthorised")
    return flask.render_template(flask.url_for("home"))

@app.route("/contact", methods = ["GET"])
def contact():
    return flask.render_template("contact.html")

@app.route('/arrosage', methods = ["GET"])
def arrosage():
    arroser(90, ARROSAGE_TIMEOUT)
    return flask.render_template(flask.url_for('home'))

@app.route('/eteindre', methods = ["GET"])
def eteindre():
    arrosage(0, 0)
    return flask.render_template(flask.url_for('home'))

def start():
    app.run()

if __name__ == '__main__':
    start()
