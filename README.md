# Projet 7 Résolvez des problèmes en utilisant des algorithmes en Python  
  
***Compétences acquises lors de la réalisation de ce projet:***  
  
*1. Déconstruire un problème*  
*2. Développer un algorithme pour résoudre un problème*  

## But du projet :

Créer des algorithmes afin de calculer la meilleure combinaison d'action (rapport coût/profit).  
Deux types d'algorithmes à créer : 
* un bruteforce qui détermine l'ensemble des combinaisons.
* Un optimized permettant de calculer au fur et à mesure la meilleure combinaison.  


## Etape 1 : Télécharger le code

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.  
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.  

## Etape 2 ; Installer Python et ouvrir le terminal de commande

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :  
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

## Etape 3 : Création de l'environnement virtuel

Se placer dans le dossier où l'on a extrait l'ensemble des documents grâce à la commande ``cd``  
Exemple :
```
cd home/magali/OpenClassrooms/Formation/Projet_7
```


Dans le terminal de commande, executer la commande suivante :
```
python3 -m venv env
```


Activez l'environnement virtuel
```
source env/bin/activate
```
> Pour les utilisateurs de Windows, la commande est la suivante : 
> ``` env\Scripts\activate.bat ```

## Etape 4 : Télécharger les packages nécessaires au bon fonctionnement du programme

Dans le terminal, taper la commande suivante :
```
pip install -r requierements.txt
```

## Etape 5 : Lancer le programme

Taper la commande suivante :
```
python3 main.py
```


## Etape 6 : Utilisation du programme

Plusieurs choix s'offrent à vous.  
1. Calcul de la meilleure combinaison à partir d'une liste de 20 actions en utilisant "bruteforce",  
2. Calcul de la meilleure combinaison à partir d'une liste de 20 actions en utilisant "optimized",  
3. Calcul de la meilleure combinaison du Set 1 de Sienna avec "optimized",  
4. Calcul de la meilleure combinaison du Set 2 de Sienna avec "optimized",  
5. Calcul de la meilleure combinaison du Set 1 de Sienna avec "bruteforce".  
