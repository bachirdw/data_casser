# app.py (Version Finale de Production)
# ----------------------------------------------------------------------
# Ce script lit le fichier Excel 'donnees_cassees.xlsx', nettoie les
# colonnes 'search_term', 'category', et 'product_name' sur l'ensemble
# des données, et crée un nouveau fichier Excel complet et corrigé.
# ----------------------------------------------------------------------

import pandas as pd

# --- La fonction de correction validée par les tests ---
def corriger_texte_simple(text):
    """
    Corrige les problèmes d'encodage les plus courants (ex: 'biÃ¨re' -> 'bière').
    Prend en entrée une chaîne de caractères et retourne la version corrigée.
    """
    if not isinstance(text, str):
        return text  # Ne fait rien si ce n'est pas du texte
    try:
        # La méthode qui a fonctionné : encoder en latin1, décoder en utf-8
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Sécurité : si une erreur se produit, on retourne le texte original
        return text

# --- Paramètres de Production ---

# Le nom de votre fichier Excel d'entrée
FICHIER_ENTREE = 'donnees_cassees.xlsx'
# Le nom du fichier Excel de sortie qui contiendra toutes les données propres
FICHIER_SORTIE = 'donnees_corrigees.xlsx'
# La liste complète des colonnes à nettoyer
COLONNES_A_NETTOYER = ['search_term', 'category', 'product_name']


print("--- Lancement du script de production ---")

try:
    # --- Étape 1 : Lecture du fichier Excel d'entrée ---
    print(f"Lecture du fichier : '{FICHIER_ENTREE}'...")
    df = pd.read_excel(FICHIER_ENTREE)
    print("✅ Fichier lu avec succès.")

    # --- Étape 2 : Nettoyage des données sur toutes les lignes ---
    print(f"Nettoyage des colonnes : {COLONNES_A_NETTOYER}...")
    for colonne in COLONNES_A_NETTOYER:
        if colonne in df.columns:
            # On crée une nouvelle colonne propre pour chaque colonne à nettoyer
            nouvelle_colonne = f"{colonne}_fixed"
            print(f"  -> Traitement de '{colonne}'...")
            # On applique la fonction de correction à la colonne entière
            df[nouvelle_colonne] = df[colonne].apply(corriger_texte_simple)
        else:
            print(f"  -> ATTENTION : La colonne '{colonne}' n'a pas été trouvée et a été ignorée.")
    print("✅ Nettoyage terminé.")

    # --- Étape 3 : Export du DataFrame complet dans un nouveau fichier Excel ---
    print(f"Exportation du fichier complet vers '{FICHIER_SORTIE}'...")
    # 'index=False' est crucial pour ne pas ajouter une colonne inutile dans le fichier Excel final.
    # 'engine='openpyxl'' est le moteur recommandé pour les fichiers .xlsx.
    df.to_excel(FICHIER_SORTIE, index=False, engine='openpyxl')
    print("✅ Exportation réussie !")
    
    print("\n--- Opération de production terminée avec succès ! ---")

except FileNotFoundError:
    print(f"ERREUR : Le fichier d'entrée '{FICHIER_ENTREE}' est introuvable.")
except Exception as e:
    print(f"\nUNE ERREUR INATTENDUE EST SURVENUE : {e}")