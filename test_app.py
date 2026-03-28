import streamlit as st
import requests

st.set_page_config(page_title="Railway System", page_icon="train")

st.title("Smart Railway Reservation")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)

with col2:
    gender = st.selectbox("Gender", ["M", "F"])
    train_id = st.number_input("Train ID", 1)

st.write("---")

if st.button("Book Ticket"):
    with st.spinner("Booking your ticket..."):
        try:
            url = f"http://127.0.0.1:8000/book?name={name}&age={age}&gender={gender}&train_id={train_id}"
            res = requests.post(url)

            if res.status_code == 200:
                data = res.json()
                st.success(f"Booking successful! Status: {data.get('status', 'UNKNOWN')}")
            else:
                st.error(f"Booking failed with status {res.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
