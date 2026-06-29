import streamlit as st
import mysql.connector
import pandas as pd

# --- 1. DATABASE CONNECTION ---
def init_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Change this to your MySQL username
        password="1234",  # Change this to your MySQL password
        database="royal_college_art"
    )

# Set page configuration
st.set_page_config(page_title="Art Circle DB", page_icon="🎨", layout="centered")
st.title("🎨 Royal College Art Circle")
st.markdown("### Student Database Management")

# Try connecting to the database
try:
    conn = init_connection()
    cursor = conn.cursor()
except Exception as e:
    st.error(f"Failed to connect to the database. Please check your credentials. Error: {e}")
    st.stop()

# --- 2. SIDEBAR MENU ---
menu = ["Add New Member", "View All Members"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- 3. ADD NEW MEMBER ---
if choice == "Add New Member":
    st.subheader("Add a New Student")
    
    with st.form("add_member_form", clear_on_submit=True):
        name = st.text_input("Student Name")
        grade = st.selectbox("Grade", ["Grade 9", "Grade 10", "Grade 11", "Grade 12", "Grade 13"])
        medium = st.text_input("Preferred Art Medium (e.g., Watercolors, Digital, Charcoal)")
        phone = st.text_input("Contact Number")

        submit_button = st.form_submit_button("Register Member")

        if submit_button:
            if name.strip() == "":
                st.warning("Student Name is required!")
            else:
                # Insert data into MySQL
                sql = "INSERT INTO members (student_name, grade, art_medium, phone_number) VALUES (%s, %s, %s, %s)"
                val = (name, grade, medium, phone)
                cursor.execute(sql, val)
                conn.commit()
                st.success(f"Successfully registered {name} to the Art Circle!")

# --- 4. VIEW ALL MEMBERS ---
elif choice == "View All Members":
    st.subheader("Current Art Circle Members")
    
    # Fetch data from MySQL
    cursor.execute("SELECT id, student_name, grade, art_medium, phone_number FROM members")
    records = cursor.fetchall()

    if records:
        # Convert data to a Pandas DataFrame for a clean table view
        df = pd.DataFrame(records, columns=["ID", "Name", "Grade", "Art Medium", "Phone Number"])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("No members found in the database. Go to 'Add New Member' to start!")

# --- 5. CLEANUP ---
# Close the database connection when the script finishes running
if conn.is_connected():
    cursor.close()
    conn.close()