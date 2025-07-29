# app.py (Version Excel -> CSV)
# ------------------------------------------
# Ce script lit un fichier EXCEL, nettoie les données,
# et exporte le résultat dans un NOUVEAU FICHIER CSV.
# ------------------------------------------

import pandas as pd
from ftfy import fix_text

# La fonction de correction ne change pas, elle est parfaite.
def deep_fix(text):
    if not isinstance(text, str):
        return text
    try:
        corrected = text.encode('utf-8').decode('latin1')
        return fix_text(corrected)
    except Exception:
        return fix_text(text)

# --- Noms des fichiers ---
fichier_entree_excel = 'donnees_cassees.xlsx'  # <--- ON LIT UN EXCEL
fichier_sortie_csv = 'donnees_corrigees.csv'   # <--- ON ÉCRIT UN CSV

print(f"Lecture du fichier Excel : {fichier_entree_excel}")

# --- Étape 1 : Lecture du fichier Excel ---
# On utilise pd.read_excel pour charger les données dans le DataFrame.
df = pd.read_excel(fichier_entree_excel)

print("Application de la fonction de correction...")
# --- Étape 2 : Application de la fonction (ne change pas) ---
df['category_fixed'] = df['category_raw'].apply(deep_fix)

print(f"Export du fichier CSV corrigé : {fichier_sortie_csv}")
# --- Étape 3 : Export du fichier au format CSV ---
# On utilise df.to_csv pour enregistrer le résultat.
# encoding='utf-8-sig' est très important pour que les accents
# s'affichent correctement si vous ouvrez le CSV avec Excel.
df.to_csv(fichier_sortie_csv, index=False, encoding='utf-8-sig')

print("✅ Opération terminée ! Le fichier Excel a été lu et un fichier CSV propre a été créé.")