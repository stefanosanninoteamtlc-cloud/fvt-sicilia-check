import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Permitting FVT Sicilia 2026", layout="wide")

st.title("⚖️ Expert System: Iter Autorizzativo FVT Sicilia 2026")
st.sidebar.header("Dati del Progetto")

# --- INPUT UTENTE ---
potenza_kw = st.sidebar.number_input("Potenza Impianto (in kWp):", min_value=1, value=1000)
potenza_mw = potenza_kw / 1000

tipo_suolo = st.sidebar.selectbox("Destinazione d'uso area:", 
                                 ["Agricola", "Industriale/Commerciale", "Cava/Discarica", "Tetto/Edificio"])

is_idonea = st.sidebar.radio("L'area è classificata come IDONEA (Mappa 2026)?", ["Sì", "No"])
# Aggiunta link alla mappa nella sidebar
url_mappa = "https://www.sitr.regione.sicilia.it/portal/apps/webappviewer/index.html?id=f3f54ac44ae04a3584885eaaf0b84d70" # URL generico del geoportale ARC GIS
st.sidebar.markdown(f"[📍Scoprilo qui! - Consulta la Mappa Ufficiale]({url_mappa})")


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
