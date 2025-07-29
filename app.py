# app.py (Version Finale de Production - Rectifiée avec lambda)
# ----------------------------------------------------------------------
# Ce script lit le fichier Excel, nettoie les colonnes spécifiées
# en utilisant la syntaxe exacte .apply(lambda ...), et crée un
# nouveau fichier Excel complet et corrigé.
# ----------------------------------------------------------------------

import pandas as pd

# --- La fonction de correction validée (elle ne change pas) ---
def corriger_texte_simple(text):
    """
    Corrige les problèmes d'encodage les plus courants (ex: 'biÃ¨re' -> 'bière').
    Prend en entrée une chaîne de caractères et retourne la version corrigée.
    """
    if not isinstance(text, str):
        return text
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

# --- Paramètres de Production ---
FICHIER_ENTREE = 'donnees_cassees.xlsx'
FICHIER_SORTIE = 'donnees_corrigees.xlsx'
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
            nouvelle_colonne = f"{colonne}_fixed"
            print(f"  -> Traitement de '{colonne}'...")
            
            # --- LA LIGNE MODIFIÉE ---
            # On utilise maintenant une fonction lambda pour appeler notre fonction de correction.
            # C'est la syntaxe exacte qui était dans la demande.
            df[nouvelle_colonne] = df[colonne].apply(lambda x: corriger_texte_simple(x))
            
        else:
            print(f"  -> ATTENTION : La colonne '{colonne}' n'a pas été trouvée et a été ignorée.")
    print("✅ Nettoyage terminé.")

    # --- Étape 3 : Export du DataFrame complet dans un nouveau fichier Excel ---
    print(f"Exportation du fichier complet vers '{FICHIER_SORTIE}'...")
    df.to_excel(FICHIER_SORTIE, index=False, engine='openpyxl')
    print("✅ Exportation réussie !")
    
    print("\n--- Opération de production terminée avec succès ! ---")

except FileNotFoundError:
    print(f"ERREUR : Le fichier d'entrée '{FICHIER_ENTREE}' est introuvable.")
except Exception as e:
    print(f"\nUNE ERREUR INATTENDUE EST SURVENUE : {e}")