import csv
import math


def convert(seconds):
    ''' La fonction permet de convertir les secondes en HH/MM/SS/SSS afin d'avoir un timing plus clair '''
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)  # Extrait les millisecondes
    return '%02d:%02d:%02d:%03d' % (hours, minutes, int(seconds), milliseconds)


def update_actions(file_path):
    '''La fonction permet de copier le .csv contenant les données de base,
       et de modifier celles-ci pour être au bon format'''
    actions_list = []
    actions_updated = []

    with open(file_path, 'r') as csv_file:
        data = csv.DictReader(csv_file)
        for row in data:
            actions_list.append(dict(row))

    # Calcul de la valeur de l'action après bénéfice

    new_actions_list = []

    for action in actions_list:
        if float(action['price']) > 0 and float(action['profit']) > 0:
            action['price'] = int((float(action['price'])) * 100)
            action['profit'] = int(round(((((float(action['price'])) * ((float(action['profit'])))) / 100)) * 100, 2))
            new_actions_list.append(action)

    # On remplace la liste de base par la liste mise à jour
    actions_list = new_actions_list

    fieldnames = ['name', 'price', 'profit']
    file_path_new = file_path[:-4] + "result.csv"
    with open(file_path_new, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(actions_list)

    with open(file_path_new, 'r') as csv_file:
        data = csv.DictReader(csv_file)
        for row in data:
            actions_updated.append(dict(row))

    return actions_updated


# On cherche à calculer toutes les possibilités de combinaisons,
# Calcul des combinaisons
# - Une action ne peut être acheté qu'une fois
# - Une action ne peut être qu'acheter entièrement
# -   Dans chaque combinaison, action = 100% d'une action, qu'une seule fois

# La liste fait n actions
# La longueur des combinaisons ira donc de 2 à n+1 items
# Calcul du nombre de combinaisons possible, sans répétition :
# Formule mathématique : C = n!/(p! *(n-p)! )
# C : nombre de combinaisons / p élements d'un ensemble à n élements, avec p <= n / "!" : factorielle du nombre
# utilisation de la fonction math.comb(i,k) de Python


def nombre_combinaisons(n):
    '''Calculer le nombre total de combinaison possible'''
    # Variables
    total_combinations = 0
    # Fonction
    for k in range(2, n + 1):
        combinations = math.comb(n, k)
        total_combinations += combinations
    return total_combinations
