import streamlit as st
import requests

st.set_page_config(page_title="Railway System", page_icon="🚆", layout="wide")

# Initialize session state for bookings
if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# --- LUXURY DARK THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Lato:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0A192F !important;
        font-family: 'Lato', 'Lora', sans-serif !important;
        color: #E6F1FF !important;
    }

    /* Center Title and Subtitle */
    .title-container {
        text-align: center;
        padding-bottom: 20px;
    }
    
    .title-container h1 {
        color: #E6F1FF !important;
        font-family: 'Lora', serif !important;
    }

    /* Card Styling for Quick Info and Status */
    .info-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    .info-card h3 {
        color: #64FFDA !important;
        font-family: 'Lora', serif !important;
    }
    
    .info-card p {
        color: #E6F1FF !important;
    }

    /* Booking Status Boxes */
    .status-confirmed {
        background: rgba(100, 255, 218, 0.08);
        border: 1px solid #64FFDA;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: #E6F1FF !important;
    }
    
    .status-waiting {
        background: rgba(197, 160, 89, 0.08);
        border: 2px solid #C5A059;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: #E6F1FF !important;
        box-shadow: 0 0 15px rgba(197, 160, 89, 0.3);
    }

    /* Button alignment fix */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background: #D4A633 !important;
        border: none !important;
        color: #0A192F !important;
        font-weight: 600 !important;
        font-family: 'Lato', sans-serif !important;
    }
    
    div.stButton > button:hover {
        background: #E8B847 !important;
        box-shadow: 0 4px 12px rgba(212, 166, 51, 0.5) !important;
    }

    /* Input labels color */
    label {
        color: #E6F1FF !important;
        font-weight: 500 !important;
    }
    
    label p {
        color: #E6F1FF !important;
        font-weight: 500 !important;
    }
    
    /* Input fields styling */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] input {
        background-color: #1E1E1E !important;
        color: #E6F1FF !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stSelectbox"] input:focus {
        background-color: #1E1E1E !important;
        color: #E6F1FF !important;
        border: 2px solid #64FFDA !important;
        box-shadow: 0 0 12px rgba(100, 255, 218, 0.4) !important;
    }
    
    /* Subheader color */
    h3 {
        color: #64FFDA !important;
        font-family: 'Lora', serif !important;
    }
    
    /* Text colors */
    p, span, div {
        color: #E6F1FF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='title-container'><h1>🚆 Smart Railway Reservation System</h1><p style='color: #A8C9EF;'>Book your train tickets seamlessly</p></div>", unsafe_allow_html=True)

# --- MAIN FORM SECTION ---
# Adjusted ratios to give Passenger Info and Details more space
col1, col2, col3 = st.columns([1.5, 1.5, 1], gap="large")

with col1:
    st.subheader("👤 Passenger Info")
    name = st.text_input("Full Name", placeholder="Enter your name")
    age = st.number_input("Age", min_value=1, max_value=120, value=None, step=1)
    travel_date = st.date_input("Date of Travelling")

with col2:
    st.subheader("📋 Additional Details")
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    train_id = st.number_input("Train ID", min_value=1, max_value=100, value=None, step=1)
    col2_A, col2_B = st.columns(2)
    with col2_A:
        source = st.text_input("From (Source)", placeholder="e.g. New York")
    with col2_B:
        destination = st.text_input("To (Destination)", placeholder="e.g. London")

with col3:
    # Use a container for the Quick Info box
    st.markdown("""
    <div class='info-card'>
        <h3 style='margin-top:0; color:#64FFDA;'>📊 Quick Info</h3>
        <p style='font-size:0.9em; color:#E6F1FF;'><b>Instructions:</b><br>
        • Fill all fields<br>
        • Train ID: 1-100<br>
        • Age: 1-120 years</p>
    </div>
    """, unsafe_allow_html=True)

# Initialize seat preference variables in session state
if 'selected_pref_type' not in st.session_state:
    st.session_state.selected_pref_type = None

st.write("##") # Spacing

# --- SEAT PREFERENCES ---
st.subheader("🪑 Seat Preferences (Select One)")

pref_col1, pref_col2 = st.columns(2)

with pref_col1:
    seat_type = st.selectbox("AC/Non-AC ChairSeat Type", ["", "Aisle", "Middle", "Window"])
    if seat_type and seat_type != "":
        st.session_state.selected_pref_type = "seat"
        berth_type = ""
    else:
        berth_type_options = ["", "Lower", "Middle", "Upper"]
        if st.session_state.selected_pref_type == "seat":
            berth_type = ""

with pref_col2:
    if seat_type and seat_type != "":
        st.write("*Seat Type selected - Berth Type disabled*")
        berth_type = ""
    else:
        berth_type = st.selectbox("AC/Non-AC Berth Type", ["", "Lower", "Middle", "Upper"])
        if berth_type and berth_type != "":
            st.session_state.selected_pref_type = "berth"

st.write("##") # Spacing

# --- TRAIN ANIMATION FUNCTION ---
def show_train_animation():
    st.markdown("""
    <style>
    @keyframes trainMove {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(calc(100vw)); }
    }
    .train-animation {
        font-size: 2em;
        animation: trainMove 3s linear forwards;
        white-space: nowrap;
    }
    </style>
    <div class='train-animation'>🚂 ━━━━━━━ 🚆 ━━━━━━━ 🎉</div>
    """, unsafe_allow_html=True)

# --- BOOKING BUTTON ---
# Centering the button using columns
_, btn_col, _ = st.columns([1.2, 1, 1.2])
with btn_col:
    book_clicked = st.button("🎟️ Book Ticket Now")

if book_clicked:
    if not name or age is None or train_id is None or not gender or not source or not destination or travel_date is None:
        st.error("❌ Please fill in all fields!")
    else:
        with st.spinner("Processing your booking..."):
            try:
                # Map gender for API
                gender_map = {"Male": "M", "Female": "F", "Other": "O"}
                api_gender = gender_map.get(gender, gender)
                
                # Call API to book ticket with seat preferences
                url = f"http://127.0.0.1:8000/book?name={name}&age={int(age)}&gender={api_gender}&train_id={int(train_id)}&source={source}&destination={destination}&travel_date={travel_date}&seat_type={seat_type}&berth_type={berth_type}"
                res = requests.post(url, timeout=5)
                
                if res.status_code == 200:
                    data = res.json()
                    booking = {
                        "name": name,
                        "status": data.get("status", "UNKNOWN"),
                        "seat_id": data.get("seat_id", "N/A"),
                        "booking_id": data.get("booking_id", None),
                        "preferences": f"{seat_type}-{berth_type}" if seat_type and berth_type else "Any",
                        "source": source,
                        "destination": destination,
                        "travel_date": str(travel_date)
                    }
                    st.session_state.bookings.append(booking)
                    st.success(f"✅ Booking successful for {name}!")
                    show_train_animation()
                else:
                    st.error(f"❌ Booking failed: {res.status_code}")
            except Exception as e:
                st.error(f"❌ Connection Error: {str(e)}")

st.divider()

# --- SEAT ALLOCATIONS ---
st.subheader("📍 Seat Allocations")
if st.session_state.bookings:
    # Use a grid layout for seats
    cols = st.columns(4) 
    for idx, booking in enumerate(st.session_state.bookings):
        with cols[idx % 4]:
            st.markdown(f"""
                <div class='info-card' style='text-align:center; margin-bottom:10px;'>
                    <h4 style='margin:0; color:#E6F1FF;'>{booking['name']}</h4>
                    <p style='color:#64FFDA; font-weight:bold;'>Seat: {booking['seat_id']}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("No bookings yet.")

st.divider()

# --- TICKETS STATUS ---
st.subheader("🎫 Tickets Status")
if st.session_state.bookings:
    for idx, booking in enumerate(st.session_state.bookings, 1):
        col_ticket, col_cancel = st.columns([4, 1])
        with col_ticket:
            if booking["status"] == "CONFIRMED":
                st.markdown(f"""
                    <div class='status-confirmed'>
                        <strong style='color:#E6F1FF;'>Ticket #{idx}:</strong> <span style='color:#E6F1FF;'>{booking['name']}</span> <strong style='color: #64FFDA;'>✓ CONFIRMED</strong>
                        <p style='margin: 5px 0; color: #E6F1FF;'>From: {booking.get('source', 'N/A')} ➔ To: {booking.get('destination', 'N/A')} | Date: {booking.get('travel_date', 'N/A')}</p>
                        <p style='margin: 5px 0; color: #E6F1FF;'>Seat: {booking['seat_id']} | Preference: {booking.get('preferences', 'Any')}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='status-waiting'>
                        <strong style='color:#E6F1FF;'>Ticket #{idx}:</strong> <span style='color:#E6F1FF;'>{booking['name']}</span> <strong style='color: #C5A059;'>⏳ WAITING</strong>
                        <p style='margin: 5px 0; color: #E6F1FF;'>From: {booking.get('source', 'N/A')} ➔ To: {booking.get('destination', 'N/A')} | Date: {booking.get('travel_date', 'N/A')}</p>
                        <p style='margin: 5px 0; color: #E6F1FF;'>Preference: {booking.get('preferences', 'Any')}</p>
                    </div>
                """, unsafe_allow_html=True)
        with col_cancel:
            if st.button("❌ Cancel", key=f"cancel_{idx}"):
                booking_id = booking.get('booking_id')
                if booking_id:
                    try:
                        res = requests.delete(f"http://127.0.0.1:8000/cancel/{booking_id}", timeout=5)
                        if res.status_code == 200:
                            st.session_state.bookings.pop(idx - 1)
                            st.success(f"✅ Booking cancelled for {booking['name']}!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error cancelling booking: {str(e)}")
else:
    st.info("No tickets booked yet.")