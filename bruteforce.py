import csv
import math
import time


# Fonction permettant de convertir le temps d'exécution de secondes en HH:MM:SS

def convert(seconds):
    ''' La fonction permet de convertir les secondes en HH/MM/SS afin d'avoir un timing plus clair '''
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)


# Budget max
budget_max = 500

file_path = "data/data_exo1.csv"
actions_list = []
actions_updated = []

with open(file_path, 'r') as csv_file:
    data = csv.DictReader(csv_file)
    for row in data:
        actions_list.append(dict(row))

# Calcul de la valeur de l'action après bénéfice

for action in actions_list:
    result_profit = int(action['Cost']) * (int(action['Profit']) * 1/100)
    action["Result_after_profit"] = int(action['Cost']) + result_profit
    action['Valeur_du_profit'] = result_profit

# Mise à jour du csv

fieldnames = actions_list[0].keys()


with open(file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(actions_list)

with open(file_path, 'r') as csv_file:
    data = csv.DictReader(csv_file)
    for row in data:
        actions_updated.append(dict(row))

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
    for i in range(0, 2 ** n):
        for j in range(0, n):
            # L'opérateur ">>" permet le décalage vers la droite. Il déplace les bits de i vers la droite de j position
            # (i >> j) donne une valeur de 1 ou 0. Si == 1 , alors le j-nième élement est inclus dans la combinaison.
            # L'opérateur "& 1" ne modifie que le dernier bit de i. Ce qui permet de lister TOUTES les combinaisons
            if (i >> j) & 1:
                combination = actions_updated[j]
                # Ajout de la combinaison à la liste all_combinations
                all_combinations.append(combination)
    print(len(all_combinations))
    return all_combinations


def profit_cout_combinaison(combinaison):
    '''Calcule le coût et le profit d'une combinaison'''
    # Variables
    cout_total = 0
    total_profit = 0
    # Fonction
    for action in combinaison:
        cout_total += float(action['Cost'])
        total_profit += float(action['Valeur_du_profit'])
    return total_profit, cout_total


def meilleur_profit(all_combinaison):
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
            best_profit = total_profit
            best_cost = cout_total
    return best_combinaison, best_profit, best_cost


def test_total(actions_updated):
    start = time.time()

    all_combinaison = generate_combinations(actions_updated)
    best_combinaison, max_profit, cout_total = meilleur_profit(all_combinaison)
    print("Combinaison: ", best_combinaison)
    print("Profit total: ", max_profit)
    print("Coût total:", cout_total)
    print('Fin du programme')
    end_time = (time.time() - start)
    print(convert(end_time))


generate_combinations(actions_updated)
