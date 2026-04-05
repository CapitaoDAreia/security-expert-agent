from src.agent.brain import CISOExpert
from src.database.storage import VectorStoreManager

def main():
    # Setup
    db_manager = VectorStoreManager()
    ciso = CISOExpert(db_manager)

    print("\n" + "="*60)
    print("🛡️  CISO AGENT - PROFESSIONAL INFRASTRUCTURE")
    print("="*60 + "\n")

    while True:
        query = input("USER > ")
        if query.lower() in ['exit', 'quit']: break
        
        print("[*] Thinking...", end="\r")
        answer, sources = ciso.ask(query)
        
        print(f"\nCISO > {answer}\n")
        print(f"DEBUG: Used {len(sources)} sources.")
        print("-" * 30)

if __name__ == "__main__":
    main()