import pandas as pd
import json


def load_data(filepath):
    """Charge les données depuis un fichier Excel."""
    return pd.read_excel(filepath)


def count_total_activity_occurrences(dataframe):
    """Compte le nombre total d'occurrences pour chaque activité pour toutes les personnes."""
    return dataframe.groupby('Activity').size().rename('Total_Occurrences')


def calculate_person_activity_ratio(dataframe, total_occurrences, person_name=None):
    """Calcule le ratio du nombre de fois qu'une personne fait une activité par rapport au total des occurrences de cette activité."""
    # Compte le nombre de fois que chaque personne fait chaque activité
    person_activity_counts = dataframe.groupby(['Nom', 'Activity']).size().rename(
        'Person_Activity_Counts').reset_index()

    # Fusionne les occurrences totales des activités pour toutes les personnes avec les données
    merged_data = person_activity_counts.merge(total_occurrences, left_on='Activity', right_index=True, how='left')

    # Calcule le ratio pour chaque personne
    merged_data['Activity_Ratio'] = merged_data['Person_Activity_Counts'] / merged_data['Total_Occurrences']

    # Normalisation des ratios pour toutes les personnes
    max_ratios = merged_data['Activity_Ratio'].max()
    merged_data['Normalized_Rating'] = ((merged_data['Activity_Ratio'] / max_ratios) * 5).round().astype(int)

    # Si une personne spécifique est mentionnée, ne garde que ses données
    if person_name:
        merged_data = merged_data[merged_data['Nom'] == person_name]

    return merged_data


def normalize_ratings(activity_data):
    """Normalise les ratings pour être entre 0 et 5 et arrondit les résultats à des entiers, normalisé par activité."""
    max_ratios = activity_data.groupby('Activity')['Activity_Ratio'].transform('max')

    # Vérifier si le maximum des ratios est nul
    activity_data['Normalized_Rating'] = 0  # Initialiser à 0 par défaut
    activity_data.loc[max_ratios > 0, 'Normalized_Rating'] = (
            (activity_data['Activity_Ratio'] / max_ratios) * 5
    ).round().astype(int)

    return activity_data


def save_to_files(activity_data, base_filename):
    """Sauvegarde les données dans un fichier CSV, JSON et TXT."""
    csv_filename = f"{base_filename}.csv"
    json_filename = f"{base_filename}.json"
    txt_filename = f"{base_filename}.txt"

    activity_data.to_csv(csv_filename, index=False)
    activity_data.to_json(json_filename, orient='records', lines=True)
    with open(txt_filename, 'w') as file:
        for idx, row in activity_data.iterrows():
            file.write(str(row.to_dict()) + '\n')


def main(filepath, base_filename='normalized_ratings', person_name=None):
    df = load_data(filepath)

    # Calcul des occurrences totales d'activités sur toutes les personnes
    total_occurrences = count_total_activity_occurrences(df)

    # Calcul des ratios, tout en tenant compte de toutes les occurrences
    person_activity_ratio = calculate_person_activity_ratio(df, total_occurrences, person_name)

    # Normalisation des données
    normalized_data = normalize_ratings(person_activity_ratio)

    # Sauvegarde des résultats
    save_to_files(normalized_data, base_filename)


if __name__ == "__main__":
    # Example usage: Generate data for "John Doe" or for everyone if no name is provided
    import sys
    # person_name = None if len(sys.argv) < 2 else sys.argv[1]
    person_name = None
    main('PKG_Dev.xlsx', 'normalized_ratings', person_name=person_name)
