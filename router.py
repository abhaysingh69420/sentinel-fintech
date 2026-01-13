import time
from sentence_transformers import SentenceTransformer, util
import torch

class PrivacyRouter:
    def __init__(self):
        print("Initializing Semantic Router... (Loading Model)")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.sensitive_anchors = [
            "What is my account balance?",
            "Show me my transaction history",
            "How much money do I have left?",
            "Did I spend money at the supermarket?",
            "My routing number and IBAN",
            "Credit card details",
            "Recent payments to spotify",
            "Salary deposit",
            "Financial statement"
        ]
        
        self.anchor_embeddings = self.model.encode(self.sensitive_anchors, convert_to_tensor=True)
        print("Router Ready. \n")

    def route_query(self, user_query):
        start_time = time.time()
        query_embedding = self.model.encode(user_query, convert_to_tensor=True)
        cosine_scores = util.cos_sim(query_embedding, self.anchor_embeddings)
        top_score = torch.max(cosine_scores).item()
        
        THRESHOLD = 0.35
        decision = "CLOUD (Gemini)"
        if top_score > THRESHOLD:
            decision = "LOCAL (Private Llama)"
            
        latency = time.time() - start_time
        
        return {
            "query": user_query,
            "decision": decision,
            "similarity_score": round(top_score, 4),
            "latency_ms": round(latency * 1000, 2)
        }

if __name__ == "__main__":
    router = PrivacyRouter()
    test_cases = [
        "What is the capital of France?",
        "How much did I spend on groceries?",
        "Write a poem about rain.",
        "I need to check my remaining cash.",
        "Explain quantum computing."
    ]
    
    print(f"{'QUERY':<40} | {'DECISION':<20} | {'SCORE':<6}")
    print("-" * 75)
    
    for query in test_cases:
        result = router.route_query(query)
        print(f"{result['query']:<40} | {result['decision']:<20} | {result['similarity_score']}")
