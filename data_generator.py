import json
import random
from datetime import datetime, timedelta

# CONFIGURATION
NUM_TRANSACTIONS = 60  # Safe limit for Llama 3.2 Context Window
START_DATE = datetime(2026, 1, 1)

# DATA POOLS
merchants = {
    "Groceries": ["Rewe City", "Aldi Süd", "Lidl Berlin", "Edeka"],
    "Tech": ["Apple Store", "Saturn", "MediaMarkt", "AWS EMEA"],
    "Transport": ["Uber Trip", "Deutsche Bahn", "Lufthansa", "Shell Station"],
    "Dining": ["Starbucks", "Vapiano", "Local Cafe", "Uber Eats"],
    "Subscriptions": ["Spotify Premium", "Netflix 4K", "Notion AI", "ChatGPT Plus"],
    "Health": ["City Apotheke", "Gymshark", "McFit Membership"]
}

def generate_data():
    transactions = []
    current_balance = 14500.50 # Starting Balance
    current_date = START_DATE

    # 1. Generate Transactions (Reverse chronological order)
    for i in range(NUM_TRANSACTIONS):
        # Randomize day step
        current_date -= timedelta(days=random.randint(0, 3), hours=random.randint(1, 12))
        
        # Determine Type (Expense vs Income)
        if i % 15 == 0: # Every ~15th transaction is salary
            category = "Income"
            merchant = "TechCorp Solutions GmbH - Salary"
            amount = 3200.00
        else:
            category = random.choice(list(merchants.keys()))
            merchant = random.choice(merchants[category])
            # Random amount with variance
            base_amount = random.uniform(5.0, 150.0)
            if category == "Tech": base_amount *= 5 # Tech is expensive
            amount = round(base_amount * -1, 2)

        current_balance += amount
        
        tx = {
            "id": f"TXN-{random.randint(10000, 99999)}",
            "date": current_date.strftime("%Y-%m-%d"),
            "merchant": merchant,
            "category": category,
            "amount": amount,
            "currency": "EUR"
        }
        transactions.append(tx)

    # 2. Construct Full Profile
    dataset = {
        "user_profile": {
            "user_id": "SENTINEL_USER_001",
            "full_name": "Abhay Singh",
            "account_type": "Platinum Business",
            "iban": "DE89 1001 0010 0559 1920 00",
            "current_balance": round(current_balance, 2)
        },
        "financial_summary": {
            "total_income_ytd": 9600.00,
            "total_spend_ytd": 4230.50,
            "credit_score": 785
        },
        "recent_transactions": transactions
    }

    # 3. Save
    with open('user_data.json', 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"✅ Generated {NUM_TRANSACTIONS} transactions.")
    print(f"✅ Starting Balance: {round(current_balance, 2)} EUR")

if __name__ == "__main__":
    generate_data()