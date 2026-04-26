import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# --- 1. CLOUD CONNECTION ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- 2. THE DESIGN SYSTEM (From your streamlit.py) ---
st.set_page_config(page_title="R&R LIVE", layout="centered", initial_sidebar_state="collapsed")

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #1A1A1A; }
.stApp { background-color: #000000; color: #F4F1EB; font-family: 'Inter', sans-serif; }
h1, h2, h3, .bebas-header { font-family: 'Bebas Neue', cursive !important; text-transform: uppercase !important; letter-spacing: 2px !important; color: #F2B01E !important; }
div.stButton > button { background-color: #F2B01E !important; color: #000000 !important; font-family: 'Bebas Neue' !important; font-size: 16px !important; border-radius: 4px !important; height: 50px; width: 100%; }
.action-card { background-color: #0A0A0A; border: 1px solid #1A1A1A; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SPLASH SCREEN ---
if "splash_done" not in st.session_state:
    st.markdown("<div style='text-align: center; padding-top: 150px;'><h1>ROCK & ROLLA'S</h1><p style='color:#F2B01E; letter-spacing:10px;'>LIVE</p></div>", unsafe_allow_html=True)
    if st.button("ENTER APP"):
        st.session_state.splash_done = True
        st.rerun()
    st.stop()

# Initialize Navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- 4. NAVIGATION LOGIC ---
# (Home and Calendar code goes here - keeping it exactly like your streamlit.py)

# --- 5. THE ARTIST HUB (Replacing old "Tours") ---
if st.session_state.current_page == "Tours":
    if "active_artist_id" not in st.session_state:
        st.title("THE ARTIST HUB")
        
        # Pull Artists from Supabase
        artists_resp = supabase.table("artists").select("*").execute()
        
        for artist in artists_resp.data:
            if st.button(f"📂 {artist['name'].upper()}", key=f"art_{artist['id']}"):
                st.session_state.active_artist_id = artist['id']
                st.session_state.active_artist_name = artist['name']
                st.rerun()
                
    elif "active_tour_id" not in st.session_state:
        # Show Projects for the selected Artist
        st.subheader(f"PROJECTS: {st.session_state.active_artist_name}")
        if st.button("← BACK TO HUB"):
            del st.session_state.active_artist_id; st.rerun()
            
        # Mocking the Tour selection for now
        if st.button("THEATER TOUR '26"):
            st.session_state.active_tour_id = "TT26"
            st.rerun()
            
    else:
        # OPEN THE 10 FOLDERS (Finance, Crew, etc.)
        st.title(st.session_state.active_artist_name)
        if st.button("← EXIT PROJECT"):
            del st.session_state.active_tour_id; st.rerun()
            
        tabs = st.tabs(["DASHBOARD", "LOG", "FINANCE", "LOGISTICS", "CREW", "MERCH", "PRODUCTION", "VIP", "SUPPORT", "GEAR"])
        with tabs[0]:
            st.write("Your Dashboard Code Goes Here...")

# --- 6. BOTTOM NAV (Same as before) ---
st.write("") 
n1, n2, n3 = st.columns(3)
if n1.button("🏠\nHOME"): st.session_state.current_page = "Home"; st.rerun()
if n2.button("📅\nCAL"): st.session_state.current_page = "Calendar"; st.rerun()
if n3.button("🎨\nHUB"): st.session_state.current_page = "Tours"; st.rerun()