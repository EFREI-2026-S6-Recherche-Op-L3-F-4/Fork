# Projet de Recherche Opérationnelle - Efrei Paris

## Description

Ce projet, réalisé dans le cadre du cours de Recherche Opérationnelle, vise à implémenter et analyser différents algorithmes pour résoudre des problèmes de transport. Les problèmes de transport concernent la minimisation des coûts de déplacement de biens entre plusieurs fournisseurs et clients, un sujet à la fois économique et écologique.

## Fonctionnalités

Le programme inclut plusieurs fonctionnalités clés :
- **Lecture de données** : Extraction des matrices de coûts et des propositions de transport à partir de fichiers `.txt`.
- **Affichage des matrices** : Présentation claire des matrices de coûts et des propositions de transport.
- **Algorithmes de résolution** :
  - **Méthode du coin nord-ouest** : Première approche pour trouver une solution initiale au problème de transport.
  - **Méthode de Balas-Hammer** : Optimisation de la solution en minimisant les coûts grâce à la gestion des pénalités.
  - **Méthode du marche-pied avec potentiel** : Itération pour améliorer la solution jusqu'à optimisation ou identification d'un cycle.

## Comment démarrer

Pour exécuter ce projet, suivez les étapes ci-dessous :

1. Clonez ce dépôt :
   ```bash
   git clone [URL_DU_DEPOT]

    Naviguez dans le répertoire du projet :

    bash

cd [NOM_DU_REPO]

Exécutez le script principal :

bash

    python main.py

Structure des fichiers

Les fichiers du projet sont organisés comme suit :

    main.py : Script principal pour lancer les algorithmes.
    fonctions.py : Contient toutes les fonctions nécessaires à la manipulation des données et à l'exécution des algorithmes.
    /Fichiers_tests : Dossier contenant les fichiers .txt des problèmes de transport à résoudre.
