import streamlit as st
import pandas as pd
import os
from src.utils.db import get_supabase
from src.portfolio.analytics import calculate_portfolio_metrics
from src.agents.factory import AdvisorAgent
from src.tasks import GryphonTasks
from crewai import Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def render_portfolio_dashboard(user):
    # ... existing start ...
    sb = get_supabase()
    
    st.markdown("## 💼 Portfolio Manager")
    
    # 1. Fetch Portfolios
    try:
        res = sb.table("portfolios").select("*").eq("user_id", user.id).execute()
        portfolios = res.data
    except Exception as e:
        st.error(f"Failed to fetch portfolios: {str(e)}")
        portfolios = []
        
    # Portfolio Selection / Creation
    col1, col2 = st.columns([3, 1])
    with col1:
        if not portfolios:
            st.info("No portfolios found. Create one to get started.")
            selected_portfolio_id = None
        else:
            options = {p['id']: p['name'] for p in portfolios}
            selected_portfolio_id = st.selectbox(
                "Select Portfolio", 
                options=list(options.keys()), 
                format_func=lambda x: options[x]
            )
            
    with col2:
        with st.popover("New Portfolio"):
            new_name = st.text_input("Name")
            if st.button("Create"):
                try:
                    sb.table("portfolios").insert({"user_id": user.id, "name": new_name}).execute()
                    st.success("Created!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    if not selected_portfolio_id:
        return

    st.divider()

    # 2. Manage Positions
    # Fetch positions
    try:
        pos_res = sb.table("positions").select("*").eq("portfolio_id", selected_portfolio_id).execute()
        positions = pos_res.data
    except Exception as e:
        st.error(f"Failed to load positions: {str(e)}")
        positions = []

    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("Holdings")
        if positions:
            df = pd.DataFrame(positions)
            display_df = df[["ticker", "shares"]]
            st.dataframe(display_df, use_container_width=True)
            
            # --- RISK METRICS & ADVISOR ---
            if st.button("📊 Calculate Risk Metrics"):
                with st.spinner("Fetching market data (2y)..."):
                    holdings_dict = {p['ticker']: float(p['shares']) for p in positions}
                    metrics = calculate_portfolio_metrics(holdings_dict)
                    
                    if "error" in metrics:
                        st.error(metrics["error"])
                    else:
                        st.success("Calculation Complete")
                        # Display nicely
                        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                        m_col1.metric("Beta", metrics['beta'])
                        m_col2.metric("Sharpe", metrics['sharpe_ratio'])
                        m_col3.metric("Volatility", metrics['volatility'])
                        m_col4.metric("Max Drawdown", metrics['max_drawdown'])
                        
                        st.caption(f"Total Value: ${metrics['total_value']:,.2f}")
                        
                        # Store metrics in session state for the Advisor to use
                        st.session_state["last_metrics"] = metrics
                        st.session_state["last_holdings"] = holdings_dict
            
            st.divider()
            
            # Advisor Section
            if "last_metrics" in st.session_state:
                st.subheader("🤖 AI Advisor")
                risk_profile = st.selectbox(
                    "Select Your Risk Profile",
                    ["Conservative (Preserve Wealth)", "Moderate (Balanced)", "Aggressive (Growth)"]
                )
                
                if st.button("Generate Rebalancing Plan"):
                    with st.status("Advisor is thinking...", expanded=True):
                        try:
                            # 1. Setup LLM
                            api_key = os.getenv("GOOGLE_API_KEY")
                            model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-1.5-flash")
                            llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.2, google_api_key=api_key)
                            
                            # 2. Setup Agent & Task
                            advisor_agent = AdvisorAgent(llm).create()
                            tasks = GryphonTasks()
                            t_rebalance = tasks.rebalance_task(
                                agent=advisor_agent,
                                holdings=st.session_state["last_holdings"],
                                metrics=st.session_state["last_metrics"],
                                risk_profile=risk_profile
                            )
                            
                            # 3. Run Crew
                            crew = Crew(
                                agents=[advisor_agent],
                                tasks=[t_rebalance],
                                verbose=True
                            )
                            result = crew.kickoff()
                            
                            st.write("Planning Complete.")
                            st.markdown("### 📝 Rebalancing Recommendations")
                            st.markdown(result)
                            
                        except Exception as e:
                            st.error(f"Advisor Error: {str(e)}")

        else:
            st.info("No positions added yet.")

    with col_b:
        st.subheader("Add Position")
        with st.form("add_position"):
            ticker = st.text_input("Ticker (e.g. AAPL)").upper()
            shares = st.number_input("Shares", min_value=0.01, step=1.0)
            if st.form_submit_button("Add Asset"):
                try:
                    sb.table("positions").insert({
                        "portfolio_id": selected_portfolio_id,
                        "ticker": ticker,
                        "shares": shares
                    }).execute()
                    st.success("Added!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
            
        if positions:
            with st.expander("Remove Position"):
                t_to_remove = st.selectbox("Select Ticker", [p['ticker'] for p in positions])
                if st.button("Delete Position"):
                     try:
                        # naive delete by ticker for this portfolio
                        sb.table("positions").delete().eq("portfolio_id", selected_portfolio_id).eq("ticker", t_to_remove).execute()
                        st.rerun()
                     except Exception as e:
                         st.error(str(e))
