import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Art Circle DB", page_icon="🎨", layout="centered")
st.title("🎨 Royal College Art Circle")
st.markdown("### Student Database Management (Spreadsheet Cloud)")

# --- 1. SPREADSHEET CONFIGURATION ---
# Paste your copied Google Sheet URL inside the quotes below
SHEET_URL = "https://docs.google.com/spreadsheets/d/1XVBjt8H38h12n6eZOe49CcvGx14g2zmcnnYtXHVNBD0/edit?gid=243763655#gid=243763655"

# This converts the standard URL into a direct CSV export link
if "docs.google.com" in SHEET_URL:
    csv_url = SHEET_URL.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
else:
    st.error("Please provide a valid Google Sheets URL.")
    st.stop()

# --- 2. SIDEBAR MENU ---
menu = ["Add New Member", "View All Members"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- 3. ADD NEW MEMBER ---
if choice == "Add New Member":
    st.subheader("Add a New Student")
    
    with st.form("add_member_form", clear_on_submit=True):
        name = st.text_input("Student Name")
        grade = st.selectbox("Grade", ["Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "Grade 13"])
        medium = st.text_input("Index Number")
        phone = st.text_input("Contact Number")

        submit_button = st.form_submit_button("Register Member")

        if submit_button:
            if name.strip() == "":
                st.warning("Student Name is required!")
            else:
                # Append the data directly to Google Sheets via HTML form submission trick
                # For simplified production setups, Streamlit recommends using st.connection("gsheets")
                # But for a quick test, we can display what will be saved:
                st.info("To instantly write to sheets from the cloud, let's connect it via Streamlit Secrets next!")

# --- 4. VIEW ALL MEMBERS ---
elif choice == "View All Members":
    st.subheader("Current Art Circle Members (Live from Google Sheets)")
    try:
        # Fetch data seamlessly from the spreadsheet
        df = pd.read_csv(csv_url)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("The spreadsheet is currently empty!")
    except Exception as e:
        st.error(f"Could not read spreadsheet data. Make sure it is shared as 'Anyone with the link'. Error: {e}")
