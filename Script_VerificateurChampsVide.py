import json


def verifier_champs_vides(chemin_fichier, champ_a_verifier):
    # Charger le fichier JSON
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)

    # Liste pour stocker les éléments avec le champ vide
    elements_vides = []
    elements_absents = []

    # Vérifier chaque élément
    for i, element in enumerate(donnees):
        # Vérifier si le champ existe
        if champ_a_verifier not in element:
            elements_absents.append((i, element))
            continue

        # Vérifier si le champ est vide
        valeur = element[champ_a_verifier]
        if valeur is None or valeur == "" or (isinstance(valeur, (list, dict)) and not valeur):
            elements_vides.append((i, element))

    # Afficher les résultats
    print(f"\nRésultats de la vérification pour le champ '{champ_a_verifier}' :")
    print(f"Total d'éléments dans le fichier : {len(donnees)}")

    if elements_absents:
        print(f"\nChamp '{champ_a_verifier}' absent dans {len(elements_absents)} éléments :")
        for i, element in elements_absents[:5]:  # Limiter l'affichage aux 5 premiers pour éviter un output trop long
            print(f"  - Index {i}: {json.dumps(element, ensure_ascii=False)[:100]}...")
        if len(elements_absents) > 5:
            print(f"  ... et {len(elements_absents) - 5} autres éléments")
    else:
        print(f"\nLe champ '{champ_a_verifier}' est présent dans tous les éléments.")

    if elements_vides:
        print(f"\nChamp '{champ_a_verifier}' vide dans {len(elements_vides)} éléments :")
        for i, element in elements_vides[:5]:  # Limiter l'affichage aux 5 premiers
            print(f"  - Index {i}: {json.dumps(element, ensure_ascii=False)[:100]}...")
        if len(elements_vides) > 5:
            print(f"  ... et {len(elements_vides) - 5} autres éléments")
    else:
        print(f"\nLe champ '{champ_a_verifier}' n'est vide dans aucun élément.")

    return {
        "elements_vides": elements_vides,
        "elements_absents": elements_absents
    }


# Utilisation du script
if __name__ == "__main__":
    chemin_fichier = "DataSet_BornesElec.json"  # Remplacez par le chemin de votre fichier JSON
    champ_a_verifier = "observations"  # Remplacez par le champ que vous voulez vérifier

    resultats = verifier_champs_vides(chemin_fichier, champ_a_verifier)
