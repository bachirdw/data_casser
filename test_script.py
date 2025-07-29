""" # test_script.py (Version pour traiter le fichier Excel multi-colonnes)
# ----------------------------------------------------
# Ce script teste la fonction deep_fix() sur le fichier Excel réel
# et nettoie les colonnes 'search_term', 'category', et 'product_name'.
# ----------------------------------------------------

import pandas as pd
import os
from ftfy import fix_text

# La fonction de correction ne change pas, elle est parfaite.
def deep_fix(text):
    if not isinstance(text, str):
        return text
    try:
        # Cette combinaison est souvent efficace pour les doubles encodages
        corrected = text.encode('latin1').decode('utf-8')
        return fix_text(corrected)
    except Exception:
        return fix_text(text)

# --- Étape 1 : Définir les noms des fichiers et des colonnes ---

# Le nom de votre fichier Excel
FICHIER_A_TESTER = 'donnees_cassees.xlsx'

# La liste des colonnes que vous voulez corriger
COLONNES_A_CORRIGER = ['search_term', 'category', 'product_name']


print(f"--- Lancement du script de test sur le fichier '{FICHIER_A_TESTER}' ---")

# Vérification de la présence du fichier
if not os.path.exists(FICHIER_A_TESTER):
    print(f"ERREUR : Le fichier '{FICHIER_A_TESTER}' est introuvable.")
else:
    print(f"✅ Fichier trouvé : {FICHIER_A_TESTER}")
    try:
        # --- Étape 2 : Lecture du fichier Excel ---
        df = pd.read_excel(FICHIER_A_TESTER)
        
        # On affiche un aperçu pour confirmer la bonne lecture
        print("\n--- Aperçu du DataFrame Original (5 premières lignes) ---")
        print(df.head())

        # --- Étape 3 : Application de la correction en boucle ---
        print(f"\nApplication de la correction sur les colonnes : {COLONNES_A_CORRIGER}...")

        for colonne in COLONNES_A_CORRIGER:
            # On vérifie si la colonne existe bien dans le DataFrame
            if colonne in df.columns:
                nouvelle_colonne = f"{colonne}_fixed"
                print(f"  -> Traitement de '{colonne}' -> création de '{nouvelle_colonne}'")
                df[nouvelle_colonne] = df[colonne].apply(deep_fix)
            else:
                print(f"  -> ATTENTION : La colonne '{colonne}' n'a pas été trouvée dans le fichier.")

        # --- Étape 4 : Affichage du résultat corrigé pour vérification ---
        print("\n--- Aperçu du DataFrame Corrigé (colonnes originales et corrigées) ---")
        
        # On construit la liste des colonnes à afficher pour comparer facilement
        colonnes_a_afficher = []
        for col in COLONNES_A_CORRIGER:
            if col in df.columns: # S'assurer que la colonne originale existe
                 colonnes_a_afficher.append(col)
                 colonnes_a_afficher.append(f"{col}_fixed")
        
        print(df[colonnes_a_afficher].head(10)) # On affiche les 10 premières lignes


        print("\n✅ Test multi-colonnes terminé avec succès !")

    except Exception as e:
        print(f"\nUNE ERREUR EST SURVENUE : {e}") """

# test_script.py (Version de test focalisée sur la colonne 'search_term')
# ----------------------------------------------------------------------
# Ce script teste une fonction de correction spécifiquement sur la colonne
# 'search_term' du fichier Excel et affiche 50 lignes pour validation.
# ----------------------------------------------------------------------

import pandas as pd
import os

# --- La fonction de correction la plus standard ---
# C'est la plus efficace pour les problèmes d'encodage courants comme "biÃ¨re" -> "bière".
def corriger_texte_simple(text):
    if not isinstance(text, str):
        return text
    try:
        # La correction la plus probable : lire le texte comme du latin-1 et l'interpréter en UTF-8
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Si une erreur se produit, retourner le texte original
        return text

# --- Paramètres du test ---

# Le nom de votre fichier Excel
FICHIER_A_TESTER = 'donnees_cassees.xlsx'
# La colonne unique que nous voulons tester
COLONNE_A_CORRIGER = 'search_term'


print(f"--- Lancement du test sur la colonne '{COLONNE_A_CORRIGER}' du fichier '{FICHIER_A_TESTER}' ---")

# Vérification de la présence du fichier
if not os.path.exists(FICHIER_A_TESTER):
    print(f"ERREUR : Le fichier '{FICHIER_A_TESTER}' est introuvable.")
else:
    print(f"✅ Fichier trouvé : {FICHIER_A_TESTER}")
    try:
        # --- Étape 1 : Lecture du fichier Excel ---
        df = pd.read_excel(FICHIER_A_TESTER)
        
        # --- Étape 2 : Application de la fonction de correction ---
        # On définit le nom de la nouvelle colonne
        colonne_corrigee = f"{COLONNE_A_CORRIGER}_fixed"
        
        print(f"\nApplication de la correction sur '{COLONNE_A_CORRIGER}'...")
        df[colonne_corrigee] = df[COLONNE_A_CORRIGER].apply(corriger_texte_simple)

        # --- Étape 3 : Affichage du résultat pour vérification ---
        print(f"\n--- Vérification des 50 premières lignes ---")
        
        # On configure Pandas pour qu'il affiche plus de texte
        pd.set_option('display.max_rows', 100)
        pd.set_option('display.max_colwidth', 80) # Augmente la largeur de la colonne affichée
        
        # On affiche les deux colonnes (originale et corrigée) pour comparer
        print(df[[COLONNE_A_CORRIGER, colonne_corrigee]].head(100))

        print("\n✅ Test focalisé terminé !")

    except Exception as e:
        print(f"\nUNE ERREUR EST SURVENUE : {e}")