import streamlit as st
import pandas as pd
from datetime import date
import base64

# Funktion zum Herunterladen des CSV
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

# Seitenkonfiguration
st.set_page_config(page_title="Veranstaltungs-Feedback", layout="centered", initial_sidebar_state="collapsed",)

# Initialisierung der Session State Variablen
if 'event_title' not in st.session_state:
    st.session_state.event_title = "Unsere tolle Veranstaltung..."
if 'header_text' not in st.session_state:
    st.session_state.header_text = "Wie fanden Sie die Veranstaltung?"
if 'votes' not in st.session_state:
    st.session_state.votes = {"Positiv": 0, "Neutral": 0, "Negativ": 0}
if 'admin_view' not in st.session_state:
    st.session_state.admin_view = False

# Titel und Logo
st.image("https://www.cas.dhbw.de/fileadmin/user_upload/Dateien_CAS/Medien/DHBW_CAS_LOGO_Sonderform.jpg", use_column_width=True)

# Veranstaltungstitel und Header
st.title(st.session_state.event_title, anchor=False)
st.header(st.session_state.header_text, anchor=False)

# Smileys für Feedback
col1, col2, col3 = st.columns(3)

if col1.button("", icon="😀", use_container_width=True):
    st.toast("Danke!", icon="✅")
    st.session_state.votes["Positiv"] += 1
if col2.button("", icon="😐", use_container_width=True):
    st.toast("Danke!", icon="✅")
    st.session_state.votes["Neutral"] += 1
if col3.button("", icon="😥", use_container_width=True):
    st.toast("Danke!", icon="✅")
    st.session_state.votes["Negativ"] += 1

# Admin-Bereich
with st.sidebar:
    admin_password = st.text_input("Admin-Passwort", type="password")
    if admin_password == "ulrike":
        st.session_state.admin_view = True
    else:
        st.session_state.admin_view = False

    if st.session_state.admin_view:
        st.subheader("Admin-Bereich")
        
        # Ändern des Veranstaltungstitels und Headers
        new_event_title = st.text_input("Veranstaltungstitel ändern:", st.session_state.event_title)
        new_header_text = st.text_input("Header-Text ändern:", st.session_state.header_text)
        
        if st.button("Titel und Header aktualisieren"):
            st.session_state.event_title = new_event_title
            st.session_state.header_text = new_header_text
            st.success("Titel und Header wurden aktualisiert!")
            st.rerun()
        
        # Anzeige der aktuellen Stimmen
        st.write("Aktuelle Stimmen:")
        for key, value in st.session_state.votes.items():
            st.write(f"{key}: {value}")
        
        # CSV-Export
        if st.button("Ergebnisse exportieren"):
            current_date = date.today().isoformat()
            df = pd.DataFrame({
            "Veranstaltung": [st.session_state.event_title] * 3,
            "Datum": [current_date] * 3,
            "Bewertung": list(st.session_state.votes.keys()),
            "Anzahl": list(st.session_state.votes.values())
            })
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="CSV herunterladen",
                data=csv,
                file_name=f'Feedback_{st.session_state.event_title}_{current_date}.csv',
                mime='text/csv'
            )
            
        # Reset-Funktion
        if st.button("Stimmen zurücksetzen"):
            st.session_state.votes = {"Positiv": 0, "Neutral": 0, "Negativ": 0}
            st.success("Stimmen wurden zurückgesetzt!")

    # Anleitung (optional, kann über die Sidebar aktiviert werden)
    if st.checkbox("Anleitung anzeigen"):
        st.info("""
        Anleitung für Vollbildmodus:
        1. Öffnen Sie die App im Browser.
        2. Drücken Sie F11 für den Vollbildmodus.
        
        Hinweis: Der "Geführte Zugriff" ist eine iOS-spezifische Funktion und kann in Streamlit nicht direkt umgesetzt werden.
        """)