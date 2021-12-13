import sqlite3
from typing import List
from operator import itemgetter
import os


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))

        if self.connection is None:

            self.connection = sqlite3.connect('db/database.db')

        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_installations(self, arrondissement):
        cursor = self.get_connection().cursor()

        cursor.execute(
            "select  * from lieu_baignade " +
            "where arrondissement = ?", (arrondissement,)
        )

        installations = cursor.fetchall()

        cursor.execute(
            "select * from patinoire " +
            "where arrondissement = ?", (arrondissement,)
        )

        installations = installations+cursor.fetchall()

        cursor.execute(
            "select * from glissade " +
            "where arrondissement = ?", (arrondissement,)
        )
        installations = installations+cursor.fetchall()

        if not installations:
            return None
        else:
            print(type(installations))
            inter = set(installations)
            return ((installation[2])for installation in inter)

    def get_all_installations(self):
        cursor = self.get_connection().cursor()

        cursor.execute(
            "select * from lieu_baignade"
        )

        installations = cursor.fetchall()

        cursor.execute(
            "select * from patinoire "
        )

        installations = installations+cursor.fetchall()

        cursor.execute(
            "select * from glissade "
        )
        installations = installations+cursor.fetchall()

        if not installations:
            return None
        else:
            inter = list(set(installations))
            return ((installation)for installation in inter)

    def get_installation_by_name(self, nom_installation):
        cursor = self.get_connection().cursor()

        cursor.execute(
            "select * from lieu_baignade " +
            "where nom= ?", (nom_installation,)
        )

        installations = cursor.fetchall()

        cursor.execute(
            "select * from patinoire " +
            "where nom = ?", (nom_installation,)
        )

        installations = installations+cursor.fetchall()

        cursor.execute(
            "select * from glissade " +
            "where nom = ?", (nom_installation,)
        )
        installations = installations+cursor.fetchall()

        if not installations:
            return None
        else:
            if len(installations) > 1:
                return (installations[0])
        return (installations[0])

    def get_installations_2021(self):
        cursor = self.get_connection().cursor()

        cursor.execute(
            "select * from lieu_baignade"
        )
        installations = cursor.fetchall()
        cursor.execute(
            "select * from patinoire " +
            "where mise_a_jour = 2021"
        )
        installations = installations+cursor.fetchall()

        cursor.execute(
            "select * from glissade " +
            "where mise_a_jour = 2021"
        )
        installations = installations+cursor.fetchall()

        if not installations:
            return None
        else:
            inter = sorted(installations, key=itemgetter(2))
            return ((installation)for installation in inter)

    def read_one_glissade(self, nom):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from glissade where nom = ?", (nom,))
        glissades = cursor.fetchall()
        if len(glissades) == 0:
            return None
        else:
            glissade = glissades[0]
            return (glissade[1], glissade[2], glissade[3], glissade[4])

    def get_all_glissades(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from glissade ")
        glissades = cursor.fetchall()
        if len(glissades) == 0:
            return None
        else:
            return ((glissade)for glissade in glissades)

    def delete_glissade(self, nom):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("delete from glissade where nom = ?", (nom,))
        connection.commit()

    def modify_glissade(self, nom, arrondissement, nouveau_nom,
                        ouvert, deblaye):
        connection = self.get_connection()
        cursor = connection.cursor()
        deblaye = deblaye.lower()
        deblaye_value = 0
        ouvert_value = 0
        if deblaye == "oui":
            deblaye_value = 1

        ouvert = ouvert.lower()
        if ouvert == "oui":
            ouvert_value = 1

        cursor.execute("update glissade set arrondissement = ?, nom = ?,"
                       "ouvert = ?, deblaye = ? where nom = ?",
                       (arrondissement, nouveau_nom, ouvert_value,
                        deblaye_value, nom))

        connection.commit()
        cursor.execute("select * from glissade where nom = ?", (nouveau_nom,))
        glissade_modified = cursor.fetchall()[0]

        return glissade_modified
