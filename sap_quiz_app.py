#!/usr/bin/env python3.11
"""
SAP Build C_LCNC_2406 Quiz Application
App interattiva per memorizzare le 60 domande del quiz SAP Build
Con interfaccia Tkinter moderna, pulsante AIUTO, e feedback istantaneo
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
from pathlib import Path


class ModernButton(tk.Frame):
    """Pulsante moderno con effetti hover - compatibile macOS"""
    def __init__(self, parent, text="", command=None, **kwargs):
        self.default_bg = kwargs.pop('bg', '#3498db')
        self.hover_bg = kwargs.pop('hover_bg', self._lighten_color(self.default_bg))
        self.default_fg = kwargs.pop('fg', 'white')
        default_font = kwargs.pop('font', ("SF Pro Display", 11, "bold"))
        default_padx = kwargs.pop('padx', 20)
        default_pady = kwargs.pop('pady', 12)
        self.command = command
        
        super().__init__(parent, bg=self.default_bg, relief=tk.FLAT, bd=0)
        
        self.label = tk.Label(
            self,
            text=text,
            bg=self.default_bg,
            fg=self.default_fg,
            font=default_font,
            cursor="hand2",
            padx=default_padx,
            pady=default_pady
        )
        self.label.pack()
        
        # Bind events
        self.label.bind("<Button-1>", self._on_click)
        self.label.bind("<Enter>", self._on_enter)
        self.label.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_click(self, e):
        if self.command:
            self.command()
    
    def _on_enter(self, e):
        self.config(bg=self.hover_bg)
        self.label.config(bg=self.hover_bg, fg=self.default_fg)
    
    def _on_leave(self, e):
        self.config(bg=self.default_bg)
        self.label.config(bg=self.default_bg, fg=self.default_fg)
    
    @staticmethod
    def _lighten_color(color):
        """Schiarisce un colore hex"""
        color_map = {
            '#d68910': '#f39c12',  # Arancione più scuro
            '#1e8449': '#27ae60',  # Verde più scuro
            '#2874a6': '#3498db',  # Blu più scuro
            '#c0392b': '#e74c3c',  # Rosso più scuro
            '#9b59b6': '#bb8fce',
            '#1a237e': '#283593',  # Blu scuro header
            '#1565c0': '#1976d2',  # Blu scuro casuale
        }
        return color_map.get(color, color)


class HomePage:
    """Schermata iniziale per scegliere la modalità di quiz"""
    def __init__(self, root, quiz_data, start_quiz_callback):
        self.root = root
        self.quiz_data = quiz_data
        self.start_quiz_callback = start_quiz_callback
        self.setup_home_ui()
    
    def setup_home_ui(self):
        """Crea l'interfaccia della home page responsive"""
        # Pulisci la finestra
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg="#121212")
        
        # Verifica se è mobile
        is_mobile = self.root.winfo_width() < 600
        
        # Dimensioni responsive
        header_height = 90 if is_mobile else 120
        title_font = 20 if is_mobile else 26
        subtitle_font = 11 if is_mobile else 14
        welcome_font = 16 if is_mobile else 18
        card_title_font = 16 if is_mobile else 18
        card_desc_font = 11 if is_mobile else 12
        icon_font = 36 if is_mobile else 48
        container_padx = 15 if is_mobile else 40
        container_pady = 20 if is_mobile else 50
        card_padx = 10 if is_mobile else 20
        card_inner_padx = 15 if is_mobile else 30
        card_inner_pady = 20 if is_mobile else 40
        
        # Header
        header_frame = tk.Frame(self.root, bg="#0d1117", height=header_height)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="SAP Build Practice Quiz",
            font=("SF Pro Display", title_font, "bold"),
            bg="#0d1117",
            fg="#ffffff"
        )
        title_label.pack(pady=(15 if is_mobile else 25, 5 if is_mobile else 8))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Certificazione C_LCNC_2406",
            font=("SF Pro Display", subtitle_font),
            bg="#0d1117",
            fg="#8b949e"
        )
        subtitle_label.pack()
        
        # Container principale
        main_container = tk.Frame(self.root, bg="#121212")
        main_container.pack(fill=tk.BOTH, expand=True, padx=container_padx, pady=container_pady)
        
        # Titolo sezione
        welcome_label = tk.Label(
            main_container,
            text="Scegli la modalità di studio",
            font=("SF Pro Display", welcome_font, "bold"),
            bg="#121212",
            fg="#e0e0e0"
        )
        welcome_label.pack(pady=(10 if is_mobile else 20, 20 if is_mobile else 40))
        
        # Frame per i pulsanti di scelta - verticale su mobile
        buttons_frame = tk.Frame(main_container, bg="#121212")
        buttons_frame.pack(expand=True, fill=tk.BOTH)
        
        if is_mobile:
            # Layout verticale per mobile
            buttons_frame.columnconfigure(0, weight=1)
            buttons_frame.rowconfigure(0, weight=1)
            buttons_frame.rowconfigure(1, weight=1)
            card_padx = 0
            card_pady = 10
        else:
            # Layout orizzontale per desktop
            card_pady = 0
        
        # Pulsante Ordine Normale
        normal_card = tk.Frame(buttons_frame, bg="#1e1e1e", relief=tk.FLAT, bd=0)
        if is_mobile:
            normal_card.grid(row=0, column=0, sticky="nsew", padx=card_padx, pady=card_pady)
        else:
            normal_card.pack(side=tk.LEFT, padx=card_padx, fill=tk.BOTH, expand=True)
        
        normal_inner = tk.Frame(normal_card, bg="#1e1e1e")
        normal_inner.pack(padx=card_inner_padx, pady=card_inner_pady)
        
        normal_icon = tk.Label(
            normal_inner,
            text="📋",
            font=("SF Pro Display", icon_font),
            bg="#1e1e1e"
        )
        normal_icon.pack(pady=(0, 10 if is_mobile else 15))
        
        normal_title = tk.Label(
            normal_inner,
            text="Ordine Normale",
            font=("SF Pro Display", card_title_font, "bold"),
            bg="#1e1e1e",
            fg="#e0e0e0"
        )
        normal_title.pack(pady=(0, 8 if is_mobile else 10))
        
        normal_desc = tk.Label(
            normal_inner,
            text="Domande in ordine sequenziale\n(dalla 1 alla 60)",
            font=("SF Pro Display", card_desc_font),
            bg="#1e1e1e",
            fg="#b0b0b0",
            justify=tk.CENTER
        )
        normal_desc.pack(pady=(0, 15 if is_mobile else 20))
        
        normal_btn = ModernButton(
            normal_inner,
            text="Inizia Quiz",
            command=lambda: self.start_quiz(shuffle=False),
            bg="#238636",
            hover_bg="#2ea043",
            fg="white",
            font=("SF Pro Display", 12 if is_mobile else 13, "bold"),
            padx=25 if is_mobile else 30,
            pady=12 if is_mobile else 15
        )
        normal_btn.pack()
        
        # Pulsante Ordine Casuale
        random_card = tk.Frame(buttons_frame, bg="#1e1e1e", relief=tk.FLAT, bd=0)
        if is_mobile:
            random_card.grid(row=1, column=0, sticky="nsew", padx=card_padx, pady=card_pady)
        else:
            random_card.pack(side=tk.LEFT, padx=card_padx, fill=tk.BOTH, expand=True)
        
        random_inner = tk.Frame(random_card, bg="#1e1e1e")
        random_inner.pack(padx=card_inner_padx, pady=card_inner_pady)
        
        random_icon = tk.Label(
            random_inner,
            text="🎲",
            font=("SF Pro Display", icon_font),
            bg="#1e1e1e"
        )
        random_icon.pack(pady=(0, 10 if is_mobile else 15))
        
        random_title = tk.Label(
            random_inner,
            text="Ordine Casuale",
            font=("SF Pro Display", card_title_font, "bold"),
            bg="#1e1e1e",
            fg="#e0e0e0"
        )
        random_title.pack(pady=(0, 8 if is_mobile else 10))
        
        random_desc = tk.Label(
            random_inner,
            text="Domande in ordine casuale\n(per una sfida maggiore)",
            font=("SF Pro Display", card_desc_font),
            bg="#1e1e1e",
            fg="#b0b0b0",
            justify=tk.CENTER
        )
        random_desc.pack(pady=(0, 15 if is_mobile else 20))
        
        random_btn = ModernButton(
            random_inner,
            text="Inizia Quiz",
            command=lambda: self.start_quiz(shuffle=True),
            bg="#1f6feb",
            hover_bg="#2c7fe8",
            fg="white",
            font=("SF Pro Display", 12 if is_mobile else 13, "bold"),
            padx=25 if is_mobile else 30,
            pady=12 if is_mobile else 15
        )
        random_btn.pack()
        
        # Info footer
        info_label = tk.Label(
            main_container,
            text=f"Totale domande disponibili: {len(self.quiz_data)}",
            font=("SF Pro Display", 10 if is_mobile else 11),
            bg="#121212",
            fg="#8b949e"
        )
        info_label.pack(pady=(20 if is_mobile else 40, 0))
    
    def start_quiz(self, shuffle=False):
        """Avvia il quiz con la modalità selezionata"""
        self.start_quiz_callback(shuffle)


class SAPBuildQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("SAP Build Quiz - C_LCNC_2406")
        
        # Dimensioni responsive - si adatta allo schermo
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calcola dimensioni ottimali (minimo 320px per mobile, massimo 1200px)
        if screen_width < 600:
            # Modalità mobile/tablet piccolo
            width = min(screen_width - 20, 600)
            height = min(screen_height - 50, 900)
        else:
            # Modalità desktop
            width = min(1000, screen_width - 100)
            height = min(750, screen_height - 100)
        
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg="#121212")
        self.root.minsize(320, 500)  # Dimensione minima per mobile
        
        # Abilita il ridimensionamento
        self.root.resizable(True, True)
        
        # Centra la finestra
        self.center_window()
        
        # Bind per aggiornare il layout quando la finestra viene ridimensionata
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Carica il database delle domande
        self.quiz_data = self.load_quiz_data()
        if not self.quiz_data:
            return
        
        # Mostra la home page
        self.home_page = HomePage(self.root, self.quiz_data, self.start_quiz)
    
    def start_quiz(self, shuffle=False):
        """Inizia il quiz con la modalità selezionata"""
        self.current_question_index = 0
        self.score = 0
        self.total_questions = len(self.quiz_data)
        self.answered_correctly = set()
        self.show_memory_help = False
        
        # Dizionari per salvare le risposte dell'utente e lo stato delle domande
        self.user_answers = {}  # {question_index: risposta_utente}
        self.question_answered_correctly = {}  # {question_index: True/False}
        
        # Prepara le domande in base alla modalità
        if shuffle:
            self.shuffled_quiz = self.quiz_data.copy()
            random.shuffle(self.shuffled_quiz)
        else:
            self.shuffled_quiz = self.quiz_data.copy()
        
        self.setup_ui()
        self.load_question()
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_window_resize(self, event):
        """Aggiorna il layout quando la finestra viene ridimensionata"""
        if hasattr(self, 'question_label') and self.question_label.winfo_exists():
            # Aggiorna wraplength basato sulla larghezza corrente
            current_width = self.root.winfo_width()
            wraplength = max(300, current_width - 100)  # Minimo 300px, lascia margini
            self.question_label.config(wraplength=wraplength)
            if hasattr(self, 'memory_label'):
                self.memory_label.config(wraplength=wraplength)
    
    def is_mobile_size(self):
        """Verifica se la finestra è in modalità mobile"""
        return self.root.winfo_width() < 600
    
    def load_quiz_data(self):
        """Carica il file JSON con le domande"""
        quiz_file = Path("sap_quiz_data.json")
        
        if quiz_file.exists():
            try:
                with open(quiz_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Errore", "File JSON non valido!")
                self.root.destroy()
                return []
        else:
            messagebox.showerror("Errore", "File sap_quiz_data.json non trovato!")
            self.root.destroy()
            return []
    
    def setup_ui(self):
        """Crea l'interfaccia utente moderna e responsive"""
        # Pulisci la finestra
        for widget in self.root.winfo_children():
            widget.destroy()
        
        is_mobile = self.is_mobile_size()
        
        # Dimensioni responsive
        header_height = 80 if is_mobile else 100
        title_font_size = 18 if is_mobile else 22
        subtitle_font_size = 10 if is_mobile else 12
        question_font_size = 13 if is_mobile else 15
        button_padx = 4 if is_mobile else 8
        button_pady = 10 if is_mobile else 12
        container_padx = 10 if is_mobile else 20
        container_pady = 10 if is_mobile else 25
        
        # Calcola wraplength dinamico
        current_width = self.root.winfo_width()
        wraplength = max(280, current_width - container_padx * 2 - 50)
        
        # Header con gradiente simulato
        header_frame = tk.Frame(self.root, bg="#0d1117", height=header_height)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Titolo principale
        title_label = tk.Label(
            header_frame,
            text="SAP Build Practice Quiz",
            font=("SF Pro Display", title_font_size, "bold"),
            bg="#0d1117",
            fg="white"
        )
        title_label.pack(pady=(10 if is_mobile else 15, 3 if is_mobile else 5))
        
        # Sottotitolo
        subtitle_label = tk.Label(
            header_frame,
            text="Certificazione C_LCNC_2406",
            font=("SF Pro Display", subtitle_font_size),
            bg="#0d1117",
            fg="#8b949e"
        )
        subtitle_label.pack()
        
        # Frame per statistiche
        stats_frame = tk.Frame(self.root, bg="#1e1e1e", relief=tk.FLAT)
        stats_frame.pack(fill=tk.X, padx=container_padx, pady=(10, 8))
        
        # Contatore domanda
        self.counter_label = tk.Label(
            stats_frame,
            text=f"Domanda 1 / {self.total_questions}",
            font=("SF Pro Display", 11 if is_mobile else 13, "bold"),
            bg="#1e1e1e",
            fg="#58a6ff"
        )
        self.counter_label.pack(side=tk.LEFT, padx=(10 if is_mobile else 20), pady=8)
        
        # Score
        self.score_label = tk.Label(
            stats_frame,
            text="Score: 0 / 0",
            font=("SF Pro Display", 11 if is_mobile else 13, "bold"),
            bg="#1e1e1e",
            fg="#3fb950"
        )
        self.score_label.pack(side=tk.RIGHT, padx=(10 if is_mobile else 20), pady=8)
        
        # Barra di progresso moderna
        progress_container = tk.Frame(self.root, bg="#121212")
        progress_container.pack(fill=tk.X, padx=container_padx, pady=(0, 10))
        
        progress_label = tk.Label(
            progress_container,
            text="Progresso",
            font=("SF Pro Display", 9 if is_mobile else 10),
            bg="#121212",
            fg="#8b949e"
        )
        progress_label.pack(anchor=tk.W, padx=(0, 5))
        
        self.progress_var = tk.DoubleVar()
        style = ttk.Style()
        style.theme_use('clam')
        progress_thickness = 20 if is_mobile else 25
        style.configure("Modern.Horizontal.TProgressbar",
                       background='#3fb950',
                       troughcolor='#21262d',
                       borderwidth=0,
                       lightcolor='#3fb950',
                       darkcolor='#3fb950',
                       thickness=progress_thickness)
        
        self.progress_bar = ttk.Progressbar(
            progress_container,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(3, 0))
        
        # Frame principale con card
        main_container = tk.Frame(self.root, bg="#121212")
        main_container.pack(fill=tk.BOTH, expand=True, padx=container_padx, pady=(0, 10))
        
        # Card per la domanda
        question_card = tk.Frame(main_container, bg="#1e1e1e", relief=tk.FLAT, bd=0)
        question_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Padding interno per la card
        question_inner = tk.Frame(question_card, bg="#1e1e1e")
        inner_padx = 15 if is_mobile else 25
        inner_pady = 15 if is_mobile else 25
        question_inner.pack(fill=tk.BOTH, expand=True, padx=inner_padx, pady=inner_pady)
        
        # Label "Domanda"
        question_header = tk.Label(
            question_inner,
            text="Domanda",
            font=("SF Pro Display", 10 if is_mobile else 11, "bold"),
            bg="#1e1e1e",
            fg="#8b949e"
        )
        question_header.pack(anchor=tk.W, pady=(0, 8))
        
        # Area della domanda
        self.question_label = tk.Label(
            question_inner,
            text="",
            font=("SF Pro Display", question_font_size),
            bg="#1e1e1e",
            fg="#e0e0e0",
            wraplength=wraplength,
            justify=tk.LEFT,
            anchor="w"
        )
        self.question_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Frame per le opzioni di risposta
        self.options_frame = tk.Frame(question_inner, bg="#1e1e1e")
        self.options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variabile per le risposte selezionate
        self.selected_answer = tk.StringVar()
        self.selected_answers = []  # Per multiple choice
        
        # Frame aiuto memoria (inizialmente nascosto)
        self.memory_card = tk.Frame(main_container, bg="#2d2d2d", relief=tk.FLAT, bd=0)
        self.memory_label = tk.Label(
            self.memory_card,
            text="",
            font=("SF Pro Display", 11 if is_mobile else 12, "italic"),
            bg="#2d2d2d",
            fg="#f1c40f",
            wraplength=wraplength,
            justify=tk.LEFT,
            anchor="w"
        )
        self.memory_label.pack(padx=inner_padx, pady=15, anchor=tk.W)
        
        # Frame inferiore con pulsanti
        button_container = tk.Frame(self.root, bg="#121212")
        button_container.pack(fill=tk.X, padx=container_padx, pady=(0, 10))
        
        # Pulsanti con stile moderno - layout verticale su mobile
        if is_mobile:
            # Layout verticale per mobile
            button_frame = tk.Frame(button_container, bg="#121212")
            button_frame.pack(fill=tk.X)
            
            # Prima riga
            row1 = tk.Frame(button_frame, bg="#121212")
            row1.pack(fill=tk.X, pady=2)
            
            self.prev_btn = ModernButton(
                row1,
                text="← Precedente",
                command=self.previous_question,
                bg="#6c757d",
                hover_bg="#868e96",
                fg="white",
                padx=15,
                pady=button_pady
            )
            self.prev_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            help_btn = ModernButton(
                row1,
                text="💡 AIUTO",
                command=self.show_memory_technique,
                bg="#d68910",
                hover_bg="#f39c12",
                fg="white",
                padx=15,
                pady=button_pady
            )
            help_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            # Seconda riga
            row2 = tk.Frame(button_frame, bg="#121212")
            row2.pack(fill=tk.X, pady=2)
            
            submit_btn = ModernButton(
                row2,
                text="✓ Invia",
                command=self.check_answer,
                bg="#1e8449",
                hover_bg="#27ae60",
                fg="white",
                padx=15,
                pady=button_pady
            )
            submit_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            skip_btn = ModernButton(
                row2,
                text="→ Prossima",
                command=self.next_question,
                bg="#2874a6",
                hover_bg="#3498db",
                fg="white",
                padx=15,
                pady=button_pady
            )
            skip_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            quit_btn = ModernButton(
                row2,
                text="✕ Esci",
                command=self.root.quit,
                bg="#c0392b",
                hover_bg="#e74c3c",
                fg="white",
                padx=15,
                pady=button_pady
            )
            quit_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        else:
            # Layout orizzontale per desktop
            button_frame = tk.Frame(button_container, bg="#121212")
            button_frame.pack()
            
            self.prev_btn = ModernButton(
                button_frame,
                text="← Precedente",
                command=self.previous_question,
                bg="#6c757d",
                hover_bg="#868e96",
                fg="white"
            )
            self.prev_btn.pack(side=tk.LEFT, padx=button_padx)
            
            help_btn = ModernButton(
                button_frame,
                text="💡 AIUTO",
                command=self.show_memory_technique,
                bg="#d68910",
                hover_bg="#f39c12",
                fg="white"
            )
            help_btn.pack(side=tk.LEFT, padx=button_padx)
            
            submit_btn = ModernButton(
                button_frame,
                text="✓ Invia Risposta",
                command=self.check_answer,
                bg="#1e8449",
                hover_bg="#27ae60",
                fg="white"
            )
            submit_btn.pack(side=tk.LEFT, padx=button_padx)
            
            skip_btn = ModernButton(
                button_frame,
                text="→ Prossima",
                command=self.next_question,
                bg="#2874a6",
                hover_bg="#3498db",
                fg="white"
            )
            skip_btn.pack(side=tk.LEFT, padx=button_padx)
            
            quit_btn = ModernButton(
                button_frame,
                text="✕ Esci",
                command=self.root.quit,
                bg="#c0392b",
                hover_bg="#e74c3c",
                fg="white"
            )
            quit_btn.pack(side=tk.LEFT, padx=button_padx)
    
    def create_option_widget(self, parent, text, idx, is_multiple=False):
        """Crea un widget per l'opzione di risposta con stile moderno e responsive"""
        is_mobile = self.is_mobile_size()
        option_frame = tk.Frame(parent, bg="#1e1e1e", relief=tk.FLAT)
        option_pady = 10 if is_mobile else 8
        option_padx = 5 if is_mobile else 10
        option_frame.pack(fill=tk.X, pady=option_pady, padx=option_padx)
        
        # Calcola wraplength dinamico
        current_width = self.root.winfo_width()
        container_padx = 10 if is_mobile else 20
        inner_padx = 15 if is_mobile else 25
        wraplength = max(250, current_width - container_padx * 2 - inner_padx * 2 - 60)
        
        option_font_size = 12 if is_mobile else 13
        option_padx_inner = 10 if is_mobile else 15
        option_pady_inner = 10 if is_mobile else 12
        
        if is_multiple:
            var = tk.BooleanVar()
            self.selected_answers.append(var)
            
            cb = tk.Checkbutton(
                option_frame,
                text=text,
                variable=var,
                font=("SF Pro Display", option_font_size),
                bg="#1e1e1e",
                fg="#e0e0e0",
                selectcolor="#238636",
                activebackground="#1e1e1e",
                activeforeground="#e0e0e0",
                wraplength=wraplength,
                justify=tk.LEFT,
                anchor="w",
                cursor="hand2",
                relief=tk.FLAT
            )
            cb.pack(anchor=tk.W, padx=option_padx_inner, pady=option_pady_inner)
        else:
            rb = tk.Radiobutton(
                option_frame,
                text=text,
                variable=self.selected_answer,
                value=idx,
                font=("SF Pro Display", option_font_size),
                bg="#1e1e1e",
                fg="#e0e0e0",
                selectcolor="#238636",
                activebackground="#1e1e1e",
                activeforeground="#e0e0e0",
                wraplength=wraplength,
                justify=tk.LEFT,
                anchor="w",
                cursor="hand2",
                relief=tk.FLAT
            )
            rb.pack(anchor=tk.W, padx=option_padx_inner, pady=option_pady_inner)
    
    def load_question(self):
        """Carica la domanda corrente"""
        self.show_memory_help = False
        self.selected_answer.set("")
        self.selected_answers = []
        
        # Pulisci il frame delle opzioni
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Nascondi frame aiuto
        self.memory_card.pack_forget()
        
        current_q = self.shuffled_quiz[self.current_question_index]
        
        # Mostra la domanda
        question_text = f"Q{current_q['id']}: {current_q['question']}"
        self.question_label.config(text=question_text)
        
        # Determina se è single choice o multiple choice
        is_multiple = isinstance(current_q['correct'], list)
        
        # Crea i widget per le opzioni
        for idx, option in enumerate(current_q['options']):
            self.create_option_widget(
                self.options_frame,
                option,
                idx,
                is_multiple
            )
        
        # Ripristina le risposte salvate se la domanda è già stata vista
        if self.current_question_index in self.user_answers:
            saved_answer = self.user_answers[self.current_question_index]
            if is_multiple:
                # Ripristina le checkbox
                for idx in saved_answer:
                    if idx < len(self.selected_answers):
                        self.selected_answers[idx].set(True)
            else:
                # Ripristina il radio button
                if saved_answer is not None:
                    self.selected_answer.set(saved_answer)
        
        # Aggiorna contatore e barra di progresso
        self.counter_label.config(
            text=f"Domanda {self.current_question_index + 1} / {self.total_questions}"
        )
        progress = ((self.current_question_index + 1) / self.total_questions) * 100
        self.progress_var.set(progress)
        
        # Aggiorna lo stato del pulsante Precedente
        self.update_prev_button_state()
    
    def show_memory_technique(self):
        """Mostra la tecnica di memoria per la domanda"""
        current_q = self.shuffled_quiz[self.current_question_index]
        
        if not self.show_memory_help:
            self.memory_card.pack(fill=tk.X, pady=(0, 15))
            self.memory_label.config(text=f"💡 {current_q['memory_technique']}")
            self.show_memory_help = True
        else:
            messagebox.showinfo(
                "Memoria Tecnica",
                f"💡 {current_q['memory_technique']}"
            )
    
    def check_answer(self):
        """Verifica se la risposta è corretta"""
        current_q = self.shuffled_quiz[self.current_question_index]
        correct_answer = current_q['correct']
        is_multiple = isinstance(correct_answer, list)
        
        # Ottieni la risposta dell'utente
        if is_multiple:
            if not self.selected_answers:
                messagebox.showwarning("Attenzione", "Seleziona almeno una risposta!")
                return
            user_answer = [i for i, var in enumerate(self.selected_answers) if var.get()]
            user_answer.sort()
            correct_sorted = sorted(correct_answer)
            is_correct = user_answer == correct_sorted
            # Salva la risposta (lista per multiple choice)
            self.user_answers[self.current_question_index] = user_answer.copy()
        else:
            try:
                user_answer = int(self.selected_answer.get())
                is_correct = user_answer == correct_answer
                # Salva la risposta (numero per single choice)
                self.user_answers[self.current_question_index] = user_answer
            except (ValueError, tk.TclError):
                messagebox.showwarning("Attenzione", "Seleziona una risposta!")
                return
        
        # Controlla se la domanda era già stata risposta correttamente
        was_correct = self.question_answered_correctly.get(self.current_question_index, False)
        
        # Aggiorna lo score solo se lo stato è cambiato
        if is_correct and not was_correct:
            # Era sbagliata, ora è corretta: incrementa
            self.score += 1
            self.answered_correctly.add(self.current_question_index)
        elif not is_correct and was_correct:
            # Era corretta, ora è sbagliata: decrementa
            self.score -= 1
            self.answered_correctly.discard(self.current_question_index)
        # Se era già corretta e lo è ancora, o era sbagliata e lo è ancora: non fare nulla
        
        # Salva lo stato corrente della domanda
        self.question_answered_correctly[self.current_question_index] = is_correct
        
        # Mostra il risultato
        if is_correct:
            messagebox.showinfo(
                "✓ Esatto!",
                f"Risposta corretta!\n\n💡 {current_q['memory_technique']}"
            )
        else:
            if is_multiple:
                correct_options = [current_q['options'][i] for i in correct_answer]
                messagebox.showerror(
                    "✕ Sbagliato!",
                    f"Risposta sbagliata.\n\nRisposte corrette:\n" + 
                    "\n".join([f"• {opt}" for opt in correct_options]) +
                    f"\n\n💡 {current_q['memory_technique']}"
                )
            else:
                messagebox.showerror(
                    "✕ Sbagliato!",
                    f"Risposta sbagliata.\n\nRisposta corretta:\n{current_q['options'][correct_answer]}\n\n💡 {current_q['memory_technique']}"
                )
        
        # Aggiorna lo score
        self.score_label.config(text=f"Score: {self.score} / {self.total_questions}")
        
        # Vai alla prossima domanda
        self.next_question()
    
    def previous_question(self):
        """Torna alla domanda precedente"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question()
    
    def next_question(self):
        """Passa alla domanda successiva"""
        if self.current_question_index < self.total_questions - 1:
            self.current_question_index += 1
            self.load_question()
        else:
            self.show_final_score()
    
    def update_prev_button_state(self):
        """Aggiorna lo stato del pulsante Precedente (abilitato/disabilitato)"""
        if hasattr(self, 'prev_btn'):
            if self.current_question_index == 0:
                # Disabilita visivamente il pulsante se siamo alla prima domanda
                self.prev_btn.config(bg="#30363d")
                self.prev_btn.label.config(bg="#30363d", fg="#6e7681", cursor="arrow")
                # Salva il comando originale e sostituiscilo con una funzione vuota
                self.prev_btn.command = None
            else:
                # Abilita il pulsante
                self.prev_btn.config(bg="#6c757d")
                self.prev_btn.label.config(bg="#6c757d", fg="white", cursor="hand2")
                # Ripristina il comando originale
                self.prev_btn.command = self.previous_question
    
    def show_final_score(self):
        """Mostra il punteggio finale con design moderno"""
        percentage = (self.score / self.total_questions) * 100
        
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
        
        message = f"""{emoji} {message_type}

Quiz Completato!

Punteggio Finale: {self.score} / {self.total_questions}
Percentuale: {percentage:.1f}%

Risposte Corrette: {self.score}
Risposte Sbagliate: {self.total_questions - self.score}"""
        
        messagebox.showinfo("Quiz Terminato", message)
        
        # Offri di ricominciare
        if messagebox.askyesno("Ricominciare?", "Vuoi fare un altro giro?"):
            # Torna alla home page
            self.home_page = HomePage(self.root, self.quiz_data, self.start_quiz)
        else:
            self.root.quit()


def main():
    root = tk.Tk()
    app = SAPBuildQuiz(root)
    root.mainloop()


if __name__ == "__main__":
    main()
