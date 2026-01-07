import streamlit as st
import psycopg2
import pandas as pd

# --- CONNECTION SETTINGS (Updated with your password & screenshot details) ---
def get_connection():
    return psycopg2.connect(
        host="aws-1-ap-southeast-1.pooler.supabase.com", 
        user="postgres.dndhhsfobtodnbwcwndr", 
        password="bhaifitness2026", 
        database="postgres",
        port=6543, 
        sslmode="require"
    )

st.set_page_config(page_title="Fitness Tracker", layout="wide")
st.title("💪 My Fitness & Calorie Tracker")

# Tables banane ke liye function taaki database empty na rahe
def create_tables():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Daily records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_records (
                id SERIAL PRIMARY KEY, 
                date DATE, 
                calories INTEGER
            )
        """)
        # Personal records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal_records (
                id SERIAL PRIMARY KEY, 
                date DATE, 
                height INTEGER, 
                weight INTEGER
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Table Creation Error: {e}")

# App start hote hi table check karega
create_tables()

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
            st.error(f"Database Error: {e}")

with tab2:
    # --- TAB 2: PERSONAL INFO & BMI CALCULATOR ---
with tab2:
    st.header("Update Stats & Calculate BMI")
    
    # Input fields for Height and Weight
    h_cm = st.number_input("Height (in cm)", min_value=50, max_value=250, value=170)
    w = st.number_input("Weight (in kg)", min_value=10, max_value=300, value=70)
    
    if st.button("Update Profile & Get BMI"):
        try:
            # BMI Calculation Logic
            h_m = h_cm / 100  # cm ko meter mein convert kiya
            bmi = round(w / (h_m ** 2), 2)
            
            # Database mein data save karne ke liye
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO personal_records (date, height, weight) VALUES (CURRENT_DATE, %s, %s)", (h_cm, w))
            conn.commit()
            conn.close()
            
            st.divider()
            st.subheader(f"Tera BMI hai: {bmi}")
            
            # BMI Status Categories
            if bmi < 18.5:
                st.warning("Status: Underweight (Bhai thoda dhyan do sehat pe!)")
            elif 18.5 <= bmi <= 24.9:
                st.success("Status: Normal (Ekdum mast fit ho!)")
            elif 25.0 <= bmi <= 29.9:
                st.info("Status: Overweight (Thoda cardio aur diet manage karo)")
            else:
                st.error("Status: Obese (Bhai mehnat shuru karni padegi!)")
                
        except Exception as e:
            st.error(f"Error: {e}")

with tab3:
    st.header("Your Fitness History")
    try:
        conn = get_connection()
        # Data fetch karke graph dikhane ke liye
        df = pd.read_sql("SELECT date, calories FROM daily_records ORDER BY date DESC", conn)
        conn.close()
        if not df.empty:
            st.line_chart(df.set_index('date'))
            st.write("### All Records", df)
        else:
            st.info("No data found. Start logging in the first tab!")
    except Exception as e:
        st.error(f"Error loading data: {e}")
