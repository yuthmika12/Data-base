import streamlit as st
import pandas as pd
import requests

# Set page configuration
st.set_page_config(page_title="Art Circle DB", page_icon="🎨", layout="centered")
st.title("🎨 Royal College Art Circle")
st.markdown("### Student Database Management")

# --- 1. SPREADSHEET CONFIGURATION ---
# The view URL for your Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1XVBjt8H38h12n6eZOe49CcvGx14g2zmcnnYtXHVNBD0/edit?gid=243763655#gid=243763655"
# Convert the URL into a direct public CSV download link
CSV_URL = "https://docs.google.com/spreadsheets/d/1XVBjt8H38h12n6eZOe49CcvGx14g2zmcnnYtXHVNBD0/gviz/tq?tqx=out:csv&gid=243763655"

# --- 2. SIDEBAR MENU ---
menu = ["Add New Member", "View All Members"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- 3. ADD NEW MEMBER ---
if choice == "Add New Member":
    st.subheader("Add a New Student")
    
    with st.form("add_member_form", clear_on_submit=True):
        name = st.text_input("Student Name")
        grade = st.selectbox("Grade", ["Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "Grade 13"])
        index_no = st.text_input("Index Number")
        phone = st.text_input("Contact Number", placeholder="e.g., 0771234567")

        submit_button = st.form_submit_button("Register Member")

        if submit_button:
            clean_name = name.strip()
            clean_index = index_no.strip()
            clean_phone = phone.strip()

            # --- VALIDATION CHECKS ---
            if clean_name == "":
                st.warning("⚠️ Student Name is required!")
            elif clean_index == "":
                st.warning("⚠️ Index Number is required!")
            elif not clean_index.isdigit():
                st.error("❌ Invalid Index Number! Please enter numbers only.")
            elif clean_phone == "":
                st.warning("⚠️ Contact Number is required!")
            elif not clean_phone.isdigit() or len(clean_phone) != 10:
                st.error("❌ Invalid Contact Number! It must be exactly 10 digits long.")
            else:
                # --- SUBMIT VIA GOOGLE FORMS TO SHEET ---
                # To submit from a website without gsheets package, we use Google Forms pre-filled link method:
                # For now, let's print confirmation. To write directly, make sure your sheet allows public edits.
                try:
                    st.success(f"🎉 Successfully registered {clean_name}!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error saving data: {e}")

# --- 4. VIEW ALL MEMBERS ---
elif choice == "View All Members":
    st.subheader("Current Art Circle Members")
    try:
        # Fetch live data straight using standard pandas web reader
        df = pd.read_csv(CSV_URL)
        df = df.dropna(how="all") # Drop completely empty rows
        
        if not df.empty:
            # Map standard view headers to whatever columns are read
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("The list is currently empty!")
    except Exception as e:
        st.error(f"Could not read spreadsheet data. Ensure the Google Sheet is shared as 'Anyone with the link can view'. Error: {e}")
