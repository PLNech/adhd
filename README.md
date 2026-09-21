# Clarté — Auto-Évaluation TDAH Adulte

<p align="center">
  <strong>🧠 Outils scientifiquement validés pour l'auto-évaluation du TDAH chez l'adulte</strong>
</p>

<p align="center">
  <a href="https://me.nech.pl/tdah/">Essayer en ligne</a> •
  <a href="#outils-inclus">Outils</a> •
  <a href="#utilisation">Utilisation</a> •
  <a href="docs/">Documentation</a>
</p>

---

## ⚠️ Avertissement Important

**Cette application est un outil d'AUTO-ÉVALUATION et NE CONSTITUE PAS un diagnostic médical.**

Seul un professionnel de santé qualifié (psychiatre, neurologue) peut établir un diagnostic de TDAH après une évaluation clinique complète. Les résultats sont destinés à faciliter la discussion avec votre médecin.

---

## Outils Inclus

### 1. ASRS v1.1 (OMS / Harvard)
- **Adult ADHD Self-Report Scale** - 18 questions
- Développé par l'Organisation Mondiale de la Santé
- Méthode de scoring validée avec seuils cliniques
- [Documentation détaillée](docs/SCALE_ASRS.md)

### 2. Critères DSM-5 (Style DIVA)
- Évaluation structurée des 18 critères diagnostiques
- 9 critères d'inattention + 9 critères d'hyperactivité/impulsivité
- Questions sur l'enfance (critère B) et le retentissement (critères C/D)
- [Documentation détaillée](docs/SCALE_DIVA.md)

### 3. Fonctions Exécutives (Modèle de Brown)
- 6 clusters cognitifs: Activation, Focus, Effort, Émotion, Mémoire, Action
- 24 items évaluant les difficultés exécutives
- [Documentation détaillée](docs/SCALE_EXECUTIVE_FUNCTIONS.md)

---

## Utilisation

### Version Web (GitHub Pages)
Accédez directement à l'application: **[me.nech.pl/tdah](https://me.nech.pl/tdah/)**

- Aucune installation requise
- Données 100% locales (rien n'est transmis)
- Génération de PDF pour votre médecin

### Version Flask (locale)

```bash
# Cloner le repo
git clone https://github.com/PLNech/adhd.git
cd adhd

# Installer les dépendances
poetry install

# Lancer l'application
poetry run python run.py
```

Ouvrez http://127.0.0.1:5001 dans votre navigateur.

---

## Fonctionnalités

- ✅ Questionnaires en français
- ✅ Scoring automatique avec interprétations cliniques
- ✅ Génération de rapport PDF complet
- ✅ Synthèse pour le clinicien + réponses détaillées en annexe
- ✅ Thème apaisant "Clarté" avec police Atkinson Hyperlegible
- ✅ Respect de la vie privée (aucune donnée transmise)
- ✅ Open source (MIT License)

---

## Structure du Projet

```
adhd/
├── static-site/          # Version statique (GitHub Pages)
│   ├── index.html
│   ├── style.css         # Thème Clarté
│   ├── app.js            # Logique questionnaires + PDF
│   └── fonts/            # Atkinson Hyperlegible (auto-hébergée)
├── app/                  # Version Flask
│   ├── questionnaires.py # Données des échelles
│   ├── scoring.py        # Logique de scoring
│   ├── routes.py         # Routes web
│   └── pdf_generator.py  # Génération PDF
├── docs/                 # Documentation scientifique
│   ├── SCALE_ASRS.md
│   ├── SCALE_DIVA.md
│   └── SCALE_EXECUTIVE_FUNCTIONS.md
└── templates/            # Templates HTML Flask
```

---

## Références Scientifiques

1. Kessler, R.C., et al. (2005). The World Health Organization Adult ADHD Self-Report Scale (ASRS). *Psychological Medicine*, 35(2), 245-256.

2. American Psychiatric Association. (2013). *Diagnostic and Statistical Manual of Mental Disorders* (5th ed.).

3. Kooij, J.J.S., et al. (2010). DIVA 2.0: Diagnostic Interview for ADHD in Adults. DIVA Foundation.

4. Brown, T.E. (2013). *A New Understanding of ADHD in Children and Adults: Executive Function Impairments*. Routledge.

---

## License

MIT License © 2025 PLNech

Voir [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">
  <em>Fait avec soin pour aider à mieux comprendre le TDAH.</em>
</p>
