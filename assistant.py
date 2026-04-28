import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Assistant | LPU Smart Grid", layout="centered")
st.title("🤖 Smart Grid AI Assistant")

# --- 1. DATA VALIDATION ---
if 'df' not in st.session_state:
    st.warning("⚠️ Please run the simulation on the main dashboard first so I can read the grid data!")
    st.stop()

# Retrieve variables from session state
df = st.session_state['df']
health = st.session_state['health']
grid_cost = st.session_state['grid_cost']
weather = st.session_state['weather']
hackathon = st.session_state['hackathon']
priority = st.session_state['priority_sector']

# --- 2. AI CONFIGURATION ---
API_KEY = "AIzaSyAFrP-frtAvlZHxchK80oYwsK5KLrHLdDU" 
genai.configure(api_key=API_KEY)

# This block automatically finds a working model name for you
try:
    # Look for any model that supports 'generateContent'
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Pick the first one (usually gemini-1.5-flash or gemini-pro)
    model_name = available_models[0] 
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Could not find a valid AI model: {e}")
    st.stop()

# This is the 'hidden' context that tells the AI exactly what is happening in your LPU grid
context_string = f"""
You are the AI Manager for the LPU Smart Grid. 
Use the following LIVE dashboard data to answer the user:
- Current Grid Health: {health}
- Electricity Cost: ₹{grid_cost}/unit
- Weather Condition: {weather}
- Hackathon Mode: {'ENABLED (High Load)' if hackathon else 'Disabled'}
- Priority Target: {priority}
- Computing Avg Uptime: {df['Computing_Uptime'].mean():.1f}%
- Electronics Avg Uptime: {df['Electronics_Uptime'].mean():.1f}%
- Total Project Savings: ₹{df['Savings'].sum():,.0f}

Be professional, concise, and explain why the Genetic Algorithm is making certain choices based on the data.
"""

# --- 3. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt
if prompt := st.chat_input("Ask about optimization or grid status..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Response Logic
    with st.chat_message("assistant"):
        try:
            # Combine the grid data (context) with the user's specific question
            full_prompt = f"{context_string}\n\nUser Question: {prompt}"
            
            response = model.generate_content(full_prompt)
            bot_reply = response.text
            
            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            st.error(f"AI Error: {e}")
            st.info("Check your API key and internet connection.")
    
    
