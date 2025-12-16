"""
Logique de scoring et interprétation des questionnaires TDAH.

Références:
- ASRS: Kessler et al. (2005). Psychological Medicine, 35(2), 245-256.
- DSM-5: APA (2013). Critères diagnostiques du TDAH.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from .questionnaires import ASRS_SHADED_THRESHOLDS


@dataclass
class ScoreResult:
    """Résultat d'un score avec interprétation."""
    score: int
    max_score: int
    percentage: float
    interpretation: str
    severity: str  # "faible", "modéré", "élevé"
    clinical_note: str


@dataclass
class ASRSResult:
    """Résultats complets de l'ASRS."""
    part_a_score: int
    part_a_shaded_count: int  # Nombre de réponses dans zones grisées
    part_b_score: int
    total_score: int
    inattention_score: int
    hyperactivity_score: int
    screening_positive: bool
    interpretation: str
    recommendation: str


@dataclass
class DIVAResult:
    """Résultats de l'évaluation DIVA-style."""
    inattention_count: int
    hyperactivity_count: int
    childhood_positive: bool
    impairment_domains: List[str]
    meets_inattention_criteria: bool
    meets_hyperactivity_criteria: bool
    presentation_type: str  # "Inattentif", "Hyperactif/Impulsif", "Combiné", "Sous-seuil"
    interpretation: str


@dataclass
class ExecFunctionResult:
    """Résultats de l'évaluation des fonctions exécutives."""
    cluster_scores: Dict[str, Tuple[int, int]]  # cluster: (score, max)
    total_score: int
    max_score: int
    most_impaired_clusters: List[str]
    interpretation: str
    severity: str


def score_asrs(responses: Dict[str, int]) -> ASRSResult:
    """
    Calcule les scores ASRS selon les méthodes validées.

    Méthode de scoring:
    - Partie A (screener): Compter les réponses dans les zones grisées (>=seuil)
    - Score total: Somme de toutes les réponses (0-4 par item)
    """
    part_a_score = 0
    part_a_shaded = 0
    part_b_score = 0
    inattention = 0
    hyperactivity = 0

    for qid, value in responses.items():
        if not qid.startswith("asrs_"):
            continue

        q_num = int(qid.split("_")[1])

        # Partie A (questions 1-6)
        if q_num <= 6:
            part_a_score += value
            # Vérifier si dans zone grisée
            threshold = ASRS_SHADED_THRESHOLDS.get(qid, 2)
            if value >= threshold:
                part_a_shaded += 1
        else:
            part_b_score += value

        # Catégorisation inattention vs hyperactivité
        # Questions 1-4, 7-11: inattention
        # Questions 5-6, 12-18: hyperactivité/impulsivité
        if q_num in [1, 2, 3, 4, 7, 8, 9, 10, 11]:
            inattention += value
        else:
            hyperactivity += value

    total = part_a_score + part_b_score
    screening_positive = part_a_shaded >= 4

    # Interprétation
    if screening_positive:
        interpretation = (
            "Le dépistage est POSITIF. Vos réponses suggèrent des symptômes "
            "compatibles avec un TDAH chez l'adulte. Une évaluation clinique "
            "approfondie par un professionnel de santé est recommandée."
        )
        recommendation = (
            "Consultation recommandée avec un psychiatre ou neurologue "
            "spécialisé dans le TDAH adulte pour une évaluation diagnostique complète."
        )
    else:
        if total >= 36:  # >50% du score max
            interpretation = (
                "Le dépistage est négatif mais votre score total est relativement élevé. "
                "Certains symptômes peuvent être présents sans atteindre le seuil clinique, "
                "ou pourraient être liés à d'autres conditions."
            )
            recommendation = (
                "Si ces difficultés impactent votre quotidien, une consultation "
                "pourrait être utile pour explorer d'autres causes possibles."
            )
        else:
            interpretation = (
                "Le dépistage est négatif. Vos réponses ne suggèrent pas "
                "de symptômes significatifs de TDAH."
            )
            recommendation = (
                "Si vous avez des préoccupations persistantes concernant votre "
                "attention ou votre comportement, n'hésitez pas à en discuter "
                "avec votre médecin."
            )

    return ASRSResult(
        part_a_score=part_a_score,
        part_a_shaded_count=part_a_shaded,
        part_b_score=part_b_score,
        total_score=total,
        inattention_score=inattention,
        hyperactivity_score=hyperactivity,
        screening_positive=screening_positive,
        interpretation=interpretation,
        recommendation=recommendation,
    )


