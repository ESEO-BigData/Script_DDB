import csv
import json

def traiter_csv_communes(chemin_csv, chemin_sortie):
    # Dictionnaire pour stocker les communes déjà traitées (pour éviter les doublons d'arrondissements)
    communes_traitees = {}

    # Lire le fichier CSV
    with open(chemin_csv, 'r', encoding='utf-8') as fichier_csv:
        lecteur_csv = csv.DictReader(fichier_csv)

        for ligne in lecteur_csv:
            nom_commune = ligne["nom_commune_complet"]

            # Vérifier si c'est un arrondissement
            if " 0" in nom_commune or " 1" in nom_commune or " 2" in nom_commune:
                # Extraire le nom de base de la commune (sans le numéro d'arrondissement)
                nom_base = nom_commune.split(" ")[0]

                # Si on a déjà traité cette commune de base, on saute
                if nom_base in communes_traitees:
                    continue

                # Sinon, on utilise le nom de base comme nom de commune
                nom_commune = nom_base

            # Vérifier si on a déjà traité cette commune
            if nom_commune in communes_traitees:
                continue

            # Formater le code département sur 2 caractères
            code_dept = ligne["code_departement"]
            if len(code_dept) == 1:
                code_dept = "0" + code_dept

            # Formater le code postal sur 5 caractères
            code_postal = ligne["code_postal"]
            if len(code_postal) < 5:
                code_postal = "0" * (5 - len(code_postal)) + code_postal

            # Formater le code INSEE sur 5 caractères
            code_insee = ligne["code_commune_INSEE"]
            if len(code_insee) < 5:
                code_insee = "0" * (5 - len(code_insee)) + code_insee

            # Créer l'objet commune
            commune = {
                "commune": nom_commune.lower(),
                "nombre_bornes": 0,
                "nombre_points_charge": 0,
                "ratio_bornes_points": 0,
                "NB_VP_RECHARGEABLES_EL": 0,
                "NB_VP_RECHARGEABLES_GAZ": 0,
                "NB_VP": 0,
                "departement": ligne["nom_departement"],
                "code_departement": code_dept,
                "region": ligne["nom_region"],
                "code_postal": code_postal,
                "code_commune_INSEE": code_insee
            }

            # Ajouter la commune au dictionnaire des communes traitées
            communes_traitees[nom_commune] = commune

    # Convertir le dictionnaire en liste pour le JSON
    communes_liste = list(communes_traitees.values())

    # Écrire le fichier JSON
    with open(chemin_sortie, 'w', encoding='utf-8') as fichier_json:
        json.dump(communes_liste, fichier_json, ensure_ascii=False, indent=2)

    print(f"Traitement terminé. {len(communes_liste)} communes ont été traitées.")
    print(f"Fichier JSON créé : {chemin_sortie}")


# Utilisation du script
if __name__ == "__main__":
    chemin_csv_entree = "communes_france.csv"  # Remplacez par le chemin de votre fichier CSV
    chemin_json_sortie = "DB_Communes.json"  # Nom du fichier JSON de sortie

    traiter_csv_communes(chemin_csv_entree, chemin_json_sortie)
