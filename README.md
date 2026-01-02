# CES'Event Donations Dashboard

Dashboard interactif de visualisation des données de donations pour l'événement caritatif CES'Event, développé avec Streamlit et Plotly.

## 📊 Fonctionnalités

### KPIs Affichés
- **Montant total collecté** - Somme de toutes les donations
- **Nombre de donations** - Nombre total de contributions
- **Don moyen/médian** - Statistiques de tendance centrale
- **€/heure** - Taux de collecte par heure
- **Donateurs uniques** - Nombre de donateurs identifiés
- **Période de collecte** - Durée de l'événement
- **Campus participants** - Nombre de campus impliqués

### Visualisations Interactives
- 📈 **Timeline cumulative** - Évolution du montant et du nombre de donations dans le temps
- 🏫 **Performance par campus** - Bar chart et pie chart de la répartition par campus
- 📊 **Distribution des montants** - Histogramme des donations par tranche
- ⏰ **Donations par heure** - Analyse temporelle des contributions
- 🏆 **Top donateurs** - Classement des plus gros contributeurs

### Design
- Thème dark moderne (#1E1E1E, #2A2A2A, #3A3A3A)
- Couleur d'accent : #D3614E
- Layout wide optimisé
- Graphiques Plotly interactifs (zoom, pan, hover)

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd cesevent-dataviz
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ajouter vos données**
   - Placez votre fichier `donations.json` dans le dossier `data/`
   - Le fichier doit contenir un tableau JSON d'objets de donations
   - Voir la section "Structure des données" ci-dessous

## 📂 Structure du Projet

```
cesevent-dataviz/
├── data/
│   └── donations.json          # Fichier de données (à ajouter)
├── src/
│   ├── __init__.py             # Module Python
│   ├── load_data.py            # Chargement et nettoyage des données
│   ├── compute_kpis.py         # Calcul des indicateurs de performance
│   └── visualizations.py       # Fonctions de visualisation Plotly
├── dashboard.py                # Application Streamlit principale
├── requirements.txt            # Dépendances Python
├── .gitignore                  # Fichiers à ignorer par Git
└── README.md                   # Documentation
```

## 📝 Structure des Données

Le fichier `donations.json` doit être un tableau JSON avec la structure suivante :

```json
[
  {
    "id": "455768204818491432",
    "name": "Louis",
    "email": "user@example.com",
    "message": "#Lyon",
    "amount": "5.00",
    "currency": "EUR",
    "timestamp": 1766151263000,
    "verified": true,
    "campus_id": "lyon",
    "campus_name": "Lyon",
    "campus_confidence": "0.90",
    "created_at": "2025-12-19 15:25:17.727658+00",
    "updated_at": "2025-12-19 15:25:17.727658+00"
  }
]
```

### Champs Requis
- `amount` (string) - Montant de la donation
- `timestamp` (number) - Timestamp Unix en millisecondes
- `campus_name` (string) - Nom du campus
- `verified` (boolean) - Statut de vérification

### Champs Optionnels
- `name` (string) - Nom du donateur (pour le classement)
- `email` (string) - Email du donateur (pour compter les uniques)
- `message` (string) - Message associé à la donation
- `campus_confidence` (string) - Score de confiance de l'attribution

## 🎯 Comment Ajouter le Fichier donations.json

1. **Préparer vos données**
   - Assurez-vous que vos données sont au format JSON
   - Vérifiez que la structure correspond au format attendu
   - Validez que les timestamps sont en millisecondes

2. **Placer le fichier**
   ```bash
   # Créer le dossier data s'il n'existe pas
   mkdir data

   # Copier votre fichier dans le dossier
   cp /chemin/vers/votre/donations.json data/
   ```

3. **Vérifier le fichier**
   - Le fichier doit se trouver à : `data/donations.json`
   - Utilisez un validateur JSON si nécessaire

## 💻 Lancer l'Application

Une fois l'installation terminée et les données ajoutées :

```bash
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse :
```
http://localhost:8501
```

### Options de Lancement

```bash
# Spécifier un port différent
streamlit run dashboard.py --server.port 8502

# Désactiver l'ouverture automatique du navigateur
streamlit run dashboard.py --server.headless true

# Mode de développement avec rechargement automatique
streamlit run dashboard.py --server.runOnSave true
```

## 🛠️ Développement

### Modifier les Visualisations
Les fonctions de visualisation se trouvent dans [src/visualizations.py](src/visualizations.py). Vous pouvez personnaliser :
- Les couleurs (variable `COLORS`)
- Les templates de graphiques
- Les types de graphiques Plotly

### Ajouter de Nouveaux KPIs
1. Ajouter la fonction de calcul dans [src/compute_kpis.py](src/compute_kpis.py)
2. Appeler la fonction dans [dashboard.py](dashboard.py)
3. Afficher le résultat avec `st.metric()` ou créer une nouvelle visualisation

### Modifier le Thème
Les couleurs du thème sont définies dans [src/visualizations.py](src/visualizations.py) :
```python
COLORS = {
    'primary': '#D3614E',
    'background': '#1E1E1E',
    'secondary_bg': '#2A2A2A',
    'tertiary_bg': '#3A3A3A',
    'text': '#FFFFFF',
    'grid': '#444444'
}
```

## 📦 Dépendances

- `pandas>=2.1.4` - Manipulation et analyse de données
- `plotly>=5.18.0` - Visualisations interactives
- `streamlit>=1.29.0` - Framework de création d'applications web

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est développé pour l'événement CES'Event.

## 🐛 Problèmes Courants

### Le fichier donations.json n'est pas trouvé
- Vérifiez que le fichier est bien dans `data/donations.json`
- Vérifiez les permissions de lecture du fichier

### Erreur d'import des modules src
- Assurez-vous d'exécuter `streamlit run dashboard.py` depuis la racine du projet
- Vérifiez que `src/__init__.py` existe

### Graphiques ne s'affichent pas correctement
- Effacez le cache de Streamlit : `streamlit cache clear`
- Redémarrez l'application

## 📧 Support

Pour toute question ou problème, veuillez ouvrir une issue sur le repository du projet.

---

**Développé avec ❤️ pour CES'Event**
