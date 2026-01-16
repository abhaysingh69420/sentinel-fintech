import pandas as pd
import streamlit as st
import json
import time
import ollama
import google.generativeai as genai
from router import PrivacyRouter

# --- CONFIGURATION ---
# PASTE YOUR KEY HERE (Keep your existing key!)
GOOGLE_API_KEY = "Api key" 

# Configure Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    pass # Handle gracefully in UI

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Sentinle | Privacy-First Fintech",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Fintech" look
st.markdown("""
<style>
    .stSuccess { border-left: 5px solid #00ff41 !important; }
    .stInfo { border-left: 5px solid #00d4ff !important; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
@st.cache_resource
def load_router():
    return PrivacyRouter()

router = load_router()

# --- MAIN INTERFACE ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Sentinel")
    st.markdown("#### The Privacy-First Smart Router for Banking")

with col2:
    st.metric(label="System Status", value="Online", delta="Secure")

# Introductory Expander
with st.expander("ℹ️ How Sentinel Protects You"):
    st.markdown("""
    1. **Intent Analysis:** Sentinel scans your question for sensitivity.
    2. **Semantic Routing:** 
       - 🛡️ **Private:** Banking data is processed **Locally** (Llama 3.2).
       - ☁️ **General:** World knowledge is processed by **Cloud** (Gemini).
    3. **Zero Leakage:** Your financial data *never* leaves this device.
    """)

st.divider()

# --- SIDEBAR: SECURE DATA VAULT ---
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/shield.png", width=50)
    st.title("Sentinel Core")
    st.caption("v1.0.0-Prototype | Encrypted")
    
    st.divider()
    
    # LOAD DATA
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
        
        # 1. Profile Card
        profile = user_data['user_profile']
        st.write(f"**User:** {profile['full_name']}")
        st.write(f"**IBAN:** `{profile['iban']}`")
        st.metric("Current Balance", f"€{profile['current_balance']:,.2f}")
        
        st.divider()
        
        # 2. Transaction Grid (The "Extensive" Look)
        st.subheader("Recent Activity")
        transactions = user_data.get('recent_transactions', [])
        
        if transactions:
            # Convert to Pandas DataFrame for a pretty table
            df = pd.DataFrame(transactions)
            # Show a scrollable, sortable table
            st.dataframe(
                df[['date', 'merchant', 'amount']], 
                hide_index=True, 
                height=300, 
                use_container_width=True
            )
        else:
            st.info("No transactions found.")

    except Exception as e:
        st.error(f"Vault Locked or Empty: {e}")
        user_data = {}
        
    st.divider()
    st.caption("© 2026 Abhay Pratap Singh | Research Prototype")

# Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcome message
    st.session_state.messages.append({"role": "assistant", "content": "Hello. I am Sentinel. I can access your secure banking data locally, or browse the web via the cloud. How can I help?"})

for message in st.session_state.messages:
    avatar = "🛡️" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about transactions, balances, or general topics..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # ROUTING
    # ... inside the "if prompt :=" block ...

    # 0. GET CONTEXT (Previous User Message)
    previous_query = None
    # We look back 2 steps in history to find the last thing the USER said
    if len(st.session_state.messages) >= 2:
        # The history looks like: [User, AI, User, AI...]
        # So the last user message is usually at index -2 (before the current append)
        # But since we JUST appended the current prompt, we need to look deeper or track it manually.
        # A simpler way: Look for the last message with role='user' that isn't the current one.
        user_msgs = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
        if len(user_msgs) > 1:
            previous_query = user_msgs[-2] # The one before the current one

    # ROUTING
    with st.status("🧠 Sentinel Neural Engine processing...", expanded=True) as status:
        start_time = time.time()
        
        # *** KEY CHANGE: PASS PREVIOUS QUERY ***
        route_result = router.route_query(prompt, previous_query=previous_query)
        
        decision = route_result['decision']
        score = route_result['similarity_score']
        latency = (time.time() - start_time) * 1000
        
        status.update(label=f"Routing Complete: {decision} ({latency:.0f}ms)", state="complete", expanded=False)
    # BRANCH 1: LOCAL
    if "LOCAL" in decision:
        with st.chat_message("assistant", avatar="🛡️"):
            st.success(f"**Secure Channel Active** (Confidence: {score:.2f})")
            
            system_prompt = f"You are Sentinel. Data: {json.dumps(user_data)}. Answer concise."
            
            response_placeholder = st.empty()
            full_response = ""
            try:
                stream = ollama.chat(model='llama3.2', messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': prompt}], stream=True)
                for chunk in stream:
                    content = chunk['message']['content']
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Local Model Error: Make sure Ollama is running! {e}")

    # BRANCH 2: CLOUD
    else:
        with st.chat_message("assistant", avatar="☁️"):
            st.info(f"**Cloud Channel Active** (Confidence: {score:.2f})")
            
            try:
                # Try 2.5, fall back to 1.5 if needed
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                except:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                response_placeholder = st.empty()
                response = model.generate_content(prompt, stream=True)
                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Cloud API Error: {e}")
