/**
 * Clarté - ADHD Self-Evaluation App
 * Client-side questionnaire logic and PDF generation
 */

// ============================================
// QUESTIONNAIRE DATA
// ============================================

const ASRS_QUESTIONS = {
    part_a: [
        { id: 'asrs_1', text: "À quelle fréquence avez-vous des difficultés à finaliser les derniers détails d'un projet, une fois que les parties les plus stimulantes ont été réalisées ?", threshold: 2 },
        { id: 'asrs_2', text: "À quelle fréquence avez-vous des difficultés à mettre de l'ordre lorsque vous devez effectuer une tâche qui requiert de l'organisation ?", threshold: 2 },
        { id: 'asrs_3', text: "À quelle fréquence avez-vous des difficultés à vous souvenir de vos rendez-vous ou de vos obligations ?", threshold: 2 },
        { id: 'asrs_4', text: "Lorsque vous devez effectuer une tâche qui demande beaucoup de réflexion, à quelle fréquence évitez-vous ou retardez-vous le moment de commencer ?", threshold: 3 },
        { id: 'asrs_5', text: "À quelle fréquence remuez-vous ou tortillez-vous les mains ou les pieds lorsque vous devez rester assis(e) pendant une longue période ?", threshold: 3 },
        { id: 'asrs_6', text: "À quelle fréquence vous sentez-vous excessivement actif(ve) et poussé(e) à faire des choses, comme si vous étiez mû(e) par un moteur ?", threshold: 3 },
    ],
    part_b: [
        { id: 'asrs_7', text: "À quelle fréquence faites-vous des erreurs d'inattention lorsque vous devez travailler sur un projet ennuyeux ou difficile ?" },
        { id: 'asrs_8', text: "À quelle fréquence avez-vous des difficultés à maintenir votre attention lorsque vous effectuez un travail ennuyeux ou répétitif ?" },
        { id: 'asrs_9', text: "À quelle fréquence avez-vous des difficultés à vous concentrer sur ce que les gens vous disent, même lorsqu'ils s'adressent directement à vous ?" },
        { id: 'asrs_10', text: "À quelle fréquence égarez-vous ou avez-vous du mal à retrouver des objets à la maison ou au travail ?" },
        { id: 'asrs_11', text: "À quelle fréquence êtes-vous distrait(e) par l'activité ou le bruit autour de vous ?" },
        { id: 'asrs_12', text: "À quelle fréquence quittez-vous votre siège lors de réunions ou dans d'autres situations où vous êtes censé(e) rester assis(e) ?" },
        { id: 'asrs_13', text: "À quelle fréquence vous sentez-vous agité(e) ou remuant(e) ?" },
        { id: 'asrs_14', text: "À quelle fréquence avez-vous des difficultés à vous détendre et à vous relaxer lorsque vous avez du temps libre ?" },
        { id: 'asrs_15', text: "À quelle fréquence vous trouvez-vous à parler trop en situation sociale ?" },
        { id: 'asrs_16', text: "Lors d'une conversation, à quelle fréquence finissez-vous les phrases des personnes avec qui vous parlez avant qu'elles ne puissent les terminer elles-mêmes ?" },
        { id: 'asrs_17', text: "À quelle fréquence avez-vous des difficultés à attendre votre tour dans des situations qui l'exigent ?" },
        { id: 'asrs_18', text: "À quelle fréquence interrompez-vous les autres lorsqu'ils sont occupés ?" },
    ]
};

const ASRS_OPTIONS = [
    { value: 0, label: 'Jamais' },
    { value: 1, label: 'Rarement' },
    { value: 2, label: 'Parfois' },
    { value: 3, label: 'Souvent' },
    { value: 4, label: 'Très souvent' }
];

const DIVA_INATTENTION = [
    { id: 'diva_ia_1', text: "Avez-vous souvent du mal à prêter attention aux détails ou faites-vous des erreurs d'inattention dans votre travail ou d'autres activités ? (ex: négliger des détails, travail inexact)" },
    { id: 'diva_ia_2', text: "Avez-vous souvent du mal à maintenir votre attention sur des tâches ou des activités ? (ex: difficulté à rester concentré pendant les réunions, lectures)" },
    { id: 'diva_ia_3', text: "Avez-vous souvent l'impression de ne pas écouter quand on vous parle directement ? (ex: esprit ailleurs, même sans distraction évidente)" },
    { id: 'diva_ia_4', text: "Avez-vous souvent du mal à suivre les instructions jusqu'au bout et à terminer vos tâches professionnelles ou obligations ?" },
    { id: 'diva_ia_5', text: "Avez-vous souvent du mal à organiser vos tâches et activités ? (ex: difficulté à gérer le temps, respecter les délais)" },
    { id: 'diva_ia_6', text: "Évitez-vous souvent, ou êtes-vous réticent(e) à vous engager dans des tâches qui nécessitent un effort mental soutenu ?" },
    { id: 'diva_ia_7', text: "Perdez-vous souvent des objets nécessaires à vos activités ? (ex: clés, portefeuille, téléphone, documents)" },
    { id: 'diva_ia_8', text: "Êtes-vous souvent facilement distrait(e) par des stimuli externes ou des pensées sans rapport ?" },
    { id: 'diva_ia_9', text: "Êtes-vous souvent oublieux(se) dans la vie quotidienne ? (ex: oublier de rappeler, payer des factures, honorer des rendez-vous)" },
];