def score_diva(responses: Dict[str, int]) -> DIVAResult:
    """
    Évalue les critères DSM-5 selon le format DIVA.

    Critères DSM-5 pour adultes (17+ ans):
    - ≥5 symptômes d'inattention ET/OU
    - ≥5 symptômes d'hyperactivité-impulsivité
    - Symptômes présents avant 12 ans
    - Retentissement dans ≥2 domaines de vie
    """
    inattention_count = 0
    hyperactivity_count = 0
    childhood_symptoms = 0
    impairment_domains = []

    for qid, value in responses.items():
        if qid.startswith("diva_ia_") and value == 1:
            inattention_count += 1
        elif qid.startswith("diva_hi_") and value == 1:
            hyperactivity_count += 1
        elif qid.startswith("diva_child_") and value == 1:
            childhood_symptoms += 1
        elif qid.startswith("diva_imp_") and value == 1:
            domain_map = {
                "diva_imp_1": "Travail/Études",
                "diva_imp_2": "Relations familiales",
                "diva_imp_3": "Relations sociales",
                "diva_imp_4": "Loisirs",
                "diva_imp_5": "Estime de soi",
            }
            if qid in domain_map:
                impairment_domains.append(domain_map[qid])

    meets_inattention = inattention_count >= 5
    meets_hyperactivity = hyperactivity_count >= 5
    childhood_positive = childhood_symptoms >= 2

    # Déterminer le type de présentation
    if meets_inattention and meets_hyperactivity:
        presentation = "Combiné (Inattentif + Hyperactif/Impulsif)"
    elif meets_inattention:
        presentation = "Prédominance Inattentive"
    elif meets_hyperactivity:
        presentation = "Prédominance Hyperactive/Impulsive"
    else:
        presentation = "Sous le seuil diagnostique"

    # Interprétation
    criteria_met = []
    criteria_not_met = []

    if meets_inattention:
        criteria_met.append(f"Critère A1 (Inattention): {inattention_count}/9 symptômes (≥5 requis)")
    else:
        criteria_not_met.append(f"Critère A1 (Inattention): {inattention_count}/9 symptômes (≥5 requis)")

    if meets_hyperactivity:
        criteria_met.append(f"Critère A2 (Hyperactivité/Impulsivité): {hyperactivity_count}/9 symptômes (≥5 requis)")
    else:
        criteria_not_met.append(f"Critère A2 (Hyperactivité/Impulsivité): {hyperactivity_count}/9 symptômes (≥5 requis)")

    if childhood_positive:
        criteria_met.append(f"Critère B (Début avant 12 ans): {childhood_symptoms}/5 indicateurs positifs")
    else:
        criteria_not_met.append(f"Critère B (Début avant 12 ans): {childhood_symptoms}/5 indicateurs positifs")

    if len(impairment_domains) >= 2:
        criteria_met.append(f"Critère C/D (Retentissement): {len(impairment_domains)} domaines affectés")
    else:
        criteria_not_met.append(f"Critère C/D (Retentissement): {len(impairment_domains)} domaine(s) affecté(s) (≥2 requis)")

    interpretation_parts = []
    if criteria_met:
        interpretation_parts.append("Critères remplis:\n• " + "\n• ".join(criteria_met))
    if criteria_not_met:
        interpretation_parts.append("Critères non remplis:\n• " + "\n• ".join(criteria_not_met))

    interpretation = "\n\n".join(interpretation_parts)

    return DIVAResult(
        inattention_count=inattention_count,
        hyperactivity_count=hyperactivity_count,
        childhood_positive=childhood_positive,
        impairment_domains=impairment_domains,
        meets_inattention_criteria=meets_inattention,
        meets_hyperactivity_criteria=meets_hyperactivity,
        presentation_type=presentation,
        interpretation=interpretation,
    )


