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

file_path = "data/dataset1.csv"
actions_list = []
actions_updated = []

with open(file_path, 'r') as csv_file:
    data = csv.DictReader(csv_file)
    for row in data:
        actions_list.append(dict(row))


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


def dynamique_best_combinaisons(actions_list, budget_max):
    n = len(actions_list)
    dp = [[0 for _ in range(budget_max + 1)] for _ in range(n + 1)]
    selected_actions = [[[] for _ in range(budget_max + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        action = actions_list[i - 1]  # Access the current action
        for j in range(1, budget_max + 1):
            if int(action['cost']) <= j:  # Convert to int assuming the cost is a string
                if (
                    float(action['profit']) + dp[i - 1][j - int(action['cost'])]
                    > dp[i - 1][j]
                ):
                    dp[i][j] = float(action['profit']) + dp[i - 1][j - int(action['cost'])]
                    selected_actions[i][j] = selected_actions[i - 1][j - int(action['cost'])] + [action['name']]
                else:
                    dp[i][j] = dp[i - 1][j]
                    selected_actions[i][j] = selected_actions[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]
                selected_actions[i][j] = selected_actions[i - 1][j]

    # Find the optimal combination
    optimal_combination = selected_actions[n][budget_max]
    return optimal_combination, dp[n][budget_max]


def profit_cout_combinaison(actions_list, budget_max):
    optimal_combination, _ = dynamique_best_combinaisons(actions_list, budget_max)

    cout_total = 0
    total_profit = 0

    for action_name in optimal_combination:
        for action in actions_list:
            if action['name'] == action_name:
                cout_total += float(action['price'])
                total_profit += float(action['profit'])
                break  # Une fois que la correspondance est trouvée, sortez de la boucle interne

    return optimal_combination, total_profit, cout_total


def diplay_best_combination(actions_list):
    print("Début du programme")

    start = time.time()

    best_combinaison, max_profit, cout_total = profit_cout_combinaison(actions_list, budget_max)
    print("La meilleure combinaison est la suivante:\n", best_combinaison)
    print("Le profit total de cette combinaison est: ", max_profit, "€")
    print("le coût total d'achat des actions de la combinaison est: ", cout_total, "€")

    end_time = (time.time() - start)
    print("Fin du programme: ", convert(end_time))


diplay_best_combination(actions_list)
