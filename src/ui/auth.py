import streamlit as st
from src.utils.db import get_supabase
# from gotrue.errors import AuthApiError

def render_login():
    """Renders the login/signup form and returns the authenticated user or None."""
    
    # Check if already logged in by checking session state or local storage token
    # (Streamlit logic usually resets on refresh, so we rely on session_state)
    if "user" in st.session_state and st.session_state["user"]:
        return st.session_state["user"]

    sb = get_supabase()
    
    st.markdown("## 🔐 Login to Gryphon")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                try:
                    res = sb.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state["user"] = res.user
                    st.success("Login Successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {str(e)}")

    with tab2:
        with st.form("register_form"):
            st.warning("Ensure email confirmation is disabled in Supabase for instant login, or check your spam folder.")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            full_name = st.text_input("Full Name")
            register = st.form_submit_button("Create Account")
            
            if register:
                try:
                    res = sb.auth.sign_up({
                        "email": new_email, 
                        "password": new_password,
                        "options": {"data": {"full_name": full_name}}
                    })
                    st.success("Account created! Please sign in.")
                except Exception as e:
                    st.error(f"Registration Failed: {str(e)}")
    
    return None
