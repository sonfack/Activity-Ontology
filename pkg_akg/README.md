# Code rating.py

# Analyse de suivi d'activités

## Vue d'ensemble
Ce script traite un fichier Excel contenant des données sur la participation individuelle à diverses activités, calcule des ratings normalisés et produit un fichier structuré avec des données agrégées.

## Étapes de la fonction `main`

1. **Chargement des Données**
   - `load_data(filepath)`: Lit un fichier Excel spécifié et le charge dans un DataFrame pandas contenant les données brutes.

2. **Comptage des Activités**
   - `count_activities(df)`: Regroupe les données par personne et par activité pour compter le nombre de fois que chaque personne a participé à chaque activité. Retourne un DataFrame avec les colonnes 'Nom', 'Activity', et 'Counts'.

3. **Calcul des Ratings**
   - `calculate_log_ratings(activity_counts)`: Transforme les comptages en ratings en utilisant une échelle logarithmique pour atténuer l'impact des grandes disparités de comptages. Les ratings sont normalisés par rapport au rating logarithmique maximal pour chaque activité et mis à l'échelle entre 1 et 5.

4. **Agrégation des Ratings par Personne**
   - `aggregate_person_ratings(rated_activities)`: Calcule le rating moyen pour chaque personne en agrégeant tous ses ratings normalisés. Cette étape simplifie les données en consolidant de multiples ratings en une seule métrique moyenne.

5. **Extraction des Ratings Extrêmes**
   - `get_min_max_ratings(person_ratings)`: Identifie les valeurs minimales et maximales parmi les ratings moyens, indiquant les ratings les plus bas et les plus élevés parmi toutes les personnes.

6. **Compilation de la Liste des Activités**
   - `get_activity_list(activity_counts)`: Extrait une liste unique de toutes les activités mentionnées dans les données, utile pour des analyses ou des affichages ultérieurs.

7. **Sauvegarde des Résultats**
   - `save_to_file(person_ratings, min_rating, max_rating, activities, filename, format)`: Prépare un fichier de sortie contenant les ratings agrégés, les ratings extrêmes et la liste des activités. Prend en charge deux formats de sortie : JSON et TXT, en fonction du paramètre spécifié.

