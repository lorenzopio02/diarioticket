import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Diario Interventi INAIL", page_icon="💻", layout="centered")

st.markdown("""
    <style>
    .main-header {
        background-color: #0B355B;
        padding: 15px;
        border-radius: 5px;
        color: white;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 20px;
    }
    </style>
    <div class="main-header">DIARIO INTERVENTI HELP DESK - INAIL</div>
""", unsafe_allow_html=True)

ticket = st.text_input("Numero Ticket (facoltativo)")
richiesta = st.text_area("1. Richiesta ricevuta (cosa ha segnalato l'utente)")
azioni = st.text_area("2. Cosa ho fatto (passaggi eseguiti)")
soluzione = st.text_area("3. Come ho risolto (esito finale)")

if st.button("Salva Intervento", type="primary"):
    if not (richiesta or azioni or soluzione):
        st.warning("Compila almeno uno dei campi principali prima di salvare.")
    else:
        # Ottiene data e ora correnti
        timestamp = datetime.now().strftime("%d/%m/%Y alle %H:%M")
        st.success(f"Intervento registrato con successo il {timestamp}!")
