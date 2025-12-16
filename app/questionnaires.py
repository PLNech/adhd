"""
Questionnaires scientifiquement validés pour l'évaluation du TDAH chez l'adulte.

Sources:
- ASRS v1.1: OMS/Harvard, Kessler et al. (2005). Psychological Medicine, 35(2), 245-256.
- Critères DSM-5 pour le DIVA: APA (2013). Diagnostic and Statistical Manual of Mental Disorders, 5th Edition.
- Évaluation des fonctions exécutives: Basée sur le modèle de Brown (2013).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ResponseScale(Enum):
    """Échelle de réponse ASRS à 5 points."""
    JAMAIS = 0
    RAREMENT = 1
    PARFOIS = 2
    SOUVENT = 3
    TRES_SOUVENT = 4


@dataclass
class Question:
    id: str
    text: str
    category: str
    subcategory: Optional[str] = None


# =============================================================================
# ASRS v1.1 - Adult ADHD Self-Report Scale (OMS)
# Traduction française basée sur les versions validées CADDRA/OMS
# =============================================================================

ASRS_RESPONSE_OPTIONS = [
    ("jamais", "Jamais", 0),
    ("rarement", "Rarement", 1),
    ("parfois", "Parfois", 2),
    ("souvent", "Souvent", 3),
    ("tres_souvent", "Très souvent", 4),
]

# Seuils de cotation pour la Partie A (screener)
# Cases grisées dans le questionnaire original
ASRS_SHADED_THRESHOLDS = {
    "asrs_1": 2,  # Parfois et plus
    "asrs_2": 2,  # Parfois et plus
    "asrs_3": 2,  # Parfois et plus
    "asrs_4": 3,  # Souvent et plus
    "asrs_5": 3,  # Souvent et plus
    "asrs_6": 3,  # Souvent et plus
}

ASRS_QUESTIONS = [
    # Partie A - Screener (6 questions les plus prédictives)
    Question(
        id="asrs_1",
        text="À quelle fréquence avez-vous des difficultés à finaliser les derniers détails d'un projet, une fois que les parties les plus stimulantes ont été réalisées ?",
        category="inattention",
        subcategory="part_a"
    ),
    Question(
        id="asrs_2",
        text="À quelle fréquence avez-vous des difficultés à mettre de l'ordre lorsque vous devez effectuer une tâche qui requiert de l'organisation ?",
        category="inattention",
        subcategory="part_a"
    ),
    Question(
        id="asrs_3",
        text="À quelle fréquence avez-vous des difficultés à vous souvenir de vos rendez-vous ou de vos obligations ?",
        category="inattention",
        subcategory="part_a"
    ),
    Question(
        id="asrs_4",
        text="Lorsque vous devez effectuer une tâche qui demande beaucoup de réflexion, à quelle fréquence évitez-vous ou retardez-vous le moment de commencer ?",
        category="inattention",
        subcategory="part_a"
    ),
    Question(
        id="asrs_5",
        text="À quelle fréquence remuez-vous ou tortillez-vous les mains ou les pieds lorsque vous devez rester assis(e) pendant une longue période ?",
        category="hyperactivite",
        subcategory="part_a"
    ),
    Question(
        id="asrs_6",
        text="À quelle fréquence vous sentez-vous excessivement actif(ve) et poussé(e) à faire des choses, comme si vous étiez mû(e) par un moteur ?",
        category="hyperactivite",
        subcategory="part_a"
    ),
    # Partie B - Questions supplémentaires (12 questions)
    Question(
        id="asrs_7",
        text="À quelle fréquence faites-vous des erreurs d'inattention lorsque vous devez travailler sur un projet ennuyeux ou difficile ?",
        category="inattention",
        subcategory="part_b"
    ),
    Question(
        id="asrs_8",
        text="À quelle fréquence avez-vous des difficultés à maintenir votre attention lorsque vous effectuez un travail ennuyeux ou répétitif ?",
        category="inattention",
        subcategory="part_b"
    ),
    Question(
        id="asrs_9",
        text="À quelle fréquence avez-vous des difficultés à vous concentrer sur ce que les gens vous disent, même lorsqu'ils s'adressent directement à vous ?",
        category="inattention",
        subcategory="part_b"
    ),
    Question(
        id="asrs_10",
        text="À quelle fréquence égarez-vous ou avez-vous du mal à retrouver des objets à la maison ou au travail ?",
        category="inattention",
        subcategory="part_b"
    ),
    Question(
        id="asrs_11",
        text="À quelle fréquence êtes-vous distrait(e) par l'activité ou le bruit autour de vous ?",
        category="inattention",
        subcategory="part_b"
    ),
    Question(
        id="asrs_12",
        text="À quelle fréquence quittez-vous votre siège lors de réunions ou dans d'autres situations où vous êtes censé(e) rester assis(e) ?",
        category="hyperactivite",
        subcategory="part_b"
    ),
    Question(
        id="asrs_13",
        text="À quelle fréquence vous sentez-vous agité(e) ou remuant(e) ?",
        category="hyperactivite",
        subcategory="part_b"
    ),
    Question(
        id="asrs_14",
        text="À quelle fréquence avez-vous des difficultés à vous détendre et à vous relaxer lorsque vous avez du temps libre ?",
        category="hyperactivite",
        subcategory="part_b"
    ),
    Question(
        id="asrs_15",
        text="À quelle fréquence vous trouvez-vous à parler trop en situation sociale ?",
        category="impulsivite",
        subcategory="part_b"
    ),
    Question(
        id="asrs_16",
        text="Lors d'une conversation, à quelle fréquence finissez-vous les phrases des personnes avec qui vous parlez avant qu'elles ne puissent les terminer elles-mêmes ?",
        category="impulsivite",
        subcategory="part_b"
    ),
    Question(
        id="asrs_17",
        text="À quelle fréquence avez-vous des difficultés à attendre votre tour dans des situations qui l'exigent ?",
        category="impulsivite",
        subcategory="part_b"
    ),
    Question(
        id="asrs_18",
        text="À quelle fréquence interrompez-vous les autres lorsqu'ils sont occupés ?",
        category="impulsivite",
        subcategory="part_b"
    ),
]


# =============================================================================
# DIVA-Style Assessment - Basé sur les critères DSM-5
# Évaluation structurée pour l'âge adulte ET l'enfance
# =============================================================================

DIVA_RESPONSE_OPTIONS = [
    ("oui", "Oui", 1),
    ("non", "Non", 0),
]

# Critères DSM-5 d'inattention avec exemples pour adultes
DIVA_INATTENTION_CRITERIA = [
    Question(
        id="diva_ia_1",
        text="Avez-vous souvent du mal à prêter attention aux détails ou faites-vous des erreurs d'inattention dans votre travail ou d'autres activités ? (ex: négliger des détails, travail inexact, erreurs dans les formulaires, les rapports)",
        category="inattention",
    ),
    Question(
        id="diva_ia_2",
        text="Avez-vous souvent du mal à maintenir votre attention sur des tâches ou des activités ? (ex: difficulté à rester concentré pendant les réunions, lectures, conversations longues)",
        category="inattention",
    ),
    Question(
        id="diva_ia_3",
        text="Avez-vous souvent l'impression de ne pas écouter quand on vous parle directement ? (ex: esprit ailleurs, même sans distraction évidente)",
        category="inattention",
    ),
    Question(
        id="diva_ia_4",
        text="Avez-vous souvent du mal à suivre les instructions jusqu'au bout et à terminer vos tâches professionnelles ou obligations ? (ex: commencer des tâches mais perdre rapidement le fil, ne pas terminer)",
        category="inattention",
    ),
    Question(
        id="diva_ia_5",
        text="Avez-vous souvent du mal à organiser vos tâches et activités ? (ex: difficulté à gérer des tâches séquentielles, à maintenir l'ordre, à respecter les délais, à gérer le temps)",
        category="inattention",
    ),
    Question(
        id="diva_ia_6",
        text="Évitez-vous souvent, ou êtes-vous réticent(e) à vous engager dans des tâches qui nécessitent un effort mental soutenu ? (ex: préparation de rapports, remplir des formulaires, relire des documents longs)",
        category="inattention",
    ),
    Question(
        id="diva_ia_7",
        text="Perdez-vous souvent des objets nécessaires à vos activités ? (ex: clés, portefeuille, téléphone, documents, lunettes)",
        category="inattention",
    ),
    Question(
        id="diva_ia_8",
        text="Êtes-vous souvent facilement distrait(e) par des stimuli externes ou des pensées sans rapport ?",
        category="inattention",
    ),
    Question(
        id="diva_ia_9",
        text="Êtes-vous souvent oublieux(se) dans la vie quotidienne ? (ex: oublier de rappeler, payer des factures, honorer des rendez-vous)",
        category="inattention",
    ),
]

# Critères DSM-5 d'hyperactivité-impulsivité avec exemples pour adultes
DIVA_HYPERACTIVITY_CRITERIA = [
    Question(
        id="diva_hi_1",
        text="Remuez-vous souvent les mains ou les pieds, ou vous tortillez-vous sur votre siège ?",
        category="hyperactivite",
    ),
    Question(
        id="diva_hi_2",
        text="Quittez-vous souvent votre siège dans des situations où vous êtes censé(e) rester assis(e) ? (ex: quitter sa place au bureau, lors de réunions)",
        category="hyperactivite",
    ),
    Question(
        id="diva_hi_3",
        text="Vous sentez-vous souvent agité(e) ou avez-vous du mal à rester en place ? (ex: sentiment d'impatience, inconfort en restant immobile longtemps)",
        category="hyperactivite",
    ),
    Question(
        id="diva_hi_4",
        text="Avez-vous souvent du mal à vous adonner à des loisirs ou activités calmes de manière tranquille ?",
        category="hyperactivite",
    ),
    Question(
        id="diva_hi_5",
        text="Êtes-vous souvent « sur la brèche » ou agissez-vous comme si vous étiez « monté(e) sur ressorts » ? (ex: mal à l'aise de rester immobile longtemps, perçu comme agité par les autres)",
        category="hyperactivite",
    ),
    Question(
        id="diva_hi_6",
        text="Parlez-vous souvent trop ?",
        category="impulsivite",
    ),
    Question(
        id="diva_hi_7",
        text="Laissez-vous souvent échapper une réponse avant qu'une question ne soit terminée ? (ex: compléter les phrases des autres, ne pas attendre son tour dans la conversation)",
        category="impulsivite",
    ),
    Question(
        id="diva_hi_8",
        text="Avez-vous souvent du mal à attendre votre tour ? (ex: files d'attente)",
        category="impulsivite",
    ),
    Question(
        id="diva_hi_9",
        text="Interrompez-vous souvent les autres ou vous imposez-vous ? (ex: s'immiscer dans des conversations, activités, utiliser les affaires des autres sans permission)",
        category="impulsivite",
    ),
]

# Questions sur l'enfance (avant 12 ans) - DSM-5
DIVA_CHILDHOOD_QUESTIONS = [
    Question(
        id="diva_child_1",
        text="Avant l'âge de 12 ans, aviez-vous des difficultés à rester attentif(ve) à l'école ou lors des devoirs ?",
        category="enfance",
    ),
    Question(
        id="diva_child_2",
        text="Avant l'âge de 12 ans, étiez-vous considéré(e) comme un enfant rêveur, « dans la lune » ?",
        category="enfance",
    ),
    Question(
        id="diva_child_3",
        text="Avant l'âge de 12 ans, aviez-vous du mal à rester assis(e) ou étiez-vous agité(e) à l'école ?",
        category="enfance",
    ),
    Question(
        id="diva_child_4",
        text="Avant l'âge de 12 ans, aviez-vous souvent des remarques sur vos bulletins concernant l'attention ou le comportement ?",
        category="enfance",
    ),
    Question(
        id="diva_child_5",
        text="Avant l'âge de 12 ans, perdiez-vous souvent vos affaires scolaires ou oubliiez-vous de faire vos devoirs ?",
        category="enfance",
    ),
]

# Questions sur le retentissement fonctionnel
DIVA_IMPAIRMENT_DOMAINS = [
    Question(
        id="diva_imp_1",
        text="Ces difficultés ont-elles un impact négatif sur votre travail ou vos études ?",
        category="retentissement",
        subcategory="travail",
    ),
    Question(
        id="diva_imp_2",
        text="Ces difficultés ont-elles un impact négatif sur vos relations familiales ou amoureuses ?",
        category="retentissement",
        subcategory="famille",
    ),
    Question(
        id="diva_imp_3",
        text="Ces difficultés ont-elles un impact négatif sur vos relations sociales et amicales ?",
        category="retentissement",
        subcategory="social",
    ),
    Question(
        id="diva_imp_4",
        text="Ces difficultés ont-elles un impact négatif sur vos loisirs et activités de temps libre ?",
        category="retentissement",
        subcategory="loisirs",
    ),
    Question(
        id="diva_imp_5",
        text="Ces difficultés ont-elles un impact négatif sur votre estime de soi ou votre confiance en vous ?",
        category="retentissement",
        subcategory="estime_soi",
    ),
]


# =============================================================================
# Évaluation des Fonctions Exécutives (inspirée du modèle de Brown)
# 6 clusters: Activation, Focus, Effort, Émotion, Mémoire, Action
# =============================================================================

EXEC_FUNCTION_RESPONSE_OPTIONS = [
    ("jamais", "Pas du tout un problème", 0),
    ("rarement", "Rarement un problème", 1),
    ("parfois", "Parfois un problème", 2),
    ("souvent", "Souvent un problème", 3),
]

EXEC_FUNCTION_QUESTIONS = [
    # Cluster 1: Activation (organisation, priorisation, démarrage)
    Question(
        id="ef_act_1",
        text="Difficulté à organiser et planifier des tâches ou projets",
        category="activation",
    ),
    Question(
        id="ef_act_2",
        text="Difficulté à établir des priorités entre différentes tâches",
        category="activation",
    ),
    Question(
        id="ef_act_3",
        text="Difficulté à commencer une tâche, même quand elle est importante",
        category="activation",
    ),
    Question(
        id="ef_act_4",
        text="Tendance à procrastiner, reporter les tâches au lendemain",
        category="activation",
    ),
    # Cluster 2: Focus (attention soutenue, distraction)
    Question(
        id="ef_foc_1",
        text="Difficulté à maintenir l'attention sur une tâche jusqu'à son achèvement",
        category="focus",
    ),
    Question(
        id="ef_foc_2",
        text="Facilement distrait(e) par des pensées ou stimuli non pertinents",
        category="focus",
    ),
    Question(
        id="ef_foc_3",
        text="Difficulté à écouter et retenir ce qui est dit lors de conversations",
        category="focus",
    ),
    Question(
        id="ef_foc_4",
        text="Passer d'une activité à l'autre sans en terminer aucune",
        category="focus",
    ),
    # Cluster 3: Effort (régulation de l'éveil, vigilance, vitesse de traitement)
    Question(
        id="ef_eff_1",
        text="Somnolence ou fatigue mentale lors de tâches peu stimulantes",
        category="effort",
    ),
    Question(
        id="ef_eff_2",
        text="Difficulté à maintenir un niveau d'énergie constant tout au long de la journée",
        category="effort",
    ),
    Question(
        id="ef_eff_3",
        text="Lenteur excessive pour accomplir des tâches routinières",
        category="effort",
    ),
    Question(
        id="ef_eff_4",
        text="Besoin de stimulation intense pour rester motivé(e)",
        category="effort",
    ),
    # Cluster 4: Émotion (gestion de la frustration, modulation des affects)
    Question(
        id="ef_emo_1",
        text="Réactions émotionnelles excessives ou disproportionnées",
        category="emotion",
    ),
    Question(
        id="ef_emo_2",
        text="Difficulté à gérer la frustration et l'irritabilité",
        category="emotion",
    ),
    Question(
        id="ef_emo_3",
        text="Sensibilité excessive aux critiques ou aux commentaires négatifs",
        category="emotion",
    ),
    Question(
        id="ef_emo_4",
        text="Fluctuations d'humeur fréquentes au cours de la journée",
        category="emotion",
    ),
    # Cluster 5: Mémoire (mémoire de travail, rappel)
    Question(
        id="ef_mem_1",
        text="Oublier ce que l'on vient de lire et devoir relire plusieurs fois",
        category="memoire",
    ),
    Question(
        id="ef_mem_2",
        text="Difficulté à se souvenir des consignes ou instructions données verbalement",
        category="memoire",
    ),
    Question(
        id="ef_mem_3",
        text="Oublier fréquemment des rendez-vous ou des tâches prévues",
        category="memoire",
    ),
    Question(
        id="ef_mem_4",
        text="Perdre le fil de ses pensées en milieu de phrase ou d'action",
        category="memoire",
    ),
    # Cluster 6: Action (inhibition, auto-régulation)
    Question(
        id="ef_act2_1",
        text="Agir ou parler impulsivement sans réfléchir aux conséquences",
        category="action",
    ),
    Question(
        id="ef_act2_2",
        text="Difficulté à rester assis(e) ou à se tenir tranquille",
        category="action",
    ),
    Question(
        id="ef_act2_3",
        text="Interrompre les autres ou s'imposer dans les conversations",
        category="action",
    ),
    Question(
        id="ef_act2_4",
        text="Difficulté à contrôler ses impulsions (achats, alimentation, etc.)",
        category="action",
    ),
]
