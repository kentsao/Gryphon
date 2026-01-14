from tools.market import YFinanceNewsTool
from tools.analysis import TechnicalAnalysisTool
from tools.duck_search import DuckSearchTool
import sys

def test_market_tool():
    print("\n--- Testing Market Tool ---")
    try:
        tool = YFinanceNewsTool()
        result = tool._run("AAPL")
        print(f"Result (truncated): {result[:200]}...")
        if "Error" in result:
            print("❌ Market Tool Failed")
        else:
            print("✅ Market Tool Passed")
    except Exception as e:
        print(f"❌ Market Tool Exception: {e}")

def test_analysis_tool():
    print("\n--- Testing Analysis Tool ---")
    try:
        tool = TechnicalAnalysisTool()
        result = tool._run("AAPL")
        print(f"Result (truncated): {result[:200]}...")
        if "Error" in result:
            print("❌ Analysis Tool Failed")
        else:
            print("✅ Analysis Tool Passed")
    except Exception as e:
        print(f"❌ Analysis Tool Exception: {e}")

def test_search_tool():
    print("\n--- Testing Search Tool ---")
    try:
        tool = DuckSearchTool()
        result = tool._run("Apple stock news")
        print(f"Result (truncated): {result[:200]}...")
        if "Error" in result:
            print("❌ Search Tool Failed")
        else:
            print("✅ Search Tool Passed")
    except Exception as e:
        print(f"❌ Search Tool Exception: {e}")

if __name__ == "__main__":
    test_market_tool()
    test_analysis_tool()
    test_search_tool()
