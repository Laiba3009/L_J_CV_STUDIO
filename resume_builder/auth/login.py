import streamlit as st
import json
from pathlib import Path

USERS_FILE = Path(__file__).parent / "users.json"

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def login():
    st.subheader("🔐 Login or Sign Up")

    # Toggle between Login and Signup form
    mode = st.radio("Select Mode", ["Login", "Sign Up"])

    users = load_users()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Sign Up":
        password_confirm = st.text_input("Confirm Password", type="password")
    
    btn = st.button(mode)

    if btn:
        if not username or not password:
            st.error("Please fill all fields.")
            return

        if mode == "Sign Up":
            if password != password_confirm:
                st.error("Passwords do not match!")
                return
            if username in users:
                st.error("Username already exists!")
                return
            # Save new user
            users[username] = password
            save_users(users)
            st.success("User registered! Please login now.")

        elif mode == "Login":
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid username or password.")

def is_logged_in():
    return st.session_state.get("logged_in", False)
