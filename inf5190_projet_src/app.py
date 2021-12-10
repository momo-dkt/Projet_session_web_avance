
from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template
from flask import request

from flask import g

from flask import jsonify
from werkzeug.utils import send_file
from .database import Database
from apscheduler.schedulers.background import BackgroundScheduler
#import extract
from pytz import utc


from dicttoxml import dicttoxml
import csv
from flask import send_file
import shutil
import os
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
from .schemas import glissade_modify_schema


app = Flask(__name__, static_folder="static", static_url_path="")
Bootstrap(app)
schema = JsonSchema(app)

"""
if os.path.isdir('db'):
    shutil.rmtree('db')

extract.initialisation()
"""

sched = BackgroundScheduler(timezone=utc)


# @sched.scheduled_job('cron', minute=1)
# def importation_automarique():
#    extract.extraction()

"""
sched = BackgroundScheduler(timezone=utc)
sched.add_job(extract.extraction, trigger='cron', hour=0)
sched.start()
"""
# commentaire


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.route("/")
def home():
    all_installations = get_db().get_all_installations()

    # for installation in installations:
    # print(installation)
    return render_template('home.html', all_installations=all_installations)
    # return "hello word"


"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
"""


@app.route('/api/installations/<arrondissement>', methods=['GET'])
def get_arrondissement(arrondissement):
    installations = get_db().get_installations(arrondissement)
    if installations is None:

        return jsonify("Aucune installation"), 404
    else:
        return jsonify([{"nom": each} for each in installations])


@app.route('/api/installations/nom/<nom_installation>', methods=['GET'])
def get_details(nom_installation):

    installation = get_db().get_installation_by_name(nom_installation)
    if installation is None:
        return jsonify("Installation inexistante"), 404
    else:
        if len(installation) == 4:

            return jsonify({"arrondissement": installation[1], "nom": installation[2], "Dernier_mise_a_jour": installation[3]})

        elif len(installation) == 5:

            return jsonify({"arrondissement": installation[1], "nom": installation[2], "type": installation[3], "adresse": installation[4]})

        elif len(installation) == 6:

            return jsonify({"arrondissement": installation[1], "nom": installation[2], "ouvert": installation[3], "deblaye": installation[4], "Dernier_mise_a_jour": installation[5]})
        else:
            return jsonify("Installation inexistante"), 404


@app.route('/api/installations/json_2021', methods=['GET'])
def get_installations_json_2021():
    installations = get_db().get_installations_2021()

    installations_json = []
    for installation in installations:
        if len(installation) == 4:
            data = {
                "arrondissement": installation[1], "nom": installation[2], "Dernier_mise_a_jour": installation[3]}

        elif len(installation) == 5:
            data = {"arrondissement": installation[1], "nom": installation[2],
                    "type": installation[3], "adresse": installation[4]}

        elif len(installation) == 6:
            data = {"arrondissement": installation[1], "nom": installation[2], "ouvert": installation[3],
                    "deblaye": installation[4], "Dernier_mise_a_jour": installation[5]}
        installations_json.append(data)
    return jsonify(installations_json)


@app.route('/api/installations/xml_2021', methods=['GET'])
def get_installations_xml_2021():
    installations = get_db().get_installations_2021()
    print(type(installations))
    #installations_json = []
    """
    for installation in installations:
        
        if len(installation) == 4:

            data = {
                "arrondissement": installation[1], "nom": installation[2], "Dernier_mise_a_jour": installation[3]}

        elif len(installation) == 5:
            data = {"arrondissement": installation[1], "nom": installation[2],
                    "type": installation[3], "adresse": installation[4]}

        elif len(installation) == 6:
            data = {"arrondissement": installation[1], "nom": installation[2], "ouvert": installation[3],
                    "deblaye": installation[4], "Dernier_mise_a_jour": installation[5]}
        
        
        installations_json.append(data)
        data_json=json.load(installations_json)
     """
    #op = dict.fromkeys("Installations", installations)

    op = {installation[2]: "installation" for installation in installations}
    print(type(op))
    xml = dicttoxml(op)

    return []


@app.route('/api/installations/csv_2021', methods=['GET'])
def get_installations_csv_2021():
    installations = get_db().get_installations_2021()
    champs = ["Arrondissement", "Nom", "Derniére Mise à jour",
              "Type", "Adresse", "Ouvert", "Deblaye"]
    lignes = []
    for installation in installations:
        if len(installation) == 4:
            data = [installation[1], installation[2], installation[3]]
        elif len(installation) == 5:
            data = [installation[1], installation[2],
                    " ", installation[3], installation[4]]
        elif len(installation) == 6:
            data = [installation[1], installation[2],
                    installation[5], "", "", installation[3], installation[4]]
        lignes.append(data)
    with open('static/file/2021.csv', 'w', encoding="utf-8") as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(champs)
        write.writerows(lignes)
    return send_file("static/file/2021.csv", mimetype="csv")


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400


@app.route('/api/installations/modifier_glissade/<nom>', methods=['PUT'])
@schema.validate(glissade_modify_schema)
def glissade_modif(nom):
    glissade = get_db().read_one_glissade(nom)
    if glissade is None:
        return jsonify("Glissade inexistante"), 404
    else:
        data = request.get_json()
        arrondissement = data["arrondissement"]
        nouveau_nom = data["nom"]
        ouvert = data["ouvert"]
        deblaye = data["deblaye"]

        glissade_modified = get_db().modify_glissade(
            nom, arrondissement, nouveau_nom, ouvert, deblaye)

        data = {"arrondissement": glissade_modified[1], "nom": glissade_modified[2], "ouvert": glissade_modified[3],
                "deblaye": glissade_modified[4], "Dernier_mise_a_jour": glissade_modified[5]}

        return jsonify(data)


@app.route('/api/installations/delete/<nom>', methods=["DELETE"])
def delete_glissade(nom):
    glissade = get_db().read_one_glissade(nom)
    if glissade is None:
        return jsonify("Glissade inexistante"), 404
    else:
        get_db().delete_glissade(nom)
        glissades = get_db().get_all_glissades()
        if glissades != None:
            glissade_json = []
            for glissade in glissades:
                data = {"arrondissement": glissade[1], "nom": glissade[2], "ouvert": glissade[3],
                        "deblaye": glissade[4], "Dernier_mise_a_jour": glissade[5]}
                glissade_json.append(data)
            return jsonify(glissade_json), 200
        else:
            return jsonify("Plus aucune glissade"), 200


@app.route('/doc')
def documentation():
    return render_template('doc.html')


@app.route('/installations_table')
def installations_tab():
    return render_template('tab.tml')


if __name__ == "__main__":
    app.run()
