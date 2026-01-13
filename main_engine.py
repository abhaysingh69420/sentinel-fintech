import json
from router import PrivacyRouter

class BankingAssistant:
    def __init__(self):
        # Initialize the Brain (Router)
        self.router = PrivacyRouter()
        
        # Load the Data (Simulating a Database connection)
        try:
            with open('user_data.json', 'r') as f:
                self.user_data = json.load(f)
            print("Database Loaded Successfully.\n")
        except FileNotFoundError:
            print("ERROR: user_data.json not found!")
            self.user_data = {}

    def process_request(self, user_query):
        # 1. DECIDE (Route the query)
        route_result = self.router.route_query(user_query)
        decision = route_result['decision']
        
        print(f"\nUser asks: '{user_query}'")
        print(f"Router says: {decision} (Score: {route_result['similarity_score']})")
        
        # 2. ACT (Fetch Context if Local)
        if "LOCAL" in decision:
            print(">>> ACTION: Fetching Secure Data...")
            # Convert JSON to string for the LLM
            context_str = json.dumps(self.user_data, indent=2)
            
            # This is what we will send to Llama 3 later
            # For now, we just prove we HAVE the data.
            print(f"    [System]: Data Retrieved. {len(self.user_data['recent_transactions'])} transactions found.")
            print(f"    [System]: Ready to send to Local LLM.")
            return "LOCAL_FLOW_COMPLETE"
            
        else:
            print(">>> ACTION: Connecting to OpenAI API...")
            print("    [System]: Data ignored. Sending ONLY user query to Cloud.")
            return "CLOUD_FLOW_COMPLETE"

# --- TEST THE FULL PIPELINE ---
if __name__ == "__main__":
    bot = BankingAssistant()
    
    # Test 1: Sensitive
    bot.process_request("How much did I spend at the Apple Store?")
    
    # Test 2: General
    bot.process_request("Write a cold email to a potential client.")