const DIVA_HYPERACTIVITY = [
    { id: 'diva_hi_1', text: "Remuez-vous souvent les mains ou les pieds, ou vous tortillez-vous sur votre siège ?" },
    { id: 'diva_hi_2', text: "Quittez-vous souvent votre siège dans des situations où vous êtes censé(e) rester assis(e) ?" },
    { id: 'diva_hi_3', text: "Vous sentez-vous souvent agité(e) ou avez-vous du mal à rester en place ?" },
    { id: 'diva_hi_4', text: "Avez-vous souvent du mal à vous adonner à des loisirs ou activités calmes de manière tranquille ?" },
    { id: 'diva_hi_5', text: "Êtes-vous souvent « sur la brèche » ou agissez-vous comme si vous étiez « monté(e) sur ressorts » ?" },
    { id: 'diva_hi_6', text: "Parlez-vous souvent trop ?" },
    { id: 'diva_hi_7', text: "Laissez-vous souvent échapper une réponse avant qu'une question ne soit terminée ?" },
    { id: 'diva_hi_8', text: "Avez-vous souvent du mal à attendre votre tour ?" },
    { id: 'diva_hi_9', text: "Interrompez-vous souvent les autres ou vous imposez-vous ?" },
];

const DIVA_CHILDHOOD = [
    { id: 'diva_child_1', text: "Avant l'âge de 12 ans, aviez-vous des difficultés à rester attentif(ve) à l'école ou lors des devoirs ?" },
    { id: 'diva_child_2', text: "Avant l'âge de 12 ans, étiez-vous considéré(e) comme un enfant rêveur, « dans la lune » ?" },
    { id: 'diva_child_3', text: "Avant l'âge de 12 ans, aviez-vous du mal à rester assis(e) ou étiez-vous agité(e) à l'école ?" },
    { id: 'diva_child_4', text: "Avant l'âge de 12 ans, aviez-vous souvent des remarques sur vos bulletins concernant l'attention ou le comportement ?" },
    { id: 'diva_child_5', text: "Avant l'âge de 12 ans, perdiez-vous souvent vos affaires scolaires ou oubliiez-vous de faire vos devoirs ?" },
];

const DIVA_IMPAIRMENT = [
    { id: 'diva_imp_1', text: "Ces difficultés ont-elles un impact négatif sur votre travail ou vos études ?", domain: "Travail/Études" },
    { id: 'diva_imp_2', text: "Ces difficultés ont-elles un impact négatif sur vos relations familiales ou amoureuses ?", domain: "Relations familiales" },
    { id: 'diva_imp_3', text: "Ces difficultés ont-elles un impact négatif sur vos relations sociales et amicales ?", domain: "Relations sociales" },
    { id: 'diva_imp_4', text: "Ces difficultés ont-elles un impact négatif sur vos loisirs et activités de temps libre ?", domain: "Loisirs" },
    { id: 'diva_imp_5', text: "Ces difficultés ont-elles un impact négatif sur votre estime de soi ou votre confiance en vous ?", domain: "Estime de soi" },
];

