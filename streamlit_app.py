import streamlit as st
from st_click_detector import click_detector
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
st.set_page_config(page_title="Veranstaltungs-Feedback",
                   layout="centered", initial_sidebar_state="collapsed",)

# Initialisierung der Session State Variablen
if 'header_text' not in st.session_state:
    st.session_state.header_text = "Wie fanden Sie die Veranstaltung?"
if 'positiv_clicks' not in st.session_state:
    st.session_state['positiv_clicks'] = 0
if 'neutral_clicks' not in st.session_state:
    st.session_state['neutral_clicks'] = 0
if 'negativ_clicks' not in st.session_state:
    st.session_state['negativ_clicks'] = 0
if 'votes' not in st.session_state:
    st.session_state['votes'] = {
        'Positiv': st.session_state['positiv_clicks'],
        'Neutral': st.session_state['neutral_clicks'],
        'Negativ': st.session_state['negativ_clicks']
    }
if 'event_title' not in st.session_state:
    st.session_state['event_title'] = "Veranstaltung"

# Titel und Logo
st.image("https://www.cas.dhbw.de/fileadmin/user_upload/Dateien_CAS/Medien/DHBW_CAS_LOGO_Sonderform.jpg", use_column_width=True)

# Header
st.header(st.session_state.header_text, anchor=False)

# HTML-Inhalt mit Bildern und Abstand
content = """
<div style='display: flex; gap: 2cm;'>
    <a href='#' id='Positiv'><img width='70%' src='https://em-content.zobj.net/source/apple/391/grinning-face_1f600.png'></a>
    <a href='#' id='Neutral'><img width='70%' src='https://em-content.zobj.net/source/apple/391/neutral-face_1f610.png'></a>
    <a href='#' id='Negativ'><img width='70%' src='https://em-content.zobj.net/source/apple/391/sad-but-relieved-face_1f625.png'></a>
</div>
"""

# Klick-Detektor verwenden
clicked = click_detector(content)

# Klickzähler aktualisieren
if clicked == 'Positiv':
    st.toast("Danke!", icon="✅")
    st.session_state['positiv_clicks'] += 1
elif clicked == 'Neutral':
    st.toast("Danke!", icon="✅")
    st.session_state['neutral_clicks'] += 1
elif clicked == 'Negativ':
    st.toast("Danke!", icon="✅")
    st.session_state['negativ_clicks'] += 1

# Aktualisiere Votes in Session State
st.session_state['votes'] = {
    'Positiv': st.session_state['positiv_clicks'],
    'Neutral': st.session_state['neutral_clicks'],
    'Negativ': st.session_state['negativ_clicks']
}

# Admin-Bereich
with st.sidebar:
    admin_password = st.text_input("Admin-Passwort", type="password")
    if admin_password == "ulrike":
        st.session_state.admin_view = True
    else:
        st.session_state.admin_view = False

    if st.session_state.admin_view:
        st.subheader("Admin-Bereich")

        # Ändern des Headers
        new_header_text = st.text_input(
            "Header-Text ändern:", st.session_state.header_text)

        if st.button("Header aktualisieren"):
            st.session_state.header_text = new_header_text
            st.success("Header aktualisiert!")
            st.experimental_rerun()

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
            st.session_state['positiv_clicks'] = 0
            st.session_state['neutral_clicks'] = 0
            st.session_state['negativ_clicks'] = 0
            st.success("Stimmen wurden zurückgesetzt!")

    # Anleitung (optional, kann über die Sidebar aktiviert werden)
    if st.checkbox("Anleitung anzeigen"):
        st.info("""
        Anleitung für Vollbildmodus:
        1. Öffnen Sie die App im Browser.
        2. Drücken Sie F11 für den Vollbildmodus.
        
        Hinweis: Der "Geführte Zugriff" ist eine iOS-spezifische Funktion und kann in Streamlit nicht direkt umgesetzt werden.
        """)