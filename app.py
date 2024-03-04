import flask
import sqlite3
import random
import datetime

import game_funcs
import db_funcs


app= flask.Flask(__name__, template_folder="views", static_folder='static')
app.secret_key = 'secret-key'



@app.route('/',methods=['GET', 'POST'])
def home():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')
    else:
        name = flask.request.values.get('nom')
        flask.session["name"] = name

        if not db_funcs.nom_existe_dans_db(name):
            db_funcs.ajouter_nom_dans_db(name)

        flask.session["id_name"] = db_funcs.recuperer_id_nom(name)

        return flask.redirect("/level")
    


@app.route('/level',methods=['GET', 'POST'])
def level():
    if flask.request.method == 'GET':
        name = flask.session.get("name")
        return flask.render_template('level.html', name=name)

    if flask.request.method == 'POST':
        flask.session["mot_a_deviner"] = None
        flask.session["mot_underscores"] = None
        flask.session["message_utilisateur"] = None
        flask.session["liste_lettres_utilisees"] = []
        flask.session["nombre_vies"] = None

        difficulte = flask.request.form.get('difficulte')
        flask.session["difficulte"] = difficulte
        return flask.redirect('/game')



@app.route('/game', methods=['GET', 'POST'])
def game():
    if flask.request.method == 'GET':
        name = flask.session.get("name")
        mot_a_deviner = flask.session.get("mot_a_deviner")
        message_utilisateur = flask.session.get("message_utilisateur")
        liste_lettres_utilisees= flask.session.get("liste_lettres_utilisees")
        nombre_vies= flask.session.get("nombre_vies")
        difficulte = flask.session.get("difficulte")

        if nombre_vies == None:
            nombre_vies = 8
            flask.session["nombre_vies"] = nombre_vies

        if flask.session["mot_a_deviner"] == None:
            connection = sqlite3.connect('bdd/ma_base.db')
            cursor = connection.cursor()
            if difficulte == 'facile':
                cursor.execute('SELECT LOWER(label_mot) FROM mot WHERE LENGTH(label_mot) < 6')
                tuples_mots = cursor.fetchall()
            elif difficulte == 'moyen':
                cursor.execute('SELECT LOWER(label_mot) FROM mot WHERE LENGTH(label_mot) BETWEEN 6 and 7')
                tuples_mots = cursor.fetchall()
            elif difficulte == 'difficile':
                cursor.execute('SELECT LOWER(label_mot) FROM mot WHERE LENGTH(label_mot) >= 8')
                tuples_mots = cursor.fetchall()
            connection.close()

            liste_mots= [e[0] for e in tuples_mots]
            mot_a_deviner = random.choice(liste_mots)
            flask.session["mot_a_deviner"] = mot_a_deviner
            flask.session["id_mot"] = db_funcs.recuperer_id_mot(mot_a_deviner)

        if flask.session["mot_underscores"] == None:
            mot_underscores = game_funcs.recuperer_mot_underscore(mot_a_deviner)
            flask.session["mot_underscores"] = mot_underscores
        else:
           mot_underscores=flask.session.get("mot_underscores")
            
        mot_underscores_avec_espaces = game_funcs.ajouter_espace_entre_chaque_lettre(mot_underscores)
        return flask.render_template('game.html', difficulte=difficulte, mot_a_deviner=mot_a_deviner, joueur=name, mot_underscore= mot_underscores_avec_espaces, message_utilisateur=message_utilisateur, liste_lettres_utilisees=liste_lettres_utilisees, nombre_vies=nombre_vies)
    
    else:
        mot_a_deviner = flask.session.get("mot_a_deviner")
        mot_underscores = flask.session.get("mot_underscores")
        liste_lettres_utilisees= flask.session.get("liste_lettres_utilisees")
        nombre_vies = flask.session.get("nombre_vies")

        lettre = flask.request.values.get("lettre")

        if not game_funcs.lettre_deja_dans_liste(lettre, liste_lettres_utilisees):   # si la lettre n'a pas déjà été tentée :
                liste_lettres_utilisees.append(lettre)                                 # - on l'ajoute a la liste des lettres déjà essayées                        
                flask.session["liste_lettres_utilisees"] = liste_lettres_utilisees     # - et on met jour la liste dans la session
        else :                                                                     # si la lettre a déjà été tentée :
            flask.session["message_utilisateur"] = f"La lettre {lettre} a déjà été essayée ! "          # - on stocke un message dans la session pour l'utilisateur
            return flask.redirect('/game')                                                                  # si on en arrive la c'est que la lettre a déjà été essayée donc on return

        if game_funcs.lettre_est_dans_mot(lettre, mot_a_deviner):                # si on arrive ici c'est que a lettre n'a pas encore été essayée : donc on regarde si la lettre est dans le mot 
            mot_underscores = game_funcs.ajouter_lettre_dans_mot_underscores(lettre, mot_a_deviner, mot_underscores)
            flask.session["mot_underscores"] = mot_underscores
            flask.session["message_utilisateur"] = None
        else:
            flask.session["message_utilisateur"] = f"La lettre {lettre} n'est pas dans le mot ! "
            nombre_vies -= 1
            flask.session["nombre_vies"]  = nombre_vies

        
        if game_funcs.partie_terminee(nombre_vies, mot_underscores, mot_a_deviner):
            return flask.redirect('/endgame')  
           

        return flask.redirect('/game')


@app.route('/endgame', methods=['GET', 'POST'])
def endgame():
    if flask.request.method == 'GET':
        name = flask.session.get("name")
        mot_a_deviner = flask.session.get("mot_a_deviner")
        mot_underscores = flask.session.get("mot_underscores")
        liste_lettres_utilisees= flask.session.get("liste_lettres_utilisees")
        nombre_vies= flask.session.get("nombre_vies")
        id_nom = flask.session.get("id_name")
        id_mot = flask.session.get("id_mot")
        difficulte = flask.session.get("difficulte")
        date_heure = datetime.datetime.now()

        db_funcs.enregistrer_partie(id_mot, id_nom,difficulte,date_heure, nombre_vies,liste_lettres_utilisees)

        if game_funcs.partie_gagnee(mot_underscores, mot_a_deviner):
            message = "Vous avez gagné ! "
        else:
            message = "Vous avez perdu ! "  
        
        return flask.render_template('endgame.html', message=message, name=name, mot_a_deviner=mot_a_deviner, liste_lettres_utilisees=liste_lettres_utilisees, nombre_vies=nombre_vies, id_nom=id_nom, id_mot=id_mot)
  

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():
    if flask.request.method == 'GET':
        pass

if __name__ == "__main__":
    app.run(debug=True)
