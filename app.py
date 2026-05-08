import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Permitting FVT Sicilia 2026", layout="centered")

st.title("⚖️ Autorizzazioni Fotovoltaico Sicilia 2026")
st.markdown("---")

# Sezione Input
potenza = st.number_input("Inserisci Potenza Impianto (in kWp):", min_value=1, value=1000)
potenza_mw = potenza / 1000

tipo_suolo = st.selectbox("Destinazione d'uso area:", 
                          ["Agricola", "Industriale/Commerciale", "Cava/Discarica", "Tetto/Edificio"])

is_idonea = st.radio("L'area è classificata come IDONEA (Mappa Regionale 2025/26)?", ["Sì", "No"])

# Logica Decisionale
if st.button("Verifica Iter"):
    risultato = ""
    colore = "blue"
    
    # Logica Industriale/Cave
    if tipo_suolo in ["Industriale/Commerciale", "Cava/Discarica"]:
        if potenza_mw <= 5: risultato = "DILA (Edilizia Libera)"
        elif potenza_mw <= 12 and is_idonea == "Sì": risultato = "PAS (Accelerata)"
        else: risultato = "AU (Autorizzazione Unica)"
        
    # Logica Agricola
    elif tipo_suolo == "Agricola":
        if is_idonea == "Sì":
            if potenza_mw <= 1: risultato = "DILA"
            elif potenza_mw <= 12: risultato = "PAS (Accelerata)"
            else: risultato = "AU"
        else:
            if potenza_mw <= 1: risultato = "PAS (Ordinaria)"
            else: risultato = "AU"
    
    # Output
    st.success(f"L'iter da seguire è: **{risultato}**")
    
    # Accortezze speciali (DL Bollette 2026)
    st.info("**Accortezze Tecniche:**")
    if is_idonea == "Sì":
        st.write("- ✅ Applichi costi di connessione standard (DL Bollette 2026).")
    if potenza_mw >= 10:
        st.write("- ⚠️ Obbligo di V.I.A. (Valutazione Impatto Ambientale) regionale in Sicilia.")