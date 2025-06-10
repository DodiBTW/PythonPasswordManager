# Gestionnaire de mots de passe Python

Ce projet est une application web de gestion de mots de passe développée en Python avec Flask. Elle permet aux utilisateurs de stocker, ajouter, modifier et supprimer leurs mots de passe de manière sécurisée via une interface web simple.

## Fonctionnalités principales

- **Inscription et connexion sécurisées**
- **Ajout, modification et suppression de mots de passe**
- **Stockage chiffré des mots de passe**
- **Importation de mots de passe depuis un fichier JSON**
- **Interface web intuitive**

## Prérequis

- Python 3.10 ou supérieur
- Les dépendances listées dans `requirements.txt`

## Installation

1. **Cloner le dépôt :**
    ```bash
    git clone https://github.com/DodiBTW/PythonPasswordManager/
    cd PythonPasswordManager
    ```

2. **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configuration de la base de données :**

    - Dans le dossier `app/db/`, vous trouverez un fichier `database.db.example`.
    - **Renommez ce fichier en `database.db`** pour initialiser la base de données :

## Lancement de l'application

Lancez le serveur Flask avec la commande suivante :

```bash
python run.py
```

L'application sera accessible à l'adresse [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Utilisation de l'interface

1. **Inscription :**
    - Rendez-vous sur `/register` pour créer un nouveau compte.
    - Dès la création de votre compte, vous allez recevoir une clé. Cette clé doit être sauvegardée de votre part. Elle sera utilisée pour chiffrer et déchiffrer les mots de passes.

2. **Connexion :**
    - Accédez à `/login` pour vous connecter avec vos identifiants.

3. **Gestion des mots de passe :**
    - Une fois connecté, vous pouvez ajouter, modifier ou supprimer vos mots de passe depuis la page d'accueil.

4. **Importation de mots de passe :**
    - Utilisez la fonctionnalité d'import pour ajouter plusieurs mots de passe à partir d'un fichier JSON.

5. **Déconnexion :**
    - Cliquez sur "Déconnexion" pour fermer votre session.

## Remarques

- **Sécurité :** Les mots de passe sont chiffrés avant d'être stockés dans la base de données.
- **Fichier de configuration :** Assurez-vous que le fichier `database.db` existe dans db avant de lancer l'application.

## Aide

En cas de problème, vérifiez que toutes les dépendances sont installées et que la base de données est bien en place.  
Pour toute question, ouvrez une issue sur le dépôt GitHub.

---