const EXEC_FUNCTIONS = {
    activation: {
        name: "Activation",
        description: "Organisation, priorisation, démarrage",
        questions: [
            { id: 'ef_act_1', text: "Difficulté à organiser et planifier des tâches ou projets" },
            { id: 'ef_act_2', text: "Difficulté à établir des priorités entre différentes tâches" },
            { id: 'ef_act_3', text: "Difficulté à commencer une tâche, même quand elle est importante" },
            { id: 'ef_act_4', text: "Tendance à procrastiner, reporter les tâches au lendemain" },
        ]
    },
    focus: {
        name: "Attention / Focus",
        description: "Attention soutenue, résistance à la distraction",
        questions: [
            { id: 'ef_foc_1', text: "Difficulté à maintenir l'attention sur une tâche jusqu'à son achèvement" },
            { id: 'ef_foc_2', text: "Facilement distrait(e) par des pensées ou stimuli non pertinents" },
            { id: 'ef_foc_3', text: "Difficulté à écouter et retenir ce qui est dit lors de conversations" },
            { id: 'ef_foc_4', text: "Passer d'une activité à l'autre sans en terminer aucune" },
        ]
    },
    effort: {
        name: "Effort / Énergie",
        description: "Régulation de l'éveil et de la vigilance",
        questions: [
            { id: 'ef_eff_1', text: "Somnolence ou fatigue mentale lors de tâches peu stimulantes" },
            { id: 'ef_eff_2', text: "Difficulté à maintenir un niveau d'énergie constant tout au long de la journée" },
            { id: 'ef_eff_3', text: "Lenteur excessive pour accomplir des tâches routinières" },
            { id: 'ef_eff_4', text: "Besoin de stimulation intense pour rester motivé(e)" },
        ]
    },
    emotion: {
        name: "Régulation émotionnelle",
        description: "Gestion de la frustration et des affects",
        questions: [
            { id: 'ef_emo_1', text: "Réactions émotionnelles excessives ou disproportionnées" },
            { id: 'ef_emo_2', text: "Difficulté à gérer la frustration et l'irritabilité" },
            { id: 'ef_emo_3', text: "Sensibilité excessive aux critiques ou aux commentaires négatifs" },
            { id: 'ef_emo_4', text: "Fluctuations d'humeur fréquentes au cours de la journée" },
        ]
    },
    memory: {
        name: "Mémoire de travail",
        description: "Mémoire active et rappel",
        questions: [
            { id: 'ef_mem_1', text: "Oublier ce que l'on vient de lire et devoir relire plusieurs fois" },
            { id: 'ef_mem_2', text: "Difficulté à se souvenir des consignes ou instructions données verbalement" },
            { id: 'ef_mem_3', text: "Oublier fréquemment des rendez-vous ou des tâches prévues" },
            { id: 'ef_mem_4', text: "Perdre le fil de ses pensées en milieu de phrase ou d'action" },
        ]
    },
    action: {
        name: "Inhibition / Action",
        description: "Contrôle des impulsions et auto-régulation",
        questions: [
            { id: 'ef_act2_1', text: "Agir ou parler impulsivement sans réfléchir aux conséquences" },
            { id: 'ef_act2_2', text: "Difficulté à rester assis(e) ou à se tenir tranquille" },
            { id: 'ef_act2_3', text: "Interrompre les autres ou s'imposer dans les conversations" },
            { id: 'ef_act2_4', text: "Difficulté à contrôler ses impulsions (achats, alimentation, etc.)" },
        ]
    }
};

const EF_OPTIONS = [
    { value: 0, label: 'Pas un problème' },
    { value: 1, label: 'Rarement' },
    { value: 2, label: 'Parfois' },
    { value: 3, label: 'Souvent' }
];

// ============================================
// APP STATE
// ============================================

const state = {
    currentSection: 'home',
    responses: {},
    results: null
};

// ============================================
// NAVIGATION
// ============================================

const sections = ['home', 'asrs', 'diva', 'executive', 'results'];

function showSection(sectionId) {
    sections.forEach(s => {
        const el = document.getElementById(s);
        if (el) el.classList.remove('active');
    });
    const target = document.getElementById(sectionId);
    if (target) {
        target.classList.add('active');
        state.currentSection = sectionId;
        updateProgress();
        window.scrollTo(0, 0);
    }
}

function updateProgress() {
    const currentIndex = sections.indexOf(state.currentSection);
    const dots = document.querySelectorAll('.step-dot');
    const connectors = document.querySelectorAll('.step-connector');
    const label = document.querySelector('.progress-label');

    dots.forEach((dot, i) => {
        dot.classList.remove('active', 'completed');
        if (i < currentIndex) dot.classList.add('completed');
        if (i === currentIndex) dot.classList.add('active');
    });

    connectors.forEach((conn, i) => {
        conn.classList.remove('completed');
        if (i < currentIndex) conn.classList.add('completed');
    });

    const labels = ['Accueil', 'ASRS (OMS)', 'Critères DSM-5', 'Fonctions Exécutives', 'Résultats'];
    if (label) label.textContent = labels[currentIndex] || '';
}

// ============================================
// RENDER QUESTIONS
// ============================================

