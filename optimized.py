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

# Décomposition du nombre de combinaisons

# Nombre de combinaisons de 2 actions : 190
# Nombre de combinaisons de 3 actions : 1140
# Nombre de combinaisons de 4 actions : 4845
# Nombre de combinaisons de 5 actions : 15504
# Nombre de combinaisons de 6 actions : 38760
# Nombre de combinaisons de 7 actions : 77520
# Nombre de combinaisons de 8 actions : 125970
# Nombre de combinaisons de 9 actions : 167960
# Nombre de combinaisons de 10 actions : 184756
# Nombre de combinaisons de 11 actions : 167960
# Nombre de combinaisons de 12 actions : 125970
# Nombre de combinaisons de 13 actions : 77520
# Nombre de combinaisons de 14 actions : 38760
# Nombre de combinaisons de 15 actions : 15504
# Nombre de combinaisons de 16 actions : 4845
# Nombre de combinaisons de 17 actions : 1140
# Nombre de combinaisons de 2 actions : 190
# Nombre de combinaisons de 19 actions : 20
# Nombre de combinaisons de 20 actions : 1


def generate_combinations(actions_updated):
    n = len(actions_updated)
    all_combinations = []

    # Fonction récursive pour générer les combinaisons

    def generate_helper(current_combination, index):
        if index == n:
            all_combinations.append(current_combination.copy())
            return

        # Inclure l'élément actuel dans la combinaison
        current_combination.append(actions_updated[index])
        generate_helper(current_combination, index + 1)

        # Ne pas inclure l'élément actuel dans la combinaison
        current_combination.pop()
        generate_helper(current_combination, index + 1)

    # Appel initial avec une liste vide et l'indice de départ 0
    generate_helper([], 0)

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


test_total(actions_updated)
