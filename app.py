# app.py
import streamlit as st
import requests
import json

# Set the API base URL
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Parcel Tracking System",
    page_icon="📦",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .title {
        font-size: 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        color: #2c3e50;
    }
    .status-delivered {
        background-color: #d4edda;
        color: #155724;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-transit {
        background-color: #cce5ff;
        color: #004085;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-processing {
        background-color: #fff3cd;
        color: #856404;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
    }
    .card {
        padding: 1.5rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-top: 1rem;
    }
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='title'>Parcel Tracking System</h1>", unsafe_allow_html=True)

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Customer Lookup", "Parcel Tracking", "Update Status"])

# Customer Lookup Tab
with tab1:
    st.header("Customer Information")
    
    with st.form("customer_form"):
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        submit_customer = st.form_submit_button("Look Up Customer")
    
    if submit_customer:
        with st.spinner("Fetching customer details..."):
            try:
                response = requests.get(f"{API_BASE_URL}/customers/{customer_id}")
                
                if response.status_code == 200:
                    customer = response.json()
                    st.markdown(f"<div class='card'><h3>Customer #{customer['CustomerID']}</h3>"
                                f"<p><strong>Name:</strong> {customer['Name']}</p>"
                                f"<p><strong>Address:</strong> {customer['Address']}</p></div>", 
                                unsafe_allow_html=True)
                elif response.status_code == 404:
                    st.error("Customer not found")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")

# Parcel Tracking Tab
with tab2:
    st.header("Parcel Information")
    
    with st.form("parcel_form"):
        parcel_id = st.number_input("Parcel ID", min_value=1, step=1)
        submit_parcel = st.form_submit_button("Track Parcel")
    
    if submit_parcel:
        with st.spinner("Tracking parcel..."):
            try:
                response = requests.get(f"{API_BASE_URL}/parcels/{parcel_id}")
                
                if response.status_code == 200:
                    parcel = response.json()
                    
                    # Determine the status class
                    status_class = "status-processing"
                    if str(parcel["Status"]).lower() == "delivered":

                        status_class = "status-delivered"
                    elif "transit" in parcel["Status"].lower():
                        status_class = "status-transit"
                    
                    st.markdown(f"<div class='card'><h3>Parcel #{parcel['ParcelID']}</h3>"
                                f"<p><strong>Customer ID:</strong> {parcel['CustomerID']}</p>"
                                f"<p><strong>Status:</strong> <span class='{status_class}'>{parcel['Status']}</span></p></div>", 
                                unsafe_allow_html=True)
                elif response.status_code == 404:
                    st.error("Parcel not found")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")

# Update Status Tab
with tab3:
    st.header("Update Parcel Status")
    
    with st.form("status_form"):
        update_parcel_id = st.number_input("Parcel ID", min_value=1, step=1)
        status = st.selectbox(
            "Status",
            [
                "Processing",
                "In Transit",
                "Out for Delivery",
                "Delivered",
                "Failed Delivery",
                "Returned"
            ]
        )
        submit_status = st.form_submit_button("Update Status")
    
    if submit_status:
        with st.spinner("Updating status..."):
            try:
                response = requests.put(
                    f"{API_BASE_URL}/parcels/{update_parcel_id}/status",
                    data=json.dumps({"status": status}),
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    st.success("Status updated successfully")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")

# Footer
st.markdown("<div class='footer'>© 2025 Parcel Tracking System</div>", unsafe_allow_html=True)


# requirements.txt
"""
streamlit==1.33.0
requests==2.31.0
"""

# Run command: streamlit run app.py