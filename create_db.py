import sqlite3

connection = sqlite3.connect('bdd/ma_base.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE joueur(
               id_joueur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
               nom_joueur VARCHAR(50) NOT NULL UNIQUE
)''')
connection.commit()

cursor.execute('''
    CREATE TABLE mot(
               id_mot INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
               label_mot VARCHAR(50) NOT NULL
    )
''')
connection.commit()

cursor.execute('''
    CREATE TABLE partie(
        id_partie INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        id_mot INTEGER NOT NULL,
        id_joueur INTEGER NOT NULL,
        niveau_partie VARCHAR(50) NOT NULL,
        date_heure_partie DATETIME NOT NULL,
        score_partie TINYINT NOT NULL,
        FOREIGN KEY(id_mot) REFERENCES mot(id_mot),
        FOREIGN KEY(id_joueur) REFERENCES joueur(id_joueur)
    )
''')
connection.commit()

cursor.execute('''
    CREATE TABLE lettre(
               label_lettre VARCHAR(1) PRIMARY KEY UNIQUE     
    )
''')
connection.commit()


cursor.execute('''
    CREATE TABLE partie_lettre(
        lettre VARCHAR(1) NOT NULL,
        id_partie INTEGER NOT NULL, 
        PRIMARY KEY(lettre, id_partie) ,
        FOREIGN KEY (lettre) REFERENCES lettre(label_lettre),
        FOREIGN KEY (id_partie) REFERENCES partie(id_partie)       
    )
''')
connection.commit()

cursor.execute('''INSERT INTO mot(label_mot) VALUES
    ('chat'),
    ('chien'),
    ('ordinateur'),
    ('maison'),
    ('soleil'),
    ('fleur'),
    ('voiture'),
    ('livre'),
    ('internet'),
    ('musique'),
    ('python'),
    ('restaurant'),
    ('plage'),
    ('football'),
    ('bonjour'),
    ('hiver'),
    ('voyage'),
    ('cafe'),
    ('souris'),
    ('telephone')
''')
connection.commit()

cursor.execute('''INSERT INTO lettre (label_lettre) VALUES
    ('a'), ('b'), ('c'), ('d'), ('e'), ('f'), ('g'), ('h'), ('i'), ('j'), ('k'), ('l'), ('m'),
    ('n'), ('o'), ('p'), ('q'), ('r'), ('s'), ('t'), ('u'), ('v'), ('w'), ('x'), ('y'), ('z')
''')
connection.commit()

connection.close()