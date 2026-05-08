from PIL import Image
import streamlit as st

# Carica l'immagine dal file locale
logo = Image.open("logonuovo.png")

# Configurazione Pagina
st.set_page_config(page_title="Permitting FVT Sicilia 2026", layout="wide")

# Header con Logo e Titolo
col_l, col_t = st.columns([0.15, 0.85])
with col_l:
    st.image(logo, width=150)
with col_t:
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
    
    tipo_impianto = st.sidebar.selectbox("Tipologia di Impianto:", 
                                        ["Fotovoltaico Standard (A terra)", "Agrivoltaico (Base)", "Agrivoltaico Avanzato"])
    
    # --- LOGICA DI CALCOLO ---
    if st.button("Analizza Progetto"):
        iter_finale = ""
        via_info = ""
        via_colore = "info"
        note = []
    
        # 1. LOGICA REGIME AUTORIZZATIVO (AU, PAS, DILA)
        if tipo_suolo in ["Industriale/Commerciale", "Cava/Discarica"]:
            if potenza_mw <= 5:
                iter_finale = "DILA (Edilizia Libera)"
            elif potenza_mw <= 12 and is_idonea == "Sì":
                iter_finale = "PAS (Procedura Accelerata)"
            else:
                iter_finale = "AU (Autorizzazione Unica)"
            note.append("✅ In queste aree l'agrivoltaico non è necessario, si procede con standard industriale.")
    
        elif tipo_suolo == "Agricola":
            if is_idonea == "Sì":
                if tipo_impianto == "Agrivoltaico Avanzato":
                    if potenza_mw <= 1:
                        iter_finale = "DILA (Edilizia Libera)"
                    elif potenza_mw <= 12:
                        iter_finale = "PAS (Accelerata)"
                    else:
                        iter_finale = "AU"
                    note.append("💎 L'Agrivoltaico Avanzato in area idonea ha la massima priorità di connessione (DL Bollette 2026).")
                elif tipo_impianto == "Agrivoltaico (Base)":
                    iter_finale = "PAS" if potenza_mw <= 12 else "AU"
                    note.append("🌾 Richiesta continuità agricola certificata secondo DGR Sicilia 27/2025.")
                else:
                    iter_finale = "PAS" if potenza_mw <= 1 else "AU"
                    note.append("⚠️ Il fotovoltaico standard a terra su suolo agricolo è fortemente limitato.")
            else:
                iter_finale = "PAS (Iter Ordinario)" if potenza_mw <= 1 else "AU (Iter Ordinario)"
                note.append("🛑 Area NON Idonea: Rischio elevato di parere negativo dalla Soprintendenza.")

        # 2. LOGICA V.I.A. (VALUTAZIONE IMPATTO AMBIENTALE) - FOCUS MASE 2026
        if potenza_mw < 10:
            via_info = "Verifica di Assoggettabilità (Screening) Regionale"
            via_colore = "info"
        elif potenza_mw >= 10:
            via_info = "V.I.A. Statale (MASE - Ministero dell'Ambiente)"
            via_colore = "warning"
            note.append("🏛️ **Nota Esperta:** Per impianti ≥ 10 MW in Sicilia, la competenza è attratta dal MASE (Commissione PNIEC-PNRR) per garantire la priorità nazionale.")
    
        # --- OUTPUT RISULTATI ---
        st.subheader(f"Iter Autorizzativo: **{iter_finale}**")
        
        # Box specifico per la VIA
        if via_colore == "warning":
            st.warning(f"🔔 **Competenza Ambientale:** {via_info}")
        else:
            st.info(f"📋 **Competenza Ambientale:** {via_info}")
        
        for nota in note:
            st.markdown(f"- {nota}")
    
        st.markdown("---")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Potenza Totale", f"{potenza_mw} MW")
        with col_res2:
            st.metric("Autorizzazione", iter_finale)

with col_info:
    st.markdown("### 🏛️ Competenza V.I.A. 2026")
    st.write("""
    In base alle ultime semplificazioni e alla prassi operativa in Sicilia:
    - **Sotto 10 MW:** Competenza Regionale (Screening).
    - **Sopra 10 MW:** Competenza **MASE** (VIA Statale). 
    
    *I progetti sopra i 10 MW vengono gestiti a Roma per accelerare gli obiettivi PNIEC, bypassando le lungaggini delle commissioni regionali.*
    """)
    
    st.markdown("---")
    st.markdown("### 📍 Mappe Ufficiali")
    st.markdown(f"[📍 Mappa SITR Sicilia](https://www.sitr.regione.sicilia.it/portal/apps/webappviewer/index.html?id=f3f54ac44ae04a3584885eaaf0b84d70)")
    st.markdown(f"[📍 Mappa Aree Idonee GSE](https://areeidonee.gse.it/)")
    st.markdown(f"[💡 Mappa Accelerazione GSE](https://areeaccelerazione.gse.it/)")
    
    st.markdown("---")
    st.markdown("### ℹ️ Info & Normative")
    st.write("**DL Bollette 2026:** Semplificazione costi connessione e priorità di rete per impianti in aree idonee e di accelerazione.")
    
    st.write("""
    **Differenza Aree:**
    - **Idonea:** Iter semplificato e pareri non vincolanti.
    - **Accelerazione:** 'Fast-track' amministrativo con tempi dimezzati.
    """)
