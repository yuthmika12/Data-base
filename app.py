import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Art Circle DB", page_icon="🎨", layout="centered")
st.title("🎨 Royal College Art Circle")
st.markdown("### Student Database Management")

# --- 1. SPREADSHEET CONFIGURATION ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1XVBjt8H38h12n6eZOe49CcvGx14g2zmcnnYtXHVNBD0/edit?gid=243763655#gid=243763655"
CSV_URL = "https://docs.google.com/spreadsheets/d/1XVBjt8H38h12n6eZOe49CcvGx14g2zmcnnYtXHVNBD0/edit?usp=sharing"

# --- 2. SIDEBAR MENU ---
menu = ["Add New Member", "View All Members"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- 3. ADD NEW MEMBER ---
if choice == "Add New Member":
    st.subheader("Add a New Student")
    
    # REMOVED clear_on_submit=True so inputs are NOT erased on error
    with st.form("add_member_form"):
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
                # --- PROCESS SUCCESS ---
                try:
                    st.success(f"🎉 Successfully registered {clean_name}!")
                    
                    
                    # Manual rerun flag can clear data here ONLY on a fully successful submission if desired,
                    # otherwise leaving it keeps the text so you can review what you just sent.
                except Exception as e:
                    st.error(f"Error saving data: {e}")

# --- 4. VIEW ALL MEMBERS ---
elif choice == "View All Members":
    st.subheader("Current Art Circle Members")
    try:
        df = pd.read_csv(CSV_URL)
        df = df.dropna(how="all") 
        
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("The list is currently empty!")
    except Exception as e:
        st.error(f"Could not read spreadsheet data. Ensure the Google Sheet is shared as 'Anyone with the link can view'. Error: {e}")
