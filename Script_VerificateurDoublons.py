import json
from collections import defaultdict


def verifier_doublons(chemin_fichier, champ_a_verifier):
    # Charger le fichier JSON
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)

    # Utiliser un defaultdict pour regrouper les éléments par la valeur du champ spécifié
    groupes = defaultdict(list)
    for element in donnees:
        if champ_a_verifier in element:
            valeur = element[champ_a_verifier]
            groupes[valeur].append(element)
        else:
            print(f"Attention : Le champ '{champ_a_verifier}' n'existe pas dans tous les éléments.")

    # Identifier les doublons
    doublons = {valeur: elements for valeur, elements in groupes.items() if len(elements) > 1}

    # Afficher les résultats
    if doublons:
        print(f"Doublons trouvés pour le champ '{champ_a_verifier}' :")
        for valeur, elements in doublons.items():
            print(f"\nValeur '{valeur}' apparaît {len(elements)} fois :")
            for element in elements:
                print(json.dumps(element, ensure_ascii=False, indent=2))
    else:
        print(f"Aucun doublon trouvé pour le champ '{champ_a_verifier}'.")

    return doublons


# Utilisation du script
if __name__ == "__main__":
    chemin_fichier = "DB_communes.json"  # Remplacez par le chemin de votre fichier JSON
    champ_a_verifier = "commune"  # Remplacez par le champ que vous voulez vérifier

    doublons = verifier_doublons(chemin_fichier, champ_a_verifier)
