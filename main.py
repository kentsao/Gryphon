import sys
from src.main_crew import GryphonEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <TICKER>")
        sys.exit(1)
        
    ticker = sys.argv[1]
    print(f"--- Running Gryphon for {ticker} ---")
    
    try:
        engine = GryphonEngine(ticker)
        result = engine.run()
        print("\n\n########################")
        print("## FINAL RECOMMENDATION ##")
        print("########################\n")
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
