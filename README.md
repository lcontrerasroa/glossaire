# Glossaire Terminologique

Cette application Streamlit permet de valider et d'éditer un glossaire terminologique.

## Fonctionnalités

- Filtrage des termes par langue et source
- Affichage des définitions automatiques
- Édition des définitions finales
- Marquage des termes à inclure dans le glossaire final
- Exportation du glossaire validé

## Déploiement

Cette application est déployée sur Streamlit Cloud.

## Utilisation locale

Pour exécuter l'application localement :

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/lcontrerasroa/glossaire.git

   
## Workflow

   ```mermaid
   flowchart TD
       A[📚 Publications : PDF, BibTeX, Google Scholar] --> B[⚙️ Extraction automatique de termes candidats]
       B --> C[✍️ Validation et enrichissement manuel : définitions, vulgarisation]
       C --> D[🧩 Fusion dans un glossaire principal]
       D --> E[🖥️ App de validation Streamlit]
       E --> F[🔗 Intégration dans Notion et GitHub]
       F --> G[🧠 Utilisation pour vulgarisation scientifique, HDR, site personnel]
