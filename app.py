import streamlit as st
from datetime import datetime
import pandas as pd
import os

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

# Gestione del file di salvataggio locale
DB_FILE = "interventi.csv"

def carica_dati():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=["Data", "Ora", "Ticket", "Richiesta", "Azioni", "Soluzione"])

df_storico = carica_dati()

# Form di inserimento
st.subheader("📝 Registra Nuovo Intervento")
with st.form("form_intervento", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        data_intervento = st.date_input("Data intervento", value=datetime.now())
    with col2:
        ora_intervento = st.time_input("Ora intervento", value=datetime.now())

    ticket = st.text_input("Numero Ticket (facoltativo)")
    richiesta = st.text_area("1. Richiesta ricevuta (cosa ha segnalato l'utente)")
    azioni = st.text_area("2. Cosa ho fatto (passaggi eseguiti)")
    soluzione = st.text_area("3. Come ho risolto (esito finale)")

    submitted = st.form_submit_button("Salva Intervento", type="primary")
    
    if submitted:
        if not (richiesta or azioni or soluzione):
            st.warning("Compila almeno uno dei campi principali prima di salvare.")
        else:
            nuova_riga = pd.DataFrame([{
                "Data": data_intervento.strftime("%d/%m/%Y"),
                "Ora": ora_intervento.strftime("%H:%M"),
                "Ticket": ticket if ticket else "N/D",
                "Richiesta": richiesta,
                "Azioni": azioni,
                "Soluzione": soluzione
            }])
            df_storico = pd.concat([df_storico, nuova_riga], ignore_index=True)
            df_storico.to_csv(DB_FILE, index=False)
            st.success("Intervento registrato con successo e aggiunto allo storico!")

st.markdown("---")
st.subheader("📋 Storico Interventi")

if not df_storico.empty:
    # Mostra la tabella con gli ultimi interventi in cima
    st.dataframe(df_storico.iloc[::-1], use_container_width=True)
    
    # Pulsante per scaricare il file Excel/CSV
    csv = df_storico.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Scarica Storico in Excel (CSV)",
        data=csv,
        file_name='diario_interventi_inail.csv',
        mime='text/csv',
    )
else:
    st.info("Nessun intervento registrato finora. Compila il modulo sopra per iniziare!")
