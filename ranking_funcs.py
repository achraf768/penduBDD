import sqlite3


def recuperer_scores_nom_joueurs():
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('''
                        select j.nom_joueur, p.score_partie, p.niveau_partie, DATE(p.date_heure_partie)
                        FROM partie p
                        join joueur j on p.id_joueur=j.id_joueur
                        ORDER by j.nom_joueur , p.score_partie desc
                   ''')
    scores = cursor.fetchall()
    connection.close()
    return scores


def recuperer_scores_decroissant():
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('''
                        select j.nom_joueur, p.score_partie, p.niveau_partie, DATE(p.date_heure_partie)
                        FROM partie p
                        join joueur j on p.id_joueur=j.id_joueur
                        ORDER BY score_partie desc, j.nom_joueur
                   ''')
    scores = cursor.fetchall()
    connection.close()
    return scores



def recuperer_scores_niveau_puis_decroissant():
    connection = sqlite3.connect('bdd/ma_base.db')
    cursor = connection.cursor()
    cursor.execute('''
                        select j.nom_joueur, p.score_partie,p.niveau_partie, DATE(p.date_heure_partie)
                        FROM partie p
                        join joueur j on p.id_joueur=j.id_joueur
                        ORDER BY p.niveau_partie desc, p.score_partie desc
                   ''')
    scores = cursor.fetchall()
    connection.close()
    return scores


if __name__ == "__main__":
    liste =recuperer_scores_nom_joueurs()
    print(liste)