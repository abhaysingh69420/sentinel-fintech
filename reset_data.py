import json

data = {
  "user_profile": {
    "user_id": "ABHAY_99X",
    "full_name": "Abhay Singh",
    "account_tier": "Premium",
    "primary_iban": "DE89 3704 0044 0532 0130 00"
  },
  "accounts": [
    {
      "type": "Checking",
      "currency": "EUR",
      "balance": 4520.50,
      "status": "Active"
    },
    {
      "type": "Savings",
      "currency": "EUR",
      "balance": 12000.00,
      "interest_rate": "2.5%"
    }
  ],
  "recent_transactions": [
    {"date": "2026-01-08", "merchant": "Rewe Supermarket", "amount": -45.20, "category": "Groceries"},
    {"date": "2026-01-07", "merchant": "Spotify Premium", "amount": -12.99, "category": "Subscription"},
    {"date": "2026-01-06", "merchant": "Deutsche Bahn", "amount": -89.50, "category": "Transport"},
    {"date": "2026-01-05", "merchant": "Salary Deposit", "amount": 3200.00, "category": "Income"},
    {"date": "2026-01-04", "merchant": "City Pharmacy", "amount": -22.40, "category": "Health"},
    {"date": "2026-01-02", "merchant": "Apple Store", "amount": -1299.00, "category": "Electronics"}
  ]
}

print("Resetting user_data.json...")
with open('user_data.json', 'w') as f:
    json.dump(data, f, indent=2)
print("SUCCESS: New database created perfectly.")