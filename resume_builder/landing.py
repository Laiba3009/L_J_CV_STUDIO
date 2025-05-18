import streamlit as st

def show_landing_page():
    st.markdown(
        """
        <div style='text-align:center; padding: 100px; background-color:#f0f4f8;'>
            <h1>Create a Professional Resume</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Streamlit native button centered using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Create Resume"):
            st.session_state.page = "start_builder"
            st.rerun()
