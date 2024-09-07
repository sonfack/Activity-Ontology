import pandas as pd
import numpy as np
import json

def load_data(filepath):
    """Charge les données depuis un fichier Excel."""
    return pd.read_excel(filepath)

def count_activities(dataframe):
    """Compte le nombre de participations à chaque activité par personne."""
    return dataframe.groupby(['Nom', 'Activity']).size().reset_index(name='Counts')

def calculate_log_ratings(activity_counts):
    """Calcule les ratings basés sur la logique logarithmique pour toutes les activités."""
    activity_counts['Log_Counts'] = np.log10(activity_counts['Counts'] + 1)  # Ajoute 1 pour éviter le log de 0
    max_log = activity_counts.groupby('Activity')['Log_Counts'].transform(max)
    activity_counts['Normalized_Ratings'] = (activity_counts['Log_Counts'] / max_log) * 5
    return activity_counts

def aggregate_person_ratings(activity_counts):
    """Agrège les ratings pour chaque personne en calculant le rating moyen et trie par rating moyen."""
    person_ratings = activity_counts.groupby('Nom')['Normalized_Ratings'].mean().reset_index()
    person_ratings.rename(columns={'Normalized_Ratings': 'Average_Rating'}, inplace=True)
    person_ratings.sort_values(by='Average_Rating', ascending=False, inplace=True)
    return person_ratings

def get_min_max_ratings(person_ratings):
    """Extrait les ratings minimum et maximum des ratings agrégés."""
    min_rating = person_ratings['Average_Rating'].min()
    max_rating = person_ratings['Average_Rating'].max()
    return min_rating, max_rating

def get_activity_list(activity_counts):
    """Retourne la liste unique des activités."""
    return activity_counts['Activity'].unique().tolist()

def save_to_file(data, min_rating, max_rating, activities, filename, format='json'):
    """Sauvegarde les données dans un fichier JSON ou TXT, incluant les ratings extrêmes et la liste des activités."""
    output = {
        "Person_Ratings": data.to_dict(orient='records'),
        "Min_Rating": min_rating,
        "Max_Rating": max_rating,
        "Activities": activities
    }
    if format == 'json':
        with open(filename, 'w') as file:
            json.dump(output, file, indent=4)
    elif format == 'txt':
        with open(filename, 'w') as file:
            file.write(str(output))

def main(filepath, filename='ratings.json', format='json'):
    """Fonction principale pour charger les données, calculer et exporter les ratings."""
    df = load_data(filepath)
    activity_counts = count_activities(df)
    rated_activities = calculate_log_ratings(activity_counts)
    person_ratings = aggregate_person_ratings(rated_activities)
    min_rating, max_rating = get_min_max_ratings(person_ratings)
    activities = get_activity_list(activity_counts)
    save_to_file(person_ratings, min_rating, max_rating, activities, filename, format)
    return person_ratings

def run_analysis():
    filepath = 'PKG_Dev.xlsx'
    output_file = 'ratings.json'
    file_format = 'json'
    results = main(filepath, output_file, file_format)
    print("Ratings exportés dans:", output_file)

if __name__ == "__main__":
    run_analysis()
