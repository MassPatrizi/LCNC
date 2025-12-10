#!/usr/bin/env python3.11
"""
SAP Cloud Application Programming Model Quiz Application - Web Version
App web interattiva per memorizzare le domande del quiz SAP CAP
Ottimizzata per mobile e desktop
"""

import streamlit as st
import json
import random
from pathlib import Path

# Configurazione pagina
st.set_page_config(
    page_title="SAP CAP Quiz",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS per tema scuro e mobile-friendly
st.markdown("""
<style>
    /* Tema scuro */
    .stApp {
        background-color: #121212;
    }
    
    /* Header personalizzato */
    .main-header {
        background: linear-gradient(135deg, #0d1117 0%, #1a1a1a 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        color: #8b949e;
        font-size: 1rem;
    }
    
    /* Card personalizzate */
    .quiz-card {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #30363d;
    }
    
    .memory-card {
        background-color: #2d2d2d;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #f1c40f;
    }
    
    .stats-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #30363d;
    }
    
    /* Pulsanti personalizzati */
    .stButton > button {
        width: 100%;
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #2ea043;
        transform: translateY(-2px);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.5rem;
        }
        .quiz-card {
            padding: 1rem;
        }
    }
    
    /* Nascondi elementi Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_quiz_data():
    """Carica il file JSON con le domande"""
    quiz_file = Path("sap_quiz_data.json")
    
    if quiz_file.exists():
        try:
            with open(quiz_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error("File JSON non valido!")
            return []
    else:
        st.error("File sap_quiz_data.json non trovato!")
        return []


def init_session_state():
    """Inizializza lo stato della sessione"""
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'shuffle_mode' not in st.session_state:
        st.session_state.shuffle_mode = False
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'question_answered_correctly' not in st.session_state:
        st.session_state.question_answered_correctly = {}
    if 'shuffled_quiz' not in st.session_state:
        st.session_state.shuffled_quiz = []
    if 'show_memory_help' not in st.session_state:
        st.session_state.show_memory_help = False
    if 'show_result_dialog' not in st.session_state:
        st.session_state.show_result_dialog = False
    if 'last_answer_correct' not in st.session_state:
        st.session_state.last_answer_correct = False
    if 'last_correct_answer_text' not in st.session_state:
        st.session_state.last_correct_answer_text = ""
    if 'shuffled_options' not in st.session_state:
        st.session_state.shuffled_options = {}


def get_shuffled_options(question_index):
    """Ottiene le opzioni mischiate per una domanda, creandole se non esistono"""
    if question_index not in st.session_state.shuffled_options:
        current_q = st.session_state.shuffled_quiz[question_index]
        num_options = len(current_q['options'])
        
        # Crea una lista di indici e la mescola
        shuffled_indices = list(range(num_options))
        random.shuffle(shuffled_indices)
        
        st.session_state.shuffled_options[question_index] = shuffled_indices
    
    return st.session_state.shuffled_options[question_index]


def start_quiz(shuffle=False):
    """Avvia il quiz"""
    st.session_state.quiz_started = True
    st.session_state.shuffle_mode = shuffle
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = {}
    st.session_state.question_answered_correctly = {}
    st.session_state.show_memory_help = False
    st.session_state.shuffled_options = {}
    
    quiz_data = load_quiz_data()
    if shuffle:
        st.session_state.shuffled_quiz = quiz_data.copy()
        random.shuffle(st.session_state.shuffled_quiz)
    else:
        st.session_state.shuffled_quiz = quiz_data.copy()


def reset_quiz():
    """Resetta il quiz e torna alla home"""
    st.session_state.quiz_started = False
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = {}
    st.session_state.question_answered_correctly = {}
    st.session_state.show_memory_help = False
    st.session_state.shuffled_options = {}


def check_answer(user_answer, correct_answer, is_multiple):
    """Verifica se la risposta è corretta"""
    if is_multiple:
        user_sorted = sorted(user_answer)
        correct_sorted = sorted(correct_answer)
        return user_sorted == correct_sorted
    else:
        return user_answer == correct_answer


def update_score(is_correct, question_index):
    """Aggiorna lo score considerando se la domanda era già stata risposta"""
    was_correct = st.session_state.question_answered_correctly.get(question_index, False)
    
    if is_correct and not was_correct:
        # Era sbagliata, ora è corretta: incrementa
        st.session_state.score += 1
    elif not is_correct and was_correct:
        # Era corretta, ora è sbagliata: decrementa
        st.session_state.score -= 1
    
    st.session_state.question_answered_correctly[question_index] = is_correct


@st.dialog("Risultato Risposta", width="large")
def show_result_popup():
    """Mostra popup con risultato e aiuto"""
    current_q = st.session_state.shuffled_quiz[st.session_state.current_question_index]
    total_questions = len(st.session_state.shuffled_quiz)
    is_last_question = st.session_state.current_question_index >= total_questions - 1
    
    if st.session_state.last_answer_correct:
        st.success("### ✓ Risposta Esatta!")
    else:
        st.error("### ✕ Risposta Sbagliata!")
        st.markdown(f"**Risposta corretta:**")
        st.info(st.session_state.last_correct_answer_text)
    
    st.markdown("---")
    st.markdown("### 💡 Aiuto Memoria")
    st.warning(current_q['memory_technique'])
    st.markdown("---")
    
    # Pulsante per continuare
    if is_last_question:
        if st.button("🏁 Vai ai Risultati Finali", use_container_width=True, type="primary"):
            st.session_state.show_result_dialog = False
            st.session_state.current_question_index += 1
            st.rerun()
    else:
        if st.button("→ Prossima Domanda", use_container_width=True, type="primary"):
            st.session_state.show_result_dialog = False
            st.session_state.current_question_index += 1
            st.session_state.show_memory_help = False
            st.rerun()


def show_home_page():
    """Mostra la home page"""
    quiz_data = load_quiz_data()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">SAP CAP Practice Quiz</div>
        <div class="main-subtitle">SAP Certified Associate - Backend Developer - SAP Cloud Application Programming Model</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Scegli la modalità di studio")
    st.markdown("---")
    
    # Due colonne per le card
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="quiz-card" style="text-align: center;">
            <h2 style="color: #e0e0e0; margin-bottom: 1rem;">📋 Ordine Normale</h2>
            <p style="color: #b0b0b0;">Domande in ordine sequenziale<br>(dalla 1 alla 80)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Inizia Quiz", key="normal_btn", use_container_width=True):
            start_quiz(shuffle=False)
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="quiz-card" style="text-align: center;">
            <h2 style="color: #e0e0e0; margin-bottom: 1rem;">🎲 Ordine Casuale</h2>
            <p style="color: #b0b0b0;">Domande in ordine casuale<br>(per una sfida maggiore)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Inizia Quiz", key="random_btn", use_container_width=True):
            start_quiz(shuffle=True)
            st.rerun()
    
    st.markdown(f"<p style='text-align: center; color: #8b949e; margin-top: 2rem;'>Totale domande disponibili: {len(quiz_data)}</p>", unsafe_allow_html=True)


def show_quiz():
    """Mostra il quiz"""
    if not st.session_state.shuffled_quiz:
        st.error("Nessuna domanda disponibile!")
        return
    
    total_questions = len(st.session_state.shuffled_quiz)
    current_q = st.session_state.shuffled_quiz[st.session_state.current_question_index]
    is_multiple = isinstance(current_q['correct'], list)
    
    # Header con statistiche
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <p style="color: #58a6ff; font-weight: bold; margin: 0;">
                Domanda {st.session_state.current_question_index + 1} / {total_questions}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <p style="color: #3fb950; font-weight: bold; margin: 0;">
                Score: {st.session_state.score} / {total_questions}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            reset_quiz()
            st.rerun()
    
    # Barra di progresso
    progress = ((st.session_state.current_question_index + 1) / total_questions) * 100
    st.progress(progress / 100)
    
    # Card domanda
    st.markdown(f"""
    <div class="quiz-card">
        <p style="color: #8b949e; font-size: 0.9rem; margin-bottom: 0.5rem;">Domanda</p>
        <h3 style="color: #e0e0e0; margin-top: 0;">Q{current_q['id']}: {current_q['question']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Ottieni l'ordine shuffled delle opzioni
    shuffled_indices = get_shuffled_options(st.session_state.current_question_index)
    
    # Opzioni di risposta
    if is_multiple:
        # Multiple choice
        selected_options = []
        
        for display_idx, original_idx in enumerate(shuffled_indices):
            option = current_q['options'][original_idx]
            
            # Ripristina selezioni salvate (usando indici originali)
            saved_answer = st.session_state.user_answers.get(st.session_state.current_question_index, [])
            checked = original_idx in saved_answer
            
            if st.checkbox(option, key=f"option_{display_idx}", value=checked):
                if original_idx not in selected_options:
                    selected_options.append(original_idx)
            else:
                if original_idx in selected_options:
                    selected_options.remove(original_idx)
        
        st.session_state.user_answers[st.session_state.current_question_index] = selected_options.copy()
    else:
        # Single choice
        saved_answer = st.session_state.user_answers.get(st.session_state.current_question_index, None)
        
        # Trova l'indice di display dell'opzione salvata
        saved_display_index = None
        if saved_answer is not None:
            saved_display_index = shuffled_indices.index(saved_answer)
        
        selected_display_idx = st.radio(
            "Seleziona una risposta:",
            options=range(len(shuffled_indices)),
            format_func=lambda x: current_q['options'][shuffled_indices[x]],
            key="radio_answer",
            index=saved_display_index if saved_display_index is not None else 0
        )
        
        # Salva l'indice originale (non quello shuffled)
        selected_original_idx = shuffled_indices[selected_display_idx]
        st.session_state.user_answers[st.session_state.current_question_index] = selected_original_idx
    
    # Mostra il dialog se necessario
    if st.session_state.show_result_dialog:
        show_result_popup()
    
    # Pulsanti di navigazione
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.current_question_index > 0:
            if st.button("← Precedente", use_container_width=True):
                st.session_state.current_question_index -= 1
                st.session_state.show_memory_help = False
                st.rerun()
        else:
            st.button("← Precedente", disabled=True, use_container_width=True)
    
    with col2:
        if st.button("✓ Invia", use_container_width=True, type="primary"):
            user_answer = st.session_state.user_answers.get(st.session_state.current_question_index)
            correct_answer = current_q['correct']
            
            if user_answer is None or (is_multiple and len(user_answer) == 0):
                st.warning("Seleziona almeno una risposta!")
            else:
                is_correct = check_answer(user_answer, correct_answer, is_multiple)
                update_score(is_correct, st.session_state.current_question_index)
                
                # Prepara i dati per il popup
                st.session_state.last_answer_correct = is_correct
                
                if not is_correct:
                    if is_multiple:
                        correct_options = [current_q['options'][i] for i in correct_answer]
                        st.session_state.last_correct_answer_text = "\n".join([f"• {opt}" for opt in correct_options])
                    else:
                        st.session_state.last_correct_answer_text = current_q['options'][correct_answer]
                
                # Apri il dialog
                st.session_state.show_result_dialog = True
                st.rerun()
    
    with col3:
        if st.button("✕ Esci", use_container_width=True):
            reset_quiz()
            st.rerun()


def show_final_score():
    """Mostra il punteggio finale"""
    total_questions = len(st.session_state.shuffled_quiz)
    percentage = (st.session_state.score / total_questions) * 100
    
    # Determina il messaggio in base al punteggio
    if percentage >= 90:
        emoji = "🎉"
        message_type = "Eccellente!"
    elif percentage >= 70:
        emoji = "👍"
        message_type = "Ottimo lavoro!"
    elif percentage >= 50:
        emoji = "📚"
        message_type = "Buon lavoro!"
    else:
        emoji = "💪"
        message_type = "Continua a studiare!"
    
    st.markdown(f"""
    <div class="quiz-card" style="text-align: center;">
        <h2 style="color: #e0e0e0;">{emoji} {message_type}</h2>
        <h3 style="color: #3fb950;">Quiz Completato!</h3>
        <p style="color: #b0b0b0; font-size: 1.2rem;">
            Punteggio Finale: <strong style="color: #e0e0e0;">{st.session_state.score} / {total_questions}</strong><br>
            Percentuale: <strong style="color: #e0e0e0;">{percentage:.1f}%</strong>
        </p>
        <p style="color: #8b949e;">
            Risposte Corrette: {st.session_state.score}<br>
            Risposte Sbagliate: {total_questions - st.session_state.score}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Ricominciare", use_container_width=True):
            start_quiz(shuffle=st.session_state.shuffle_mode)
            st.rerun()
    
    with col2:
        if st.button("🏠 Torna alla Home", use_container_width=True):
            reset_quiz()
            st.rerun()


def main():
    """Funzione principale"""
    init_session_state()
    
    if not st.session_state.quiz_started:
        show_home_page()
    else:
        if st.session_state.current_question_index >= len(st.session_state.shuffled_quiz):
            show_final_score()
        else:
            show_quiz()


if __name__ == "__main__":
    main()

