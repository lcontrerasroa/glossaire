
import streamlit as st
import pandas as pd
import os

# ✨ Chargement du glossaire enrichi
def load_data():
    file_path = "glossaire_complet_chatgpt.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error("Fichier glossaire non trouvé.")
        return pd.DataFrame()

# ✨ Sauvegarde
def save_data(df):
    df.to_csv("glossaire_validé_streamlit.csv", index=False)
    st.success("Glossaire sauvegardé avec succès.")

# 🔁 Génération automatique de définition (locale)
def generer_definition_generique(term, langue="en"):
    term = term.strip().capitalize()
    if langue == "fr":
        return f"{term} est un concept utilisé dans les domaines de la linguistique, de la traduction ou de l'enseignement."
    elif langue == "es":
        return f"{term} es un concepto utilizado en los campos de la lingüística, la traducción o la enseñanza."
    else:
        return f"{term} is a concept used in the fields of linguistics, translation, or education."

# 📂 Interface principale
def main():
    st.title("Validation du glossaire terminologique")

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

    # Édition ligne par ligne
    edited_rows = []
    for i, row in filtered.iterrows():
        with st.expander(f"{row['term']} ({row['langue']})"):
            st.markdown(f"**Source :** {row['source']}")
            st.markdown(f"**Définition automatique :** {row['auto_definition'] if isinstance(row['auto_definition'], str) else ''}")
            def_key = f"def_{i}"
            val_key = f"valide_{i}"
            gen_key = f"gen_{i}"

            new_def = st.text_area("Définition finale", value=row['definition_finale'] if isinstance(row['definition_finale'], str) else "", key=def_key)

            # Si définition faible, proposer une suggestion automatique
            if not isinstance(new_def, str) or len(new_def.strip()) < 30:
                if st.button("Suggérer une définition automatique", key=gen_key):
                    new_def = generer_definition_generique(row['term'], row['langue'])
                    st.session_state[def_key] = new_def

            is_valid = st.checkbox("Inclure ce terme dans le glossaire final", value=row['valide_auto'] == "oui", key=val_key)
            edited_rows.append((i, new_def, "oui" if is_valid else "non"))

    # Sauvegarde
    if st.button("Sauvegarder les modifications"):
        for idx, new_def, valid_flag in edited_rows:
            df.at[idx, 'definition_finale'] = new_def
            df.at[idx, 'valide_auto'] = valid_flag
        save_data(df)

    # Export des termes validés uniquement
    if st.button("Exporter uniquement les termes validés"):
        df_validated = df[df['valide_auto'] == "oui"]
        export_path = "glossaire_validé_seulement.csv"
        df_validated.to_csv(export_path, index=False)
        st.success(f"Fichier exporté : {export_path}")

if __name__ == "__main__":
    main()
