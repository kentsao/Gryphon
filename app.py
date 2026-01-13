import os
import signal
import threading

# Monkeypatch signal.signal to ignore errors when not in main thread
_original_signal = signal.signal
def _safe_signal(sig, handler):
    try:
        if threading.current_thread() is threading.main_thread():
            return _original_signal(sig, handler)
    except ValueError:
        pass # Ignore "signal only works in main thread"
signal.signal = _safe_signal

# Must be set before importing crewai
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

import streamlit as st
import sys
import io
from src.main_crew import GryphonEngine
from src.ui.auth import render_login
from src.ui.portfolio import render_portfolio_dashboard

# Page Config
st.set_page_config(page_title="Gryphon AI Info", page_icon="🦁", layout="wide")

# Enable Tracing
os.environ["CREWAI_TRACING_ENABLED"] = "true"

# Authentication Check
user = render_login()

if user:
    # Sidebar Profile Info
    with st.sidebar:
        st.write(f"👤 **{user.email}**")
        
        # Navigation
        page = st.radio("Navigation", ["Portfolio Manager", "Generation Engine"])
        
        st.divider()
        if st.button("Logout"):
            del st.session_state["user"]
            st.rerun()

    st.title("🦁 Gryphon: AI Portfolio Manager")
    st.markdown("### The Autonomous Multi-Agent Investment Committee")

    if page == "Portfolio Manager":
        render_portfolio_dashboard(user)

    elif page == "Generation Engine":
        # Sidebar Config for Generation
        with st.sidebar:
            st.header("Analysis Config")
            tickers_input = st.text_input("Stock Tickers (comma-separated)", value="AAPL, TSLA").upper()
            run_btn = st.button("Run Analysis Engine")

        # Main Area
        if run_btn:
            if not tickers_input:
                st.error("Please enter at least one ticker.")
            else:
                # Parse tickers
                tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]
                
                st.write(f"**Analyzing {len(tickers)} assets:** {', '.join(tickers)}")
                
                for ticker in tickers:
                    with st.status(f"Generative Analysis: {ticker}", expanded=True) as status:
                        st.write("Initializing Agents...")
                        
                        # Capture stdout
                        log_capture = io.StringIO()
                        original_stdout = sys.stdout
                        sys.stdout = log_capture
                        
                        try:
                            engine = GryphonEngine(ticker)
                            
                            # Note: To show "granular" progress inside the agent run, we'd need a custom callback.
                            # For now, we show "Busy".
                            
                            st.write("Engine Started...")
                            result = engine.run()
                            st.write("Analysis Complete.")
                            status.update(label=f"Completed: {ticker}", state="complete", expanded=False)
                            
                        except Exception as e:
                            st.error(f"Error analyzing {ticker}: {str(e)}")
                            status.update(label=f"Failed: {ticker}", state="error")
                            result = f"Error: {str(e)}"
                        
                        finally:
                            # Reset stdout
                            sys.stdout = original_stdout
                            logs = log_capture.getvalue()

                    # Display Results for this ticker
                    st.markdown(f"## 📊 Verdict: {ticker}")
                    st.markdown(result)
                    with st.expander(f"View Agent Logs ({ticker})"):
                        st.code(logs)
                        
                    st.divider()

        else:
            st.info("Select tickers in the sidebar and click 'Run Analysis Engine'.")


