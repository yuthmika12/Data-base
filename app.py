import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Art Circle DB", page_icon="🎨", layout="centered")
st.title("🎨 Royal College Art Circle")
st.markdown("### Student Database Management")

# --- 1. SPREADSHEET CONFIGURATION ---
# The URL to your Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1XVBjt8H38h12n6eZOe49CcvGx14g2zmcnnYtXHVNBD0/edit?gid=243763655#gid=243763655"

# Establish connection with Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Failed to initialize Google Sheets connection. Make sure 'streamlit-gsheets' is installed.")
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
        index_no = st.text_input("Index Number")
        phone = st.text_input("Contact Number", placeholder="e.g., 0771234567")

        submit_button = st.form_submit_button("Register Member")

        if submit_button:
            # Clean spaces out of inputs to check them accurately
            clean_name = name.strip()
            clean_index = index_no.strip()
            clean_phone = phone.strip()

            # --- VALIDATION CHECKS ---
            if clean_name == "":
                st.warning("⚠️ Student Name is required!")
            
            elif clean_index == "":
                st.warning("⚠️ Index Number is required!")
            
            # Check if Index Number contains anything other than digits
            elif not clean_index.isdigit():
                st.error("❌ Invalid Index Number! Please enter numbers only.")
            
            elif clean_phone == "":
                st.warning("⚠️ Contact Number is required!")
            
            # Check if Contact Number is exactly 10 digits and only numbers
            elif not clean_phone.isdigit() or len(clean_phone) != 10:
                st.error("❌ Invalid Contact Number! It must be exactly 10 digits long (e.g., 0771234567).")
            
            else:
                # --- SAVE TO GOOGLE SHEETS IF ALL CHECKS PASS ---
                try:
                    # 1. Fetch existing data
                    existing_data = conn.read(spreadsheet=SHEET_URL, usecols=[0,1,2,3])
                    existing_data = existing_data.dropna(how="all")
                    
                    # 2. Match your Google Sheet column headings perfectly
                    new_member = pd.DataFrame([{
                        "student_name": clean_name,
                        "grade": grade,
                        "index_number": clean_index, 
                        "phone_number": clean_phone
                    }])
                    
                    # 3. Combine and write back to cloud sheet
                    updated_df = pd.concat([existing_data, new_member], ignore_index=True)
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    
                    st.success(f"🎉 Successfully registered {clean_name}!")
                except Exception as e:
                    st.error(f"Error saving data to Google Sheets: {e}")
            

# --- 4. VIEW ALL MEMBERS ---
elif choice == "View All Members":
    st.subheader("Current Art Circle Members")
    try:
        # Fetch live data directly from the sheet link
        df = conn.read(spreadsheet=SHEET_URL)
        df = df.dropna(how="all") # Remove empty rows
        
        if not df.empty:
            # Map clean visual names for the table viewer headers
            df.columns = ["Student Name", "Grade", "Index Number", "Contact Number"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("The list is currently empty!")
    except Exception as e:
        st.error(f"Could not read spreadsheet data. Make sure it is shared as 'Anyone with the link'. Error: {e}")
