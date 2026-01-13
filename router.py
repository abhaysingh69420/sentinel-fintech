import time
from sentence_transformers import SentenceTransformer, util
import torch

class PrivacyRouter:
    def __init__(self):
        print("Initializing Semantic Router... (Loading Model)")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # --- FUTURE-PROOF ANCHORS ---
        # These cover almost every possible banking scenario
        self.sensitive_anchors = [
            # 1. Basic Balance & Accounts
            "What is my account balance?", "How much money do I have?", "Check checking account", "Savings overview",
            # 2. Transactions & History
            "Show me my transaction history", "List recent payments", "Did I get my salary?", "Incoming transfers",
            # 3. Specific Spending Categories
            "How much did I spend on groceries?", "Expenses on food and dining", "Transport and travel costs", 
            "Health, medicine, and pharmacy bills", "Tech and electronics spending", "Subscriptions like Spotify or Netflix",
            # 4. Identity & PII
            "Show my IBAN", "What is my routing number?", "My credit card details", "Account holder name",
            # 5. Cards & Security
            "Freeze my card", "Report a lost card", "Change my pin", "Suspicious activity",
            # 6. Ambiguous Follow-ups (Contextual)
            "And what about yesterday?", "How much for that?", "List the details", "Show me the amount"
        ]
        
        self.anchor_embeddings = self.model.encode(self.sensitive_anchors, convert_to_tensor=True)
        print("Router Ready. \n")

    def route_query(self, user_query, previous_query=None):
        """
        Input: user_query (current), previous_query (context)
        """
        start_time = time.time()
        
        # --- CONTEXTUAL AWARENESS LAYER ---
        # If there is a previous question, we combine them to understand "And medicines?"
        if previous_query:
            # We give more weight to the current query, but include the previous one for context
            combined_input = f"{previous_query} {user_query}"
            print(f"--> Contextual Routing: Analyzing '{combined_input}'")
        else:
            combined_input = user_query
            
        # 1. Vectorize
        query_embedding = self.model.encode(combined_input, convert_to_tensor=True)
        
        # 2. Compare against Anchors
        cosine_scores = util.cos_sim(query_embedding, self.anchor_embeddings)
        top_score = torch.max(cosine_scores).item()
        
        # 3. DECISION LOGIC
        THRESHOLD = 0.35
        
        decision = "CLOUD (Gemini 2.5)"
        if top_score > THRESHOLD:
            decision = "LOCAL (Llama 3.2)"
            
        latency = time.time() - start_time
        
        return {
            "query": user_query,
            "context_used": previous_query if previous_query else "None",
            "decision": decision,
            "similarity_score": round(top_score, 4),
            "latency_ms": round(latency * 1000, 2)
        }