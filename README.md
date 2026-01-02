# CES'Event - Dashboard de Donations

Dashboard de visualisation des donations pour l'événement caritatif CES'Event. Construit avec Streamlit et Plotly pour une expérience interactive.

## Ce que ça fait

Le dashboard affiche en temps réel les statistiques de donations :
- Montant total collecté et nombre de contributions
- Don moyen et médian
- Taux de collecte par heure
- Évolution des donations dans le temps
- Distribution des montants par tranche
- Activité par heure de la journée
- Top donateurs

Tous les graphiques sont interactifs (zoom, survol pour les détails, etc.).

## Installation rapide

**Prérequis** : Python 3.8+

```bash
# Installer les dépendances
pip install -r requirements.txt

# Ajouter votre fichier de données
# Placez donations.json dans le dossier data/

# Lancer le dashboard
python -m streamlit run dashboard.py
```

Le dashboard s'ouvre automatiquement dans votre navigateur sur `http://localhost:8501`

> **Note Windows** : Si `streamlit` n'est pas reconnu, utilisez `python -m streamlit run dashboard.py`

## Structure du projet

```
.
├── data/
│   └── donations.json       # Vos données (à ajouter)
├── src/
│   ├── load_data.py         # Chargement des données
│   ├── compute_kpis.py      # Calculs des statistiques
│   └── visualizations.py    # Graphiques Plotly
├── dashboard.py             # Application principale
└── requirements.txt
```

## Format des données

Le fichier `donations.json` doit contenir un tableau d'objets :

```json
[
  {
    "id": "455768204818491432",
    "name": "Louis",
    "amount": "5.00",
    "currency": "EUR",
    "timestamp": 1766151263000,
    "verified": true,
    "created_at": "2025-12-19 15:25:17.727658+00",
    "updated_at": "2025-12-19 15:25:17.727658+00"
  }
]
```

**Champs obligatoires** :
- `amount` - Montant de la donation (string)
- `timestamp` - Date/heure en millisecondes Unix
- `verified` - Statut de vérification

**Champs optionnels** :
- `name` - Nom du donateur (pour le top donateurs)
- `id` - Identifiant unique de la donation
- `currency` - Devise (EUR par défaut)
- `created_at` / `updated_at` - Dates de création/mise à jour

## Personnalisation

### Modifier les couleurs

Éditez `COLORS` dans `src/visualizations.py` :

```python
COLORS = {
    'primary': '#FF6B5A',      # Couleur principale
    'background': '#1A1A1A',   # Fond
    'text': '#FFFFFF',         # Texte
    ...
}
```

### Ajouter un KPI

1. Créez une fonction dans `src/compute_kpis.py`
2. Appelez-la dans `dashboard.py`
3. Affichez avec `st.metric()`

---

Développé pour CES'Event
