# Évaluation des Fonctions Exécutives - Modèle de Brown

## Référence Scientifique

**Auteur:** Thomas E. Brown, PhD

**Publications:**
- Brown, T.E. (2013). *A New Understanding of ADHD in Children and Adults: Executive Function Impairments*. Routledge.
- Brown, T.E. (2005). *Attention Deficit Disorder: The Unfocused Mind in Children and Adults*. Yale University Press.

**Outil commercial:** Brown EF/A Scales (Pearson Assessments) - Propriétaire

**Note:** Notre implémentation est basée sur le modèle conceptuel public de Brown, non sur les items propriétaires des Brown Scales.

---

## Le Modèle de Brown

Brown conceptualise le TDAH comme un trouble des **fonctions exécutives** plutôt qu'un simple déficit d'attention ou hyperactivité. Les fonctions exécutives sont les capacités cognitives de "chef d'orchestre" du cerveau.

### Métaphore de Brown:
> "Le TDAH n'est pas un problème de savoir quoi faire, mais de faire ce qu'on sait qu'on devrait faire."

---

## Les 6 Clusters de Fonctions Exécutives

### 1. ACTIVATION
**Fonction:** Organiser, prioriser et activer le travail

| Aspect | Description | Manifestations TDAH |
|--------|-------------|---------------------|
| Organisation | Structurer tâches et matériel | Désordre chronique, perd des choses |
| Priorisation | Identifier ce qui est important | Tout semble urgent ou rien ne l'est |
| Estimation du temps | Évaluer durée des tâches | Sous-estime toujours le temps nécessaire |
| Activation | Démarrer une tâche | Procrastination chronique |

### 2. FOCUS
**Fonction:** Focaliser, maintenir et déplacer l'attention

| Aspect | Description | Manifestations TDAH |
|--------|-------------|---------------------|
| Attention sélective | Se concentrer sur une chose | Facilement distrait |
| Attention soutenue | Maintenir la concentration | "Décroche" après quelques minutes |
| Flexibilité attentionnelle | Passer d'une tâche à l'autre | Reste "bloqué" ou change trop vite |
| Hyperfocus | Concentration excessive | Perd la notion du temps sur intérêts |

### 3. EFFORT
**Fonction:** Réguler la vigilance, l'effort soutenu et la vitesse de traitement

| Aspect | Description | Manifestations TDAH |
|--------|-------------|---------------------|
| Vigilance | Maintenir l'éveil | Somnolence sur tâches peu stimulantes |
| Effort soutenu | Persister dans l'effort | Abandonne vite, sauf si intéressant |
| Vitesse de traitement | Rapidité cognitive | Lenteur ou précipitation excessive |
| Énergie | Niveau d'énergie mental | Fluctuations importantes |

### 4. ÉMOTION
**Fonction:** Gérer la frustration et moduler les émotions

| Aspect | Description | Manifestations TDAH |
|--------|-------------|---------------------|
| Tolérance à la frustration | Gérer les obstacles | Irritabilité, abandon rapide |
| Régulation émotionnelle | Moduler l'intensité | Réactions excessives |
| Sensibilité au rejet | Réaction aux critiques | RSD (Rejection Sensitive Dysphoria) |
| Motivation | Maintenir l'intérêt | Dépendant de la nouveauté/intérêt |

### 5. MÉMOIRE
**Fonction:** Utiliser la mémoire de travail et accéder aux souvenirs

| Aspect | Description | Manifestations TDAH |
|--------|-------------|---------------------|
| Mémoire de travail | Retenir en manipulant | Oublie ce qu'il lisait/faisait |
| Rappel | Accéder aux souvenirs | "C'est sur le bout de la langue" |
| Mémoire prospective | Se souvenir de faire | Oublie rendez-vous, tâches prévues |
| Consolidation | Encoder en mémoire | Doit relire plusieurs fois |

### 6. ACTION
**Fonction:** Surveiller et auto-réguler l'action

| Aspect | Description | Manifestations TDAH |
|--------|-------------|---------------------|
| Inhibition | Freiner les impulsions | Agit/parle sans réfléchir |
| Auto-monitoring | Observer son comportement | Ne remarque pas ses erreurs |
| Auto-régulation | Ajuster son comportement | Difficulté à se corriger |
| Contrôle moteur | Gérer l'agitation | Bouge, remue, ne tient pas en place |

---

## Scoring de notre implémentation

### Échelle de réponse (4 points)
```
0 = Pas du tout un problème
1 = Rarement un problème
2 = Parfois un problème
3 = Souvent un problème
```

### Structure
- 4 items par cluster × 6 clusters = **24 items**
- Score par cluster: 0-12
- **Score total maximum: 72**

### Interprétation

| Score total (%) | Niveau | Interprétation |
|-----------------|--------|----------------|
| ≥ 66% | Élevé | Difficultés significatives, cohérent avec TDAH |
| 40-65% | Modéré | Difficultés modérées, évaluation recommandée |
| < 40% | Faible | Pas de difficultés majeures apparentes |

### Identification des clusters impactés
Un cluster est considéré "impacté" si le score atteint **≥ 50%** du maximum (≥ 6/12).

---

## Différences avec les Brown Scales officielles

| Aspect | Brown EF/A Scales | Notre implémentation |
|--------|-------------------|----------------------|
| Items | 50+ items propriétaires | 24 items basés sur modèle public |
| Validation | Études psychométriques extensives | Basé sur construits validés |
| Clusters | 6 (identiques) | 6 (identiques) |
| Échelle | Sévérité (0-3) | Fréquence (0-3) |
| Coût | Licence Pearson requise | Libre |
| Usage | Diagnostic clinique | Dépistage/sensibilisation |

---

## Liens avec le TDAH

### Pourquoi les fonctions exécutives?
- Le TDAH est de plus en plus compris comme un trouble développemental des fonctions exécutives
- Les critères DSM-5 capturent principalement les manifestations comportementales
- Le modèle de Brown explique le "pourquoi" derrière les symptômes

### Exemple:
- **Symptôme DSM:** "Ne termine pas ses tâches"
- **Explication FE:** Déficit en Activation (démarrage) + Effort (persistance) + Mémoire (oubli de la tâche)

---

## Limites

1. **Non spécifique au TDAH** - Les difficultés exécutives se retrouvent dans: dépression, anxiété, troubles du sommeil, traumatismes crâniens
2. **Auto-évaluation** - Manque d'insight possible chez certains patients
3. **Non diagnostique** - Complément, pas substitut à l'évaluation clinique

---

## Sources

- https://www.brownadhdclinic.com/brown-ef-model-adhd
- https://www.pearsonassessments.com/store/usassessments/en/Store/Professional-Assessments/Behavior/Executive-Function/Brown-Executive-Function-Attention-Scales/p/100001978.html
- Barkley, R.A. (2012). Executive Functions: What They Are, How They Work, and Why They Evolved. Guilford Press.
