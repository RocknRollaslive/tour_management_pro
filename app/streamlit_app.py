import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# --- 1. CLOUD CONNECTION ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- 2. THE DESIGN SYSTEM ---
st.set_page_config(page_title="R&R LIVE", layout="centered", initial_sidebar_state="collapsed")

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
header { visibility: hidden; }
.stApp { background-color: #000000; color: #F4F1EB; font-family: 'Inter', sans-serif; }
h1, h2, h3, .bebas-header { font-family: 'Bebas Neue', cursive !important; text-transform: uppercase !important; letter-spacing: 2px !important; color: #F2B01E !important; }
div.stButton > button { background-color: #F2B01E !important; color: #000000 !important; font-family: 'Bebas Neue' !important; font-size: 16px !important; border-radius: 4px !important; border: none !important; height: 50px; width: 100%; line-height: 1.2; }
.action-card { background-color: #0A0A0A; border: 1px solid #1A1A1A; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.block-container { padding-bottom: 140px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE & SPLASH ---
if "splash_done" not in st.session_state:
    st.markdown("<div style='text-align: center; padding-top: 150px;'><h1>ROCK & ROLLA'S</h1><p style='color:#F2B01E; letter-spacing:10px;'>LIVE</p></div>", unsafe_allow_html=True)
    if st.button("ENTER APP"):
        st.session_state.splash_done = True
        st.rerun()
    st.stop()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- 4. PAGE: HOME ---
if st.session_state.current_page == "Home":
    st.markdown("<p style='color: #666; margin:0;'>GOOD MORNING, <span style='color:#F2B01E;'>DYLAN.</span></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-weight:bold;'>{datetime.now().strftime('%a, %b %d').upper()}</p>", unsafe_allow_html=True)
    st.info("Home dashboard logic goes here...")

# --- 5. PAGE: CALENDAR ---
elif st.session_state.current_page == "Calendar":
    st.title("MASTER CALENDAR")
    st.info("Calendar filtering and agenda view goes here...")

# --- 6. PAGE: THE ARTIST HUB (Tours) ---
elif st.session_state.current_page == "Tours":
    # LEVEL 1: LIST ARTISTS
    if "active_artist_id" not in st.session_state:
        st.title("THE ARTIST HUB")
        artists = supabase.table("artists").select("*").execute()
        
        if artists.data:
            for a in artists.data:
                if st.button(f"📂 {a['name'].upper()}", key=a['id']):
                    st.session_state.active_artist_id = a['id']
                    st.session_state.active_artist_name = a['name']
                    st.rerun()
        
        with st.expander("➕ New Artist"):
            new_name = st.text_input("Name")
            if st.button("Initialize"):
                supabase.table("artists").insert({"name": new_name}).execute()
                st.rerun()

    # LEVEL 2: LIST PROJECTS (Tours)
    elif "active_tour_id" not in st.session_state:
        st.title(f"ARTIST: {st.session_state.active_artist_name}")
        if st.button("← BACK TO HUB"):
            del st.session_state.active_artist_id; st.rerun()
        
        st.divider()
        st.subheader("Active Projects")
        # Placeholder for project selection
        if st.button("THEATER TOUR '26"):
            st.session_state.active_tour_id = "TT26"
            st.rerun()

    # LEVEL 3: OPEN 10 FOLDERS
    else:
        st.title(f"PROJECT: THEATER TOUR '26")
        if st.button("← EXIT PROJECT"):
            del st.session_state.active_tour_id; st.rerun()
        
        folders = st.tabs(["DASHBOARD", "LOG", "FINANCE", "LOGISTICS", "CREW", "MERCH", "PRODUCTION", "VIP", "SUPPORT", "GEAR"])
        with folders[0]:
            st.write("Full Finance/Logistics/Crew code from streamlit.py goes here.")

# --- 7. PAGE: MORE (Account & Settings) ---
elif st.session_state.current_page == "More":
    st.title("ACCOUNT & SETTINGS")
    
    with st.container(border=True):
        st.markdown("<p class='bebas-header'>USER PROFILE</p>", unsafe_allow_html=True)
        st.write(f"**Logged in as:** Dylan")
        st.write(f"**Role:** Super Admin")
        st.button("Edit Profile")

    st.write("")
    with st.container(border=True):
        st.markdown("<p class='bebas-header'>APP SETTINGS</p>", unsafe_allow_html=True)
        st.toggle("Push Notifications", value=True)
        st.toggle("Offline Mode", value=False)
        st.selectbox("Default Currency", ["GBP (£)", "EUR (€)", "USD ($)"])

    st.write("")
    if st.button("🚪 LOG OUT"):
        st.session_state.clear()
        st.rerun()

# --- 8. BOTTOM NAVIGATION ---
st.write("") 
n1, n2, n3, n4 = st.columns(4)
if n1.button("🏠\nHOME"): st.session_state.current_page = "Home"; st.rerun()
if n2.button("📅\nCAL"): st.session_state.current_page = "Calendar"; st.rerun()
if n3.button("🎨\nHUB"): st.session_state.current_page = "Tours"; st.rerun()
if n4.button("🔍\nMORE"): st.session_state.current_page = "More"; st.rerun()