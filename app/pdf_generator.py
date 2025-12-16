"""
Générateur de rapport PDF pour l'évaluation TDAH.
Utilise WeasyPrint pour convertir HTML en PDF.
"""

from datetime import datetime
from weasyprint import HTML, CSS
from .scoring import GlobalAssessment


def generate_pdf_report(assessment: GlobalAssessment, responses: dict, questions: dict) -> bytes:
    """Génère un rapport PDF complet avec synthèse et annexes détaillées."""

    # Options de réponse pour affichage
    asrs_options = {0: "Jamais", 1: "Rarement", 2: "Parfois", 3: "Souvent", 4: "Très souvent"}
    diva_options = {0: "Non", 1: "Oui"}
    exec_options = {0: "Pas un problème", 1: "Rarement", 2: "Parfois", 3: "Souvent"}

    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")

    # Construction du HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @bottom-center {{
                    content: "Page " counter(page) " / " counter(pages);
                    font-size: 9pt;
                    color: #666;
                }}
            }}
            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                font-size: 18pt;
            }}
            h2 {{
                color: #2980b9;
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 5px;
                font-size: 14pt;
                margin-top: 20px;
            }}
            h3 {{
                color: #34495e;
                font-size: 12pt;
                margin-top: 15px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .disclaimer {{
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
                font-size: 10pt;
            }}
            .summary-box {{
                background-color: #e8f4f8;
                border: 2px solid #3498db;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
            }}
            .result-positive {{
                background-color: #ffebee;
                border-left: 4px solid #e74c3c;
                padding: 10px 15px;
                margin: 10px 0;
            }}
            .result-negative {{
                background-color: #e8f5e9;
                border-left: 4px solid #27ae60;
                padding: 10px 15px;
                margin: 10px 0;
            }}
            .result-moderate {{
                background-color: #fff8e1;
                border-left: 4px solid #f39c12;
                padding: 10px 15px;
                margin: 10px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-size: 10pt;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #3498db;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .score-bar {{
                background-color: #ecf0f1;
                border-radius: 5px;
                height: 20px;
                margin: 5px 0;
            }}
            .score-fill {{
                background-color: #3498db;
                height: 100%;
                border-radius: 5px;
            }}
            .annexe {{
                page-break-before: always;
            }}
            .response-yes {{
                color: #e74c3c;
                font-weight: bold;
            }}
            .response-no {{
                color: #27ae60;
            }}
            .clinical-note {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 15px;
                margin: 15px 0;
                font-style: italic;
            }}
            .references {{
                font-size: 9pt;
                color: #666;
                margin-top: 30px;
                border-top: 1px solid #ddd;
                padding-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Rapport d'Auto-Évaluation TDAH Adulte</h1>
            <p>Document généré le {date_str}</p>
        </div>

        <div class="disclaimer">
            <strong>AVERTISSEMENT IMPORTANT</strong><br>
            Ce document est un outil d'AUTO-ÉVALUATION et NE CONSTITUE PAS un diagnostic médical.
            Seul un professionnel de santé qualifié (psychiatre, neurologue) peut établir un diagnostic de TDAH
            après une évaluation clinique complète. Ce rapport est destiné à faciliter la discussion
            avec votre professionnel de santé.
        </div>

        <div class="summary-box">
            <h2 style="margin-top: 0; border: none;">Synthèse des Résultats</h2>
            <p style="white-space: pre-line;">{assessment.summary}</p>
            <p><strong>Recommandation:</strong> {assessment.clinical_recommendation}</p>
        </div>

        <h2>1. ASRS v1.1 - Échelle d'auto-évaluation OMS</h2>
        <div class="{'result-positive' if assessment.asrs.screening_positive else 'result-negative'}">
            <strong>Résultat du dépistage:</strong>
            {'POSITIF' if assessment.asrs.screening_positive else 'NÉGATIF'}
            ({assessment.asrs.part_a_shaded_count}/6 critères de la Partie A atteints, seuil ≥4)
        </div>
        <table>
            <tr>
                <th>Mesure</th>
                <th>Score</th>
                <th>Maximum</th>
            </tr>
            <tr>
                <td>Partie A (Screener)</td>
                <td>{assessment.asrs.part_a_score}</td>
                <td>24</td>
            </tr>
            <tr>
                <td>Partie B (Complémentaire)</td>
                <td>{assessment.asrs.part_b_score}</td>
                <td>48</td>
            </tr>
            <tr>
                <td><strong>Score Total</strong></td>
                <td><strong>{assessment.asrs.total_score}</strong></td>
                <td><strong>72</strong></td>
            </tr>
            <tr>
                <td>Sous-score Inattention</td>
                <td>{assessment.asrs.inattention_score}</td>
                <td>36</td>
            </tr>
            <tr>
                <td>Sous-score Hyperactivité/Impulsivité</td>
                <td>{assessment.asrs.hyperactivity_score}</td>
                <td>36</td>
            </tr>
        </table>
        <p><em>{assessment.asrs.interpretation}</em></p>

        <h2>2. Évaluation selon les critères DSM-5</h2>
        <div class="{'result-positive' if (assessment.diva.meets_inattention_criteria or assessment.diva.meets_hyperactivity_criteria) else 'result-negative'}">
            <strong>Présentation suggérée:</strong> {assessment.diva.presentation_type}
        </div>
        <table>
            <tr>
                <th>Critère</th>
                <th>Résultat</th>
                <th>Seuil DSM-5</th>
            </tr>
            <tr>
                <td>A1 - Inattention</td>
                <td>{assessment.diva.inattention_count}/9 symptômes</td>
                <td>≥5 requis</td>
            </tr>
            <tr>
                <td>A2 - Hyperactivité/Impulsivité</td>
                <td>{assessment.diva.hyperactivity_count}/9 symptômes</td>
                <td>≥5 requis</td>
            </tr>
            <tr>
                <td>B - Début avant 12 ans</td>
                <td>{'Oui' if assessment.diva.childhood_positive else 'Non confirmé'}</td>
                <td>Requis</td>
            </tr>
            <tr>
                <td>C/D - Retentissement</td>
                <td>{len(assessment.diva.impairment_domains)} domaine(s)</td>
                <td>≥2 domaines</td>
            </tr>
        </table>
        {f'<p><strong>Domaines impactés:</strong> {", ".join(assessment.diva.impairment_domains)}</p>' if assessment.diva.impairment_domains else ''}

        <h2>3. Évaluation des Fonctions Exécutives</h2>
        <div class="{'result-positive' if assessment.exec_functions.severity == 'Élevé' else 'result-moderate' if assessment.exec_functions.severity == 'Modéré' else 'result-negative'}">
            <strong>Niveau de difficulté global:</strong> {assessment.exec_functions.severity}
            (Score: {assessment.exec_functions.total_score}/{assessment.exec_functions.max_score})
        </div>
        <table>
            <tr>
                <th>Cluster</th>
                <th>Score</th>
                <th>Maximum</th>
                <th>%</th>
            </tr>
    """

    for cluster_name, (score, max_score) in assessment.exec_functions.cluster_scores.items():
        pct = round((score / max_score * 100) if max_score > 0 else 0)
        html_content += f"""
            <tr>
                <td>{cluster_name}</td>
                <td>{score}</td>
                <td>{max_score}</td>
                <td>{pct}%</td>
            </tr>
        """

    html_content += f"""
        </table>
        {f'<p><strong>Domaines les plus impactés:</strong> {", ".join(assessment.exec_functions.most_impaired_clusters)}</p>' if assessment.exec_functions.most_impaired_clusters else ''}
        <p><em>{assessment.exec_functions.interpretation}</em></p>

        <div class="clinical-note">
            <strong>Note pour le clinicien:</strong><br>
            Cette auto-évaluation utilise trois outils complémentaires: l'ASRS v1.1 (OMS/Harvard),
            une évaluation structurée basée sur les critères DSM-5, et une évaluation des fonctions
            exécutives. Les résultats doivent être interprétés dans le contexte d'une évaluation
            clinique complète incluant l'histoire développementale, les comorbidités possibles,
            et l'exclusion de diagnostics différentiels.
        </div>

        <!-- ANNEXES -->
        <div class="annexe">
            <h1>Annexes - Réponses Détaillées</h1>

            <h2>A. ASRS v1.1 - Réponses complètes</h2>
            <h3>Partie A (Screener)</h3>
            <table>
                <tr>
                    <th style="width: 70%;">Question</th>
                    <th>Réponse</th>
                </tr>
    """

    # Annexe ASRS Partie A
    for q in questions['asrs']:
        if q.subcategory == 'part_a':
            val = responses.get(q.id, 0)
            response_text = asrs_options.get(val, "Non répondu")
            html_content += f"""
                <tr>
                    <td>{q.text}</td>
                    <td>{response_text}</td>
                </tr>
            """

    html_content += """
            </table>
            <h3>Partie B (Questions supplémentaires)</h3>
            <table>
                <tr>
                    <th style="width: 70%;">Question</th>
                    <th>Réponse</th>
                </tr>
    """

    # Annexe ASRS Partie B
    for q in questions['asrs']:
        if q.subcategory == 'part_b':
            val = responses.get(q.id, 0)
            response_text = asrs_options.get(val, "Non répondu")
            html_content += f"""
                <tr>
                    <td>{q.text}</td>
                    <td>{response_text}</td>
                </tr>
            """

    html_content += """
            </table>

            <h2>B. Critères DSM-5 - Réponses complètes</h2>
            <h3>Critères d'Inattention (A1)</h3>
            <table>
                <tr>
                    <th style="width: 80%;">Critère</th>
                    <th>Réponse</th>
                </tr>
    """

    # Annexe DIVA Inattention
    for q in questions['diva_inattention']:
        val = responses.get(q.id, 0)
        response_text = diva_options.get(val, "Non répondu")
        css_class = "response-yes" if val == 1 else "response-no"
        html_content += f"""
                <tr>
                    <td>{q.text}</td>
                    <td class="{css_class}">{response_text}</td>
                </tr>
        """

    html_content += """
            </table>
            <h3>Critères d'Hyperactivité-Impulsivité (A2)</h3>
            <table>
                <tr>
                    <th style="width: 80%;">Critère</th>
                    <th>Réponse</th>
                </tr>
    """

    # Annexe DIVA Hyperactivité
    for q in questions['diva_hyperactivity']:
        val = responses.get(q.id, 0)
        response_text = diva_options.get(val, "Non répondu")
        css_class = "response-yes" if val == 1 else "response-no"
        html_content += f"""
                <tr>
                    <td>{q.text}</td>
                    <td class="{css_class}">{response_text}</td>
                </tr>
        """

    html_content += """
            </table>
            <h3>Symptômes dans l'enfance</h3>
            <table>
                <tr>
                    <th style="width: 80%;">Question</th>
                    <th>Réponse</th>
                </tr>
    """

    # Annexe DIVA Enfance
    for q in questions['diva_childhood']:
        val = responses.get(q.id, 0)
        response_text = diva_options.get(val, "Non répondu")
        css_class = "response-yes" if val == 1 else "response-no"
        html_content += f"""
                <tr>
                    <td>{q.text}</td>
                    <td class="{css_class}">{response_text}</td>
                </tr>
        """

    html_content += """
            </table>
            <h3>Retentissement fonctionnel</h3>
            <table>
                <tr>
                    <th style="width: 80%;">Domaine</th>
                    <th>Impact</th>
                </tr>
    """

    # Annexe DIVA Retentissement
    for q in questions['diva_impairment']:
        val = responses.get(q.id, 0)
        response_text = diva_options.get(val, "Non répondu")
        css_class = "response-yes" if val == 1 else "response-no"
        html_content += f"""
                <tr>
                    <td>{q.text}</td>
                    <td class="{css_class}">{response_text}</td>
                </tr>
        """

    html_content += """
            </table>

            <h2>C. Fonctions Exécutives - Réponses complètes</h2>
            <table>
                <tr>
                    <th>Cluster</th>
                    <th style="width: 50%;">Item</th>
                    <th>Réponse</th>
                </tr>
    """

    # Annexe Fonctions Exécutives
    cluster_names = {
        'activation': 'Activation',
        'focus': 'Focus',
        'effort': 'Effort',
        'emotion': 'Émotion',
        'memoire': 'Mémoire',
        'action': 'Action',
    }
    for q in questions['exec_functions']:
        val = responses.get(q.id, 0)
        response_text = exec_options.get(val, "Non répondu")
        html_content += f"""
                <tr>
                    <td>{cluster_names.get(q.category, q.category)}</td>
                    <td>{q.text}</td>
                    <td>{response_text}</td>
                </tr>
        """

    html_content += f"""
            </table>
        </div>

        <div class="references">
            <h3>Références scientifiques</h3>
            <ol>
                <li>Kessler, R.C., et al. (2005). The World Health Organization Adult ADHD Self-Report Scale (ASRS). <em>Psychological Medicine</em>, 35(2), 245-256.</li>
                <li>American Psychiatric Association. (2013). <em>Diagnostic and Statistical Manual of Mental Disorders</em> (5th ed.).</li>
                <li>Kooij, J.J.S., et al. (2010). DIVA 2.0: Diagnostic Interview for ADHD in Adults. DIVA Foundation.</li>
                <li>Brown, T.E. (2013). A New Understanding of ADHD in Children and Adults: Executive Function Impairments. Routledge.</li>
            </ol>
            <p><em>Document généré automatiquement - Ne constitue pas un diagnostic médical</em></p>
        </div>
    </body>
    </html>
    """

    # Génération du PDF
    pdf = HTML(string=html_content).write_pdf()
    return pdf
