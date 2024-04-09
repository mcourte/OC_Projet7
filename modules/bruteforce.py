import time
import psutil
import csv

from modules import general


def update_data_BF(file_path):
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


def generate_combinations(actions_updated):
    '''Permet de lister la totalité des combinaisons possibles'''
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
    '''Programme qui permet d'afficher la meilleure combinaison, son coût, son bénéfice,
    le temps d'éxécution du programme ainsi que la mémoire utilisée'''
    # Variables
    budget_max = 500
    # Fonction

    print("Début du programme")
    start = time.time()
    actions_updated = update_data_BF(file_path)
    all_combinaison = generate_combinations(actions_updated)
    best_combinaison, max_profit, cout_total = meilleur_profit(all_combinaison, budget_max)

    print("La meilleure combinaison est la suivante:\n", best_combinaison)
    print("Le profit total de cette combinaison est: ", max_profit, "€")
    print("Le coût total d'achat des actions de la combinaison est: ", cout_total, "€")
    process = psutil.Process()
    print(f"Utilisation de la mémoire : {process.memory_info().rss / (1024 * 1024):.2f} MiB")
    end_time = (time.time() - start)
    print("Fin du programme: ", general.convert(end_time))
