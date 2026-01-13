# 🛡️ Sentinel: Privacy-First Hybrid AI Router

![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![Status](https://img.shields.io/badge/status-prototype-orange)

**A Proof-of-Concept architecture for Fintech that solves the "Privacy vs. Intelligence" deadlock.**

Sentinel is a **Semantic Smart Router** that sits between the user and the LLM. It analyzes user intent in real-time (200ms) and dynamically routes queries:
1.  **Sensitive Data (Balance, Transactions)** → Processed **Locally** by Llama 3.2 (Zero Data Leakage).
2.  **General Knowledge (Market Trends, Advice)** → Processed by **Gemini Cloud** (High Intelligence).

---

## 🚀 Key Features
*   **Semantic Routing:** Uses `all-MiniLM-L6-v2` vector embeddings (not just keywords) to understand context.
*   **Privacy Firewall:** PII and Banking JSON data *never* leave the local environment.
*   **Frugal Architecture:** Reduces API costs by ~60% by offloading simple queries to the local CPU.
*   **Fail-Safe UI:** Explicit "Green Shield" signaling builds user trust.

## 🛠️ Tech Stack
*   **Frontend:** Streamlit (Python)
*   **Local Brain:** Ollama (Llama 3.2 3B)
*   **Cloud Brain:** Google Gemini 2.5 Flash
*   **Router Logic:** Sentence-Transformers (HuggingFace)

---

## 💻 Installation Guide

### Prerequisites
1.  **Python 3.9+** installed.
2.  **Ollama** installed and running ([Download Here](https://ollama.com)).

### Step 1: Clone the Repository
```bash
git clone https://github.com/abhaysingh69420/sentinel-fintech.git
cd sentinel-fintech