def score_executive_functions(responses: Dict[str, int]) -> ExecFunctionResult:
    """
    Évalue les 6 clusters de fonctions exécutives.

    Clusters (modèle de Brown):
    - Activation: organisation, priorisation, démarrage
    - Focus: attention soutenue, résistance à la distraction
    - Effort: régulation de l'éveil, vitesse de traitement
    - Émotion: gestion de la frustration, modulation des affects
    - Mémoire: mémoire de travail, rappel
    - Action: inhibition, auto-régulation
    """
    cluster_mapping = {
        "activation": "ef_act_",
        "focus": "ef_foc_",
        "effort": "ef_eff_",
        "emotion": "ef_emo_",
        "memoire": "ef_mem_",
        "action": "ef_act2_",
    }

    cluster_names_fr = {
        "activation": "Activation",
        "focus": "Attention/Focus",
        "effort": "Effort/Énergie",
        "emotion": "Régulation émotionnelle",
        "memoire": "Mémoire de travail",
        "action": "Inhibition/Action",
    }

    cluster_scores = {}
    total = 0
    max_total = 0

    for cluster, prefix in cluster_mapping.items():
        score = 0
        count = 0
        for qid, value in responses.items():
            if qid.startswith(prefix):
                score += value
                count += 1
        max_score = count * 3  # Max 3 par question
        cluster_scores[cluster_names_fr[cluster]] = (score, max_score)
        total += score
        max_total += max_score

    # Identifier les clusters les plus impactés (>50% du max)
    impaired = []
    for name, (score, max_s) in cluster_scores.items():
        if max_s > 0 and (score / max_s) >= 0.5:
            impaired.append(name)

    # Déterminer la sévérité globale
    if max_total > 0:
        percentage = (total / max_total) * 100
    else:
        percentage = 0

    if percentage >= 66:
        severity = "Élevé"
        interp = (
            "Vos réponses indiquent des difficultés significatives dans plusieurs "
            "domaines des fonctions exécutives. Ces difficultés sont fréquemment "
            "associées au TDAH mais peuvent aussi être présentes dans d'autres conditions."
        )
    elif percentage >= 40:
        severity = "Modéré"
        interp = (
            "Vos réponses suggèrent des difficultés modérées dans certains domaines "
            "des fonctions exécutives. Une évaluation plus approfondie pourrait être utile."
        )
    else:
        severity = "Faible"
        interp = (
            "Vos réponses ne suggèrent pas de difficultés majeures dans les "
            "fonctions exécutives évaluées."
        )

    if impaired:
        interp += f"\n\nDomaines les plus impactés: {', '.join(impaired)}."

    return ExecFunctionResult(
        cluster_scores=cluster_scores,
        total_score=total,
        max_score=max_total,
        most_impaired_clusters=impaired,
        interpretation=interp,
        severity=severity,
    )


@dataclass
class GlobalAssessment:
    """Évaluation globale combinant tous les questionnaires."""
    asrs: ASRSResult
    diva: DIVAResult
    exec_functions: ExecFunctionResult
    summary: str
    clinical_recommendation: str
    confidence_level: str


def generate_global_assessment(
    asrs: ASRSResult,
    diva: DIVAResult,
    exec_func: ExecFunctionResult
) -> GlobalAssessment:
    """Génère une évaluation globale synthétisant tous les résultats."""

    # Compter les indicateurs positifs
    positive_indicators = 0
    total_indicators = 3

    if asrs.screening_positive:
        positive_indicators += 1
    if diva.meets_inattention_criteria or diva.meets_hyperactivity_criteria:
        positive_indicators += 1
    if exec_func.severity in ["Modéré", "Élevé"]:
        positive_indicators += 1

    # Générer le résumé
    if positive_indicators >= 2:
        summary = (
            f"SYNTHÈSE: {positive_indicators}/{total_indicators} outils d'évaluation suggèrent "
            "des symptômes compatibles avec un TDAH.\n\n"
        )
        if asrs.screening_positive:
            summary += "• ASRS: Dépistage POSITIF\n"
        if diva.meets_inattention_criteria or diva.meets_hyperactivity_criteria:
            summary += f"• Critères DSM-5: Présentation {diva.presentation_type}\n"
        if exec_func.severity in ["Modéré", "Élevé"]:
            summary += f"• Fonctions exécutives: Difficultés de niveau {exec_func.severity}\n"

        confidence = "Élevée" if positive_indicators == 3 else "Modérée"
        recommendation = (
            "Une évaluation clinique par un spécialiste du TDAH adulte "
            "(psychiatre, neurologue) est fortement recommandée. "
            "Apportez ce rapport lors de votre consultation."
        )
    elif positive_indicators == 1:
        summary = (
            f"SYNTHÈSE: {positive_indicators}/{total_indicators} outil d'évaluation suggère "
            "des symptômes possiblement compatibles avec un TDAH.\n\n"
            "Les résultats sont mixtes et nécessitent une interprétation clinique."
        )
        confidence = "Faible"
        recommendation = (
            "Si ces difficultés impactent significativement votre quotidien, "
            "une consultation avec un professionnel de santé pourrait être bénéfique "
            "pour explorer les causes possibles."
        )
    else:
        summary = (
            f"SYNTHÈSE: {positive_indicators}/{total_indicators} outils d'évaluation "
            "ne suggèrent pas de symptômes significatifs de TDAH."
        )
        confidence = "N/A"
        recommendation = (
            "Les résultats de cette auto-évaluation ne suggèrent pas de TDAH. "
            "Si vous avez des préoccupations persistantes, n'hésitez pas à "
            "consulter un professionnel de santé."
        )

    return GlobalAssessment(
        asrs=asrs,
        diva=diva,
        exec_functions=exec_func,
        summary=summary,
        clinical_recommendation=recommendation,
        confidence_level=confidence,
    )
