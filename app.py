import streamlit as st
import requests

st.set_page_config(page_title="Railway System", page_icon="🚆", layout="wide")

# Initialize session state for bookings
if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
    }
    .stContainer {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    h1 {
        color: #667eea;
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .status-confirmed {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .status-waiting {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .seat-allocation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Main container
with st.container():
    st.title("🚆 Smart Railway Reservation System")
    
    # Subtitle
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.1em;'>Book your train tickets seamlessly</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Create columns for better layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("👤 Passenger Info")
        name = st.text_input("Full Name", placeholder="Enter your name", key="passenger_name")
        age = st.number_input("Age", min_value=1, max_value=120, value=None)
    
    with col2:
        st.subheader("🚹 Additional Details")
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other"], key="gender_select")
        train_id = st.number_input("Train ID", min_value=1, value=None)
    
    with col3:
        st.subheader("📊 Quick Info")
        st.info("""
        **Booking Instructions:**
        - Fill all passenger fields
        - Train ID: 1-100
        - Age: 1-120 years
        - Gender: Select preference
        """)
    
    st.divider()
    
    # Booking section
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        if st.button("🎟️ Book Ticket Now", use_container_width=True, type="primary"):
            if not name or not age or not train_id or not gender:
                st.error("❌ Please fill in all fields!")
            elif not name.strip():
                st.error("❌ Please enter a valid name!")
            else:
                with st.spinner("⏳ Processing your booking..."):
                    try:
                        # Map display gender to API gender
                        gender_map = {"Male": "M", "Female": "F", "Other": "O"}
                        api_gender = gender_map.get(gender, gender) if gender else ""
                        
                        url = f"http://127.0.0.1:8000/book?name={name}&age={age}&gender={api_gender}&train_id={train_id}"
                        res = requests.post(url, timeout=5)

                        if res.status_code == 200:
                            data = res.json()
                            status = data.get('status', 'UNKNOWN')
                            seat_id = data.get('seat_id', 'N/A')
                            
                            # Store booking in session state
                            booking = {
                                "name": name,
                                "age": age,
                                "gender": gender,
                                "train_id": train_id,
                                "status": status,
                                "seat_id": seat_id
                            }
                            st.session_state.bookings.append(booking)
                            
                            # Show success message with booking details
                            if status == "CONFIRMED":
                                st.markdown("""
                                    <div class='status-confirmed'>
                                    <h3>✅ Booking Confirmed!</h3>
                                    <p><strong>Status:</strong> <span style='color: #28a745; font-weight: bold;'>CONFIRMED</span></p>
                                    <p><strong>Seat Number:</strong> <span style='color: #28a745; font-weight: bold;'>{}</span></p>
                                    </div>
                                    """.format(seat_id), unsafe_allow_html=True)
                                st.balloons()
                            else:
                                st.markdown("""
                                    <div class='status-waiting'>
                                    <h3>⏳ Booking in Waiting List</h3>
                                    <p><strong>Status:</strong> <span style='color: #ffc107; font-weight: bold;'>WAITING</span></p>
                                    <p style='margin-top: 10px; font-size: 0.9em;'>⚠️ No seats available. You're in the waiting list.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.error(f"❌ Booking failed with status {res.status_code}")
                    except Exception as e:
                        st.error(f"❌ Connection Error: {str(e)}")
                        st.error("Make sure the FastAPI server is running on http://127.0.0.1:8000")
    
    st.divider()
    
    # Seat Allocations Section
    st.subheader("📍 Seat Allocations")
    if st.session_state.bookings:
        seat_cols = st.columns(len(st.session_state.bookings))
        for idx, (col, booking) in enumerate(zip(seat_cols, st.session_state.bookings)):
            with col:
                if booking["status"] == "CONFIRMED":
                    st.markdown(f"""
                        <div class='seat-allocation-card'>
                        <h4>{booking['name']}</h4>
                        <p>Train #{booking['train_id']}</p>
                        <p style='font-size: 1.2em; font-weight: bold;'>Seat: {booking['seat_id']}</p>
                        <p style='color: #90EE90;'>✓ Allocated</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class='seat-allocation-card' style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);'>
                        <h4>{booking['name']}</h4>
                        <p>Train #{booking['train_id']}</p>
                        <p>Seat: Waiting</p>
                        <p>⏳ In Queue</p>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No seat allocations yet. Make a booking to see allocations here.")
    
    st.divider()
    
    # Tickets Status Section
    st.subheader("🎫 Tickets Status")
    if st.session_state.bookings:
        for idx, booking in enumerate(st.session_state.bookings, 1):
            if booking["status"] == "CONFIRMED":
                st.markdown(f"""
                    <div class='status-confirmed'>
                    <strong>Ticket #{idx}:</strong> {booking['name']} (Age: {booking['age']}, {booking['gender']}) 
                    <strong style='color: #28a745;'>✓ CONFIRMED</strong> - Train #{booking['train_id']}, Seat #{booking['seat_id']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='status-waiting'>
                    <strong>Ticket #{idx}:</strong> {booking['name']} (Age: {booking['age']}, {booking['gender']}) 
                    <strong style='color: #ffc107;'>⏳ WAITING</strong> - Train #{booking['train_id']}
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No ticket bookings yet. Make a booking to see ticket status here.")