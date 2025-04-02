import streamlit as st
import pandas as pd
import os

# ✨ Chargement du glossaire enrichi

def load_data(): file_path = "glossaire_complet_chatgpt.csv" if os.path.exists(file_path): return pd.read_csv(file_path) else: st.error("Fichier glossaire non trouvé.") return pd.DataFrame()

#✨ Sauvegarde

def save_data(df): df.to_csv("glossaire_validé_streamlit.csv", index=False) st.success("Glossaire sauvegardé avec succès.")

# 📂 Interface principale

def main(): st.title("Validation du glossaire terminologique")

df = load_data()
if df.empty:
    return

# Filtres
with st.sidebar:
    st.header("Filtres")
    langue = st.selectbox("Langue", options=["Toutes"] + sorted(df['langue'].dropna().unique().tolist()))
    source = st.multiselect("Source", options=sorted(df['source'].dropna().unique().tolist()), default=df['source'].unique().tolist())
    show_only_invalid = st.checkbox("Afficher uniquement les termes non validés")

# Application des filtres
filtered = df.copy()
if langue != "Toutes":
    filtered = filtered[filtered['langue'] == langue]
if source:
    filtered = filtered[filtered['source'].isin(source)]
if show_only_invalid:
    filtered = filtered[filtered['valide_auto'] != "oui"]

st.write(f"{len(filtered)} terme(s) affiché(s) sur {len(df)}")

# Edition ligne par ligne
edited_rows = []
for i, row in filtered.iterrows():
    with st.expander(f"{row['term']} ({row['langue']})"):
        st.markdown(f"**Source :** {row['source']}")
        st.markdown(f"**Définition automatique :** {row['auto_definition'] if isinstance(row['auto_definition'], str) else ''}")
        new_def = st.text_area("Définition finale", value=row['definition_finale'] if isinstance(row['definition_finale'], str) else "", key=f"def_{i}")
        is_valid = st.checkbox("Inclure ce terme dans le glossaire final", value=row['valide_auto'] == "oui", key=f"valide_{i}")
        edited_rows.append((i, new_def, "oui" if is_valid else "non"))

# Sauvegarde
if st.button("Sauvegarder les modifications"):
    for idx, new_def, valid_flag in edited_rows:
        df.at[idx, 'definition_finale'] = new_def
        df.at[idx, 'valide_auto'] = valid_flag
    save_data(df)

if name == "main": main()

