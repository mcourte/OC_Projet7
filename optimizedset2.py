import csv
import math
import time


# Fonction permettant de convertir le temps d'exécution de secondes en HH:MM:SS

def convert(seconds):
    ''' La fonction permet de convertir les secondes en HH/MM/SS/SSS afin d'avoir un timing plus clair '''
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)  # Extrait les millisecondes
    return '%02d:%02d:%02d:%03d' % (hours, minutes, int(seconds), milliseconds)


def update_actions(file_path):
    actions_list = []
    actions_updated = []

    with open(file_path, 'r') as csv_file:
        data = csv.DictReader(csv_file)
        for row in data:
            actions_list.append(dict(row))

    # Calcul de la valeur de l'action après bénéfice

    new_actions_list = []

    for action in actions_list:
        if float(action['price']) >= 0 and float(action['profit']) >= 0:
            action['price'] = int((float(action['price'])) * 100)
            action['profit'] = int(round(((((float(action['price'])) * ((float(action['profit'])))) / 100)) * 100, 2))
            new_actions_list.append(action)

    # Replace the original actions_list with the filtered list
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


def nombre_combinaisons(n):
    # Variables
    total_combinations = 0
    # Fonction
    for k in range(2, n + 1):
        combinations = math.comb(n, k)
        total_combinations += combinations
    return total_combinations


def dynamique_best_combinaisons(actions_updated, budget_max):
    # Convertir les clés du dictionnaire en une liste d'actions
    actions_list = list(actions_updated)
    # Obtenir le nombre d'actions
    n = len(actions_list)
    # Initialiser une liste 2D (dp) pour stocker les résultats intermédiaires
    dp = [[0 for _ in range(budget_max + 1)] for _ in range(n + 1)]
    # Initialiser une liste 2D (selected_actions) pour stocker les actions sélectionnées pour chaque budget
    selected_actions = [[[] for _ in range(budget_max + 1)] for _ in range(n + 1)]

    # Parcourir chaque action
    for i in range(0, n):
        # Obtenir l'action courante
        action = actions_list[i]
        # Obtenir le prix et le profit de l'action courante
        action_price = int(action.get('price'))
        action_profit = int(action.get('profit'))

        # Parcourir chaque valeur de budget
        for j in range(1, budget_max):
            # Vérifier si l'action courante peut être incluse dans le budget
            if action_price <= j:
                # Vérifier si l'inclusion de l'action courante donne un profit plus élevé
                if action_profit + dp[i][j - action_price] > dp[i][j]:
                    # Mettre à jour le profit pour le budget courant
                    dp[i + 1][j] = action_profit + dp[i][j - action_price]
                    # Mettre à jour les actions sélectionnées pour le budget courant
                    selected_actions[i + 1][j] = selected_actions[i][j - action_price] + [action.get("name")]
                else:
                    # Si ne pas inclure l'action courante est plus rentable, mettre à jour les valeurs en conséquence
                    dp[i + 1][j] = dp[i][j]
                    selected_actions[i + 1][j] = selected_actions[i][j]
            else:
                # Si l'action courante ne peut pas être incluse dans le budget,
                # utiliser les valeurs de la ligne précédente
                dp[i + 1][j] = dp[i][j]
                selected_actions[i + 1][j] = selected_actions[i][j]

    # Obtenir la combinaison optimale d'actions pour le budget maximum
    combinaison_optimale = selected_actions[n][budget_max - 1]
    # Retourner la combinaison optimale
    return combinaison_optimale


def profit_cout_combinaison(actions_list, budget_max):
    optimal_combination = dynamique_best_combinaisons(actions_list, budget_max)

    cout_total = 0
    total_profit = 0

    for action_name in optimal_combination:
        for action in actions_list:
            if action['name'] == action_name:
                cout_total += float(action['price'])
                total_profit += (float(action['profit']))

                break  # Une fois que la correspondance est trouvée, sortez de la boucle interne
    cout_total = cout_total / 100
    total_profit = round(total_profit / (100 * 100), 2)

    return optimal_combination, total_profit, cout_total


def diplay_best_combination(file_path):
    # Variables
    budget_max = 500 * 100
    # Fonction
    print("Début du programme")
    start = time.time()
    actions_list = update_actions(file_path)
    best_combinaison, max_profit, cout_total = profit_cout_combinaison(actions_list, budget_max)
    print("La meilleure combinaison est la suivante:\n", best_combinaison)
    print("Le profit total de cette combinaison est: ", max_profit, "€")
    print("le coût total d'achat des actions de la combinaison est: ", cout_total, "€")

    end_time = (time.time() - start)
    print("Fin du programme: ", convert(end_time))


file_path = "data/dataset2.csv"
diplay_best_combination(file_path)
