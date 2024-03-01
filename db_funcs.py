import sqlite3

def nom_existe_dans_db(nom):
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM joueur WHERE nom_joueur = ?', (nom.lower().strip(),))
    nom_existe = cursor.fetchone()[0] > 0
    connection.close()
    return nom_existe


def ajouter_nom_dans_db(nom):
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO joueur (nom_joueur) values(?)', (nom.lower().strip(),))
    connection.commit()
    connection.close()


def recuperer_id_nom(nom):
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id_joueur FROM joueur WHERE nom_joueur = ?', (nom.lower().strip(),))
    id_nom = cursor.fetchone()[0]
    connection.close()
    return id_nom


def recuperer_id_mot(mot):
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id_mot FROM mot WHERE label_mot = ?', (mot,))
    id_mot = cursor.fetchone()[0]
    connection.close()
    return id_mot


def enregistrer_partie(id_mot, id_joueur, niveau, date_heure, score,liste_lettres_utilisees):
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO partie (id_mot, id_joueur, niveau_partie, date_heure_partie, score_partie) values(?,?,?,?,?)', (id_mot, id_joueur, niveau, date_heure, score))
    connection.commit()

    cursor.execute('SELECT id_partie FROM partie WHERE id_mot = ? and id_joueur = ? and niveau_partie= ? and  date_heure_partie=? and score_partie=?', (id_mot, id_joueur, niveau, date_heure, score))
    id_partie = cursor.fetchone()[0]

    for lettre in liste_lettres_utilisees:
        cursor.execute('INSERT INTO partie_lettre (lettre, id_partie) values(?,?)', (lettre, id_partie))
        connection.commit()

    connection.close()