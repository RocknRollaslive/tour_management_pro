import streamlit as st
import pandas as pd
from datetime import datetime
import io  # <--- ADD THIS LINE

st.set_page_config(page_title="R&R LIVE", layout="centered", initial_sidebar_state="collapsed")

# 1. DESIGN SYSTEM - Locked in a variable so it cannot leak
css_string = """
<style>
[data-testid="stSidebar"] { display: none; }
header { visibility: hidden; }
.stApp { background-color: #000000; color: #F4F1EB; font-family: 'Inter', sans-serif; }
h1, h2, h3, .bebas-header { font-family: 'Bebas Neue', cursive !important; text-transform: uppercase !important; letter-spacing: 2px !important; color: #F2B01E !important; }
div.stButton > button { background-color: #F2B01E !important; color: #000000 !important; font-family: 'Bebas Neue' !important; font-size: 16px !important; border-radius: 4px !important; border: none !important; height: 50px; width: 100%; line-height: 1.2; }
.action-card { background-color: #0A0A0A; border: 1px solid #1A1A1A; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.alert-banner { background-color: #CC1E1E; color: white; padding: 10px; border-radius: 4px; font-weight: bold; margin-bottom: 15px; }
.tour-card { background-color: #000000; margin-bottom: 20px; border: 1px solid #1A1A1A; display: flex; flex-direction: column; }
.tour-card img { width: 100%; height: 200px; object-fit: cover; filter: grayscale(100%); }
.tour-info { padding: 15px 0px; }
.stTabs [data-baseweb="tab-list"] { background-color: #000000 !important; }
.stTabs [data-baseweb="tab"] { font-family: 'Bebas Neue'; color: #444 !important; font-size: 18px !important; }
.stTabs [aria-selected="true"] { color: #F2B01E !important; border-bottom: 3px solid #F2B01E !important; }
.block-container { padding-bottom: 140px; }
</style>
"""

# Inject fonts and styles
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown(css_string, unsafe_allow_html=True)

