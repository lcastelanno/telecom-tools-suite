import math
import json
import os

import customtkinter as ctk
import phonenumbers
from phonenumbers import number_type, geocoder
import csv
import re
from tkinter import filedialog, messagebox

# Configuração do Tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

LOCALES = {
    'en-GB': {
        'home': 'Home', 'lookup': 'Search & Validator', 'splitter': 'Range Manager', 'capacity': 'Call Capacity (CAC)', 'dialplan': 'Global Dial Plan',
        'dark': '🌙 Dark Mode', 'light': '☀️ Light Mode',
        'homeTitle': 'Telecom Tools Suite', 'homeSub': 'Select an application from the sidebar to start.',
        'devBy': 'Developed in Python + CustomTkinter', 'devDescPy': 'Offline Version, Secure and Fast.',
        'lookTitle': 'DDI Search & Validator', 'btnAnalyse': 'Analyse', 'btnClear': 'Clear',
        'errInvalid': 'Invalid or incomplete number.', 'errFormat': 'Format Error. Make sure to use the international code (e.g. +44).',
        'resCountry': 'Country (DDI):', 'resLoc': 'Location/State:', 'resNational': 'National Format:', 'resType': 'Estimated Type:', 'resUri': 'SIP URI (RFC 3966):',
        'splitTitle': 'DDI Range Manager', 'splitConf': '1. Range Settings', 'startDdi': 'Start (Start DDI)', 'endDdi': 'End (End DDI)', 'chunkSize': 'Chunk Size',
        'btnSplit': 'Split Range', 'btnFull': 'Generate Full List', 'splitRes': '2. Result', 'btnExport': 'Export CSV',
        'errValid': 'Set valid numbers.', 'errGreater': 'The end number must be greater than or equal to the start number.', 'errLarge': 'Generating a list with more than 50k numbers can crash the app.',
        'errChunk': 'Chunk size must be a positive integer.',
        'capTitle': 'Call Capacity (CAC)', 'capParam': '1. Calculation Parameters', 'calcMethod': 'Calculation Method',
        'calcStd': 'Standard UC (5 Licences / 1 SIP Channel)', 'calcErlang': 'Erlang B (Traffic Based)',
        'users': 'Total Users / Licences', 'bhca': 'Calls/User/Hour (BHCA)', 'dur': 'Avg Duration (s)', 'gos': 'GoS (e.g. 0.01 = 1%)', 'codec': 'Codec Used',
        'btnCalc': 'Calculate', 'capRes': '2. Sizing Results', 'sipChans': 'Recommended SIP Channels', 'bwEst': 'Estimated Bandwidth (SIP Trunk)', 'calcDetails': 'Calculation Details:', 'capMsg': 'Fill in the data and click Calculate.',
        'errUsers': 'Invalid number of users.', 'errErlang': 'Invalid Erlang B parameters.',
        'detMethStd': 'Method: Standard UC (1 Channel per 5 Licences)', 'detStdIdeal': 'Ideal for Webex Calling and Teams Phone System.',
        'detMethErl': 'Method: Erlang B', 'detTraf': 'Traffic (Erlangs):', 'detGos': 'Grade of Service (GoS):',
        'detMult': '- Multiplier for calls in the same branch may\n  require more local/LAN bandwidth.',
        'optG711': 'G.711 (87.2 kbps)', 'optG729': 'G.729 (31.2 kbps)', 'optOpus': 'Opus (50.0 kbps)',
        'typFixedMob': 'Fixed or Mobile', 'typMob': 'Mobile', 'typFixed': 'Fixed', 'typOther': 'Other', 'locUnknown': 'Unknown',
        'errTitle': 'Error', 'warnTitle': 'Warning', 'succTitle': 'Success', 'msgSuccess': 'File saved successfully at:\n',
        'warnNoData': 'No formatted data to export.', 'expTitle': 'Export as CSV',
        'dpTitle': 'Global Dial Plan', 'dpSelCountry': 'Select Country:', 'dpOutbound': 'Outbound Calling Plan', 'dpDigitMap': 'Digit Map', 'dpCallType': 'Call Type', 'dpDesc': 'Description', 'dpTollFree': 'Toll-Free & Non-geographic', 'dpEmerg': 'Emergency Numbers', 'dpNoEmerg': 'No emergency numbers listed.', 'dpEmergDesc': 'Emergency numbers cannot be assigned in an internal dial plan.'
    },
    'pt-BR': {
        'home': 'Home', 'lookup': 'Busca e Validador', 'splitter': 'Gerenciador de Range', 'capacity': 'Capacidade de Chamadas (CAC)', 'dialplan': 'Global Dial Plan',
        'dark': '🌙 Modo Escuro', 'light': '☀️ Modo Claro',
        'homeTitle': 'Telecom Tools Suite', 'homeSub': 'Selecione uma das aplicações no menu lateral para iniciar.',
        'devBy': 'Desenvolvido em Python + CustomTkinter', 'devDescPy': 'Versão Offline, Segura e Rápida.',
        'lookTitle': 'Busca e Validador de DDI', 'btnAnalyse': 'Analisar', 'btnClear': 'Limpar',
        'errInvalid': 'Número Inválido ou incompleto.', 'errFormat': 'Erro de Formato. Certifique-se de usar o código internacional (ex: +55).',
        'resCountry': 'País (DDI):', 'resLoc': 'Localização/Estado:', 'resNational': 'Formato Nacional:', 'resType': 'Tipo Estimado:', 'resUri': 'SIP URI (RFC 3966):',
        'splitTitle': 'Gerenciador de Range de DDI', 'splitConf': '1. Configurações do Range', 'startDdi': 'Início (Start DDI)', 'endDdi': 'Fim (End DDI)', 'chunkSize': 'Tamanho do Bloco (Chunk)',
        'btnSplit': 'Dividir Range', 'btnFull': 'Gerar Lista Completa', 'splitRes': '2. Resultado', 'btnExport': 'Exportar CSV',
        'errValid': 'Defina números válidos.', 'errGreater': 'O número final deve ser maior ou igual ao inicial.', 'errLarge': 'Gerar uma lista com mais de 50k números pode travar o aplicativo.',
        'errChunk': 'Chunk size deve ser um número inteiro positivo.',
        'capTitle': 'Capacidade de Chamadas (CAC)', 'capParam': '1. Parâmetros de Cálculo', 'calcMethod': 'Método de Cálculo',
        'calcStd': 'Standard UC (5 Licenças / 1 Canal SIP)', 'calcErlang': 'Erlang B (Baseado em Tráfego)',
        'users': 'Total de Usuários / Licenças', 'bhca': 'Chamadas/Usuário/Hora (BHCA)', 'dur': 'Duração Média (s)', 'gos': 'GoS (Ex: 0.01 = 1%)', 'codec': 'Codec Utilizado',
        'btnCalc': 'Calcular', 'capRes': '2. Resultados do Dimensionamento', 'sipChans': 'Canais SIP Recomendados', 'bwEst': 'Banda Estimada (Trunk SIP)', 'calcDetails': 'Detalhes do Cálculo:', 'capMsg': 'Preencha os dados e clique em Calcular.',
        'errUsers': 'Número de usuários inválido.', 'errErlang': 'Parâmetros de Erlang B inválidos.',
        'detMethStd': 'Método: Standard UC (1 Canal para 5 Licenças)', 'detStdIdeal': 'Ideal para Webex Calling e Teams Phone System.',
        'detMethErl': 'Método: Erlang B', 'detTraf': 'Tráfego (Erlangs):', 'detGos': 'Grade de Serviço (GoS):',
        'detMult': '- Multiplicador de chamadas na mesma filial pode\n  exigir mais banda local/LAN.',
        'optG711': 'G.711 (87.2 kbps)', 'optG729': 'G.729 (31.2 kbps)', 'optOpus': 'Opus (50.0 kbps)',
        'typFixedMob': 'Fixo ou Móvel', 'typMob': 'Móvel', 'typFixed': 'Fixo', 'typOther': 'Outro', 'locUnknown': 'Desconhecida',
        'errTitle': 'Erro', 'warnTitle': 'Aviso', 'succTitle': 'Sucesso', 'msgSuccess': 'Arquivo salvo com sucesso em:\n',
        'warnNoData': 'Não há dados formatados para exportar.', 'expTitle': 'Exportar como CSV',
        'dpTitle': 'Global Dial Plan', 'dpSelCountry': 'Selecione o País:', 'dpOutbound': 'Plano de Chamadas de Saída', 'dpDigitMap': 'Mapa de Dígitos', 'dpCallType': 'Tipo de Chamada', 'dpDesc': 'Descrição', 'dpTollFree': 'Toll-Free e Não Geográficos', 'dpEmerg': 'Números de Emergência', 'dpNoEmerg': 'Nenhum número de emergência listado.', 'dpEmergDesc': 'Não é possível atribuir números de emergência em um plano de discagem interno (ramal).'
    },
    'es-CO': {
        'home': 'Inicio', 'lookup': 'Búsqueda y Validador', 'splitter': 'Gestor de Rangos', 'capacity': 'Capacidad de Llamadas (CAC)', 'dialplan': 'Plan de Marcación Global',
        'dark': '🌙 Modo Oscuro', 'light': '☀️ Modo Claro',
        'homeTitle': 'Telecom Tools Suite', 'homeSub': 'Seleccione una de las aplicaciones en el menú lateral para iniciar.',
        'devBy': 'Desarrollado en Python + CustomTkinter', 'devDescPy': 'Versión Offline, Segura y Rápida.',
        'lookTitle': 'Búsqueda y Validador de DDI', 'btnAnalyse': 'Analizar', 'btnClear': 'Limpiar',
        'errInvalid': 'Número inválido o incompleto.', 'errFormat': 'Error de formato. Asegúrese de usar el código (ej: +57).',
        'resCountry': 'País (DDI):', 'resLoc': 'Ubicación/Estado:', 'resNational': 'Formato Nacional:', 'resType': 'Tipo Estimado:', 'resUri': 'SIP URI (RFC 3966):',
        'splitTitle': 'Gestor de Rangos de DDI', 'splitConf': '1. Configuraciones de Rango', 'startDdi': 'Inicio (DDI Inicial)', 'endDdi': 'Fin (DDI Final)', 'chunkSize': 'Tamaño del Bloque',
        'btnSplit': 'Dividir Rango', 'btnFull': 'Generar Lista Completa', 'splitRes': '2. Resultado', 'btnExport': 'Exportar CSV',
        'errValid': 'Defina números válidos.', 'errGreater': 'El número final debe ser mayor o igual al inicial.', 'errLarge': 'Generar una lista con más de 50k números puede bloquear la app.',
        'errChunk': 'Tamaño del bloque debe ser entero positivo.',
        'capTitle': 'Capacidad de Llamadas (CAC)', 'capParam': '1. Parámetros de Cálculo', 'calcMethod': 'Método de Cálculo',
        'calcStd': 'Standard UC (5 Licencias / 1 Canal SIP)', 'calcErlang': 'Erlang B (Basado en Tráfico)',
        'users': 'Total de Usuarios / Licencias', 'bhca': 'Llamadas/Usuario/Hora (BHCA)', 'dur': 'Duración Promedio (s)', 'gos': 'GoS (Ej: 0.01 = 1%)', 'codec': 'Códec Utilizado',
        'btnCalc': 'Calcular', 'capRes': '2. Resultados de Dimensionamiento', 'sipChans': 'Canales SIP Recomendados', 'bwEst': 'Ancho de Banda Estimado (Trunk SIP)', 'calcDetails': 'Detalles del Cálculo:', 'capMsg': 'Llene los datos y haga clic en Calcular.',
        'errUsers': 'Número de usuarios inválido.', 'errErlang': 'Parámetros de Erlang B inválidos.',
        'detMethStd': 'Método: Standard UC (1 Canal por 5 Licencias)', 'detStdIdeal': 'Ideal para Webex Calling y Teams Phone System.',
        'detMethErl': 'Método: Erlang B', 'detTraf': 'Tráfico (Erlangs):', 'detGos': 'Grado de Servicio (GoS):',
        'detMult': '- Un multiplicador de llamadas en la misma sucursal\n  puede requerir más ancho de banda local/LAN.',
        'optG711': 'G.711 (87.2 kbps)', 'optG729': 'G.729 (31.2 kbps)', 'optOpus': 'Opus (50.0 kbps)',
        'typFixedMob': 'Fijo o Móvil', 'typMob': 'Móvil', 'typFixed': 'Fijo', 'typOther': 'Otro', 'locUnknown': 'Desconocida',
        'errTitle': 'Error', 'warnTitle': 'Advertencia', 'succTitle': 'Éxito', 'msgSuccess': 'Archivo guardado con éxito en:\n',
        'warnNoData': 'No hay datos formateados para exportar.', 'expTitle': 'Exportar como CSV',
        'dpTitle': 'Global Dial Plan', 'dpSelCountry': 'Seleccionar País:', 'dpOutbound': 'Plan de Llamadas de Salida', 'dpDigitMap': 'Mapa de Dígitos', 'dpCallType': 'Tipo de Llamada', 'dpDesc': 'Descripción', 'dpTollFree': 'Toll-Free y No Geográficos', 'dpEmerg': 'Números de Emergencia', 'dpNoEmerg': 'No hay números de emergencia.', 'dpEmergDesc': 'No se pueden asignar números de emergencia en un plan interno.'
    }
}

class TelecomApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = 'en-GB'
        self.text_vars = {k: ctk.StringVar(value=v) for k, v in LOCALES[self.lang].items()}

        try:
            with open(os.path.join(os.path.dirname(__file__), "DialPlanGlobal.json"), "r", encoding="utf-8") as f:
                self.dialplan_data = json.load(f)
        except Exception:
            self.dialplan_data = {}

        self.title("Telecom Tools Suite")
        self.geometry("950x650")
        self.minsize(800, 500)
        
        # Configuração do Grid principal (Sidebar + Conteúdo)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ==========================================
        # 1. SIDEBAR (Navegação)
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Espaçador inferior

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Telecom Tools", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color=("#7e22ce", "#d8b4fe")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Botões de navegação
        self.btn_home = ctk.CTkButton(
            self.sidebar_frame, textvariable=self.text_vars['home'], command=lambda: self.select_frame("home"),
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w"
        )
        self.btn_home.grid(row=1, column=0, padx=20, pady=5)

        self.btn_lookup = ctk.CTkButton(
            self.sidebar_frame, textvariable=self.text_vars['lookup'], command=lambda: self.select_frame("lookup"),
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w"
        )
        self.btn_lookup.grid(row=2, column=0, padx=20, pady=5)

        self.btn_splitter = ctk.CTkButton(
            self.sidebar_frame, textvariable=self.text_vars['splitter'], command=lambda: self.select_frame("splitter"),
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w"
        )
        self.btn_splitter.grid(row=3, column=0, padx=20, pady=5)

        self.btn_capacity = ctk.CTkButton(
            self.sidebar_frame, textvariable=self.text_vars['capacity'], command=lambda: self.select_frame("capacity"),
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w"
        )
        self.btn_capacity.grid(row=4, column=0, padx=20, pady=5)
        
        self.btn_dialplan = ctk.CTkButton(
            self.sidebar_frame, textvariable=self.text_vars['dialplan'], command=lambda: self.select_frame("dialplan"),
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w"
        )
        self.btn_dialplan.grid(row=5, column=0, padx=20, pady=5)
        
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_frame, textvariable=self.text_vars['dark'], command=self.toggle_theme
        )
        self.theme_switch.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Language Switcher
        self.lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lang_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)
        
        ctk.CTkButton(self.lang_frame, text="🇬🇧", width=30, fg_color="transparent", text_color=("black", "white"), command=lambda: self.set_language('en-GB')).pack(side="left", padx=2)
        ctk.CTkButton(self.lang_frame, text="🇧🇷", width=30, fg_color="transparent", text_color=("black", "white"), command=lambda: self.set_language('pt-BR')).pack(side="left", padx=2)
        ctk.CTkButton(self.lang_frame, text="🇨🇴", width=30, fg_color="transparent", text_color=("black", "white"), command=lambda: self.set_language('es-CO')).pack(side="left", padx=2)

        # ==========================================
        # 2. FRAMES DE CONTEÚDO
        # ==========================================
        self.home_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lookup_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.splitter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.capacity_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dialplan_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.build_home_frame()
        self.build_lookup_frame()
        self.build_splitter_frame()
        self.build_capacity_frame()
        self.build_dialplan_frame()

        # Selecionar a aba inicial
        self.select_frame("home")

    def set_language(self, lang):
        self.lang = lang
        t = LOCALES[self.lang]
        for k, v in t.items():
            self.text_vars[k].set(v)
            
        self.theme_switch.configure(text=t['light'] if self.theme_switch.get() == 1 else t['dark'])
        self.entry_phone.configure(placeholder_text="+44 20 7123 4567" if lang=='en-GB' else "+55 11 98765 4321")

        # Update comboboxes keeping current logic selection
        curr_calc = self.combo_calc_type.get()
        is_erlang = "Erlang" in curr_calc or "Tráfico" in curr_calc or "Tráfego" in curr_calc
        self.combo_calc_type.configure(values=[t['calcStd'], t['calcErlang']])
        self.combo_calc_type.set(t['calcErlang'] if is_erlang else t['calcStd'])
        
        curr_codec = self.combo_codec.get()
        opts = [t['optG711'], t['optG729'], t['optOpus']]
        idx = 1 if "729" in curr_codec else (2 if "Opus" in curr_codec or "OPUS" in curr_codec else 0)
        self.combo_codec.configure(values=opts)
        self.combo_codec.set(opts[idx])
        
        self._clear_lookup()
        self._clear_capacity()
        if hasattr(self, 'combo_country') and self.combo_country.get():
            self._update_dialplan_view(self.combo_country.get())

    def toggle_theme(self):
        t = LOCALES[self.lang]
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text=t['light'])
        else:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text=t['dark'])

    def select_frame(self, name):
        # Reseta as cores dos botões
        self.btn_home.configure(fg_color="transparent")
        self.btn_lookup.configure(fg_color="transparent")
        self.btn_splitter.configure(fg_color="transparent")
        self.btn_capacity.configure(fg_color="transparent")
        self.btn_dialplan.configure(fg_color="transparent")

        # Oculta todos os frames
        self.home_frame.grid_forget()
        self.lookup_frame.grid_forget()
        self.splitter_frame.grid_forget()
        self.capacity_frame.grid_forget()
        self.dialplan_frame.grid_forget()

        # Destaca o botão selecionado e mostra o frame correto
        active_color = "#9333ea" # Roxo do seu tema original
        if name == "home":
            self.btn_home.configure(fg_color=active_color)
            self.home_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "lookup":
            self.btn_lookup.configure(fg_color=active_color)
            self.lookup_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "splitter":
            self.btn_splitter.configure(fg_color=active_color)
            self.splitter_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "capacity":
            self.btn_capacity.configure(fg_color=active_color)
            self.capacity_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "dialplan":
            self.btn_dialplan.configure(fg_color=active_color)
            self.dialplan_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    # ==========================================
    # BUILD: HOME FRAME
    # ==========================================
    def build_home_frame(self):
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        container = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        container.grid(row=0, column=0)

        ctk.CTkLabel(container, textvariable=self.text_vars['homeTitle'], font=ctk.CTkFont(size=32, weight="bold")).pack(pady=10)
        ctk.CTkLabel(container, textvariable=self.text_vars['homeSub'], text_color=("gray40", "gray60")).pack(pady=10)
        
        # Info Box
        info_box = ctk.CTkFrame(container, fg_color=("gray85", "gray25"), corner_radius=10)
        info_box.pack(pady=30, padx=20, fill="x")
        ctk.CTkLabel(info_box, textvariable=self.text_vars['devBy'], font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        ctk.CTkLabel(info_box, textvariable=self.text_vars['devDescPy']).pack(pady=(0, 15))

    # ==========================================
    # BUILD: LOOKUP FRAME
    # ==========================================
    def build_lookup_frame(self):
        self.lookup_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.lookup_frame, textvariable=self.text_vars['lookTitle'], font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        input_frame = ctk.CTkFrame(self.lookup_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=10)
        
        self.entry_phone = ctk.CTkEntry(input_frame, placeholder_text="+44 20 7123 4567", width=300, font=ctk.CTkFont(size=16))
        self.entry_phone.pack(side="left", padx=(0, 10))
        
        btn_analyze = ctk.CTkButton(input_frame, textvariable=self.text_vars['btnAnalyse'], command=self.analyze_number, fg_color="#9333ea", hover_color="#7e22ce", width=120)
        btn_analyze.pack(side="left", padx=(0, 10))
        
        btn_clear = ctk.CTkButton(input_frame, textvariable=self.text_vars['btnClear'], command=self._clear_lookup, fg_color=("gray75", "gray30"), text_color=("black", "white"), hover_color=("gray65", "gray40"), width=120)
        btn_clear.pack(side="left")

        # Área de Resultados
        self.result_frame = ctk.CTkFrame(self.lookup_frame, corner_radius=10)
        self.result_frame.pack(fill="both", expand=True, pady=20)
        
        self.lbl_e164 = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=28, weight="bold"), text_color=("#2563eb", "#60a5fa"))
        self.lbl_e164.pack(pady=(20, 10))
        
        self.lbl_details = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=14), justify="left")
        self.lbl_details.pack(pady=10, padx=20, anchor="w")

    def _clear_lookup(self):
        self.entry_phone.delete(0, 'end')
        self.lbl_e164.configure(text="")
        self.lbl_details.configure(text="")

    def analyze_number(self):
        t = LOCALES[self.lang]
        number_str = self.entry_phone.get().strip()
        if not number_str:
            return
            
        formatted_input = number_str if number_str.startswith('+') else '+' + re.sub(r'\D', '', number_str)
        
        try:
            parsed_num = phonenumbers.parse(formatted_input, None)
            
            if not phonenumbers.is_valid_number(parsed_num):
                self.lbl_e164.configure(text=t['errInvalid'], text_color=("#dc2626", "#f87171"))
                self.lbl_details.configure(text="")
                return
                
            e164 = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.E164)
            national = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.NATIONAL)
            rfc3966 = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.RFC3966)
            country_code = parsed_num.country_code
            
            # Tipo de linha
            n_type = phonenumbers.number_type(parsed_num)
            type_str = t['typFixedMob'] if n_type == 2 else t['typMob'] if n_type == 1 else t['typFixed'] if n_type == 0 else t['typOther']
            
            # Localização
            loc_lang = "en" if self.lang == 'en-GB' else ("pt" if self.lang == 'pt-BR' else "es")
            location = geocoder.description_for_number(parsed_num, loc_lang)
            location_str = location if location else t['locUnknown']
            
            self.lbl_e164.configure(text=e164, text_color=("#2563eb", "#60a5fa"))
            
            details_text = (
                f"{t['resCountry']} +{country_code}\n\n"
                f"{t['resLoc']} {location_str}\n\n"
                f"{t['resNational']} {national}\n\n"
                f"{t['resType']} {type_str}\n\n"
                f"{t['resUri']} {rfc3966}"
            )
            self.lbl_details.configure(text=details_text)
            
        except phonenumbers.NumberParseException:
            self.lbl_e164.configure(text=t['errTitle'], text_color=("#dc2626", "#f87171"))
            self.lbl_details.configure(text=t['errFormat'])

    # ==========================================
    # BUILD: SPLITTER FRAME
    # ==========================================
    def build_splitter_frame(self):
        self.splitter_frame.grid_columnconfigure(0, weight=1)
        self.splitter_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.splitter_frame, textvariable=self.text_vars['splitTitle'], font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        # Configurações
        config_frame = ctk.CTkFrame(self.splitter_frame)
        config_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(config_frame, textvariable=self.text_vars['splitConf'], font=ctk.CTkFont(weight="bold")).pack(pady=(15,5), padx=15, anchor="w")
        
        # Frame para colocar os inputs lado a lado
        inputs_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        inputs_frame.pack(fill="x", padx=15, pady=5)
        inputs_frame.grid_columnconfigure(0, weight=1)
        inputs_frame.grid_columnconfigure(1, weight=1)
        
        start_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        start_frame.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkLabel(start_frame, textvariable=self.text_vars['startDdi']).pack(anchor="w")
        self.entry_start = ctk.CTkEntry(start_frame, placeholder_text="+551140001000")
        self.entry_start.pack(fill="x")
        
        end_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        end_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(end_frame, textvariable=self.text_vars['endDdi']).pack(anchor="w")
        self.entry_end = ctk.CTkEntry(end_frame, placeholder_text="+551140001099")
        self.entry_end.pack(fill="x")
        
        ctk.CTkLabel(config_frame, textvariable=self.text_vars['chunkSize']).pack(padx=15, pady=(15,0), anchor="w")
        self.entry_chunk = ctk.CTkEntry(config_frame)
        self.entry_chunk.insert(0, "10")
        self.entry_chunk.pack(fill="x", padx=15, pady=5)

        btn_split = ctk.CTkButton(config_frame, textvariable=self.text_vars['btnSplit'], command=self.split_ranges, fg_color="#9333ea", hover_color="#7e22ce")
        btn_split.pack(fill="x", padx=15, pady=15)
        
        btn_list = ctk.CTkButton(config_frame, textvariable=self.text_vars['btnFull'], command=self.generate_list, fg_color=("gray75", "gray30"), text_color=("black", "white"), hover_color=("gray65", "gray40"))
        btn_list.pack(fill="x", padx=15, pady=(0,15))
        
        btn_clear = ctk.CTkButton(config_frame, textvariable=self.text_vars['btnClear'], command=self._clear_splitter, fg_color=("gray75", "gray30"), text_color=("black", "white"), hover_color=("gray65", "gray40"))
        btn_clear.pack(fill="x", padx=15, pady=(0,15))

        # Área de Output
        output_frame = ctk.CTkFrame(self.splitter_frame)
        output_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        top_output = ctk.CTkFrame(output_frame, fg_color="transparent")
        top_output.pack(fill="x", padx=15, pady=(15,5))
        
        ctk.CTkLabel(top_output, textvariable=self.text_vars['splitRes'], font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        btn_export = ctk.CTkButton(top_output, textvariable=self.text_vars['btnExport'], command=self.export_csv, width=100)
        btn_export.pack(side="right")

        self.txt_output = ctk.CTkTextbox(output_frame, font=ctk.CTkFont(family="monospace", size=13))
        self.txt_output.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _clear_splitter(self):
        self.entry_start.delete(0, 'end')
        self.entry_end.delete(0, 'end')
        self.entry_chunk.delete(0, 'end')
        self.entry_chunk.insert(0, "10")
        self.txt_output.delete("1.0", "end")

    def get_range_data(self):
        t = LOCALES[self.lang]
        start_str = self.entry_start.get().strip()
        end_str = self.entry_end.get().strip()
        
        clean_start = re.sub(r'\D', '', start_str)
        clean_end = re.sub(r'\D', '', end_str)
        
        if not clean_start or not clean_end:
            messagebox.showerror(t['errTitle'], t['errValid'])
            return None
            
        val_start = int(clean_start)
        val_end = int(clean_end)
        
        if val_start > val_end:
            messagebox.showerror(t['errTitle'], t['errGreater'])
            return None
            
        return {
            "start_val": val_start,
            "end_val": val_end,
            "has_plus": start_str.startswith('+'),
            "length": len(clean_start)
        }

    def split_ranges(self):
        t = LOCALES[self.lang]
        data = self.get_range_data()
        if not data: return
        
        try:
            chunk_size = int(self.entry_chunk.get())
            if chunk_size < 1: raise ValueError
        except ValueError:
            messagebox.showerror(t['errTitle'], t['errChunk'])
            return

        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("end", f"{LOCALES['en-GB']['startDdi']}\t{LOCALES['en-GB']['endDdi']}\tSize\n") # Mantém em inglês para padronizar CSV
        
        current = data["start_val"]
        end_limit = data["end_val"]
        prefix = "+" if data["has_plus"] else ""
        
        while current <= end_limit:
            block_end = min(current + chunk_size - 1, end_limit)
            
            start_fmt = f"{prefix}{str(current).zfill(data['length'])}"
            end_fmt = f"{prefix}{str(block_end).zfill(data['length'])}"
            size = block_end - current + 1
            
            self.txt_output.insert("end", f"{start_fmt}\t{end_fmt}\t{size}\n")
            current = block_end + 1

    def generate_list(self):
        t = LOCALES[self.lang]
        data = self.get_range_data()
        if not data: return
        
        size = data["end_val"] - data["start_val"] + 1
        if size > 50000:
            messagebox.showwarning(t['warnTitle'], t['errLarge'])
            return
            
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("end", "DDI Number\n")
        
        prefix = "+" if data["has_plus"] else ""
        
        # Usando um array para gerar o texto de uma vez (mais rápido)
        lines = []
        for i in range(data["start_val"], data["end_val"] + 1):
            lines.append(f"{prefix}{str(i).zfill(data['length'])}")
            
        self.txt_output.insert("end", "\n".join(lines) + "\n")

    def export_csv(self):
        t = LOCALES[self.lang]
        content = self.txt_output.get("1.0", "end-1c").strip()
        if not content or content.startswith(LOCALES['en-GB']['startDdi']) is False and content.startswith("DDI Number") is False:
            messagebox.showinfo(t['warnTitle'], t['warnNoData'])
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title=t['expTitle']
        )
        
        if not filepath:
            return
            
        try:
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                # O encoding 'utf-8-sig' adiciona o BOM, garantindo que o Excel abra os acentos e formatos corretamente
                lines = content.split('\n')
                writer = csv.writer(f, delimiter=';') # Ponto e vírgula é padrão pt-BR no Excel
                
                for line in lines:
                    if not line: continue
                    row = line.split('\t')
                    
                    # Hack para o Excel não transformar números com "+" em fórmulas ou Notação Científica
                    formatted_row = [f'="{cell}"' if cell.startswith('+') else cell for cell in row]
                    writer.writerow(formatted_row)
                    
            messagebox.showinfo(t['succTitle'], f"{t['msgSuccess']}{filepath}")
        except Exception as e:
            messagebox.showerror(t['errTitle'], f"Error:\n{str(e)}")

    # ==========================================
    # BUILD: CAPACITY FRAME
    # ==========================================
    def build_capacity_frame(self):
        self.capacity_frame.grid_columnconfigure(0, weight=1)
        self.capacity_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.capacity_frame, textvariable=self.text_vars['capTitle'], font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        self._build_capacity_config_section()
        self._build_capacity_result_section()

    def _build_capacity_config_section(self):
        t = LOCALES[self.lang]
        config_frame = ctk.CTkFrame(self.capacity_frame)
        config_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(config_frame, textvariable=self.text_vars['capParam'], font=ctk.CTkFont(weight="bold")).pack(pady=(15,5), padx=15, anchor="w")
        
        # Método de Cálculo
        ctk.CTkLabel(config_frame, textvariable=self.text_vars['calcMethod']).pack(padx=15, anchor="w")
        self.combo_calc_type = ctk.CTkComboBox(
            config_frame,
            values=[t['calcStd'], t['calcErlang']],
            command=self._on_calc_type_change
        )
        self.combo_calc_type.set(t['calcStd'])
        self.combo_calc_type.pack(fill="x", padx=15, pady=5)
        
        # Usuários
        ctk.CTkLabel(config_frame, textvariable=self.text_vars['users']).pack(padx=15, anchor="w")
        self.entry_users = ctk.CTkEntry(config_frame)
        self.entry_users.insert(0, "100")
        self.entry_users.pack(fill="x", padx=15, pady=5)

        # Campos Erlang B
        self._build_erlang_inputs(config_frame)

        # Codec
        ctk.CTkLabel(config_frame, textvariable=self.text_vars['codec']).pack(padx=15, pady=(10,0), anchor="w")
        self.combo_codec = ctk.CTkComboBox(config_frame, values=[t['optG711'], t['optG729'], t['optOpus']])
        self.combo_codec.set(t['optG711'])
        self.combo_codec.pack(fill="x", padx=15, pady=5)

        # Botões Calcular e Limpar
        btn_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=20)
        
        btn_calc = ctk.CTkButton(btn_frame, textvariable=self.text_vars['btnCalc'], command=self._calculate_capacity, fg_color="#9333ea", hover_color="#7e22ce")
        btn_calc.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        btn_clear = ctk.CTkButton(btn_frame, textvariable=self.text_vars['btnClear'], command=self._clear_capacity, fg_color=("gray75", "gray30"), text_color=("black", "white"), hover_color=("gray65", "gray40"))
        btn_clear.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def _build_erlang_inputs(self, parent):
        self.erlang_frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        ctk.CTkLabel(self.erlang_frame, textvariable=self.text_vars['bhca']).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_bhca = ctk.CTkEntry(self.erlang_frame, width=100)
        self.entry_bhca.insert(0, "3.0")
        self.entry_bhca.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(self.erlang_frame, textvariable=self.text_vars['dur']).grid(row=0, column=1, sticky="w", padx=5)
        self.entry_duration = ctk.CTkEntry(self.erlang_frame, width=100)
        self.entry_duration.insert(0, "120")
        self.entry_duration.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(self.erlang_frame, textvariable=self.text_vars['gos']).grid(row=0, column=2, sticky="w", padx=5)
        self.entry_gos = ctk.CTkEntry(self.erlang_frame, width=100)
        self.entry_gos.insert(0, "0.01")
        self.entry_gos.grid(row=1, column=2, sticky="w", padx=5, pady=5)

    def _build_capacity_result_section(self):
        result_container = ctk.CTkFrame(self.capacity_frame)
        result_container.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(result_container, textvariable=self.text_vars['capRes'], font=ctk.CTkFont(weight="bold")).pack(pady=(15,5), padx=15, anchor="w")
        
        ctk.CTkLabel(result_container, textvariable=self.text_vars['sipChans'], text_color="#9333ea", font=ctk.CTkFont(weight="bold")).pack(pady=(10,0))
        self.lbl_res_channels = ctk.CTkLabel(result_container, text="-", font=ctk.CTkFont(size=48, weight="bold"), text_color=("#9333ea", "#d8b4fe"))
        self.lbl_res_channels.pack()

        ctk.CTkLabel(result_container, textvariable=self.text_vars['bwEst'], text_color="#9333ea", font=ctk.CTkFont(weight="bold")).pack(pady=(20,0))
        self.lbl_res_bw = ctk.CTkLabel(result_container, text="-", font=ctk.CTkFont(size=24, weight="bold"), text_color=("#2563eb", "#60a5fa"))
        self.lbl_res_bw.pack()
        
        self.lbl_res_details = ctk.CTkLabel(result_container, textvariable=self.text_vars['capMsg'], justify="left", text_color=("gray40", "gray70"))
        self.lbl_res_details.pack(pady=30, padx=20, anchor="w")

    def _clear_capacity(self):
        t = LOCALES[self.lang]
        self.entry_users.delete(0, 'end')
        self.entry_bhca.delete(0, 'end')
        self.entry_duration.delete(0, 'end')
        self.entry_gos.delete(0, 'end')
        self.lbl_res_channels.configure(text="-")
        self.lbl_res_bw.configure(text="-")
        self.lbl_res_details.configure(text=t['capMsg'])

    def _on_calc_type_change(self, choice):
        if "Erlang" in choice:
            self.erlang_frame.pack(fill="x", padx=10, pady=10, after=self.entry_users)
        else:
            self.erlang_frame.pack_forget()

    @staticmethod
    def _compute_erlang_channels(erlangs: float, target_gos: float) -> int:
        """Calculates required channels using the Erlang B formula."""
        channels = 1
        p = 1.0
        while channels <= 10000:
            p = (erlangs * p) / (channels + erlangs * p)
            if p <= target_gos:
                return channels
            channels += 1
        return channels

    def _calculate_capacity(self):
        t = LOCALES[self.lang]
        try:
            num_users = int(self.entry_users.get() or 0)
            if num_users < 0: raise ValueError
        except ValueError:
            messagebox.showerror(t['errTitle'], t['errUsers'])
            return

        calc_type = self.combo_calc_type.get()
        codec = self.combo_codec.get()
        details = []

        if "Standard" in calc_type:
            channels = math.ceil(num_users / 5)
            details.extend([
                t['detMethStd'],
                t['detStdIdeal']
            ])
        else:
            try:
                bhca = float(self.entry_bhca.get() or 0)
                duration = float(self.entry_duration.get() or 0)
                gos = float(self.entry_gos.get() or 0.01)
                if any(v < 0 for v in (bhca, duration, gos)): raise ValueError
            except ValueError:
                messagebox.showerror(t['errTitle'], t['errErlang'])
                return
                
            total_calls = num_users * bhca
            erlangs = (total_calls * duration) / 3600
            channels = self._compute_erlang_channels(erlangs, gos)
            
            details.extend([
                t['detMethErl'],
                f"{t['detTraf']} {erlangs:.2f}",
                f"{t['detGos']} {gos*100:.1f}%"
            ])

        # Determina a banda por chamada
        bw_map = {"711": 87.2, "729": 31.2, "Opus": 50.0, "OPUS": 50.0}
        bw_per_call = next((bw for key, bw in bw_map.items() if key in codec), 50.0)

        # Formatação do Resultado
        total_bw = channels * bw_per_call
        bw_string = f"{(total_bw / 1000):.2f} Mbps" if total_bw > 1000 else f"{total_bw:.2f} kbps"

        self.lbl_res_channels.configure(text=str(channels))
        self.lbl_res_bw.configure(text=bw_string)
        
        details.extend([
            f"\n{t['detMult']}"
        ])
        
        self.lbl_res_details.configure(text="\n".join(details), text_color=("gray20", "gray90"))

    # ==========================================
    # BUILD: DIAL PLAN FRAME
    # ==========================================
    def build_dialplan_frame(self):
        self.dialplan_frame.grid_columnconfigure(0, weight=1)
        self.dialplan_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(self.dialplan_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        ctk.CTkLabel(header, textvariable=self.text_vars['dpTitle'], font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        
        # Country Selection
        sel_frame = ctk.CTkFrame(header, fg_color="transparent")
        sel_frame.pack(side="right")
        
        ctk.CTkLabel(sel_frame, textvariable=self.text_vars['dpSelCountry']).pack(side="left", padx=10)
        
        self.countries = sorted([{"id": k, "name": v["name"], "code": v["code"]} for k, v in self.dialplan_data.items()], key=lambda x: x["name"])
        self.country_options = [f"{c['name']} (+{c['code']})" for c in self.countries]
        
        self.combo_country = ctk.CTkComboBox(sel_frame, values=self.country_options, command=self._update_dialplan_view, width=250)
        self.combo_country.pack(side="left")
        
        if self.country_options:
            # Selecionar Africa do Sul ou o primeiro
            idx = next((i for i, c in enumerate(self.countries) if c['id'] == 'south_africa'), 0)
            self.combo_country.set(self.country_options[idx])
        
        # Content Scroll
        self.dp_scroll = ctk.CTkScrollableFrame(self.dialplan_frame, fg_color="transparent")
        self.dp_scroll.grid(row=1, column=0, sticky="nsew")
        self.dp_scroll.grid_columnconfigure(0, weight=1)
        
        # Sub-frames
        self.dp_outbound_frame = ctk.CTkFrame(self.dp_scroll, corner_radius=15)
        self.dp_outbound_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.dp_outbound_frame.grid_columnconfigure(0, weight=1)
        
        self.dp_tollfree_frame = ctk.CTkFrame(self.dp_scroll, corner_radius=15)
        self.dp_tollfree_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.dp_tollfree_frame.grid_columnconfigure(0, weight=1)
        
        self.dp_emergency_frame = ctk.CTkFrame(self.dp_scroll, corner_radius=15)
        self.dp_emergency_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.dp_emergency_frame.grid_columnconfigure(0, weight=1)
        
        if self.country_options:
            self._update_dialplan_view(self.combo_country.get())

    def _update_dialplan_view(self, choice):
        t = LOCALES[self.lang]
        country_id = next((c['id'] for c in self.countries if f"{c['name']} (+{c['code']})" == choice), None)
        if not country_id or country_id not in self.dialplan_data: return
        
        data = self.dialplan_data[country_id]
        outbound = [o for o in data.get("outbound", []) if o.get("type") not in ['Toll Free', 'Toll']]
        tollfree = [o for o in data.get("outbound", []) if o.get("type") in ['Toll Free', 'Toll']]
        emergencies = data.get("emergency", [])
        
        # Clear Outbound
        for widget in self.dp_outbound_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.dp_outbound_frame, text=t['dpOutbound'], text_color=("#2563eb", "#60a5fa"), font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15, padx=15, anchor="w")
        
        if outbound:
            # Table Header
            th_frame = ctk.CTkFrame(self.dp_outbound_frame, fg_color="transparent")
            th_frame.pack(fill="x", padx=15, pady=(0, 10))
            th_frame.grid_columnconfigure((0,1,2), weight=1)
            ctk.CTkLabel(th_frame, text=t['dpDigitMap'], font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(th_frame, text=t['dpCallType'], font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(th_frame, text=t['dpDesc'], font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w")
            
            # Table Rows
            for i, row in enumerate(outbound):
                tr_frame = ctk.CTkFrame(self.dp_outbound_frame, fg_color=("gray90", "gray20") if i%2==0 else "transparent")
                tr_frame.pack(fill="x", padx=15, pady=2)
                tr_frame.grid_columnconfigure((0,1,2), weight=1)
                
                ctk.CTkLabel(tr_frame, text=row.get("map", ""), font=ctk.CTkFont(family="monospace")).grid(row=0, column=0, sticky="w", pady=5, padx=5)
                c_type = row.get("type", "")
                lbl_type = ctk.CTkLabel(tr_frame, text=c_type, font=ctk.CTkFont(weight="bold"))
                if "Premium" in c_type: lbl_type.configure(text_color=("#2563eb", "#60a5fa"))
                lbl_type.grid(row=0, column=1, sticky="w", pady=5)
                ctk.CTkLabel(tr_frame, text=row.get("desc", ""), text_color=("gray30", "gray70")).grid(row=0, column=2, sticky="w", pady=5)
        
        # Clear Toll Free
        for widget in self.dp_tollfree_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.dp_tollfree_frame, text=t['dpTollFree'], text_color=("#16a34a", "#4ade80"), font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15, padx=15, anchor="w")
        
        if tollfree:
            for row in tollfree:
                item_frame = ctk.CTkFrame(self.dp_tollfree_frame, fg_color=("gray90", "gray20"))
                item_frame.pack(fill="x", padx=15, pady=5)
                
                left = ctk.CTkFrame(item_frame, fg_color="transparent")
                left.pack(side="left", padx=10, pady=10)
                ctk.CTkLabel(left, text=row.get("map", ""), font=ctk.CTkFont(family="monospace", weight="bold")).pack(anchor="w")
                if row.get("desc", "") and row.get("desc", "") != "-":
                    ctk.CTkLabel(left, text=row.get("desc", "").upper(), font=ctk.CTkFont(size=10), text_color=("gray40", "gray60")).pack(anchor="w")
                
                badge_color = ("#dcfce7", "#166534") if row.get("type") == "Toll Free" else ("#f1f5f9", "#334155")
                text_color = ("#16a34a", "#4ade80") if row.get("type") == "Toll Free" else ("#475569", "#94a3b8")
                
                badge = ctk.CTkFrame(item_frame, fg_color=badge_color, corner_radius=10)
                badge.pack(side="right", padx=10, pady=10)
                ctk.CTkLabel(badge, text=row.get("type", ""), text_color=text_color, font=ctk.CTkFont(size=12, weight="bold")).pack(padx=10, pady=2)
        else:
            ctk.CTkLabel(self.dp_tollfree_frame, text=t.get('dpNotConfigured', 'Não configurado.'), text_color=("gray40", "gray60")).pack(pady=(0, 15), padx=15, anchor="w")
            
        # Clear Emergency
        for widget in self.dp_emergency_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.dp_emergency_frame, text=t['dpEmerg'], text_color=("#dc2626", "#f87171"), font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 5), padx=15, anchor="w")
        ctk.CTkLabel(self.dp_emergency_frame, text=t['dpEmergDesc'], font=ctk.CTkFont(size=12), text_color=("gray40", "gray60")).pack(pady=(0, 15), padx=15, anchor="w")
        
        if emergencies:
            em_grid = ctk.CTkFrame(self.dp_emergency_frame, fg_color="transparent")
            em_grid.pack(fill="x", padx=15, pady=(0, 15))
            
            for i, em in enumerate(emergencies):
                col = i % 4
                row_idx = i // 4
                em_grid.grid_columnconfigure(col, weight=1)
                
                box = ctk.CTkFrame(em_grid, fg_color=("#fef2f2", "#450a0a"), corner_radius=10)
                box.grid(row=row_idx, column=col, padx=5, pady=5, sticky="ew")
                
                ctk.CTkLabel(box, text=em, font=ctk.CTkFont(size=20, weight="bold"), text_color=("#dc2626", "#f87171")).pack(pady=(10, 0))
                ctk.CTkLabel(box, text="EMERGENCY", font=ctk.CTkFont(size=10), text_color=("#dc2626", "#f87171")).pack(pady=(0, 10))
        else:
            ctk.CTkLabel(self.dp_emergency_frame, text=t['dpNoEmerg'], text_color=("gray40", "gray60")).pack(pady=(0, 15), padx=15, anchor="w")

if __name__ == "__main__":
    app = TelecomApp()
    app.mainloop()