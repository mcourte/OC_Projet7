import csv
import math
import time
import psutil

# Fonction permettant de convertir le temps d'exécution de secondes en HH:MM:SS


def convert(seconds):
    ''' La fonction permet de convertir les secondes en HH/MM/SS/SSS afin d'avoir un timing plus clair '''
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)  # Extrait les millisecondes
    return '%02d:%02d:%02d:%03d' % (hours, minutes, int(seconds), milliseconds)


def update_data(file_path):
    actions_list = []
    actions_updated = []

    with open(file_path, 'r') as csv_file:
        data = csv.DictReader(csv_file)
        for row in data:
            actions_list.append(dict(row))

    # Calcul de la valeur de l'action après bénéfice

        for action in actions_list:
            if float(action['price']) > 0 and float(action['profit']) > 0:
                action['profit'] = ((float(action['price'])) * (((float(action['profit'])))) / 100)

    # Mise à jour du csv

    fieldnames = actions_list[0].keys()

    file_path_new = file_path[:-4] + "result_BF.csv"
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
# Toutes les actions ont une valeur de coût & de bénéfice dans notre exemple
# voire pour exclusion si ce n'est pas le cas?

# La liste fait 20 actions
# La longueur des combinaisons ira donc de 2 à 20 items
# Calcul du nombre de combinaisons possible, sans répétition :
# Formule mathématique : C = n!/(p! *(n-p)! )
# C : nombre de combinaisons / p élements d'un ensemble à n élements, avec p <= n / "!" : factorielle du nombre
# utilisation de la fonction math.comb(i,k) de Python


def nombre_combinaisons(n):
    # Variables
    total_combinations = 0
    # Fonction
    for k in range(2, n + 1):
        combinations = math.comb(n, k)
        total_combinations += combinations
    return total_combinations

# Resultat = 1 048 554 combinaisons possibles !

# Faire la liste des combinaisons
# On doit faire: A1+A2, A1+A3,... A2+A3, A2+A4..., A1+A2+A3...


def generate_combinations(actions_updated):
    # Longueur de la liste d'actions
    n = len(actions_updated)
    # Initie la liste all_combinations qui contiendra toutes les combinaisons possibles
    all_combinations = []
    # Itération de toutes les combinaisons:
    # On considère que chaque entier i représente une combinaison unique
    # Un entier i de 0 à 2^n - 1 représente une combinaison possible. ( 2 ** n = 0 à 2^n)
    for i in range(1, 2 ** n):
        combination = []
        for j in range(0, n):
            # L'opérateur ">>" permet le décalage vers la droite. Il déplace les bits de i vers la droite de j position
            # (i >> j) donne une valeur de 1 ou 0. Si == 1 , alors le j-nième élement est inclus dans la combinaison.
            # L'opérateur "& 1" ne modifie que le dernier bit de i. Ce qui permet de lister TOUTES les combinaisons
            if (i >> j) & 1:
                combination.append(actions_updated[j])
        # Ajout de la combinaison à la liste all_combinations
        all_combinations.append(combination)

    print("Le nombre total de combinaisons possibles est: ", len(all_combinations))
    return all_combinations


def profit_cout_combinaison(combinaison):
    '''Calcule le coût et le profit d'une combinaison'''
    # Variables
    cout_total = 0
    total_profit = 0
    # Fonction
    for action in combinaison:
        cout_total += float(action['price'])
        total_profit += float(action['profit'])
    return total_profit, cout_total


def meilleur_profit(all_combinaison, budget_max):
    '''Trouve le meilleur profit, en respectant la contrainte du budget max'''
    '''return : la meilleure des combinaisons'''
    # On initie le profit max à la première combinaison
    best_combinaison = []
    best_profit = 0
    best_cost = 0
    for combinaison in all_combinaison:
        total_profit, cout_total = profit_cout_combinaison(combinaison)
        # On compare à tous les total_profit de chaque combinaison jusqu'à trouver le plus grand
        if float(cout_total) <= budget_max and float(total_profit) > best_profit:
            best_combinaison = combinaison
            best_profit = round(total_profit, 2)
            best_cost = round(cout_total, 2)
    return best_combinaison, best_profit, best_cost


def diplay_best_combination(file_path):
    # Variables
    budget_max = 500
    # Fonction

    print("Début du programme")
    start = time.time()
    actions_updated = update_data(file_path)
    all_combinaison = generate_combinations(actions_updated)
    best_combinaison, max_profit, cout_total = meilleur_profit(all_combinaison, budget_max)

    print("La meilleure combinaison est la suivante:\n", best_combinaison)
    print("Le profit total de cette combinaison est: ", max_profit, "€")
    print("Le coût total d'achat des actions de la combinaison est: ", cout_total, "€")
    process = psutil.Process()
    print(f"Utilisation de la mémoire : {process.memory_info().rss / (1024 * 1024):.2f} MiB")
    end_time = (time.time() - start)
    print("Fin du programme: ", convert(end_time))
