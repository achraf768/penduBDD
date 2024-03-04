import sqlite3


def recuperer_scores_nom_joueurs():
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('''
                        select j.nom_joueur, score_partie as nb_erreurs
                        FROM partie p
                        join joueur j on p.id_joueur=j.id_joueur
                        ORDER by nom_joueur
                   ''')
    connection.close()


def recuperer_scores_decroissant():
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('''
                        select j.nom_joueur, score_partie as nb_erreurs
                        FROM partie p
                        join joueur j on p.id_joueur=j.id_joueur
                        ORDER BY nb_erreurs, nom_joueur
                   ''')
    connection.close()



def recuperer_scores_niveau_puis_decroissant():
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('''
                        select j.nom_joueur, score_partie as nb_erreurs
                        FROM partie p
                        join joueur j on p.id_joueur=j.id_joueur
                        ORDER BY p.niveau_partie
                   ''')
    connection.close()