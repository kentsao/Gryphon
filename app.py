import streamlit as st
import sys
import io
from src.main_crew import GryphonEngine

# Page Config
st.set_page_config(page_title="Gryphon AI Info", page_icon="🦁", layout="wide")

st.title("🦁 Gryphon: AI Portfolio Manager")
st.markdown("### The Autonomous Multi-Agent Investment Committee")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    ticker = st.text_input("Stock Ticker", value="AAPL").upper()
    st.info("Ensure your .env file has valid API keys (OpenAI, etc).")
    run_btn = st.button("Initialize Logic")

# Main Area
if run_btn:
    if not ticker:
        st.error("Please enter a ticker.")
    else:
        st.write(f"**Analyzing {ticker}...** This may take a minute.")
        
        # Tabs for "War Room" vs "Verdict"
        tab1, tab2 = st.tabs(["The Verdict", "The War Room (Logs)"])
        
        # Capture stdout for "War Room" logs
        log_capture = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = log_capture
        
        try:
            # Run the Engine
            engine = GryphonEngine(ticker)
            result = engine.run()
            
            # Reset stdout
            sys.stdout = original_stdout
            logs = log_capture.getvalue()
            
            # Display Results
            with tab1:
                st.success("Analysis Complete!")
                st.markdown(result)
                
            with tab2:
                st.text_area("Agent logs", logs, height=600)
                
        except Exception as e:
            sys.stdout = original_stdout # Ensure reset on error
            st.error(f"An error occurred: {str(e)}")

else:
    st.info("Enter a ticker and click 'Initialize Logic' to start the agents.")
