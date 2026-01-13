import streamlit as st
import json
import time
import ollama
import google.generativeai as genai
from router import PrivacyRouter

# --- CONFIGURATION ---
# PASTE YOUR KEY HERE (Keep your existing key!)
GOOGLE_API_KEY = "AIzaSyBE3U4YIjLUXGWPwMD__ahwuGFUVHlZlSQ" 

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

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/shield.png", width=50)
    st.title("Sentinel Core")
    st.caption("v1.0.0-Prototype")
    
    st.divider()
    
    st.subheader("📂 Secure Data Vault")
    st.info("Status: ENCRYPTED (Local)")
    
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
        st.json(user_data, expanded=False)
    except:
        st.error("Vault Empty")
        user_data = {}
        
    st.divider()
    st.caption("© 2026 Abhay Singh | Research Prototype")

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
    with st.status("🧠 Sentinel Neural Engine processing...", expanded=True) as status:
        start_time = time.time()
        route_result = router.route_query(prompt)
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