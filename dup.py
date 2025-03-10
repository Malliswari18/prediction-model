import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import hashlib
import os

# Function to Set Background Image
def set_background(image_url):
    """Applies a background image using CSS."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({image_url});
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load existing users from file
users = {}
user_file = "users.txt"
if os.path.exists(user_file):
    with open(user_file, "r") as file:
        for line in file:
            email, hashed_password = line.strip().split(",")
            users[email] = hashed_password

# Session state initialization
if "page" not in st.session_state:
    st.session_state["page"] = "Welcome"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "predicted_score" not in st.session_state:
    st.session_state["predicted_score"] = None

# Welcome Page (Before Login) - Background image applied only on Welcome page
if st.session_state["page"] == "Welcome":
    set_background("https://www.evolv28.com/wp-content/uploads/2022/11/Group-25-1080x675.png")
    st.title("**✨🚀 Welcome 🚀✨**")
    st.title("🧠 Mental Health Detection System")
    st.markdown(
        "**Welcome to the Mental Health Detection System. This tool helps assess mental health risk based on various factors. Get started by logging in or registering.**"
    )
    if st.button("🚀 Get Started"):
        st.session_state["page"] = "Authentication"
        st.rerun()

# Authentication (Login/Register)
elif st.session_state["page"] == "Authentication":
    st.sidebar.title("🔐 User Authentication")
    auth_choice = st.sidebar.radio("Select Option", ["Login", "Register"])
    
    if auth_choice == "Register":
        st.subheader("🆕 Create a New Account")
        new_email = st.text_input("📧 Email")
        new_password = st.text_input("🔑 Password", type="password")
        if st.button("Register"):
            if new_email in users:
                st.error("❌ Email already registered! Try logging in.")
            else:
                hashed_password = hash_password(new_password)
                users[new_email] = hashed_password
                with open(user_file, "a") as file:
                    file.write(f"{new_email},{hashed_password}\n")
                st.success("✅ Registration successful! Please log in.")
                st.rerun()
    
    elif auth_choice == "Login":
        st.subheader("🔓 Login to Your Account")
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        if st.button("Login"):
            hashed_password = hash_password(password)
            if email in users and users[email] == hashed_password:
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
                st.session_state["page"] = "Prediction"
                st.success("✅ Login Successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Incorrect email or password")

# Main App (After Login)
elif st.session_state["logged_in"]:
    # Prediction Page
    if st.session_state["page"] == "Prediction":
        st.title("🧠 Mental Health Detection System")
        
        # Input fields
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        anxiety = st.selectbox("Anxiety", ["Yes", "No"])
        depression = st.selectbox("Depression", ["Yes", "No"])
        sleep_issues = st.selectbox("Sleep Issues", ["No", "Yes", "Sometimes"])
        social_withdrawal = st.selectbox("Social Withdrawal", ["No", "Yes"])
        stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
        work_study_pressure = st.selectbox("Work/Study Pressure", ["Low", "Medium", "High"])
        family_history = st.selectbox("Family History", ["Yes", "No"])
        physical_activity = st.selectbox("Physical Activity", ["Low", "Medium", "High", "Regular"])
        social_support = st.selectbox("Social Support", ["Low", "Medium", "High"])
        
        if st.button("🔍 Predict Mental Health Score"):
            data = {
                "AGE": age,
                "GENDER": gender,
                "ANXIETY": anxiety,
                "DEPRESSION": depression,
                "SLEEP_ISSUES": sleep_issues,
                "SOCIAL_WITHDRAWAL": social_withdrawal,
                "STRESS_LEVEL": stress_level,
                "WORK_STUDY_PRESSURE": work_study_pressure,
                "FAMILY_HISTORY": family_history,
                "PHYSICAL_ACTIVITY": physical_activity,
                "SOCIAL_SUPPORT": social_support
            }
            response = requests.post("http://127.0.0.1:5000/predict", json=data)
            if response.status_code == 200:
                result = response.json()
                st.session_state["predicted_score"] = result["predicted_score"]
                st.success(f"🎯 Predicted Mental Health Score: **{result['predicted_score']}**")
            else:
                st.error(f"⚠️ Error: {response.json().get('error', 'Unknown error')}")
        
        # Show Prediction Analysis button only if prediction exists
        if st.session_state["predicted_score"] is not None:
            if st.button("📊 Go to Prediction Analysis"):
                st.session_state["page"] = "Prediction Analysis"
                st.rerun()
                
    # Prediction Analysis Page
    elif st.session_state["page"] == "Prediction Analysis":
        # Scroll to top on page load
        st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)
        
        st.title("📊 Prediction Analysis")
        score = st.session_state["predicted_score"]
        st.write("### 📝 Understanding Your Mental Health Score")
        
        # Detailed suggestions based on predicted score
        if score <= 2:
            st.info(
                "🟢 Low Risk (Score: 1-2)\n\n"
                "💡 Your mental health appears to be in a stable state!\n"
                "✅ You seem to have good emotional well-being and a balanced lifestyle.\n"
                "✅ Regular physical activity, strong social connections, and effective stress management contribute to this.\n\n"
                "📌 Suggestions:\n"
                "- Continue maintaining a healthy work-life balance.\n"
                "- Engage in activities that bring joy and relaxation.\n"
                "- Keep socializing with family and friends.\n"
                "- Practice mindfulness or meditation for mental clarity."
            )
        elif 3 <= score <= 4:
            st.warning(
                "🟠 Moderate Risk (Score: 3-4)\n\n"
                "⚠️ You may be experiencing mild to moderate mental health challenges.\n"
                "🔹 Some signs of stress, anxiety, or mild depressive symptoms could be present.\n"
                "🔹 Factors like sleep issues, work pressure, or social withdrawal might be affecting your well-being.\n\n"
                "📌 Suggestions:\n"
                "- Try incorporating stress-relieving activities like yoga, journaling, or deep breathing exercises.\n"
                "- Get adequate sleep (7-9 hours per night) to improve mood and cognitive function.\n"
                "- Spend time outdoors—nature exposure helps reduce stress and anxiety.\n"
                "- Don’t hesitate to talk to a trusted friend or counselor about how you feel."
            )
        else:
            st.error(
                "🔴 High Risk (Score: 5+)\n\n"
                "❗ Your mental health may be at risk. It's important to seek support.\n"
                "🔺 Persistent stress, anxiety, or depressive symptoms can affect daily life.\n"
                "🔺 Lack of social support, excessive stress, or unhealthy coping mechanisms might be involved.\n\n"
                "📌 Suggestions:\n"
                "- Reach out to a mental health professional for guidance and support.\n"
                "- Identify and avoid stress triggers, if possible.\n"
                "- Engage in self-care routines such as hobbies, reading, or creative activities.\n"
                "- Try therapy or support groups to connect with people facing similar challenges.\n"
                "- Maintain a balanced diet—nutrition plays a vital role in mental health."
            )
        
        # Display Bar Graph using matplotlib
        st.write("### 📊 Your Mental Health Score (Bar Graph)")
        max_score = 6  # Define the maximum score for scaling
        fig1, ax1 = plt.subplots()
        ax1.bar(["Mental Health Score"], [score], color="#4CAF50")
        ax1.set_ylim(0, max_score)
        ax1.set_ylabel("Score")
        ax1.set_title("Mental Health Score")
        st.pyplot(fig1)
        
        # Display Pie Chart for score breakdown (assuming maximum score is 6)
        st.write("###  Your Score Breakdown (Assuming max score of 6)")
        pie_data = [score, max_score - score]
        pie_labels = ["Your Score", "Remaining"]
        fig2, ax2 = plt.subplots()
        ax2.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=['#4CAF50', '#FFC107'], startangle=90)
        ax2.axis('equal')  # Ensures the pie chart is circular
        st.pyplot(fig2)
        
        # Feedback Section
        st.write("### 📣 Feedback")
        feedback = st.text_area("Please share your feedback on the analysis:", "")
        if st.button("Submit Feedback"):
            with open("feedback.txt", "a") as f:
                f.write(f"{st.session_state.get('user_email', 'anonymous')}: {feedback}\n")
            st.success("Thank you for your feedback!")
        
        if st.button("🔙 Back to Prediction"):
            st.session_state["page"] = "Prediction"
            st.rerun()
