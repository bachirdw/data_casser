# app.py (Version Finale avec Interface Streamlit)
# ----------------------------------------------------------------------
# Une application web simple pour nettoyer les problèmes d'encodage
# dans des fichiers Excel, comme demandé.
# ----------------------------------------------------------------------

import streamlit as st
import pandas as pd
from io import BytesIO  # Nécessaire pour créer le fichier en mémoire pour le téléchargement

# --- La fonction de correction que nous avons validée ---
# On la place en haut du script pour qu'elle soit disponible pour l'application.
def corriger_texte_simple(text):
    """
    Corrige du problèmes d'encodage (ex: 'biÃ¨re' -> 'bière').
    """
    if not isinstance(text, str):
        return text
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

# --- Fonction utilitaire pour préparer le fichier Excel pour le téléchargement ---
def to_excel(df):
    """Convertit un DataFrame en un fichier Excel en mémoire (bytes)."""
    output = BytesIO()
    # On utilise 'xlsxwriter' comme moteur pour écrire dans le buffer mémoire
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Donnees_Corrigees')
    # On récupère les données binaires du fichier Excel créé
    processed_data = output.getvalue()
    return processed_data


# ======================================================================
# --- INTERFACE DE L'APPLICATION STREAMLIT ---
# ======================================================================

# Configuration de la page
st.set_page_config(layout="wide", page_title="Correcteur de Fichiers")

# On crée deux colonnes : une petite pour le logo, une grande pour le titre.
# Le ratio [1, 5] signifie que la deuxième colonne sera 5 fois plus large que la première.
col1, col2 = st.columns([1, 5])

with col1:
    st.image("unlimitail_logo.png", width=1000) 

with col2:
    st.title("Outil de Génération de Rapports ")
    st.write("Application pour nettoyer les fichiers Excel")
# --- FIN DE LA MODIFICATION ---


st.header("1. Téléchargez votre fichier")
# --- Widget pour le téléchargement du fichier ---
uploaded_file = st.file_uploader("Choisissez un fichier Excel à nettoyer", type=['xlsx'], label_visibility="collapsed")


if uploaded_file is not None:
    with st.spinner('Lecture du fichier Excel...'):
        df = pd.read_excel(uploaded_file)
    
    st.success("✅ Fichier lu avec succès !")
    st.header("2. Aperçu des données originales")
    st.dataframe(df.head())

    with st.sidebar:
        st.header("⚙️ Options")
        
        colonnes_a_corriger = st.multiselect(
            "Choisissez les colonnes à nettoyer",
            options=df.columns,
            default=None
        )
        
        appliquer_correction = st.checkbox("Oui, remplacer les caractères spéciaux")

    if appliquer_correction and colonnes_a_corriger:
        
        st.header("3. Résultats de la Correction")
        df_corrige = df.copy()

        with st.spinner("Application de la correction..."):
            for colonne in colonnes_a_corriger:
                nouvelle_colonne = f"{colonne}_fixed"
                df_corrige[nouvelle_colonne] = df[colonne].apply(corriger_texte_simple)

        st.success("✅ Correction appliquée !")
        
        colonnes_a_afficher = []
        for col in colonnes_a_corriger:
             colonnes_a_afficher.append(col)
             colonnes_a_afficher.append(f"{col}_fixed")
        st.dataframe(df_corrige[colonnes_a_afficher].head(20))

        st.header("4. Téléchargement")
        st.write("Le fichier complet avec les nouvelles colonnes corrigées est prêt.")

        donnees_excel_a_telecharger = to_excel(df_corrige)

        st.download_button(
            label="📥 Télécharger le fichier corrigé",
            data=donnees_excel_a_telecharger,
            file_name=f"corrige_{uploaded_file.name}",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    elif appliquer_correction and not colonnes_a_corriger:
        st.warning("Veuillez choisir au moins une colonne à corriger dans la barre latérale.")