function renderASRS() {
    const container = document.getElementById('asrs-questions');
    let html = '';

    // Part A
    html += `<div class="question-group">
        <h3>Partie A — Dépistage</h3>
        <p class="hint">Ces 6 questions sont les plus prédictives du TDAH.</p>`;

    ASRS_QUESTIONS.part_a.forEach((q, i) => {
        html += renderQuestion(q, i + 1, ASRS_OPTIONS);
    });
    html += '</div>';

    // Part B
    html += `<div class="question-group">
        <h3>Partie B — Questions complémentaires</h3>`;

    ASRS_QUESTIONS.part_b.forEach((q, i) => {
        html += renderQuestion(q, i + 7, ASRS_OPTIONS);
    });
    html += '</div>';

    container.innerHTML = html;
    attachOptionHandlers(container);
}

function renderDIVA() {
    const container = document.getElementById('diva-questions');
    let html = '';

    // Inattention
    html += `<div class="question-group">
        <h3>Critère A1 — Inattention</h3>
        <p class="hint">Pour les adultes, ≥5 symptômes sont requis. Répondez Oui si le symptôme est fréquent depuis plus de 6 mois.</p>`;
    DIVA_INATTENTION.forEach((q, i) => {
        html += renderBinaryQuestion(q, i + 1);
    });
    html += '</div>';

    // Hyperactivity
    html += `<div class="question-group">
        <h3>Critère A2 — Hyperactivité / Impulsivité</h3>`;
    DIVA_HYPERACTIVITY.forEach((q, i) => {
        html += renderBinaryQuestion(q, i + 1);
    });
    html += '</div>';

    // Childhood
    html += `<div class="question-group">
        <h3>Critère B — Symptômes dans l'enfance</h3>
        <p class="hint">Le DSM-5 exige que des symptômes aient été présents avant l'âge de 12 ans.</p>`;
    DIVA_CHILDHOOD.forEach((q, i) => {
        html += renderBinaryQuestion(q, i + 1);
    });
    html += '</div>';

    // Impairment
    html += `<div class="question-group">
        <h3>Critères C/D — Retentissement fonctionnel</h3>
        <p class="hint">Les symptômes doivent causer une gêne significative dans au moins 2 domaines.</p>`;
    DIVA_IMPAIRMENT.forEach((q, i) => {
        html += renderBinaryQuestion(q, i + 1);
    });
    html += '</div>';

    container.innerHTML = html;
    attachOptionHandlers(container);
}

function renderExecutive() {
    const container = document.getElementById('executive-questions');
    let html = '';

    Object.values(EXEC_FUNCTIONS).forEach(cluster => {
        html += `<div class="question-group">
            <h3>${cluster.name}</h3>
            <p class="hint">${cluster.description}</p>`;
        cluster.questions.forEach((q, i) => {
            html += renderQuestion(q, i + 1, EF_OPTIONS, true);
        });
        html += '</div>';
    });

    container.innerHTML = html;
    attachOptionHandlers(container);
}

