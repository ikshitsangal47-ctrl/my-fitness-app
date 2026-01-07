import streamlit as st
import mysql.connector
import pandas as pd

# --- DATABASE CONNECTION ---
def get_connection():
    return mysql.connector.connect(
        host="db.b0tddfsqahnvacnfmazi.supabase.co", 
        user="postgres",
        password="bhai fitness @123",  # Tera ekdum sahi password yahan daal diya hai
        database="postgres",
        port=5432
    )

st.set_page_config(page_title="Fitness Tracker", layout="wide")
st.title("💪 My Fitness & Calorie Tracker")

# Tabs for Navigation
tab1, tab2, tab3 = st.tabs(["Daily Logs", "Personal Info", "View Progress"])

with tab1:
    st.header("Daily Calorie Entry")
    date = st.date_input("Date")
    calories = st.number_input("Calories Consumed", min_value=0)
    if st.button("Save Daily Log"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO daily_records (date, calories) VALUES (%s, %s)", (date, calories))
            conn.commit()
            conn.close()
            st.success("Entry Saved Successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.header("Update Personal Stats")
    h = st.number_input("Height (cm)", min_value=0)
    w = st.number_input("Weight (kg)", min_value=0)
    if st.button("Update Profile"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO personal_records (date, height, weight) VALUES (CURDATE(), %s, %s)", (h, w))
            conn.commit()
            conn.close()
            st.success("Stats Updated!")
        except Exception as e:
            st.error(f"Error: {e}")

with tab3:
    st.header("Your Fitness History")
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT date, calories FROM daily_records ORDER BY date DESC", conn)
        conn.close()
        if not df.empty:
            st.line_chart(df.set_index('date'))
            st.write(df)
        else:
            st.info("No data found. Start logging!")
    except Exception as e:
        st.error(f"Error loading data: {e}")


