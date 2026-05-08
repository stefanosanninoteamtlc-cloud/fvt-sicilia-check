from PIL import Image
import streamlit as st

# Carica l'immagine dal file locale
logo = Image.open("logonuovo.png")

# Configurazione Pagina
st.set_page_config(page_title="Permitting FVT Sicilia 2026", layout="wide")

st.image(logo, width=100)
st.markdown("""
        <style>
            .title-text {
                display: flex;
                align-items: center;
                height: 80px; /* Deve essere simile alla width/altezza del logo */
                margin: 0;
            }
        </style>
        <h1 class="title-text">Expert System: Iter Autorizzativo FVT Sicilia 2026</h1>
    """, unsafe_allow_html=True)
st.title("Expert System: Iter Autorizzativo FVT Sicilia 2026")

# Creiamo due colonne: la prima occupa il 70% dello spazio, la seconda il 30%
col_principale, col_info = st.columns([0.7, 0.3])

with col_principale:
    st.sidebar.header("Dati del Progetto")
    
    # --- INPUT UTENTE ---
    potenza_kw = st.sidebar.number_input("Potenza Impianto (in kWp):", min_value=1, value=1000)
    potenza_mw = potenza_kw / 1000
    
    tipo_suolo = st.sidebar.selectbox("Destinazione d'uso area:", 
                                     ["Agricola", "Industriale/Commerciale", "Cava/Discarica", "Tetto/Edificio"])
    
    is_idonea = st.sidebar.radio("L'area è classificata come IDONEA (Mappa 2026)?", ["Sì", "No"])
    
    # NUOVO INPUT: Tipologia Impianto
    tipo_impianto = st.sidebar.selectbox("Tipologia di Impianto:", 
                                        ["Fotovoltaico Standard (A terra)", "Agrivoltaico (Base)", "Agrivoltaico Avanzato"])
    
    # --- LOGICA DI CALCOLO ---
    if st.button("Analizza Progetto"):
        iter_finale = ""
        note = []
    
        # 1. LOGICA AREE INDUSTRIALI / CAVE
        if tipo_suolo in ["Industriale/Commerciale", "Cava/Discarica"]:
            if potenza_mw <= 5:
                iter_finale = "DILA (Edilizia Libera)"
            elif potenza_mw <= 12 and is_idonea == "Sì":
                iter_finale = "PAS (Procedura Accelerata)"
            else:
                iter_finale = "AU (Autorizzazione Unica)"
            note.append("✅ In queste aree l'agrivoltaico non è necessario, si procede con standard industriale.")
    
        # 2. LOGICA AREE AGRICOLE
        elif tipo_suolo == "Agricola":
            if is_idonea == "Sì":
                # Caso Area Idonea
                if tipo_impianto == "Agrivoltaico Avanzato":
                    if potenza_mw <= 1:
                        iter_finale = "DILA (Edilizia Libera)"
                    elif potenza_mw <= 12:
                        iter_finale = "PAS (Accelerata)"
                    else:
                        iter_finale = "AU"
                    note.append("💎 L'Agrivoltaico Avanzato in area idonea ha la massima priorità di connessione (DL Bollette 2026).")
                
                elif tipo_impianto == "Agrivoltaico (Base)":
                    if potenza_mw <= 12:
                        iter_finale = "PAS"
                    else:
                        iter_finale = "AU"
                    note.append("🌾 Richiesta continuità agricola certificata secondo DGR Sicilia 27/2025.")
                
                else: # Standard a terra
                    if potenza_mw <= 1:
                        iter_finale = "PAS"
                    else:
                        iter_finale = "AU"
                    note.append("⚠️ Il fotovoltaico standard a terra su suolo agricolo è fortemente limitato se non 'avanzato'.")
    
            else:
                # Caso Area NON Idonea
                if potenza_mw <= 1:
                    iter_finale = "PAS (Iter Ordinario)"
                else:
                    iter_finale = "AU (Iter Ordinario)"
                note.append("🛑 Area NON Idonea: Rischio elevato di parere negativo dalla Soprintendenza BB.CC.AA.")
    
        # --- OUTPUT RISULTATI ---
        st.subheader(f"Risultato: {iter_finale}")
        
        for nota in note:
            st.info(nota)
    
        # Widget riassuntivo per Developer
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Potenza", f"{potenza_mw} MW")
        with col2:
            st.metric("Regime", iter_finale)

with col_info:
    st.markdown("### ℹ️ Scopri la classificazione delle tue aree")
    # Aggiunta link alla mappa
    url_mappa1 = "https://www.sitr.regione.sicilia.it/portal/apps/webappviewer/index.html?id=f3f54ac44ae04a3584885eaaf0b84d70" # URL generico del geoportale ARC GIS
    url_mappa2 = "https://areeidonee.gse.it/" # URL del geoportale aree idonee del GSE
    url_mappa3 = "https://areeaccelerazione.gse.it/" # URL del geoportale aree di accelerazione del GSE
    st.markdown(f"[📍Mappa Ufficiale del SITR]({url_mappa1})")
    st.markdown(f"[📍Mappa Ufficiale GSE, con aree idonee dichiarate dalla regione (fino ad adesso)]({url_mappa2})")
    st.markdown(f"[💡Mappa Ufficiale GSE, per capire (nel caso in cui l'area è idonea) se fa anche parte delle aree di accelerazione]({url_mappa3})")

    
    # Questa è la tua "Sidebar Destra" informativa
    st.markdown("### ℹ️ Info & Normative")
    st.write("""
    **DL Bollette 2026**  
    Le nuove norme semplificano i costi di connessione per le aree idonee.  
    
    ---
    
    **Soglie Autorizzative**  
    * **DILA:** < 1MW (Agri Avanzato)  
    * **PAS:** 1-12 MW (Aree Idonee)  
    * **AU:** > 12 MW  
    
    ---
    
    **Documentazione**  
    Assicurati di avere i titoli di possesso del terreno pronti per il caricamento sul portale SUER.
    """)
    st.write("""La differenza è importante, perché spesso vengono confuse ma giuridicamente non sono la stessa cosa.
    In sintesi:
    -Area idonea:	area dove gli impianti FER sono considerati compatibili/favoriti
    -Area di accelerazione: sottoinsieme “premium” delle aree idonee con iter molto più rapido
    
    Quindi:
    tutte le aree di accelerazione sono (di fatto) aree idonee,
    ma non tutte le aree idonee sono aree di accelerazione.""")


