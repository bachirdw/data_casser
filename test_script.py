# test_script.py (Version de test finale pour 3 colonnes)
# ----------------------------------------------------------------------
# Ce script teste la fonction de correction sur les colonnes
# 'search_term', 'category', et 'product_name' du fichier Excel.
# ----------------------------------------------------------------------

import pandas as pd
import os

# --- La fonction de correction que nous avons validée ---
def corriger_texte_simple(text):
    if not isinstance(text, str):
        return text
    try:
        # La correction qui fonctionne : encode en latin1, décode en utf-8
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

# --- Paramètres du test ---

# Le nom de votre fichier Excel
FICHIER_A_TESTER = 'donnees_cassees.xlsx'
# La liste COMPLÈTE des colonnes que nous voulons tester
COLONNES_A_CORRIGER = ['search_term', 'category', 'product_name'] # <--- MODIFIÉ


print(f"--- Lancement du test final sur les colonnes {COLONNES_A_CORRIGER} ---")

# Vérification de la présence du fichier
if not os.path.exists(FICHIER_A_TESTER):
    print(f"ERREUR : Le fichier '{FICHIER_A_TESTER}' est introuvable.")
else:
    print(f"✅ Fichier trouvé : {FICHIER_A_TESTER}")
    try:
        # --- Étape 1 : Lecture du fichier Excel ---
        df = pd.read_excel(FICHIER_A_TESTER)
        
        # --- Étape 2 : Application de la correction en boucle ---
        print(f"\nApplication de la correction...")
        for colonne in COLONNES_A_CORRIGER:
            if colonne in df.columns:
                nouvelle_colonne = f"{colonne}_fixed"
                print(f"  -> Traitement de '{colonne}'...")
                df[nouvelle_colonne] = df[colonne].apply(corriger_texte_simple)
            else:
                print(f"  -> ATTENTION : Colonne '{colonne}' non trouvée.")

        # --- Étape 3 : Affichage du résultat pour vérification ---
        print(f"\n--- Vérification des 50 premières lignes ---")
        
        # On construit la liste des colonnes à afficher
        colonnes_a_afficher = []
        for col in COLONNES_A_CORRIGER:
            if col in df.columns:
                 colonnes_a_afficher.append(col)
                 colonnes_a_afficher.append(f"{col}_fixed")
        
        # On configure Pandas pour bien voir les résultats
        pd.set_option('display.max_rows', 100)
        pd.set_option('display.max_colwidth', 60)
        
        # On affiche le tableau comparatif
        print(df[colonnes_a_afficher].head(50))

        print("\n✅ Test final des 3 colonnes terminé !")

    except Exception as e:
        print(f"\nUNE ERREUR EST SURVENUE : {e}")