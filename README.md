# K-Means — Cooccurrence de mots

Projet scolaire d'apprentissage automatique non supervisé appliqué à l'analyse de textes littéraires.  
L'algorithme K-Means regroupe les mots d'un corpus selon leurs patterns de cooccurrence, révélant des similarités sémantiques entre termes.

---

## Technologies utilisées

`Python` · `NumPy` · `Matplotlib` · `SQLite3` · `argparse`

---

## Fonctionnalités

- **Entraînement sur corpus littéraire** — analyse de *Don Quichote*, *Les Trois Mousquetaires*, *Le Ventre de Paris* et *Germinal*
- **Matrice de cooccurrence** — construit une représentation vectorielle de chaque mot selon une fenêtre de contexte paramétrable
- **Persistance SQLite** — sauvegarde et rechargement du vocabulaire et des cooccurrences via une base de données locale
- **Prédiction de synonymes** — trouve les mots les plus proches selon trois métriques : produit scalaire, moindres carrés (least-squares), city-block
- **Clustering K-Means** — regroupe les mots en *k* partitions sémantiques, implémenté from scratch avec NumPy
- **Visualisation** — génère un graphique Matplotlib de la convergence de l'algorithme (migrations par itération)

---

## Installation

**Prérequis :** Python 3.11+

```bash
# Cloner le dépôt
git clone https://github.com/Laurent-Dumesnil/K-Mean.git
cd kmeans-cooccurrence

# Installer les dépendances
pip install numpy matplotlib
```

---

## Utilisation

### 1. Initialiser la base de données
```bash
python main.py -b
```

### 2. Entraîner le modèle sur un texte
```bash
python main.py -e -t 7 --encodage UTF-8 --chemin chemin/vers/texte.txt
```

### 3. Prédire des synonymes
```bash
python main.py -p -t 7 --normaliser --conserver 500
# Puis entrer : <mot> <nb_résultats> <méthode (0=dot, 1=ls, 2=cb)>
```

### 4. Générer des clusters de mots
```bash
python main.py -c -t 7 -k 5 -n 10 --normaliser --conserver 500 --graphe
```

| Option | Description |
|---|---|
| `-t` | Taille de la fenêtre de cooccurrence |
| `-k` | Nombre de clusters |
| `-n` | Nombre de mots affichés par cluster |
| `--conserver` | Nombre de features (colonnes) à conserver |
| `--normaliser` | Normalise les vecteurs avant clustering |
| `--graphe` | Affiche le graphique de convergence |

---

## Structure du projet

```
├── main.py          # Point d'entrée, gestion des modes
├── parser.py        # Validation des arguments CLI
├── entrainer.py     # Construction de la matrice de cooccurrence
├── entrainerBD.py   # Extension avec persistance SQLite
├── DAO.py           # Accès à la base de données
├── cluster.py       # Algorithme K-Means (from scratch)
├── predire.py       # Prédiction de synonymes
├── graphe.py        # Visualisation Matplotlib
└── ai_db            # Base de données SQLite
```

---

## Ce que j'ai appris

Ce projet m'a permis de comprendre en profondeur le fonctionnement du K-Means en l'implémentant sans librairie. La partie la plus intéressante a été de représenter le sens des mots uniquement à partir de leur contexte d'apparition — et de constater que l'algorithme regroupe naturellement des mots de champs lexicaux similaires.
