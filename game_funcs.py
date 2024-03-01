def recuperer_mot_underscore(mot_a_deviner):
    liste_mot_underscore = ['_' for lettre in mot_a_deviner]
    mot_underscore = ''.join(liste_mot_underscore)
    return mot_underscore


def ajouter_espace_entre_chaque_lettre(mot):
    liste_mot = [caractere + " " for caractere in mot]
    mot = ''.join(liste_mot)
    return mot


def lettre_est_dans_mot(lettre, mot):
    if lettre in mot:
        return True
    return False


def recuperer_indices_lettre_dans_mot(lettre, mot_a_deviner):
    indices = []
    for i in range(len(mot_a_deviner)):
        if mot_a_deviner[i] == lettre:
            indices.append(i)
    return indices


def ajouter_lettre_dans_mot_underscores(lettre,mot_a_deviner, mot_underscores):
    if lettre_est_dans_mot(lettre, mot_a_deviner):
        indices = recuperer_indices_lettre_dans_mot(lettre, mot_a_deviner)
        mot_underscores_liste = list(mot_underscores)
        for indice in indices:
            mot_underscores_liste[indice] = lettre
        mot_underscores = ''.join(mot_underscores_liste)
        return mot_underscores


def lettre_deja_dans_liste(lettre, liste_lettres):
    if lettre in liste_lettres:
        return True
    return False


def partie_terminee(nombre_tentatives, mot_underscores, mot_a_deviner):
    if nombre_tentatives > 7 or mot_a_deviner == mot_underscores:
        return True
    return False


def partie_gagnee(mot_underscores, mot_a_deviner):
    if mot_a_deviner == mot_underscores:
        return True
    return False

        



# ----------   TEST   ----------- #
if __name__ == '__main__':
    mot_a_deviner = "coucou"
    mot_underscores = recuperer_mot_underscore("coucou")
    mot_underscores = ajouter_lettre_dans_mot_underscores("c", mot_a_deviner, mot_underscores)
    print(mot_underscores)
    


    