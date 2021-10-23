import flask, json


nb_capteurs = 1
app = flask.Flask(__name__)
app.secret_key = "mykey"

def read_config():
    with open(f"Config/config.json") as file:
        data = json.load(file)
    return data

@app.route("/", methods = ["POST", "GET"])
@app.route("/home", methods = ["POST", "GET"])
def home():
    return flask.render_template("index.html")

@app.route("/capteurs", methods = ["POST", "GET"])
def capteurs():
    if flask.request.method == "POST":
        with open(f"Capteurs info/Capteurs.json") as file:
            data = json.load(file)
        data2 = {}
        data2[flask.request.form["ID"]] = flask.request.form
        for key in data2.keys():
            if data2[key] != "":
                data[key] = data2[key]
        print(data)
        with open(f"Capteurs info/Capteurs.json", 'w') as file:
            file.write(json.dumps(data))
        return flask.redirect(flask.url_for('view'))
    if flask.request.method == "GET":
        return flask.render_template('capteurs.html')

@app.route("/view", methods = ["GET"])
def view():
    with open(f"Capteurs info/Capteurs.json") as file:
        data = json.load(file)
        for key in data.keys():
            flask.flash(f"ID capteur : {data[key]['ID']}")
            flask.flash(f"Temperature : {data[key]['temp']}")
            flask.flash(f"Humidite : {data[key]['humidity']}")
    return flask.render_template("view.html")

@app.route("/config", methods = ["GET", "POST"])
def config_page():
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
        with open(f"Config/config.json", 'w') as file:
            file.write(json.dumps(config))
        return flask.redirect(flask.url_for("config_page"))

if __name__ == '__main__':
    app.run()
