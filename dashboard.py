import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

# ================= LOGIN =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏫 School Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Login ❌")

# ================= DASHBOARD =================
else:
    logo = Image.open("logo.png")
    st.image(logo, width=80)
    st.title("🏫 Jamia Arabia School")
    st.write("School Management Dashboard")
    st.write("Designed By Sumayya Jawed")

    #Get Data 
    sheets = ["GradeIII", "GradeIV", "GradeV", "GradeVI"]
    
    all_data = {}
    for sheet in sheets:
        df = pd.read_excel("data.xlsx", sheet_name=sheet, header=6)
        df["Grade"] = sheet  # Grade column add
        all_data[sheet] = df

    # ================= SIDEBAR FILTERS =================
    st.sidebar.header("Dashboard Filter")
    
    select_grade = st.sidebar.selectbox("Select Grade", sheets)
    
    df_selected = all_data[select_grade]
    
    sections = df_selected["Section"].dropna().unique()
    select_section = st.sidebar.multiselect("Select Section", sections, default=sections)
    
    gender = df_selected["Gender"].dropna().unique()
    select_gender = st.sidebar.multiselect("Select Gender", gender, default=gender)

    df_filtered = df_selected[
        df_selected["Section"].isin(select_section) &
        df_selected["Gender"].isin(select_gender)
    ]

    # ================= KPIs =================
    total_students = len(df_filtered)
    male = (df_filtered["Gender"] == "Male").sum()
    female = (df_filtered["Gender"] == "Female").sum()
    avg_marks = df_filtered["Obt_Marks"].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Male", male)
    col3.metric("Female", female)
    col4.metric("Avg Obtained Marks", f"{avg_marks:.1f}")

    st.divider()

    # ================= STUDENT SEARCH =================
    st.subheader("🔍 Student Search")
    student_id = st.text_input("Enter Student ID (GR_001 - GR_0080)")
#find particular data
    if student_id:
       
        found = False
        for grade, df in all_data.items():
            result = df[df["GR.No"] == student_id]
            if len(result) > 0:
                found = True
                st.success(f"Student found in {grade}!")
                row = result.iloc[0]

                # Basic Info
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Name", row["Std_Name"])
                c2.metric("Father Name", row["Father_Name"])
                c3.metric("Gender", row["Gender"])
                c4.metric("Section", row["Section"])

                st.divider()

                # Marks
                c5, c6, c7 = st.columns(3)
                c5.metric("Total Marks", row["Total_Marks"])
                c6.metric("Obtained Marks", row["Obt_Marks"])
                c7.metric("Attendance", row["Attendance%"])

                st.divider()

                # Subject wise bar chart
                st.subheader("📊 Subject Wise Marks")
                subjects = ["Eng", "Urdu", "Math", "Science", "Islamiat", "Computer", "S.St", "Sindhi"]
                marks = [row[s] for s in subjects]

                fig, ax = plt.subplots(figsize=(10, 4))
                bars = ax.bar(subjects, marks, color=["#2196F3","#4CAF50","#FF5722","#9C27B0","#FF9800","#00BCD4","#E91E63","#795548"])
                ax.set_ylim(0, 110)
                ax.set_ylabel("Marks")
                ax.set_title(f"Subject Wise Marks - {row['Std_Name']}")
                ax.bar_label(bars, padding=3)
                st.pyplot(fig)

                st.divider()

                # Fee & Progress
                c8, c9 = st.columns(2)
                c8.metric("Fee Status", row["Fee_Status"])
                c9.metric("Progress", row["Progress"])  

                break

        if not found:
            st.error("Student ID not found! Check karein.")

    st.divider()

    # ================= CHARTS =================
    st.subheader("📈 Class Overview")

    chart1, chart2 = st.columns(2)

    with chart1:
        fig1, ax1 = plt.subplots()
        gender_count = df_filtered["Gender"].value_counts()
        ax1.pie(gender_count.values, labels=gender_count.index, autopct="%1.1f%%", colors=["#2196F3","#E91E63"])
        ax1.set_title("Gender Distribution")
        st.pyplot(fig1)

    with chart2:
        fig2, ax2 = plt.subplots()
        fee_count = df_filtered["Fee_Status"].value_counts()
        ax2.bar(fee_count.index, fee_count.values, color=["#4CAF50","#F44336","#FF9800"])
        ax2.set_title("Fee Status")
        ax2.set_ylabel("Students")
        st.pyplot(fig2)

    # Subject wise avg
    st.subheader("📚 Subject Wise Class Average")
    subjects = ["Eng", "Urdu", "Math", "Science", "Islamiat", "Computer", "S.St", "Sindhi"]
    avg_subject = df_filtered[subjects].mean()

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    bars3 = ax3.bar(subjects, avg_subject, color="#2196F3")
    ax3.set_ylabel("Average Marks")
    ax3.set_title("Subject Wise Average Marks")
    ax3.bar_label(bars3, fmt="%.1f", padding=3)
    st.pyplot(fig3)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()