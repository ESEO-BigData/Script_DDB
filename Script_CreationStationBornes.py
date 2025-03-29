import json
from collections import defaultdict


def traiter_bornes_par_station(chemin_fichier_entree, chemin_fichier_sortie):
    # Charger le fichier JSON d'entrée
    with open(chemin_fichier_entree, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)

    # Vérifier si le fichier a la structure attendue
    if "type" not in donnees or donnees["type"] != "FeatureCollection" or "features" not in donnees:
        print("Le fichier JSON d'entrée n'a pas la structure FeatureCollection attendue.")
        return

    # Dictionnaire pour regrouper les informations par station
    stations = defaultdict(lambda: {"nombre_bornes_station": 0, "code_insee_commune": "", "consolidated_commune": ""})

    # Parcourir toutes les features (bornes)
    for feature in donnees["features"]:
        if "properties" not in feature:
            continue

        properties = feature["properties"]
        id_station = properties.get("id_station_itinerance")

        if id_station:
            stations[id_station]["nombre_bornes_station"] += 1

            # Si c'est la première borne pour cette station, enregistrer les autres informations
            if stations[id_station]["code_insee_commune"] == "":
                code_insee = properties.get("code_insee_commune", "")
                stations[id_station]["code_insee_commune"] = code_insee.zfill(5)  # Assurer 5 caractères
                stations[id_station]["consolidated_commune"] = properties.get("consolidated_commune", "")

    # Créer la liste finale des stations
    liste_stations = [
        {
            "id_station_itinerance": id_station,
            "nombre_bornes_station": info["nombre_bornes_station"],
            "code_insee_commune": info["code_insee_commune"],
            "consolidated_commune": info["consolidated_commune"]
        }
        for id_station, info in stations.items()
    ]

    # Écrire le fichier JSON de sortie
    with open(chemin_fichier_sortie, 'w', encoding='utf-8') as fichier_sortie:
        json.dump(liste_stations, fichier_sortie, ensure_ascii=False, indent=2)

    print(f"Traitement terminé. {len(liste_stations)} stations traitées.")
    print(f"Fichier JSON créé : {chemin_fichier_sortie}")


# Utilisation du script
if __name__ == "__main__":
    chemin_fichier_entree = "DataSet_BornesElec.json"  # Remplacez par le chemin de votre fichier JSON d'entrée
    chemin_fichier_sortie = "stations_bornes.json"  # Nom du fichier JSON de sortie

    traiter_bornes_par_station(chemin_fichier_entree, chemin_fichier_sortie)