# 2. AUTH / SPLASH
if "splash_done" not in st.session_state:
    st.markdown("<div style='text-align: center; padding-top: 150px;'><h1>ROCK & ROLLA'S</h1><p style='color:#F2B01E; letter-spacing:10px;'>LIVE</p></div>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    if col_b.button("ENTER APP"):
        st.session_state.splash_done = True
        st.rerun()
    st.stop()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# 3. PAGE: HOME
if st.session_state.current_page == "Home":
    col_greet, col_id = st.columns([4, 1])
    with col_greet:
        st.markdown("<p style='color: #666; margin:0;'>GOOD MORNING, <span style='color:#F2B01E;'>LOUIS.</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight:bold;'>{datetime.now().strftime('%a, %b %d').upper()}</p>", unsafe_allow_html=True)
    with col_id:
        st.markdown("<div style='background:#F2B01E; color:black; width:40px; height:40px; border-radius:50%; text-align:center; line-height:40px; font-weight:bold; float:right;'>LS</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.6, 1])
    with col_left:
        st.markdown("<span style='background:#F2B01E; color:black; padding:2px 10px; font-family:Bebas Neue;'>TODAY</span>", unsafe_allow_html=True)
        
        # --- DYNAMIC DATA LOOKUP ---
        today_str = datetime.now().strftime('%Y-%m-%d')
        display_city = "LOCATION UNKNOWN" # Default if no data found
        
        # Check if we have imported data in memory
        if 'tour_data' in st.session_state:
            # We assume your main sheet is named 'Daily Log' or you can use the first sheet
            # Adjust 'Daily Log' to match your actual Excel tab name
            sheet_name = list(st.session_state.tour_data.keys())[0] 
            df = st.session_state.tour_data[sheet_name]
            
            # Ensure the Date column is in string format for easy matching
            df['Date_Str'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            
            # Find the row for today
            today_row = df[df['Date_Str'] == today_str]
            
            if not today_row.empty:
                city = today_row.iloc[0].get('City', 'Unknown City')
                country = today_row.iloc[0].get('Country', 'UK')
                display_city = f"{city.upper()}, {country.upper()}"
        
        st.markdown(f"<h2 style='margin:0; font-size:32px;'>{display_city}</h2>", unsafe_allow_html=True)
        
        # Schedule (You can eventually make this dynamic too!)
        sch = {"14:00": "LOAD IN", "17:00": "SOUNDCHECK", "19:00": "DOORS", "20:30": "SHOWTIME"}
        for t, v in sch.items():
            st.markdown(f"<p style='margin:4px 0;'><span style='color:#F2B01E; font-weight:bold;'>{t}</span> &nbsp; {v}</p>", unsafe_allow_html=True)
        st.markdown("<div class='alert-banner'>⚠️ DRIVER DELAY: +20 MIN</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<p style='font-size:11px; color:#666; font-weight:bold; margin-bottom:5px;'>SHARING</p>", unsafe_allow_html=True)
        with st.container(border=True):
            st.toggle("JB", value=True)
            st.toggle("SL", value=True)
            st.button("INVITE", key="inv_home")

    st.markdown("<p class='bebas-header'>QUICK ACTIONS</p>", unsafe_allow_html=True)
    
    # --- HERE IS PIECE 1: THE WIRED-UP BUTTONS ---
    q1, q2, q3 = st.columns([1, 1, 1.5])
    
    with q1:
        with st.popover("➕\nEVENT", use_container_width=True):
            st.markdown("**Create New Event**")
            
            # The crucial routing question
            event_type = st.selectbox("Event Type", ["Show", "Travel", "Promo", "Rehearsal", "Day Off"])
            link_tour = st.selectbox("Link to Tour?", ["None (Standalone Event)", "European Tour 2025", "Summer Festivals"])
            
            event_name = st.text_input("City / Venue / Name", placeholder="e.g., London - O2 Academy")
            event_date = st.date_input("Date")
            
            if st.button("Save Event", use_container_width=True):
                if link_tour == "None (Standalone Event)":
                    st.success(f"Standalone '{event_type}' saved to Calendar!")
                else:
                    st.success(f"Added to {link_tour} routing!")
                
    with q2:
        with st.popover("🤖\nIMPORT", use_container_width=True):
            st.markdown("**Import Master Data**")
            uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                        st.session_state.tour_data = {"CSV_Data": df}
                    else:
                        # This reads EVERY sheet in your Excel file into memory at once
                        st.session_state.tour_data = pd.read_excel(uploaded_file, sheet_name=None)
                    st.success("Successfully loaded into memory!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    
    with q3:
        st.markdown("<div class='action-card'><p style='font-size:12px; margin:0; color:#F2B01E;'>AI ASSIST BETA</p><p style='font-size:10px; color:#666;'>Forward info to add to calendar.</p></div>", unsafe_allow_html=True)

# 4. PAGE: CALENDAR
elif st.session_state.current_page == "Calendar":
    st.markdown("<h2 style='margin-bottom: 0px;'>MASTER CALENDAR</h2>", unsafe_allow_html=True)
    st.write("")
    
    # 1. THE CALENDAR TOGGLES (Google Calendar style filtering)
    st.markdown("<p style='font-size:12px; color:#666; font-weight:bold; margin-bottom:5px;'>VISIBLE CALENDARS</p>", unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.columns(4)
    show_tour = t1.toggle("🚌 Tour", value=True)
    show_me = t2.toggle("👤 Me", value=True)
    show_jb = t3.toggle("🎧 JB", value=False)
    show_sl = t4.toggle("🚐 SL", value=False)

    st.markdown("<hr style='border: 1px solid #1A1A1A; margin-top:5px;'>", unsafe_allow_html=True)

    # 2. VIEW SELECTION
    cal_tabs = st.tabs(["📋 COMBINED AGENDA", "👥 DAILY TEAM VIEW"])
    
    # --- TAB 1: THE BLENDED TIMELINE ---
    with cal_tabs[0]:
        st.markdown("<p style='color:#666; font-size:14px;'>Chronological list of all active calendars.</p>", unsafe_allow_html=True)
        
        # If Tour is toggled ON, and data is imported, show the tour dates
        if show_tour and 'tour_data' in st.session_state and 'Daily Log' in st.session_state.tour_data:
            df = st.session_state.tour_data['Daily Log'].dropna(subset=['Date']).copy()
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values(by='Date').head(3) # Just showing the next 3 for the prototype
            
            for index, row in df.iterrows():
                date_str = row['Date'].strftime('%a, %b %d').upper()
                st.markdown(f"""
                <div class='action-card' style='border-left: 4px solid #F2B01E;'>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='color:#F2B01E; font-weight:bold; font-size:14px;'>{date_str}</span>
                        <span style='background:#1A1A1A; padding:2px 8px; border-radius:4px; font-size:11px;'>TOUR</span>
                    </div>
                    <h3 style='margin:5px 0px 2px 0px;'>{row['City'].upper()}</h3>
                    <p style='margin:0; font-size:12px; color:#888;'>{row['Daytype']}</p>
                </div>
                """, unsafe_allow_html=True)
                
        # If "Me" is toggled ON, inject personal events
        if show_me:
            st.markdown("""
            <div class='action-card' style='border-left: 4px solid #4A90E2;'>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='color:#4A90E2; font-weight:bold; font-size:14px;'>THU, OCT 16</span>
                    <span style='background:#1A1A1A; padding:2px 8px; border-radius:4px; font-size:11px;'>PERSONAL</span>
                </div>
                <h3 style='margin:5px 0px 2px 0px;'>DENTIST APPT</h3>
                <p style='margin:0; font-size:12px; color:#888;'>London, UK - 09:00 AM</p>
            </div>
            """, unsafe_allow_html=True)

        if not show_tour and not show_me and not show_jb and not show_sl:
            st.warning("No calendars selected.")

    # --- TAB 2: THE SIDE-BY-SIDE GRID ---
    with cal_tabs[1]:
        st.markdown("<p style='color:#666; font-size:14px;'>Compare today's schedules side-by-side.</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:white;'>TODAY: {datetime.now().strftime('%b %d').upper()}</h3>", unsafe_allow_html=True)
        
        # Build dynamic columns based on who is toggled ON
        active_cals = []
        if show_me: active_cals.append(("ME", "#4A90E2", ["09:00 - Flight to LHR", "14:00 - Load In", "19:00 - Doors"]))
        if show_jb: active_cals.append(("JB", "#9013FE", ["10:00 - Pick up rental", "14:00 - Load In", "17:00 - Soundcheck"]))
        if show_sl: active_cals.append(("SL", "#50E3C2", ["08:00 - Bus Maintenance", "13:00 - Drive to Venue", "16:00 - Sleep in bunk"]))
        
        if len(active_cals) > 0:
            cols = st.columns(len(active_cals))
            for i, (name, color, events) in enumerate(active_cals):
                with cols[i]:
                    st.markdown(f"<div style='text-align:center; background:{color}; color:white; padding:5px; border-radius:4px; font-weight:bold; margin-bottom:10px;'>{name}</div>", unsafe_allow_html=True)
                    for event in events:
                        st.markdown(f"<div style='background:#111; padding:8px; border-radius:4px; margin-bottom:5px; font-size:12px; border-left:2px solid {color};'>{event}</div>", unsafe_allow_html=True)
        else:
            st.info("Select a crew member to view their daily schedule.")

# 5. PAGE: TOURS
elif st.session_state.current_page == "Tours":
    if "active_tour_id" not in st.session_state:
        st.markdown("<h1 style='font-size: 45px;'>PROJECTS</h1>", unsafe_allow_html=True)
        t_data = [
            {"id": "LS", "name": "LIEVEN SCHEIRE", "sub": "THEATER TOUR '26", "img": "https://images.unsplash.com/photo-1502680390469-be75c86b636f?w=800"},
            {"id": "FR", "name": "FESTIVAL RUN", "sub": "SUMMER '26", "img": "https://images.unsplash.com/photo-1459749411177-042180ce673c?w=800"}
        ]
        for t in t_data:
            st.markdown(f'<div class="tour-card"><img src="{t["img"]}"><div class="tour-info"><span class="bebas-header">{t["name"]}</span><br><span style="color:#666; font-size:12px;">{t["sub"]}</span></div></div>', unsafe_allow_html=True)
            if st.button(f"OPEN {t['name']}", key=f"btn_{t['id']}"):
                st.session_state.active_tour_id = t['id']
                st.session_state.active_tour_name = t['name']
                st.rerun()
    else:
        c1, c2 = st.columns([4, 1])
        c1.markdown(f"<h1>{st.session_state.active_tour_name}</h1>", unsafe_allow_html=True)
        if c2.button("EXIT"):
            del st.session_state.active_tour_id; st.rerun()
        
        folders = st.tabs(["DASHBOARD", "LOG", "FINANCE", "LOGISTICS", "CREW", "MERCH", "PRODUCTION", "VIP", "SUPPORT", "GEAR"])
        with folders[0]: # DASHBOARD SUBFOLDER
            st.markdown("<h2 style='margin-bottom: 0px;'>TOUR DASHBOARD</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>High-level financial and logistical overview.</p>", unsafe_allow_html=True)
            
            st.write("") # Spacer

            # --- MOCK DATA FOR PROTOTYPE ---
            # In a real app, these variables would be pulled directly from the other tabs' calculations.
            # For this prototype, we're hardcoding realistic numbers based on our previous discussions.
            total_expected_income = 150000.00
            total_actually_received = 45000.00
            
            total_logistics_cost = 26000.00
            total_crew_cost = 18500.00
            total_other_expenses = 12000.00 
            
            total_expenses = total_logistics_cost + total_crew_cost + total_other_expenses
            
            est_payout = total_expected_income - total_expenses

            # --- 1. FINANCIAL SUMMARY (The Big Numbers) ---
            st.markdown("<p class='bebas-header'>FINANCIAL STATUS</p>", unsafe_allow_html=True)
            
            # The "Est. Payout" gets the hero treatment
            st.markdown("<p style='color: #666; font-size: 14px; margin-bottom: 0px; font-weight: bold;'>ESTIMATED NET PAYOUT</p>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: #F2B01E; margin-top: 0px; font-size: 70px;'>£{est_payout:,.2f}</h1>", unsafe_allow_html=True)
            
            st.markdown("<hr style='border: 1px solid #1A1A1A; margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)
            
            # Breakdowns
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                st.metric("Total Income (Gross)", f"£{total_expected_income:,.2f}")
                st.markdown(f"<p style='color: #666; font-size: 12px; margin-top: -15px;'>Received: £{total_actually_received:,.2f}</p>", unsafe_allow_html=True)
            
            with col_f2:
                st.metric("Total Expenses", f"£{total_expenses:,.2f}")
                
            with col_f3:
                # Calculate margin percentage
                margin = (est_payout / total_expected_income) * 100 if total_expected_income > 0 else 0
                st.metric("Profit Margin", f"{margin:.1f}%")

            st.write("")
            st.write("")

            # --- 2. EXPENSE BREAKDOWN & LOGISTICS SNAPSHOT ---
            col_d1, col_d2 = st.columns([1.5, 1])
            
            with col_d1:
                st.markdown("<p class='bebas-header'>EXPENSE BREAKDOWN</p>", unsafe_allow_html=True)
                
                # A simple progress bar visualization for expenses
                st.markdown("<p style='font-size: 14px; margin-bottom: 5px;'>Logistics & Fleet</p>", unsafe_allow_html=True)
                st.progress(total_logistics_cost / total_expenses if total_expenses > 0 else 0)
                st.markdown(f"<p style='color: #F2B01E; font-size: 12px; text-align: right; margin-top: -10px;'>£{total_logistics_cost:,.2f}</p>", unsafe_allow_html=True)

                st.markdown("<p style='font-size: 14px; margin-bottom: 5px;'>Crew Payroll & PDs</p>", unsafe_allow_html=True)
                st.progress(total_crew_cost / total_expenses if total_expenses > 0 else 0)
                st.markdown(f"<p style='color: #F2B01E; font-size: 12px; text-align: right; margin-top: -10px;'>£{total_crew_cost:,.2f}</p>", unsafe_allow_html=True)

                st.markdown("<p style='font-size: 14px; margin-bottom: 5px;'>Other (Accommodation, Catering, etc.)</p>", unsafe_allow_html=True)
                st.progress(total_other_expenses / total_expenses if total_expenses > 0 else 0)
                st.markdown(f"<p style='color: #F2B01E; font-size: 12px; text-align: right; margin-top: -10px;'>£{total_other_expenses:,.2f}</p>", unsafe_allow_html=True)

            with col_d2:
                st.markdown("<p class='bebas-header'>TOUR VITALS</p>", unsafe_allow_html=True)
                
                # These would also be dynamic in a real app
                st.markdown("<div class='action-card'>", unsafe_allow_html=True)
                st.metric("Next Show", "Oct 23 - Stockholm")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='action-card'>", unsafe_allow_html=True)
                st.metric("Active Fleet", "62 Vehicles")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='action-card'>", unsafe_allow_html=True)
                st.metric("Touring Headcount", "24 Personnel")
                st.markdown("</div>", unsafe_allow_html=True)
        with folders[1]: # OPERATIONAL LOG FOLDER
            st.markdown("<h2 style='margin-bottom: 0px;'>DAILY OPERATIONAL LOG</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Track routing, day types, show categories, and tickets sold.</p>", unsafe_allow_html=True)
            st.write("")
            
            default_routing = pd.DataFrame([
                {"Date": pd.to_datetime('2025-10-12'), "City": "Dilbeek", "Country": "Belgium", "Venue": "Rehearsal Space", "Day Category": "Production Day", "Show Type": "N/A", "Capacity": 0, "Tickets": 0, "Distance": 0},
                {"Date": pd.to_datetime('2025-10-23'), "City": "Stockholm", "Country": "Sweden", "Venue": "Fryshuset", "Day Category": "Showday", "Show Type": "Headline", "Capacity": 1500, "Tickets": 1420, "Distance": 650},
                {"Date": pd.to_datetime('2025-10-24'), "City": "Oslo", "Country": "Norway", "Venue": "Vulkan Arena", "Day Category": "Showday", "Show Type": "Support", "Capacity": 800, "Tickets": 800, "Distance": 520},
                {"Date": pd.to_datetime('2025-10-26'), "City": "Copenhagen", "Country": "Denmark", "Venue": "Copenhell", "Day Category": "Showday", "Show Type": "Festival", "Capacity": 20000, "Tickets": 20000, "Distance": 400}
            ])
            
            edited_routing = st.data_editor(
                default_routing,
                num_rows="dynamic",
                column_config={
                    "Date": st.column_config.DateColumn("Date", required=True),
                    "City": st.column_config.TextColumn("City"),
                    "Country": st.column_config.TextColumn("Country"),
                    "Venue": st.column_config.TextColumn("Venue"),
                    "Day Category": st.column_config.SelectboxColumn("Day Category", options=["Production Day", "Techday", "Travelday", "Showday", "Fly In", "Day Off"]),
                    "Show Type": st.column_config.SelectboxColumn("Show Type", options=["Headline", "Support", "Festival", "Promo", "Corporate/Private", "N/A"]),
                    "Capacity": st.column_config.NumberColumn("Capacity", min_value=0, step=50),
                    "Tickets": st.column_config.NumberColumn("Tickets Sold", min_value=0, step=10),
                    "Distance": st.column_config.NumberColumn("Distance (km)", min_value=0, step=10)
                },
                use_container_width=True,
                hide_index=True
            )
            
            total_km = edited_routing["Distance"].sum()
            total_tickets = edited_routing["Tickets"].sum()
            st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            r1.metric("Total Tour Distance", f"{total_km:,} km")
            r2.metric("Total Tickets Sold", f"{total_tickets:,}")
        with folders[2]: # FINANCE SUBFOLDER
            st.markdown("<h2 style='margin-bottom: 0px;'>MASTER FINANCE & ACCOUNTING</h2>", unsafe_allow_html=True)
            
            # 1. Global Currency Selector
            base_currency = st.selectbox("Tour Base Currency", ["EUR (€)", "GBP (£)", "USD ($)", "SEK (kr)"], index=0)
            # Extract just the symbol (e.g., '€') for our UI metrics
            sym = base_currency.split(' ')[1].replace('(', '').replace(')', '')
            
            st.write("") # Spacer
            
            # 2. The 3 Financial Pillars
            fin_tabs = st.tabs(["📊 BUDGET PROJECTIONS", "💸 EXPENSE LEDGER", "💰 INCOME TRACKER"])
            
            # --- PILLAR 1: BUDGET PROJECTIONS ---
            with fin_tabs[0]:
                st.markdown("<p style='color:#666; font-size:14px;'>Set your estimated budgets per category to track against actual spend.</p>", unsafe_allow_html=True)
                
                default_budget = pd.DataFrame([
                    {"Category": "Logistics & Fleet", "Budgeted": 30000.00, "Notes": "Buses, Trucks, Flights"},
                    {"Category": "Crew Payroll & PDs", "Budgeted": 25000.00, "Notes": "Wages + Per Diems"},
                    {"Category": "Production & Tech", "Budgeted": 15000.00, "Notes": "Rentals, Backline"},
                    {"Category": "Accommodation", "Budgeted": 10000.00, "Notes": "Hotels, Day Rooms"},
                    {"Category": "Catering & Rider", "Budgeted": 5000.00, "Notes": "Venue catering, bus stock"},
                    {"Category": "Miscellaneous", "Budgeted": 2500.00, "Notes": "Buffer, Visas, Carnets"}
                ])
                
                edited_budget = st.data_editor(
                    default_budget,
                    num_rows="dynamic",
                    column_config={
                        "Category": st.column_config.TextColumn("Category", required=True),
                        "Budgeted": st.column_config.NumberColumn(f"Budgeted Amt ({sym})", min_value=0.0, step=500.0, format="%.2f"),
                        "Notes": st.column_config.TextColumn("Notes")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                total_budget = edited_budget["Budgeted"].sum()
                st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
                st.markdown("<p style='color: #666; font-size: 12px; margin-bottom: 0px; font-weight: bold;'>TOTAL PROJECTED BUDGET</p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: white; margin-top: 0px; font-size: 45px;'>{sym}{total_budget:,.2f}</h3>", unsafe_allow_html=True)

            # --- PILLAR 2: EXPENSE LEDGER (Moved & Upgraded) ---
            with fin_tabs[1]:
                col_e1, col_e2 = st.columns([2, 1])
                col_e1.markdown("<p style='color:#666; font-size:14px;'>Multi-currency tracking with automated FX conversion.</p>", unsafe_allow_html=True)
                
                # THE RECEIPT SCANNER / UPLOADER
                uploaded_receipt = col_e2.file_uploader("📸 Scan / Upload Receipt", type=["png", "jpg", "pdf"], help="Attach a photo of a receipt to the ledger.")
                if uploaded_receipt is not None:
                    col_e2.success(f"Attached: {uploaded_receipt.name}")
                
                default_ledger = pd.DataFrame([
                    {"Date": pd.to_datetime('2025-10-13'), "Vendor": "Hippocketwifi", "Category": "Miscellaneous", "Method": "Credit Card", "Curr": "EUR", "Local Amt": 353.00, "FX Rate": 1.00},
                    {"Date": pd.to_datetime('2025-11-17'), "Vendor": "Hotel Glasgow", "Category": "Accommodation", "Method": "Credit Card", "Curr": "GBP", "Local Amt": 744.38, "FX Rate": 1.13},
                ])
                
                edited_ledger = st.data_editor(
                    default_ledger,
                    num_rows="dynamic",
                    column_config={
                        "Date": st.column_config.DateColumn("Date", required=True),
                        "Vendor": st.column_config.TextColumn("Vendor / Supplier"),
                        "Category": st.column_config.SelectboxColumn("Category", options=["Logistics & Fleet", "Crew Payroll & PDs", "Production & Tech", "Accommodation", "Catering & Rider", "Miscellaneous"]),
                        "Method": st.column_config.SelectboxColumn("Payment", options=["Credit Card", "Bank Transfer", "Cash"]),
                        "Curr": st.column_config.SelectboxColumn("Curr", options=["EUR", "GBP", "SEK", "DKK", "NOK", "PLN", "CZK", "USD"]),
                        "Local Amt": st.column_config.NumberColumn("Local Amt", min_value=0.0, step=10.0, format="%.2f", required=True),
                        "FX Rate": st.column_config.NumberColumn("FX Rate", min_value=0.01, step=0.01, format="%.4f", required=True),
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                edited_ledger["Base Amount"] = edited_ledger["Local Amt"] * edited_ledger["FX Rate"]
                total_tour_expenses = edited_ledger["Base Amount"].sum()
                
                st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #666; font-size: 12px; margin-bottom: 0px; font-weight: bold;'>TOTAL ACTUAL SPEND ({base_currency})</p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: #CC1E1E; margin-top: 0px; font-size: 35px;'>{sym}{total_tour_expenses:,.2f}</h3>", unsafe_allow_html=True)

            # --- PILLAR 3: INCOME TRACKER (Moved & Upgraded) ---
            with fin_tabs[2]:
                col_i1, col_i2 = st.columns([2, 1])
                col_i1.markdown("<p style='color:#666; font-size:14px;'>Track incoming funds (Guarantees, Merch, Advances).</p>", unsafe_allow_html=True)
                
                # THE INVOICE UPLOADER
                uploaded_invoice = col_i2.file_uploader("📥 Upload Promoter Settlement", type=["pdf", "xlsx", "jpg"])
                if uploaded_invoice is not None:
                    col_i2.success(f"Attached: {uploaded_invoice.name}")
                
                default_income = pd.DataFrame([
                    {"Date": pd.to_datetime('2025-10-01'), "Source": "Promoter Advance (Dilbeek)", "Type": "Wire", "Amount": 2500.00, "Received": True},
                    {"Date": pd.to_datetime('2025-10-23'), "Source": "Merch Settlement (Stockholm)", "Type": "Cash", "Amount": 3450.00, "Received": False},
                ])
                
                edited_income = st.data_editor(
                    default_income,
                    num_rows="dynamic",
                    column_config={
                        "Date": st.column_config.DateColumn("Date", required=True),
                        "Source": st.column_config.TextColumn("Source / Payer"),
                        "Type": st.column_config.SelectboxColumn("Type", options=["Wire", "Cash", "Credit/Stripe"]),
                        "Amount": st.column_config.NumberColumn(f"Amount ({sym})", min_value=0.0, step=100.0, format="%.2f"),
                        "Received": st.column_config.CheckboxColumn("Received in Bank/Hand")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                total_expected = edited_income["Amount"].sum()
                total_received = edited_income[edited_income["Received"] == True]["Amount"].sum()
                
                st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
                i1, i2 = st.columns(2)
                i1.metric("Total Expected Income", f"{sym}{total_expected:,.2f}")
                i2.metric("Total Actually Received", f"{sym}{total_received:,.2f}")
        with folders[3]: # LOGISTICS SUBFOLDER
            st.subheader("Master Fleet Manifest")
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Scale from 1 van to a 60+ vehicle convoy.</p>", unsafe_allow_html=True)
            
            st.write("") # Spacer
            
            # 1. Expanded Fleet Data (Now with Vendors, Drivers, and Notes)
            default_fleet = pd.DataFrame(
                [
                    {"Vehicle": "Nightliner (Double)", "Vendor": "Beat The Street", "Driver": "Mike T.", "Qty": 27, "Daily Rate (£)": 1800, "Days": 14, "Notes": "Band + A-Party"},
                    {"Vehicle": "Articulated Truck", "Vendor": "Fly By Nite", "Driver": "TBD", "Qty": 30, "Daily Rate (£)": 600, "Days": 14, "Notes": "Production & LX"},
                    {"Vehicle": "Crew Van (9-Seater)", "Vendor": "Enterprise", "Driver": "JB / Self-Drive", "Qty": 5, "Daily Rate (£)": 250, "Days": 14, "Notes": "Pick up @ LHR"}
                ]
            )
            
            st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>EDIT FLEET MANIFEST</p>", unsafe_allow_html=True)
            
            # 2. Dynamic Data Editor (Expanded Columns)
            edited_fleet = st.data_editor(
                default_fleet,
                num_rows="dynamic",
                column_config={
                    "Vehicle": st.column_config.TextColumn("Vehicle Type", required=True),
                    "Vendor": st.column_config.TextColumn("Rental Company"),
                    "Driver": st.column_config.TextColumn("Driver(s)"),
                    "Qty": st.column_config.NumberColumn("Qty", min_value=1, step=1, required=True),
                    "Daily Rate (£)": st.column_config.NumberColumn("Daily Rate (£)", min_value=0, step=50, required=True),
                    "Days": st.column_config.NumberColumn("Active Days", min_value=1, step=1, required=True),
                    "Notes": st.column_config.TextColumn("Notes / Plates")
                },
                use_container_width=True,
                hide_index=True
            )
            
            # 3. Mass Scale Math
            edited_fleet["Line Total"] = edited_fleet["Qty"] * edited_fleet["Daily Rate (£)"] * edited_fleet["Days"]
            total_fleet_cost = int(edited_fleet["Line Total"].sum())
            total_vehicles = int(edited_fleet["Qty"].sum())
            
            st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
            
            # 4. Display Massive Scale Metrics
            st.markdown("<p style='color: #666; font-size: 12px; margin-bottom: 0px; font-weight: bold;'>TOTAL FLEET COST</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color: white; margin-top: 0px; font-size: 45px;'>£{total_fleet_cost:,}</h3>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='color: #F2B01E; font-size: 16px; font-weight: bold;'>MANAGING {total_vehicles} ACTIVE VEHICLES</p>", unsafe_allow_html=True)
        with folders[4]: # CREW MATRIX SUBFOLDER
            st.subheader("Master Crew Manifest")
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Track personnel, day rates, retainers, and per diems.</p>", unsafe_allow_html=True)
            
            st.write("") # Spacer
            
            # 1. Default Crew Data
            default_crew = pd.DataFrame([
                {"Name": "Louis", "Role": "Tour Manager", "Rate Type": "Weekly", "Rate (£)": 1500, "Qty (Days/Wks)": 4, "Per Diem (£)": 30, "PD Days": 28},
                {"Name": "JB", "Role": "FOH Audio", "Rate Type": "Day Rate", "Rate (£)": 250, "Qty (Days/Wks)": 28, "Per Diem (£)": 30, "PD Days": 28},
                {"Name": "Mike T.", "Role": "Driver", "Rate Type": "Project", "Rate (£)": 4500, "Qty (Days/Wks)": 1, "Per Diem (£)": 30, "PD Days": 28}
            ])
            
            st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>EDIT CREW & PAYROLL</p>", unsafe_allow_html=True)
            
            # 2. Interactive Crew Grid
            edited_crew = st.data_editor(
                default_crew,
                num_rows="dynamic",
                column_config={
                    "Name": st.column_config.TextColumn("Name", required=True),
                    "Role": st.column_config.SelectboxColumn("Role", options=["Band", "Tour Manager", "Production Manager", "FOH Audio", "Monitors", "LX/Lighting", "Backline", "Merch", "Driver", "VIP Rep"]),
                    "Rate Type": st.column_config.SelectboxColumn("Rate Type", options=["Day Rate", "Weekly", "Project"]),
                    "Rate (£)": st.column_config.NumberColumn("Rate (£)", min_value=0, step=50),
                    "Qty (Days/Wks)": st.column_config.NumberColumn("Qty", min_value=1, step=1, help="Number of days, weeks, or 1 for project"),
                    "Per Diem (£)": st.column_config.NumberColumn("Daily PD (£)", min_value=0, step=5),
                    "PD Days": st.column_config.NumberColumn("Total PD Days", min_value=0, step=1)
                },
                use_container_width=True,
                hide_index=True
            )
            
            # 3. Automated Payroll Math
            # Calculate wages (Rate * Qty) and PDs (Daily PD * PD Days)
            edited_crew["Total Wages"] = edited_crew["Rate (£)"] * edited_crew["Qty (Days/Wks)"]
            edited_crew["Total PDs"] = edited_crew["Per Diem (£)"] * edited_crew["PD Days"]
            
            total_payroll = edited_crew["Total Wages"].sum()
            total_pds = edited_crew["Total PDs"].sum()
            headcount = len(edited_crew)
            
            st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
            
            # 4. Display Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Active Headcount", f"{headcount} Touring")
            c2.metric("Total Per Diems", f"£{total_pds:,.2f}")
            c3.metric("Total Payroll", f"£{total_payroll:,.2f}")
            
            st.markdown("<p style='color: #666; font-size: 12px; margin-bottom: 0px; font-weight: bold;'>TOTAL CREW COST (WAGES + PDS)</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color: white; margin-top: 0px; font-size: 45px;'>£{(total_payroll + total_pds):,.2f}</h3>", unsafe_allow_html=True)
        with folders[5]: # MERCH SUBFOLDER
            st.markdown("<h2 style='margin-bottom: 0px;'>MERCHANDISE OPERATIONS</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Track inventory, nightly settlements, and spend-per-head.</p>", unsafe_allow_html=True)
            
            st.write("")
            
            # Sub-tabs for Merch operations
            merch_tabs = st.tabs(["🛒 NIGHTLY SETTLEMENT", "📦 MASTER INVENTORY", "📋 NIGHTLY COUNTS"])
            
            # --- TAB 1: NIGHTLY SETTLEMENT ---
            with merch_tabs[0]:
                col_m1, col_m2 = st.columns([2, 1])
                selected_show = col_m1.selectbox("Select Show to Settle", ["Oct 23 - Stockholm (Fryshuset)", "Oct 24 - Oslo (Vulkan Arena)", "Oct 25 - Aarhus (Train)", "Oct 29 - Hamburg (Docks)"])
                col_m2.write("")
                col_m2.button("📥 EXPORT SETTLEMENT")
                
                st.markdown("<p class='bebas-header'>SHOW VITALS</p>", unsafe_allow_html=True)
                v1, v2, v3 = st.columns(3)
                actual_attendance = v1.number_input("Actual Attendance (Drop Count)", min_value=1, value=1420)
                venue_cut = v2.number_input("Venue Concession Cut (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
                tax_rate = v3.number_input("VAT / Tax (%)", min_value=0.0, max_value=100.0, value=25.0, step=1.0)
                
                st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px; margin-top:20px;'>ENTER NIGHTLY SALES</p>", unsafe_allow_html=True)
                
                sales_data = pd.DataFrame([
                    {"Item": "Tour Tee - Black", "Price (€)": 35.00, "Sold": 120},
                    {"Item": "Tour Tee - White", "Price (€)": 35.00, "Sold": 85},
                    {"Item": "Hoodie - Logo", "Price (€)": 65.00, "Sold": 40},
                    {"Item": "Poster - Signed", "Price (€)": 20.00, "Sold": 150},
                    {"Item": "Tote Bag", "Price (€)": 15.00, "Sold": 60}
                ])
                
                edited_sales = st.data_editor(
                    sales_data,
                    column_config={
                        "Item": st.column_config.TextColumn("Item", disabled=True),
                        "Price (€)": st.column_config.NumberColumn("Price (€)", disabled=True),
                        "Sold": st.column_config.NumberColumn("Qty Sold", min_value=0, step=1)
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                edited_sales["Gross"] = edited_sales["Price (€)"] * edited_sales["Sold"]
                total_gross = edited_sales["Gross"].sum()
                
                sph = total_gross / actual_attendance if actual_attendance > 0 else 0
                gross_ex_tax = total_gross / (1 + (tax_rate / 100))
                venue_fee = gross_ex_tax * (venue_cut / 100)
                net_artist = gross_ex_tax - venue_fee
                
                st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
                
                sm1, sm2, sm3 = st.columns(3)
                sm1.metric("Total Gross Sales", f"€{total_gross:,.2f}")
                sm2.metric("Venue Fee (Est.)", f"€{venue_fee:,.2f}")
                sm3.metric("Artist Net (Ex-Tax)", f"€{net_artist:,.2f}")
                
                st.markdown("<p style='color: #666; font-size: 12px; margin-bottom: 0px; font-weight: bold; margin-top:15px;'>SPEND PER HEAD (€/HEAD)</p>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: #F2B01E; margin-top: 0px; font-size: 45px;'>€{sph:.2f}</h3>", unsafe_allow_html=True)
                
            # --- TAB 2: MASTER INVENTORY ---
            with merch_tabs[1]:
                st.markdown("<p style='color:#666; font-size:14px;'>Master item list and base pricing.</p>", unsafe_allow_html=True)
                
                inventory_df = pd.DataFrame([
                    {"Item": "Tour Tee - Black", "Category": "Apparel", "Cost to Make (€)": 8.50, "Sell Price (€)": 35.00},
                    {"Item": "Tour Tee - White", "Category": "Apparel", "Cost to Make (€)": 8.50, "Sell Price (€)": 35.00},
                    {"Item": "Hoodie - Logo", "Category": "Apparel", "Cost to Make (€)": 18.00, "Sell Price (€)": 65.00},
                    {"Item": "Poster - Signed", "Category": "Accessories", "Cost to Make (€)": 2.00, "Sell Price (€)": 20.00},
                    {"Item": "Tote Bag", "Category": "Accessories", "Cost to Make (€)": 3.50, "Sell Price (€)": 15.00}
                ])
                
                st.data_editor(
                    inventory_df,
                    num_rows="dynamic",
                    column_config={
                        "Cost to Make (€)": st.column_config.NumberColumn("Cost (€)", format="%.2f"),
                        "Sell Price (€)": st.column_config.NumberColumn("Price (€)", format="%.2f")
                    },
                    use_container_width=True,
                    hide_index=True
                )

            # --- TAB 3: NIGHTLY STOCK COUNTS ---
            with merch_tabs[2]:
                st.markdown("<p style='color:#666; font-size:14px;'>Track physical count-in, adds, comps, and count-out.</p>", unsafe_allow_html=True)
                
                stock_show = st.selectbox("Select Show for Count", ["Oct 23 - Stockholm (Fryshuset)", "Oct 24 - Oslo (Vulkan Arena)", "Oct 25 - Aarhus (Train)", "Oct 29 - Hamburg (Docks)"], key="count_selector")
                
                stock_df = pd.DataFrame([
                    {"Item": "Tour Tee - Black", "Count In": 880, "Adds": 0, "Comps": 2, "Count Out": 758},
                    {"Item": "Tour Tee - White", "Count In": 415, "Adds": 0, "Comps": 0, "Count Out": 330},
                    {"Item": "Hoodie - Logo", "Count In": 160, "Adds": 0, "Comps": 1, "Count Out": 119},
                    {"Item": "Poster - Signed", "Count In": 850, "Adds": 0, "Comps": 5, "Count Out": 695},
                    {"Item": "Tote Bag", "Count In": 440, "Adds": 0, "Comps": 0, "Count Out": 380}
                ])
                
                edited_stock = st.data_editor(
                    stock_df,
                    column_config={
                        "Item": st.column_config.TextColumn("Item", disabled=True),
                        "Count In": st.column_config.NumberColumn("Count In", min_value=0),
                        "Adds": st.column_config.NumberColumn("Adds", min_value=0),
                        "Comps": st.column_config.NumberColumn("Comps", min_value=0),
                        "Count Out": st.column_config.NumberColumn("Count Out", min_value=0)
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Math: (In + Adds) - Comps - Out = Sold
                edited_stock["Calculated Sold"] = edited_stock["Count In"] + edited_stock["Adds"] - edited_stock["Comps"] - edited_stock["Count Out"]
                
                st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
                st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>CALCULATED SALES FROM STOCK</p>", unsafe_allow_html=True)
                
                # Display just the final tally
                st.dataframe(edited_stock[["Item", "Calculated Sold"]], hide_index=True, use_container_width=True)
        with folders[6]: # PRODUCTION SUBFOLDER
            st.subheader("Production Advance & Tech Specs")
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Daily technical requirements, local crew calls, and power specs.</p>", unsafe_allow_html=True)
            
            st.write("") # Spacer
            
            # 1. Day Selector & Quick Actions
            col_sd1, col_sd2 = st.columns([2, 1])
            show_selector = col_sd1.selectbox(
                "Select Show Date", 
                ["Oct 23 - Stockholm (Fryshuset)", "Oct 24 - Oslo (Vulkan Arena)", "Oct 25 - Aarhus (Train)", "Oct 29 - Hamburg (Docks)"]
            )
            col_sd2.write("") # Alignment spacer
            col_sd2.button("📥 MASTER RIDER")
            
            st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
            
            # 2. The Run of Show (ROS)
            st.markdown("<p class='bebas-header'>RUN OF SHOW (ROS)</p>", unsafe_allow_html=True)
            ros_cols = st.columns(4)
            ros_cols[0].metric("Load In", "12:00")
            ros_cols[1].metric("Rigging/LX", "13:30")
            ros_cols[2].metric("Soundcheck", "16:00")
            ros_cols[3].metric("Doors", "19:00")
            
            st.write("")
            
            # 3. Heavy Tech Departments (Expandable to save space)
            with st.expander("🔊 AUDIO (FOH & MONITORS)", expanded=True):
                st.markdown("**System:** L-Acoustics K2 or d&b J-Series (Provided by Local)")
                st.markdown("**Control FOH:** DiGiCo SD12 (Touring)")
                st.markdown("**Control MON:** Yamaha Rivage PM7 (Touring)")
                st.markdown("**Power Required:** 1x 63A 3-Phase (Audio Only) @ Stage Left")
                st.markdown("**Multicore:** 2x Cat6E shielded runs from FOH to Stage Left")
                
            with st.expander("💡 LIGHTING & VIDEO (LX/SFX)", expanded=False):
                st.markdown("**Console:** GrandMA3 Light (Touring)")
                st.markdown("**Floor Package:** 12x Robe MegaPointe, 8x GLP JDC1")
                st.markdown("**Video Wall:** 5m x 3m ROE Visual (Pitch 3.9mm) - Flown upstage center")
                st.markdown("**Power Required:** 1x 125A 3-Phase (Lighting), 1x 32A 3-Phase (Video)")
                
            with st.expander("🛠 LOCAL CREW CALL", expanded=False):
                st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>EDIT LOCAL CALL TIMES</p>", unsafe_allow_html=True)
                crew_df = pd.DataFrame([
                    {"Department": "Load-in/Out Pushers", "Call Time": "12:00 / 23:30", "Qty": 8, "Status": "Confirmed"},
                    {"Department": "Riggers (Up/Down)", "Call Time": "12:00 / 23:00", "Qty": 4, "Status": "Confirmed"},
                    {"Department": "LX Hands", "Call Time": "13:00 / 23:00", "Qty": 2, "Status": "Pending"},
                    {"Department": "Audio Hands", "Call Time": "13:00 / 23:00", "Qty": 2, "Status": "Confirmed"}
                ])
                # We use data_editor here so you can actively check off confirmations
                st.data_editor(
                    crew_df,
                    column_config={
                        "Status": st.column_config.SelectboxColumn("Status", options=["Confirmed", "Pending", "Cancelled"])
                    },
                    hide_index=True, 
                    use_container_width=True
                )
            
            with st.expander("📐 STAGING & BARRICADE", expanded=False):
                st.markdown("**Stage Size:** 12m wide x 8m deep minimum")
                st.markdown("**Clearance:** 6m minimum from stage deck to grid")
                st.markdown("**Barricade:** Mojo style, curved, 1.5m from stage edge")
                st.markdown("**Risers:** 1x 8x8ft rolling drum riser (0.5m high) on dark carpet")
        with folders[7]: # VIP SUBFOLDER
            st.markdown("<h2 style='margin-bottom: 0px;'>VIP MANAGEMENT</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Track nightly VIP sales, capacities, and net profit.</p>", unsafe_allow_html=True)
            
            st.write("")
            vip_tabs = st.tabs(["🌟 NIGHTLY SETTLEMENT", "🎟️ MASTER VIP TIERS"])
            
            # --- TAB 1: NIGHTLY SETTLEMENT ---
            with vip_tabs[0]:
                col_v1, col_v2 = st.columns([2, 1])
                selected_vip_show = col_v1.selectbox(
                    "Select Show to Settle", 
                    ["Oct 23 - Stockholm (Fryshuset)", "Oct 24 - Oslo (Vulkan Arena)", "Oct 25 - Aarhus (Train)"], 
                    key="vip_show"
                )
                col_v2.write("")
                col_v2.button("📥 EXPORT VIP LIST")
                
                st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>ENTER NIGHTLY TIER SALES</p>", unsafe_allow_html=True)
                
                # Dynamic grid: Add rows only for the tiers active at this specific show
                vip_sales_df = pd.DataFrame([
                    {"VIP Tier": "Meet & Greet", "Tickets Sold": 30, "Price (€)": 150.00},
                    {"VIP Tier": "Early Entry", "Tickets Sold": 20, "Price (€)": 75.00}
                ])
                
                edited_vip_sales = st.data_editor(
                    vip_sales_df,
                    num_rows="dynamic",
                    column_config={
                        "VIP Tier": st.column_config.SelectboxColumn("VIP Tier", options=["Meet & Greet", "Early Entry", "Acoustic Set", "Side Stage Experience"], required=True),
                        "Tickets Sold": st.column_config.NumberColumn("Tickets Sold", min_value=0),
                        "Price (€)": st.column_config.NumberColumn("Ticket Price (€)", format="%.2f")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # Math calculations
                edited_vip_sales["Gross"] = edited_vip_sales["Tickets Sold"] * edited_vip_sales["Price (€)"]
                total_vip_tickets = edited_vip_sales["Tickets Sold"].sum()
                total_vip_gross = edited_vip_sales["Gross"].sum()
                
                st.markdown("<hr style='border: 1px solid #1A1A1A;'>", unsafe_allow_html=True)
                v1, v2 = st.columns(2)
                v1.metric("Total VIP Tickets", int(total_vip_tickets))
                v2.metric("Total VIP Gross", f"€{total_vip_gross:,.2f}")

            # --- TAB 2: MASTER VIP TIERS ---
            with vip_tabs[1]:
                st.markdown("<p style='color:#666; font-size:14px;'>Define all possible VIP packages and their deliverables.</p>", unsafe_allow_html=True)
                
                vip_tiers_df = pd.DataFrame([
                    {"Tier Name": "Meet & Greet", "Base Price (€)": 150.00, "Global Cap": 50, "Deliverables": "Photo, Signed Poster, Laminate"},
                    {"Tier Name": "Early Entry", "Base Price (€)": 75.00, "Global Cap": 100, "Deliverables": "Early Access, Laminate"},
                    {"Tier Name": "Acoustic Set", "Base Price (€)": 200.00, "Global Cap": 20, "Deliverables": "Private 3-song set, Q&A, Photo"}
                ])
                
                st.data_editor(
                    vip_tiers_df,
                    num_rows="dynamic",
                    column_config={
                        "Tier Name": st.column_config.TextColumn("Tier Name", required=True),
                        "Base Price (€)": st.column_config.NumberColumn("Base Price (€)", format="%.2f"),
                        "Global Cap": st.column_config.NumberColumn("Default Cap", min_value=0),
                        "Deliverables": st.column_config.TextColumn("Deliverables Included")
                    },
                    use_container_width=True,
                    hide_index=True
                )
        with folders[8]: # SUPPORT ACTS SUBFOLDER
            st.markdown("<h2 style='margin-bottom: 0px;'>SUPPORT ACTS</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Manage support band logistics, fees, and scheduling.</p>", unsafe_allow_html=True)
            
            st.write("")
            
            st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>SUPPORT BAND LOGISTICS</p>", unsafe_allow_html=True)
            support_df = pd.DataFrame([
                {"Band Name": "The Openers", "Agreed Fee (€)": 500.00, "Load In": "15:00", "Soundcheck": "17:00", "Set Time": "19:30 - 20:00", "Notes": "Sharing drum shell"}
            ])
            
            st.data_editor(
                support_df,
                num_rows="dynamic",
                column_config={
                    "Band Name": st.column_config.TextColumn("Support Act"),
                    "Agreed Fee (€)": st.column_config.NumberColumn("Fee/Buyout (€)", min_value=0.0, format="%.2f"),
                    "Load In": st.column_config.TextColumn("Load In Time"),
                    "Soundcheck": st.column_config.TextColumn("Soundcheck"),
                    "Set Time": st.column_config.TextColumn("Set Time"),
                    "Notes": st.column_config.TextColumn("Production Notes")
                },
                use_container_width=True,
                hide_index=True
            )

        with folders[9]: # GEAR / ADVANCE SUBFOLDER (Shifted to index 9)
            st.markdown("<h2 style='margin-bottom: 0px;'>GEAR & PRODUCTION ADVANCE</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#666; font-size:14px; margin-top:-10px;'>Master inventory split by Buy, Rent, and Bring.</p>", unsafe_allow_html=True)
            
            st.write("")
            
            gear_tabs = st.tabs(["🛒 BUY GEAR", "📦 RENT GEAR", "🎸 BRING GEAR (OWNED)"])
            
            with gear_tabs[0]:
                st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>PURCHASED FOR TOUR</p>", unsafe_allow_html=True)
                buy_gear_df = pd.DataFrame([
                    {"Category": "Audio", "Item": "Wireless Mic Systems", "Qty": 2, "Vendor": "Thomann", "Date": "2025-10-01", "Cost/Unit": 500.00, "Curr": "EUR"}
                ])
                
                edited_buy = st.data_editor(
                    buy_gear_df,
                    num_rows="dynamic",
                    column_config={
                        "Category": st.column_config.SelectboxColumn("Category", options=["Audio", "Lighting", "Backline", "Video", "Misc"]),
                        "Item": st.column_config.TextColumn("Item"),
                        "Qty": st.column_config.NumberColumn("Qty", min_value=1),
                        "Vendor": st.column_config.TextColumn("Vendor/Source"),
                        "Date": st.column_config.TextColumn("Purchase Date"),
                        "Cost/Unit": st.column_config.NumberColumn("Cost/Unit", format="%.2f"),
                        "Curr": st.column_config.SelectboxColumn("Curr.", options=["EUR", "GBP", "USD"])
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                edited_buy["Total (€)"] = edited_buy["Qty"] * edited_buy["Cost/Unit"]
                st.metric("Total Buy Gear Spend", f"€{edited_buy['Total (€)'].sum():,.2f}")

            with gear_tabs[1]:
                st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>RENTED FOR TOUR</p>", unsafe_allow_html=True)
                rent_gear_df = pd.DataFrame([
                    {"Category": "Lighting", "Item": "GrandMA3 Console", "Qty": 1, "Vendor": "PRG", "Return Date": "2025-11-30", "Cost/Unit": 1500.00, "Curr": "EUR"}
                ])
                
                edited_rent = st.data_editor(
                    rent_gear_df,
                    num_rows="dynamic",
                    column_config={
                        "Category": st.column_config.SelectboxColumn("Category", options=["Audio", "Lighting", "Backline", "Video", "Misc"]),
                        "Item": st.column_config.TextColumn("Item"),
                        "Qty": st.column_config.NumberColumn("Qty", min_value=1),
                        "Vendor": st.column_config.TextColumn("Vendor/Source"),
                        "Return Date": st.column_config.TextColumn("Return Date (Out)"),
                        "Cost/Unit": st.column_config.NumberColumn("Cost/Unit", format="%.2f"),
                        "Curr": st.column_config.SelectboxColumn("Curr.", options=["EUR", "GBP", "USD"])
                    },
                    use_container_width=True,
                    hide_index=True
                )
                edited_rent["Total (€)"] = edited_rent["Qty"] * edited_rent["Cost/Unit"]
                st.metric("Total Rent Gear Spend", f"€{edited_rent['Total (€)'].sum():,.2f}")
                
            with gear_tabs[2]:
                st.markdown("<p style='color:#F2B01E; font-size:12px; font-weight:bold; margin-bottom:5px;'>OWNED / BAND BACKLINE</p>", unsafe_allow_html=True)
                bring_gear_df = pd.DataFrame([
                    {"Category": "Backline", "Item": "Fender Twin Reverb", "Qty": 2, "Owner": "Marlies Bocken", "Notes": "Needs new tubes"}
                ])
                
                st.data_editor(
                    bring_gear_df,
                    num_rows="dynamic",
                    column_config={
                        "Category": st.column_config.SelectboxColumn("Category", options=["Audio", "Lighting", "Backline", "Video", "Misc"]),
                        "Item": st.column_config.TextColumn("Item"),
                        "Qty": st.column_config.NumberColumn("Qty", min_value=1),
                        "Owner": st.column_config.TextColumn("Owner"),
                        "Notes": st.column_config.TextColumn("Notes")
                    },
                    use_container_width=True,
                    hide_index=True
                )

# 6. BOTTOM NAVIGATION
st.write("") 
n1, n2, n3, n4 = st.columns(4)
if n1.button("🏠\nHOME"): st.session_state.current_page = "Home"; st.rerun()
if n2.button("📅\nCAL"): st.session_state.current_page = "Calendar"; st.rerun()
if n3.button("🚌\nTOURS"): st.session_state.current_page = "Tours"; st.rerun()
if n4.button("🔍\nMORE"): st.session_state.current_page = "More"; st.rerun()