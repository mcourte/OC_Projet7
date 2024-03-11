from modules import bruteforce
from modules import optimized


def main():
    while True:
        print("\nMenu :")
        print("1. Bruteforce avec 20 actions.")
        print("2. Optimized avec 20 actions.")
        print("3. Optimized avec Data Sienna1.")
        print("4. Optimized avec Data Sienna2.")
        print("5. Bruteforce avec Data Sienna1.")
        print("6. Quitter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            file_path = "data/dataexo1.csv"
            bruteforce.diplay_best_combination(file_path)
        elif choice == "2":
            file_path = "data/dataexo1.csv"
            optimized.diplay_best_combination(file_path)
        elif choice == "3":
            file_path = "data/dataset1.csv"
            optimized.diplay_best_combination(file_path)
        elif choice == "4":
            file_path = "data/dataset2.csv"
            optimized.diplay_best_combination(file_path)
        elif choice == "5":
            file_path = "data/dataset1.csv"
            bruteforce.diplay_best_combination(file_path)
        elif choice == "6":
            print("Arrêt du programme ! A bientôt")
            break
        else:
            print("Choix invalide. Veuillez choisir une option valide.")


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print("Arret du programme")
