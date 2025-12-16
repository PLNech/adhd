"""Routes Flask pour l'application d'évaluation TDAH."""

from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from .questionnaires import (
    ASRS_QUESTIONS, ASRS_RESPONSE_OPTIONS,
    DIVA_INATTENTION_CRITERIA, DIVA_HYPERACTIVITY_CRITERIA,
    DIVA_CHILDHOOD_QUESTIONS, DIVA_IMPAIRMENT_DOMAINS, DIVA_RESPONSE_OPTIONS,
    EXEC_FUNCTION_QUESTIONS, EXEC_FUNCTION_RESPONSE_OPTIONS,
)
from .scoring import score_asrs, score_diva, score_executive_functions, generate_global_assessment
from .pdf_generator import generate_pdf_report

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Page d'accueil avec avertissements et consentement."""
    return render_template('index.html')


@bp.route('/start', methods=['POST'])
def start():
    """Démarre l'évaluation après consentement."""
    session.clear()
    session['consent'] = True
    session['responses'] = {}
    return redirect(url_for('main.asrs'))


@bp.route('/asrs', methods=['GET', 'POST'])
def asrs():
    """Questionnaire ASRS (OMS)."""
    if not session.get('consent'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        responses = session.get('responses', {})
        for q in ASRS_QUESTIONS:
            value = request.form.get(q.id)
            if value is not None:
                responses[q.id] = int(value)
        session['responses'] = responses
        return redirect(url_for('main.diva'))

    part_a = [q for q in ASRS_QUESTIONS if q.subcategory == 'part_a']
    part_b = [q for q in ASRS_QUESTIONS if q.subcategory == 'part_b']

    return render_template(
        'asrs.html',
        part_a=part_a,
        part_b=part_b,
        options=ASRS_RESPONSE_OPTIONS,
        responses=session.get('responses', {}),
    )


@bp.route('/diva', methods=['GET', 'POST'])
def diva():
    """Questionnaire DIVA-style (critères DSM-5)."""
    if not session.get('consent'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        responses = session.get('responses', {})
        all_questions = (
            DIVA_INATTENTION_CRITERIA +
            DIVA_HYPERACTIVITY_CRITERIA +
            DIVA_CHILDHOOD_QUESTIONS +
            DIVA_IMPAIRMENT_DOMAINS
        )
        for q in all_questions:
            value = request.form.get(q.id)
            if value is not None:
                responses[q.id] = int(value)
        session['responses'] = responses
        return redirect(url_for('main.exec_functions'))

    return render_template(
        'diva.html',
        inattention=DIVA_INATTENTION_CRITERIA,
        hyperactivity=DIVA_HYPERACTIVITY_CRITERIA,
        childhood=DIVA_CHILDHOOD_QUESTIONS,
        impairment=DIVA_IMPAIRMENT_DOMAINS,
        options=DIVA_RESPONSE_OPTIONS,
        responses=session.get('responses', {}),
    )


@bp.route('/executive', methods=['GET', 'POST'])
def exec_functions():
    """Questionnaire fonctions exécutives."""
    if not session.get('consent'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        responses = session.get('responses', {})
        for q in EXEC_FUNCTION_QUESTIONS:
            value = request.form.get(q.id)
            if value is not None:
                responses[q.id] = int(value)
        session['responses'] = responses
        return redirect(url_for('main.results'))

    # Grouper par cluster
    clusters = {}
    cluster_names = {
        'activation': 'Activation (organisation, démarrage)',
        'focus': 'Attention / Focus',
        'effort': 'Effort / Énergie',
        'emotion': 'Régulation émotionnelle',
        'memoire': 'Mémoire de travail',
        'action': 'Inhibition / Action',
    }
    for q in EXEC_FUNCTION_QUESTIONS:
        if q.category not in clusters:
            clusters[q.category] = {
                'name': cluster_names.get(q.category, q.category),
                'questions': []
            }
        clusters[q.category]['questions'].append(q)

    return render_template(
        'executive.html',
        clusters=clusters,
        options=EXEC_FUNCTION_RESPONSE_OPTIONS,
        responses=session.get('responses', {}),
    )


@bp.route('/results')
def results():
    """Affiche les résultats de l'évaluation."""
    if not session.get('consent'):
        return redirect(url_for('main.index'))

    responses = session.get('responses', {})
    if not responses:
        return redirect(url_for('main.asrs'))

    asrs_result = score_asrs(responses)
    diva_result = score_diva(responses)
    exec_result = score_executive_functions(responses)
    global_assessment = generate_global_assessment(asrs_result, diva_result, exec_result)

    return render_template(
        'results.html',
        asrs=asrs_result,
        diva=diva_result,
        exec_func=exec_result,
        assessment=global_assessment,
    )


@bp.route('/download-pdf')
def download_pdf():
    """Génère et télécharge le rapport PDF."""
    if not session.get('consent'):
        return redirect(url_for('main.index'))

    responses = session.get('responses', {})
    if not responses:
        return redirect(url_for('main.asrs'))

    asrs_result = score_asrs(responses)
    diva_result = score_diva(responses)
    exec_result = score_executive_functions(responses)
    global_assessment = generate_global_assessment(asrs_result, diva_result, exec_result)

    # Récupérer les questions pour les annexes
    all_questions = {
        'asrs': ASRS_QUESTIONS,
        'diva_inattention': DIVA_INATTENTION_CRITERIA,
        'diva_hyperactivity': DIVA_HYPERACTIVITY_CRITERIA,
        'diva_childhood': DIVA_CHILDHOOD_QUESTIONS,
        'diva_impairment': DIVA_IMPAIRMENT_DOMAINS,
        'exec_functions': EXEC_FUNCTION_QUESTIONS,
    }

    pdf_bytes = generate_pdf_report(global_assessment, responses, all_questions)

    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=evaluation_tdah.pdf'
    return response
