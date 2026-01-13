# 🛡️ Sentinel: Privacy-First AI Architecture for Fintech

<div align="center">

![Status](https://img.shields.io/badge/Status-Prototype_v1.0-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Privacy_%26_Sovereignty-red?style=for-the-badge)

**The "Smart Router" that bridges the gap between Secure Local LLMs and SOTA Cloud Intelligence.**

[**🌐 Live Product Page**](https://abhaysingh69420.github.io/sentinel-fintech/) | [**📄 Read the Paper**](#) | [**🐛 Report Bug**](https://github.com/abhaysingh69420/sentinel-fintech/issues)

</div>

---

## 🧐 The Problem
Financial institutions face a deadlock:
*   **Cloud AI (GPT-4/Gemini)** is smart but **unsafe** for banking data (GDPR/PII risks).
*   **Local AI (Chatbots)** is private but **dumb** (lacks world knowledge).

## 💡 The Sentinel Solution
Sentinel introduces a **Semantic Firewall**. It sits between the user and the AI, routing queries based on *intent* rather than keywords.

### System Architecture
```mermaid
graph TD
    User[👤 User Query] --> Router{🛡️ Sentinel Router}
    
    subgraph "Secure Local Environment"
    Router -- "Sensitive (Balance/Tx)" --> LocalLLM[🦙 Llama 3.2 (Local)]
    LocalLLM <--> Database[(📂 Encrypted JSON)]
    end
    
    subgraph "Public Cloud Environment"
    Router -- "General (Market/News)" --> CloudLLM[☁️ Gemini 2.5 Flash]
    end
    
    LocalLLM --> UI[🖥️ Streamlit Interface]
    CloudLLM --> UI