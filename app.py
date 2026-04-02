import streamlit as st
from src.auth import create_users_table, add_user, login_user
from src.pdf_processor import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.action_extractor import extract_meeting_data
from src.summarizer import summarize_meeting

# Setup
create_users_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# LOGIN SECTION
if not st.session_state.logged_in:
    st.title("Login to AgendaExtractor")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.button("Create Account"):
            if add_user(username, password):
                st.success("Account created successfully!")
            else:
                st.error("Username already exists.")

    if choice == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# MAIN APP
else:
    st.set_page_config(page_title="AgendaExtractor", page_icon="📋", layout="wide")
    st.image("C:\\Users\\hp\\Downloads\\notebook_2296227.png", width=100)
    st.title("AgendaExtractor")
    
    st.markdown(
        "Upload a meeting transcript PDF, and AgendaExtractor will clean the text, extract motions, approvals, proposals, resolutions, withdrawals, and generate a concise summary."
    )

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        # Extract text
        text = extract_text_from_pdf(uploaded_file)

        # Clean text
        cleaned_text = clean_text(text)

        # Extract meeting data
        motions, seconds, decisions, action_items = extract_meeting_data(cleaned_text)

        # Generate summary
        summary = summarize_meeting(motions, seconds, decisions, action_items)

        # Display results
        st.subheader("Meeting Summary")
        st.text(summary)

        st.subheader("Motions")
        for m in motions:
            st.write("-", m)

        st.subheader("Seconds")
        for s in seconds:
            st.write("-", s)

        st.subheader("Decisions")
        for d in decisions:
            st.write("-", d)

        st.subheader("Action Items")
        for a in action_items:
            st.write("-", a)

        # Download results
        if st.button("Download Results as TXT"):
            results = "Meeting Summary:\n" + summary + "\n\n"
            results += "Motions:\n" + "\n".join(motions) + "\n\n"
            results += "Seconds:\n" + "\n".join(seconds) + "\n\n"
            results += "Decisions:\n" + "\n".join(decisions) + "\n\n"
            results += "Action Items:\n" + "\n".join(action_items)

            st.download_button(
                label="Download TXT",
                data=results,
                file_name="AgendaExtractor_results.txt",
                mime="text/plain"
            )

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()