function renderQuestion(q, num, options, compact = false) {
    const answered = state.responses[q.id] !== undefined;
    return `
        <div class="question ${answered ? 'answered' : ''}" data-id="${q.id}">
            <p class="question-text"><span class="question-number">${num}.</span> ${q.text}</p>
            <div class="options">
                ${options.map(opt => `
                    <div class="option">
                        <input type="radio" name="${q.id}" id="${q.id}_${opt.value}" value="${opt.value}"
                            ${state.responses[q.id] === opt.value ? 'checked' : ''}>
                        <label for="${q.id}_${opt.value}">${opt.label}</label>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function renderBinaryQuestion(q, num) {
    const answered = state.responses[q.id] !== undefined;
    return `
        <div class="question ${answered ? 'answered' : ''}" data-id="${q.id}">
            <p class="question-text"><span class="question-number">${num}.</span> ${q.text}</p>
            <div class="options binary">
                <div class="option yes">
                    <input type="radio" name="${q.id}" id="${q.id}_1" value="1"
                        ${state.responses[q.id] === 1 ? 'checked' : ''}>
                    <label for="${q.id}_1">Oui</label>
                </div>
                <div class="option no">
                    <input type="radio" name="${q.id}" id="${q.id}_0" value="0"
                        ${state.responses[q.id] === 0 ? 'checked' : ''}>
                    <label for="${q.id}_0">Non</label>
                </div>
            </div>
        </div>
    `;
}

function attachOptionHandlers(container) {
    container.querySelectorAll('input[type="radio"]').forEach(input => {
        input.addEventListener('change', (e) => {
            state.responses[e.target.name] = parseInt(e.target.value);
            const question = e.target.closest('.question');
            if (question) question.classList.add('answered');
        });
    });
}

// ============================================
// SCORING
// ============================================

function calculateResults() {
    const results = {
        asrs: scoreASRS(),
        diva: scoreDIVA(),
        executive: scoreExecutive()
    };

    // Global assessment
    let positiveIndicators = 0;
    if (results.asrs.screeningPositive) positiveIndicators++;
    if (results.diva.meetsInattention || results.diva.meetsHyperactivity) positiveIndicators++;
    if (results.executive.severity !== 'Faible') positiveIndicators++;

    results.global = {
        positiveIndicators,
        confidence: positiveIndicators >= 3 ? 'Élevée' : positiveIndicators >= 2 ? 'Modérée' : 'Faible'
    };

    state.results = results;
    return results;
}

function scoreASRS() {
    let partAScore = 0, partAShaded = 0, partBScore = 0;
    let inattention = 0, hyperactivity = 0;
    const inattentionQs = [1, 2, 3, 4, 7, 8, 9, 10, 11];

    ASRS_QUESTIONS.part_a.forEach(q => {
        const val = state.responses[q.id] || 0;
        partAScore += val;
        if (val >= q.threshold) partAShaded++;

        const num = parseInt(q.id.split('_')[1]);
        if (inattentionQs.includes(num)) inattention += val;
        else hyperactivity += val;
    });

    ASRS_QUESTIONS.part_b.forEach(q => {
        const val = state.responses[q.id] || 0;
        partBScore += val;

        const num = parseInt(q.id.split('_')[1]);
        if (inattentionQs.includes(num)) inattention += val;
        else hyperactivity += val;
    });

    const screeningPositive = partAShaded >= 4;

    return {
        partAScore,
        partAShaded,
        partBScore,
        total: partAScore + partBScore,
        inattention,
        hyperactivity,
        screeningPositive,
        interpretation: screeningPositive
            ? "Le dépistage est POSITIF. Vos réponses suggèrent des symptômes compatibles avec un TDAH chez l'adulte."
            : "Le dépistage est négatif. Une évaluation clinique reste recommandée si vous avez des préoccupations."
    };
}

function scoreDIVA() {
    let inattentionCount = 0, hyperactivityCount = 0, childhoodCount = 0;
    const impairmentDomains = [];

    DIVA_INATTENTION.forEach(q => {
        if (state.responses[q.id] === 1) inattentionCount++;
    });

    DIVA_HYPERACTIVITY.forEach(q => {
        if (state.responses[q.id] === 1) hyperactivityCount++;
    });

    DIVA_CHILDHOOD.forEach(q => {
        if (state.responses[q.id] === 1) childhoodCount++;
    });

    DIVA_IMPAIRMENT.forEach(q => {
        if (state.responses[q.id] === 1) impairmentDomains.push(q.domain);
    });

    const meetsInattention = inattentionCount >= 5;
    const meetsHyperactivity = hyperactivityCount >= 5;

    let presentation = "Sous les seuils cliniques";
    if (meetsInattention && meetsHyperactivity) presentation = "Inattention + Hyperactivité/Impulsivité";
    else if (meetsInattention) presentation = "Inattention prédominante";
    else if (meetsHyperactivity) presentation = "Hyperactivité/Impulsivité prédominante";

    return {
        inattentionCount,
        hyperactivityCount,
        childhoodCount,
        childhoodPositive: childhoodCount >= 2,
        impairmentDomains,
        meetsInattention,
        meetsHyperactivity,
        presentation
    };
}

function scoreExecutive() {
    const clusterScores = {};
    let total = 0, maxTotal = 0;

    Object.entries(EXEC_FUNCTIONS).forEach(([key, cluster]) => {
        let score = 0;
        cluster.questions.forEach(q => {
            score += state.responses[q.id] || 0;
        });
        const max = cluster.questions.length * 3;
        clusterScores[cluster.name] = { score, max, percentage: Math.round((score / max) * 100) };
        total += score;
        maxTotal += max;
    });

    const percentage = Math.round((total / maxTotal) * 100);
    let severity = 'Faible';
    if (percentage >= 66) severity = 'Élevé';
    else if (percentage >= 40) severity = 'Modéré';

    const impaired = Object.entries(clusterScores)
        .filter(([_, s]) => s.percentage >= 50)
        .map(([name, _]) => name);

    return { clusterScores, total, maxTotal, percentage, severity, impaired };
}

// ============================================
// RENDER RESULTS
// ============================================

function renderResults() {
    const results = calculateResults();
    const container = document.getElementById('results-content');

    const asrsLevel = results.asrs.screeningPositive ? 'high' : 'low';
    const divaLevel = (results.diva.meetsInattention || results.diva.meetsHyperactivity) ? 'high' : 'low';
    const efLevel = results.executive.severity === 'Élevé' ? 'high' : results.executive.severity === 'Modéré' ? 'moderate' : 'low';

    let html = `
        <div class="summary-card">
            <h2>Synthèse</h2>
            <p class="summary-text">
                <strong>${results.global.positiveIndicators}/3</strong> outils d'évaluation suggèrent des symptômes
                ${results.global.positiveIndicators >= 2 ? 'évocateurs, méritant une évaluation clinique' : 'à explorer si besoin'}.
            </p>
            ${results.asrs.screeningPositive ? '<p>• ASRS: Seuil de dépistage <strong>atteint</strong></p>' : ''}
            ${results.diva.meetsInattention || results.diva.meetsHyperactivity ?
                `<p>• Critères DSM-5: <strong>${results.diva.presentation}</strong></p>` : ''}
            ${results.executive.severity !== 'Faible' ?
                `<p>• Fonctions exécutives: Difficultés de niveau <strong>${results.executive.severity}</strong></p>` : ''}
            <div class="recommendation">
                <strong>Recommandation:</strong>
                ${results.global.positiveIndicators >= 2
                    ? "Une évaluation clinique par un spécialiste (psychiatre, neurologue) est recommandée pour explorer ces symptômes. Apportez ce rapport lors de votre consultation."
                    : "Si ces difficultés impactent votre quotidien, une consultation pourrait être utile pour explorer les causes possibles."}
            </div>
        </div>

        <div class="result-card ${asrsLevel}">
            <h3>1. ASRS v1.1 — Dépistage OMS</h3>
            <div class="result-status ${asrsLevel}">
                Seuil ${results.asrs.screeningPositive ? 'atteint' : 'non atteint'}
                (${results.asrs.partAShaded}/6 critères, seuil ≥4)
            </div>
            <div class="scores-grid">
                <div class="score-item">
                    <span class="score-label">Partie A</span>
                    <span class="score-value">${results.asrs.partAScore}/24</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Partie B</span>
                    <span class="score-value">${results.asrs.partBScore}/48</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Total</span>
                    <span class="score-value">${results.asrs.total}/72</span>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label-row">
                    <span>Inattention</span>
                    <span>${results.asrs.inattention}/36</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: ${Math.round(results.asrs.inattention / 36 * 100)}%"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label-row">
                    <span>Hyperactivité/Impulsivité</span>
                    <span>${results.asrs.hyperactivity}/36</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: ${Math.round(results.asrs.hyperactivity / 36 * 100)}%"></div>
                </div>
            </div>
        </div>

        <div class="result-card ${divaLevel}">
            <h3>2. Critères DSM-5</h3>
            <div class="result-status ${divaLevel}">
                ${results.diva.presentation}
            </div>
            <div class="scores-grid">
                <div class="score-item">
                    <span class="score-label">Inattention (A1)</span>
                    <span class="score-value">${results.diva.inattentionCount}/9</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Hyperactivité (A2)</span>
                    <span class="score-value">${results.diva.hyperactivityCount}/9</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Enfance (B)</span>
                    <span class="score-value">${results.diva.childhoodPositive ? '✓' : '✗'}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Retentissement</span>
                    <span class="score-value">${results.diva.impairmentDomains.length}/5</span>
                </div>
            </div>
            ${results.diva.impairmentDomains.length > 0 ? `
                <p class="interpretation">Domaines impactés: ${results.diva.impairmentDomains.join(', ')}</p>
            ` : ''}
        </div>

        <div class="result-card ${efLevel}">
            <h3>3. Fonctions Exécutives</h3>
            <div class="result-status ${efLevel}">
                Niveau de difficulté: ${results.executive.severity} (${results.executive.percentage}%)
            </div>
            ${Object.entries(results.executive.clusterScores).map(([name, s]) => `
                <div class="progress-item">
                    <div class="progress-label-row">
                        <span>${name}</span>
                        <span>${s.score}/${s.max}</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill ${s.percentage >= 50 ? 'high' : ''}" style="width: ${s.percentage}%"></div>
                    </div>
                </div>
            `).join('')}
            ${results.executive.impaired.length > 0 ? `
                <p class="interpretation">Domaines les plus impactés: ${results.executive.impaired.join(', ')}</p>
            ` : ''}
        </div>
    `;

    container.innerHTML = html;
}

// ============================================
// PDF GENERATION
// ============================================

function generatePDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const results = state.results;
    const now = new Date().toLocaleString('fr-FR');

    let y = 20;
    const margin = 20;
    const pageWidth = doc.internal.pageSize.width;

    // Helper functions
    const addTitle = (text, size = 16) => {
        doc.setFontSize(size);
        doc.setFont(undefined, 'bold');
        doc.text(text, margin, y);
        y += size * 0.5;
    };

    const addText = (text, size = 11) => {
        doc.setFontSize(size);
        doc.setFont(undefined, 'normal');
        const lines = doc.splitTextToSize(text, pageWidth - 2 * margin);
        doc.text(lines, margin, y);
        y += lines.length * size * 0.4 + 2;
    };

    const addLine = () => {
        doc.setDrawColor(200);
        doc.line(margin, y, pageWidth - margin, y);
        y += 5;
    };

    const checkPage = (needed = 30) => {
        if (y + needed > 280) {
            doc.addPage();
            y = 20;
        }
    };

    // Title
    addTitle('Rapport d\'Auto-Évaluation TDAH Adulte', 18);
    y += 5;
    addText(`Généré le ${now}`);
    addLine();

    // Disclaimer
    doc.setFillColor(255, 243, 205);
    doc.rect(margin, y, pageWidth - 2 * margin, 25, 'F');
    y += 5;
    doc.setFontSize(9);
    doc.setFont(undefined, 'bold');
    doc.text('AVERTISSEMENT', margin + 2, y);
    y += 4;
    doc.setFont(undefined, 'normal');
    const disclaimer = 'Ce document est un outil d\'AUTO-ÉVALUATION et NE CONSTITUE PAS un diagnostic médical. Seul un professionnel de santé qualifié peut établir un diagnostic de TDAH.';
    const disclaimerLines = doc.splitTextToSize(disclaimer, pageWidth - 2 * margin - 4);
    doc.text(disclaimerLines, margin + 2, y);
    y += 20;

    // Summary
    checkPage(50);
    addTitle('Synthèse des Résultats', 14);
    y += 3;
    addText(`${results.global.positiveIndicators}/3 outils suggèrent des symptômes ${results.global.positiveIndicators >= 2 ? 'évocateurs, méritant une évaluation clinique' : 'à explorer si besoin'}.`);

    if (results.asrs.screeningPositive) addText('• ASRS: Seuil de dépistage atteint');
    if (results.diva.meetsInattention || results.diva.meetsHyperactivity)
        addText(`• Critères DSM-5: ${results.diva.presentation}`);
    if (results.executive.severity !== 'Faible')
        addText(`• Fonctions exécutives: Difficultés de niveau ${results.executive.severity}`);
    y += 5;
    addLine();

    // ASRS Results
    checkPage(40);
    addTitle('1. ASRS v1.1 (OMS/Harvard)', 12);
    addText(`Seuil: ${results.asrs.screeningPositive ? 'Atteint' : 'Non atteint'} (${results.asrs.partAShaded}/6 critères)`);
    addText(`Score total: ${results.asrs.total}/72 | Inattention: ${results.asrs.inattention}/36 | Hyperactivité: ${results.asrs.hyperactivity}/36`);
    y += 3;

    // DIVA Results
    checkPage(40);
    addTitle('2. Critères DSM-5', 12);
    addText(`Présentation: ${results.diva.presentation}`);
    addText(`Inattention: ${results.diva.inattentionCount}/9 | Hyperactivité: ${results.diva.hyperactivityCount}/9`);
    addText(`Enfance: ${results.diva.childhoodPositive ? 'Confirmé' : 'Non confirmé'} | Retentissement: ${results.diva.impairmentDomains.length} domaines`);
    y += 3;

    // Executive Functions
    checkPage(50);
    addTitle('3. Fonctions Exécutives', 12);
    addText(`Niveau global: ${results.executive.severity} (${results.executive.percentage}%)`);
    Object.entries(results.executive.clusterScores).forEach(([name, s]) => {
        addText(`  • ${name}: ${s.score}/${s.max} (${s.percentage}%)`);
    });

    // New page for detailed responses
    doc.addPage();
    y = 20;
    addTitle('Annexe: Réponses Détaillées', 14);
    addLine();

    // ASRS responses
    addTitle('ASRS v1.1', 11);
    [...ASRS_QUESTIONS.part_a, ...ASRS_QUESTIONS.part_b].forEach((q, i) => {
        checkPage(15);
        const val = state.responses[q.id];
        const label = ASRS_OPTIONS.find(o => o.value === val)?.label || 'Non répondu';
        doc.setFontSize(9);
        const qText = doc.splitTextToSize(`${i + 1}. ${q.text}`, pageWidth - 2 * margin - 40);
        doc.text(qText, margin, y);
        doc.text(label, pageWidth - margin - 30, y);
        y += qText.length * 4 + 2;
    });

    // DIVA responses
    checkPage(20);
    addTitle('Critères DSM-5', 11);
    [...DIVA_INATTENTION, ...DIVA_HYPERACTIVITY, ...DIVA_CHILDHOOD, ...DIVA_IMPAIRMENT].forEach((q, i) => {
        checkPage(12);
        const val = state.responses[q.id];
        doc.setFontSize(9);
        const qText = doc.splitTextToSize(`${q.text}`, pageWidth - 2 * margin - 20);
        doc.text(qText, margin, y);
        doc.text(val === 1 ? 'Oui' : 'Non', pageWidth - margin - 15, y);
        y += qText.length * 4 + 2;
    });

    // References page
    doc.addPage();
    y = 20;
    addTitle('Références Scientifiques', 14);
    addLine();
    doc.setFontSize(10);
    addText('1. Kessler RC, et al. (2005). The World Health Organization Adult ADHD Self-Report Scale (ASRS).');
    addText('   Psychological Medicine, 35(2), 245-256. https://pubmed.ncbi.nlm.nih.gov/15841682/');
    y += 3;
    addText('2. American Psychiatric Association (2013). Diagnostic and Statistical Manual of Mental Disorders (5th ed.).');
    addText('   https://www.psychiatry.org/psychiatrists/practice/dsm');
    y += 3;
    addText('3. Kooij JJS, et al. (2010). DIVA 2.0: Diagnostic Interview for ADHD in Adults.');
    addText('   DIVA Foundation. https://www.divacenter.eu/');
    y += 3;
    addText('4. Brown TE (2013). A New Understanding of ADHD in Children and Adults.');
    addText('   Executive Function Impairments. Routledge. https://pubmed.ncbi.nlm.nih.gov/24232170/');

    // Footer on each page
    const pageCount = doc.internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(128);
        doc.text(`Page ${i}/${pageCount} | Ce document ne constitue pas un diagnostic médical`, margin, 290);
    }

    doc.save('evaluation_tdah.pdf');
}

