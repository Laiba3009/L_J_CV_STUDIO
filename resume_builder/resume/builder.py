import os
import streamlit as st
import base64

class ResumeBuilder:
    def render_form(self):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email")
        career_objective = st.text_area("Career Objective")
        education = st.text_area("Education")
        skills = st.text_area("Skills")
        experience = st.text_area("Experience")
        language = st.text_input("Languages")
        profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])

        image_base64 = None
        if profile_pic:
            image_data = profile_pic.getvalue()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            image_base64 = f"data:image/png;base64,{image_base64}"

        return {
            "first_name": first_name,
            "last_name": last_name,
            "contact": contact,
            "email": email,
            "career_objective": career_objective,
            "education": education,
            "skills": skills,
            "experience": experience,
            "language": language,
            "image_path": image_base64,  # Send as base64
        }
