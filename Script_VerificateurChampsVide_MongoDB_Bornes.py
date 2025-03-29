import json


def verifier_champ_json(chemin_fichier, champ_a_verifier):
    # Charger le fichier JSON
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)

    # Compteurs pour les statistiques
    total_features = len(donnees)
    champ_present = 0
    champ_absent = 0
    champ_vide = 0

    # Liste pour stocker les features problématiques
    features_problematiques = []

    # Parcourir toutes les features
    for i, feature in enumerate(donnees):
        if "type" not in feature or feature["type"] != "Feature" or "properties" not in feature:
            print(f"La feature {i} n'a pas la structure attendue.")
            continue

        properties = feature["properties"]

        if champ_a_verifier in properties:
            champ_present += 1
            if properties[champ_a_verifier] == "" or properties[champ_a_verifier] is None:
                champ_vide += 1
                features_problematiques.append((i, feature))
        else:
            champ_absent += 1
            features_problematiques.append((i, feature))

    # Afficher les résultats
    print(f"\nRésultats de la vérification pour le champ '{champ_a_verifier}' :")
    print(f"Total des features : {total_features}")
    print(f"Champ présent : {champ_present}")
    print(f"Champ absent : {champ_absent}")
    print(f"Champ vide : {champ_vide}")

    # Afficher les détails des features problématiques
    if features_problematiques:
        print("\nDétails des features problématiques :")
        for i, feature in features_problematiques[:5]:
            print(f"\nFeature {i}:")
            print(json.dumps(feature, ensure_ascii=False, indent=2))
        if len(features_problematiques) > 5:
            print(f"\n... et {len(features_problematiques) - 5} autres features problématiques.")

    return {
        "total_features": total_features,
        "champ_present": champ_present,
        "champ_absent": champ_absent,
        "champ_vide": champ_vide,
        "features_problematiques": features_problematiques
    }


# Utilisation du script
if __name__ == "__main__":
    chemin_fichier = "MongoDB_BornesElec.json"
    champ_a_verifier = "consolidated_commune"

    resultats = verifier_champ_json(chemin_fichier, champ_a_verifier)