// ============================================
// VALIDATION
// ============================================

function validateSection(section) {
    let questions = [];

    if (section === 'asrs') {
        questions = [...ASRS_QUESTIONS.part_a, ...ASRS_QUESTIONS.part_b].map(q => q.id);
    } else if (section === 'diva') {
        questions = [
            ...DIVA_INATTENTION, ...DIVA_HYPERACTIVITY,
            ...DIVA_CHILDHOOD, ...DIVA_IMPAIRMENT
        ].map(q => q.id);
    } else if (section === 'executive') {
        questions = Object.values(EXEC_FUNCTIONS).flatMap(c => c.questions.map(q => q.id));
    }

    const answered = questions.filter(id => state.responses[id] !== undefined).length;
    return answered === questions.length;
}

// ============================================
// EVENT HANDLERS
// ============================================

function init() {
    // Render all questionnaires
    renderASRS();
    renderDIVA();
    renderExecutive();

    // Consent checkbox
    document.getElementById('consent').addEventListener('change', (e) => {
        document.getElementById('start-btn').disabled = !e.target.checked;
    });

    // Navigation buttons
    document.getElementById('start-btn').addEventListener('click', () => showSection('asrs'));

    document.getElementById('asrs-next').addEventListener('click', () => {
        if (!validateSection('asrs')) {
            alert('Veuillez répondre à toutes les questions avant de continuer.');
            return;
        }
        showSection('diva');
    });

    document.getElementById('diva-back').addEventListener('click', () => showSection('asrs'));
    document.getElementById('diva-next').addEventListener('click', () => {
        if (!validateSection('diva')) {
            alert('Veuillez répondre à toutes les questions avant de continuer.');
            return;
        }
        showSection('executive');
    });

    document.getElementById('exec-back').addEventListener('click', () => showSection('diva'));
    document.getElementById('exec-next').addEventListener('click', () => {
        if (!validateSection('executive')) {
            alert('Veuillez répondre à toutes les questions avant de continuer.');
            return;
        }
        renderResults();
        showSection('results');
    });

    document.getElementById('download-pdf').addEventListener('click', generatePDF);
    document.getElementById('restart').addEventListener('click', () => {
        state.responses = {};
        state.results = null;
        renderASRS();
        renderDIVA();
        renderExecutive();
        showSection('home');
    });

    // Initialize
    showSection('home');
}

// Start app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
