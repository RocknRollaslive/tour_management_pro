import streamlit as st
from supabase import create_client, Client

# --- 1. DATABASE CONNECTION ---
# This pulls the keys from your Streamlit Secrets
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Rock & Rolla's LIVE", layout="wide")

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.markdown(f"👤 **User:** Dylan")
if url:
    st.sidebar.success("Cloud Brain Connected")

menu = st.sidebar.radio("NAVIGATE", ["The Hub", "Routing", "Finance", "Gear"])

# --- 4. THE HUB (ARTISTS) ---
if menu == "The Hub":
    st.title("🎨 The Artist Hub")
    
    # Form to add a new artist
    with st.expander("➕ Add New Artist"):
        artist_name = st.text_input("Artist Name")
        if st.button("Create Hub"):
            if artist_name:
                supabase.table("artists").insert({"name": artist_name}).execute()
                st.success(f"Hub created for {artist_name}!")
                st.rerun()

    st.divider()
    
    # List existing artists from Supabase
    st.subheader("Your Artists")
    artists_resp = supabase.table("artists").select("*").execute()
    
    if artists_resp.data:
        for artist in artists_resp.data:
            st.button(f"📂 {artist['name']}", key=artist['id'])
    else:
        st.info("No artists found. Add your first one above!")

# --- 5. OTHER SECTIONS (Placeholders for now) ---
elif menu == "Routing":
    st.title("🗺️ Routing & Shows")
    st.info("This is where your Cities and Dates will live.")

elif menu == "Finance":
    st.title("💸 Tour Finance")
    st.info("Deal memos and financial tracking coming soon.")

elif menu == "Gear":
    st.title("⚙️ Gear Inventory")
    st.info("Inventory will sync to the Artist Hub from here.")