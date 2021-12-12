
import re
import requests
import sqlite3
import pandas as pd
import csv
import xml.etree.ElementTree as ET
import os
import shutil


from shared import get_path


def create_table_lieu_baignade(cursor):
    create_table = '''
    CREATE TABLE IF NOT EXISTS lieu_baignade(
        id integer primary key,
        arrondissement varchar(50),
        nom varchar(50),
        genre varchar(50),
        adresse varchar(50)
    );
    '''
    # Écriture de la table lieu_baignade dans le fichier sql
    with open("db/db.sql", "a") as filout:
        filout.write(create_table)
    # Création de la table
    cursor.execute(create_table)


def import_file_piscine():
    # Imporation des données
    req = requests.get(
        "https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv")
    url_content = req.content

    csv_file = open(get_path('static/file/piscines.csv'), 'wb')
    # Écriture des données dans une fichier
    csv_file.write(url_content)
    csv_file.close


def insert_lieu_baignade(cursor, data):
    data.to_csv(get_path("static/file/baignades.csv"),
                index=False, encoding="UTF-8")

    with open(get_path("static/file/baignades.csv"), 'r', encoding='utf8') as fin:
        dr = csv.DictReader(fin)
        data = [(i['ARRONDISSE'], i['NOM'], i['TYPE'],
                 i['ADRESSE']) for i in dr]

    insert = "INSERT INTO lieu_baignade (arrondissement, nom, genre, adresse) VALUES(?, ?, ?, ?);"
    # Insére toutes les données de façon simultannée
    cursor.executemany(insert, data)


def extraction_piscine():
    print("PISCINE")
    import_file_piscine()
    # Transformation en DataFrame avec le fichier csv
    data = pd.read_csv(get_path("static/file/piscines.csv"), encoding="UTF-8")
    data = data.drop(['ID_UEV', 'PROPRIETE', 'GESTION', 'POINT_X',
                     'POINT_Y', 'EQUIPEME', 'LONG', 'LAT'], axis=1)
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    # Création et insertion
    create_table_lieu_baignade(cursor)
    insert_lieu_baignade(cursor, data)
    connection.commit()
    connection.close()


def create_table_patinoire(cursor):
    create_table = '''
    CREATE TABLE IF NOT EXISTS patinoire (
        id integer primary key,
        arrondissement varchar(50),
        nom vachar(50),
        mise_a_jour varchar(20),
        ouvert varchar(10),
        deblaye varchar(10)
    );
    '''

    # Écriture de la table lieu_baignade dans le fichier sql
    with open("db/db.sql", "a") as filout:
        filout.write(create_table)
    # Création de la table
    cursor.execute(create_table)


def import_file_patinoire():
    # Imporation des données
    data = requests.get(
        "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml")
    url_content = data.content.decode('utf-8')
    return url_content


def extraction_patinoires():
    print("patinoire")
    url_content = import_file_patinoire()
    root = ET.fromstring(url_content)
    nom, date_heure, deblaye, ouvert, i = 0, 0, 0, 0, 0

    debut = True

    # Connection base de données
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    create_table_patinoire(cursor)
    arrondissements = root.findall('arrondissement')
    # for traitant l'extraction et l'insertion dans la base de données
    for arrondissement in arrondissements:

        debut = True
        deblaye = 0
        ouvert = 0
        i = 0
        nom_arr = arrondissement.findall('nom_arr')[0]
        patinoire = arrondissement.findall('patinoire')[0]

        for child in patinoire:

            if child.tag == "nom_pat" and debut:
                nom = child.text
                debut = False
            elif child.tag == "nom_pat":
                if nom != child.text:
                    arr = re.sub("\ |\n", "", nom_arr.text)
                    name = re.sub("\n", "", nom)
                    lname = len(name)-3
                    name = name[4:lname]
                    annee = date_heure[5][0:4]
                    # Insertion base de données
                    cursor.execute(("insert into patinoire(arrondissement,nom,mise_a_jour,ouvert,deblaye)"
                                    "values(?, ?, ?, ?, ?)"), (arr, name, annee, ouvert, deblaye))
                nom = child.text
            elif child.tag == "condition":
                for son in child:
                    if son.tag == "date_heure":
                        date_heure = son.text.split(" ")
                    elif son.tag == "deblaye":
                        deblaye = son.text
                    elif son.tag == "ouvert":
                        ouvert = son.text

    connection.commit()
    connection.close()


def create_table_glissade(cursor):
    create_table = '''
    CREATE TABLE IF NOT EXISTS glissade(
        id integer primary key,
        arrondissement varchar(50),
        nom varchar(50),
        ouvert integer,
        deblaye integer,
        mise_a_jour varchar(10)
    );
    '''

    # Écriture de la table lieu_baignade dans le fichier sql
    with open("db/db.sql", "a") as filout:
        filout.write(create_table)
    # Création de la table
    cursor.execute(create_table)


def insert_glissade(df, cursor):
    name = get_path("static/file/data_aires_de _jeu.csv")
    insert = "INSERT INTO glissade (arrondissement, nom, ouvert, deblaye, mise_a_jour) VALUES(?, ?, ?, ?, ?);"
    df.to_csv(path_or_buf=name, index=False)
    with open(name, 'r', encoding='utf8') as fin:
        dr = csv.DictReader(fin)
        data = [(i['ARRONDISSEMENT'], i['NOM'], i['OUVERT'],
                 i['DEBLAYE'], i['DATE']) for i in dr]
    cursor.executemany(insert, data)


def import_file_glissade():

    # Imporation des données
    data = requests.get(
        "http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml")
    url_content = data.content
    return url_content


def extraction_glissade():
    print("GLISSADE")
    url_content = import_file_glissade()
    root = ET.fromstring(url_content)
    rows = []
    cols = ["NOM", "ARRONDISSEMENT", "OUVERT", "DEBLAYE", "DATE"]
    # for qui extrait les données du xml
    for glissade in root.findall('glissade'):
        nom = glissade.find('nom').text
        ouvert = glissade.find('ouvert').text
        deblaye = glissade.find('deblaye').text
        condition = glissade.find('condition').text
        ar = glissade.find('arrondissement')
        arrondissement = ar.find('nom_arr').text
        date_maj = ar.find('date_maj').text.split(" ")[0][0:4]
        rows.append({"NOM": nom, "ARRONDISSEMENT": arrondissement,
                    "OUVERT": ouvert, "DEBLAYE": deblaye, "DATE": date_maj})
    df = pd.DataFrame(rows, columns=cols)
    df.drop_duplicates()
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    # Création table
    create_table_glissade(cursor)
    # Insert dans la table
    insert_glissade(df, cursor)
    connection.commit()
    connection.close()

# Fonction du background scheduler


def extraction():
    if os.path.isdir('db'):
        shutil.rmtree('db')
        os.mkdir('db')
    extraction_piscine()
    extraction_patinoires()
    extraction_glissade()

# Initialisation des données


def initialisation():
    if not os.path.isdir('db'):
        os.mkdir('db')

    extraction_piscine()
    extraction_patinoires()
    extraction_glissade()


# Fonction main
if (__name__ == "__main__"):
    """
    if not os.path.isdir('db'):
        os.mkdir('db')
    extraction_piscine()
    extraction_patinoires()
    extraction_glissade()
    """
