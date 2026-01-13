import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.db import get_supabase

# Page Config (Independent of main app.py)
st.set_page_config(page_title="Gryphon Admin", page_icon="🛡️", layout="wide")

def render_admin():
    supabase = get_supabase()
    
    st.title("🛡️ Gryphon Admin Console")
    
    # 1. Fetch Stats
    try:
        # Users (Since we can't query auth.users directly easily without service role in client, 
        # we'll query the public.profiles table we setup)
        users_res = supabase.table("profiles").select("*", count="exact").execute()
        total_users = users_res.count if users_res.count is not None else len(users_res.data)
        
        # Portfolios
        port_res = supabase.table("portfolios").select("*", count="exact").execute()
        total_portfolios = port_res.count if port_res.count is not None else len(port_res.data)
        
        # Positions (to estimate AUM or Activity)
        pos_res = supabase.table("positions").select("*", count="exact").execute()
        total_positions = pos_res.count if pos_res.count is not None else len(pos_res.data)
        
    except Exception as e:
        st.error(f"Error fetching stats: {str(e)}")
        total_users = 0
        total_portfolios = 0
        total_positions = 0

    # 2. Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", total_users)
    col2.metric("Active Portfolios", total_portfolios)
    col3.metric("Total Assets Tracked", total_positions)
    
    st.divider()
    
    # 3. Recent Activity (Visuals)
    st.subheader("System Health & Activity")
    
    # Mock some data if 'events' table is empty/not populated fully yet
    # In a real app, we'd query the 'period' from an 'events' table.
    # For now, let's visualize the portfolio growth or something if we had timestamps.
    
    if port_res.data:
        df_port = pd.DataFrame(port_res.data)
        if "created_at" in df_port.columns:
            df_port["created_at"] = pd.to_datetime(df_port["created_at"])
            df_port["date"] = df_port["created_at"].dt.date
            daily_growth = df_port.groupby("date").size().cumsum().reset_index(name="count")
            
            fig = px.line(daily_growth, x="date", y="count", title="Portfolio Growth Over Time")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data to visualize yet.")

# Simple Auth Check (Hardcoded Admin or reuse Supabase Auth but check for specific email)
# For now, we'll just guard it slightly or leave open for the demo user.

sb = get_supabase()
session = sb.auth.get_session()

if session:
    # In a real app, check user.email == "admin@gryphon.com"
    render_admin()
else:
    st.warning("Please log in via the main app to view the admin console.")
    st.markdown("[Go to Main App](/)")
