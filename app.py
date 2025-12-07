"""MedLink Agent - Unified Chat Interface (Fixed)"""
import streamlit as st
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="MedLink Agent", page_icon="🏥", layout="wide")

# CSS - Clean Modern Light Theme with Mobile Responsive
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .user-msg {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        border-radius: 18px 18px 4px 18px;
        padding: 14px 18px;
        margin: 10px 0;
        color: white !important;
        box-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
        word-wrap: break-word;
    }
    
    .bot-msg {
        background: white;
        border-radius: 18px 18px 18px 4px;
        padding: 14px 18px;
        margin: 10px 0;
        border-left: 4px solid #8b5cf6;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        color: #1e293b !important;
        word-wrap: break-word;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1e293b !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
        width: 100%;
    }
    
    .stFileUploader > div {
        background: white;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
    }
    
    section[data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e2e8f0;
    }
    
    h1, h2, h3, h4, p, span, li, label {
        color: #1e293b !important;
    }
    
    /* MOBILE RESPONSIVE */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem !important;
        }
        
        .stButton > button {
            padding: 12px 16px !important;
            font-size: 13px !important;
        }
        
        .user-msg, .bot-msg {
            padding: 12px 14px;
            font-size: 14px;
            max-width: 95% !important;
        }
        
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        .stTextInput > div > div > input {
            font-size: 16px !important;
        }
        
        h2, h3 {
            font-size: 1.2rem !important;
        }
        
        section[data-testid="stSidebar"] {
            width: 260px !important;
        }
    }
    
    /* Smaller phones */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.5rem !important;
        }
        
        .stButton > button {
            padding: 10px 12px !important;
            font-size: 12px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏥 MedLink Agent</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#64748b !important;">Your AI Health Companion - Upload & Chat</p>', unsafe_allow_html=True)

# Safety notice
st.markdown("""<div style="background:#fef3c7;border-left:4px solid #f59e0b;padding:10px 15px;border-radius:0 10px 10px 0;margin:10px 0;color:#92400e !important;">
⚠️ <b>Safety:</b> This provides general health information only. NO diagnosis. Always consult your doctor.
</div>""", unsafe_allow_html=True)

# Sidebar - Settings only
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("🌐 Language", ["English", "ಕನ್ನಡ", "हिंदी"])
    lang_map = {"English": "english", "ಕನ್ನಡ": "kannada", "हिंदी": "hindi"}
    lang_key = lang_map[language]
    
    st.markdown("---")
    st.header("📁 Your Data")
    try:
        with open("data/reports.json", "r") as f:
            reports = json.load(f)
        st.info(f"📋 {len(reports)} report(s)")
    except:
        reports = []
        st.info("No reports yet")
    
    if st.button("🗑️ Clear All Data"):
        for f in ["data/reports.json", "data/medicines.json", "data/timeline.json", "data/reminders.json"]:
            try:
                with open(f, "w") as file:
                    json.dump([], file)
            except:
                pass
        if "messages" in st.session_state:
            st.session_state.messages = []
        st.rerun()

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main content - Upload Section
st.markdown("### 📤 Upload Medical Report")
col_upload, col_analyze = st.columns([3, 1])

with col_upload:
    uploaded_file = st.file_uploader("Drop your report here (PDF, JPG, PNG)", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")

with col_analyze:
    if uploaded_file:
        if st.button("📊 Analyze", use_container_width=True):
            with st.spinner("Analyzing..."):
                try:
                    from agents.report_agent import extract_report, save_report
                    result = extract_report(image_bytes=uploaded_file.getvalue(), file_type=uploaded_file.type)
                    save_report(result)
                    st.success("✅ Done!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

if uploaded_file:
    st.success(f"📄 **{uploaded_file.name}** ready - Click **Analyze** to process")

st.markdown("---")

# Main content
st.header("💬 Chat with MedLink")

# Quick Actions Grid
st.markdown("**🎯 Quick Actions:**")
col1, col2, col3 = st.columns(3)
with col1:
    btn1 = st.button("📋 Summarize Report", use_container_width=True)
with col2:
    btn2 = st.button("💊 Check Medicines", use_container_width=True)
with col3:
    btn3 = st.button("🏥 Find Doctor", use_container_width=True)

col4, col5, col6 = st.columns(3)
with col4:
    btn4 = st.button("📅 Health Timeline", use_container_width=True)
with col5:
    btn5 = st.button("👨‍⚕️ Compare Doctors", use_container_width=True)
with col6:
    btn6 = st.button("❓ Ask Question", use_container_width=True)

# Emergency First-Aid Resources
st.markdown("""
<div style="background:#ecfdf5;border-left:4px solid #10b981;padding:8px 12px;border-radius:0 8px 8px 0;margin:8px 0;">
🆘 <b>Emergency First-Aid Kit:</b> <a href="https://t.me/NCINC_BOT" target="_blank" style="color:#059669;">@NCINC_BOT on Telegram</a> | 
📞 Emergency: <b>112</b>
</div>
""", unsafe_allow_html=True)

# Handle quick action buttons
action_query = None
if btn1:
    action_query = "Please summarize my uploaded medical report in simple terms"
elif btn2:
    action_query = "What medicines are mentioned in my report? Are there any I should be careful about?"
elif btn3:
    action_query = "Based on my report, what type of doctor should I see? Find nearby specialists."
elif btn4:
    action_query = "Build a timeline of my health records and show any trends"
elif btn5:
    action_query = "Help me compare different doctor opinions"
elif btn6:
    action_query = None  # Just focus on input

st.markdown("---")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# Chat input using form to prevent duplicate submissions
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="user_input", label_visibility="collapsed", placeholder="Ask me anything about your health...")
    col_send, col_clear = st.columns([1, 1])
    with col_send:
        submit_btn = st.form_submit_button("📤 Send", use_container_width=True)
    with col_clear:
        clear_btn = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)

# Handle form submission
if clear_btn:
    st.session_state.messages = []
    st.rerun()

# Process message (from input or action button)
query_to_process = None
if submit_btn and user_input:
    query_to_process = user_input
elif action_query:
    query_to_process = action_query

if query_to_process:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query_to_process})
    
    # Generate response
    try:
        # Load reports context
        try:
            with open("data/reports.json", "r") as f:
                reports_context = json.load(f)
        except:
            reports_context = []
        
        from tools.gemini_client import generate_content
        
        # Enhanced prompt with smart actions
        current_date = "2025-12-07"
        routing_prompt = f"""You are MedLink AI, a helpful medical assistant.

User message: "{query_to_process}"

User has {len(reports_context)} medical reports.
Latest report: {json.dumps(reports_context[-1] if reports_context else {{}}, ensure_ascii=False)[:1500]}

Current date: {current_date}
Respond in {language}. Be helpful and conversational.

EXTRA BEHAVIOUR - Support these 3 special actions:

1) MEDICINES (when user asks about medicines):
   - Explain in GENERAL terms only (e.g., "pain relievers", "acid-reducing tablets")
   - NEVER prescribe exact medicines or doses
   - Add: OPEN_BROWSER_SEARCH: "<google search text>"
   - Example: OPEN_BROWSER_SEARCH: "gall bladder stones treatment overview"

2) FIND DOCTOR (when user wants a doctor):
   - Decide suitable specialist (gastroenterologist, cardiologist, neurologist, etc.)
   - Say: "You should consult a <specialist>."
   - Add: MAP_SEARCH: "<specialist> near me"
   - Example: MAP_SEARCH: "gastroenterologist near me"

3) REMINDER (when user wants reminder/schedule):
   - Create clear reminder with reasonable defaults
   - Add: CREATE_REMINDER: {{"title":"<what>", "date":"YYYY-MM-DD", "time":"HH:MM", "repeat":"daily|none|weekly"}}
   - Example: CREATE_REMINDER: {{"title":"Take BP medicine", "date":"2025-12-07", "time":"21:00", "repeat":"daily"}}

RULES:
- Never diagnose diseases
- Never prescribe exact medicines
- Keep OPEN_BROWSER_SEARCH/MAP_SEARCH/CREATE_REMINDER in English only
- Always add: "I am an AI assistant and not a doctor. Please consult a qualified doctor for final medical advice."

Keep response helpful and concise."""

        response, _ = generate_content(routing_prompt)
        response_text = response.text
        
        # Parse and handle special actions
        import re
        import urllib.parse
        
        # Handle OPEN_BROWSER_SEARCH
        browser_match = re.search(r'OPEN_BROWSER_SEARCH:\s*["\']?([^"\'\n]+)["\']?', response_text)
        if browser_match:
            search_query = browser_match.group(1).strip()
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
            response_text = re.sub(r'OPEN_BROWSER_SEARCH:\s*["\']?[^"\'\n]+["\']?', '', response_text)
            response_text += f"\n\n🔗 [**Search: {search_query}**]({search_url})"
        
        # Handle MAP_SEARCH
        map_match = re.search(r'MAP_SEARCH:\s*["\']?([^"\'\n]+)["\']?', response_text)
        if map_match:
            map_query = map_match.group(1).strip()
            map_url = f"https://www.google.com/maps/search/{urllib.parse.quote(map_query)}"
            response_text = re.sub(r'MAP_SEARCH:\s*["\']?[^"\'\n]+["\']?', '', response_text)
            response_text += f"\n\n📍 [**Find on Map: {map_query}**]({map_url})"
        
        # Handle CREATE_REMINDER
        reminder_match = re.search(r'CREATE_REMINDER:\s*(\{[^}]+\})', response_text)
        if reminder_match:
            try:
                reminder_json = json.loads(reminder_match.group(1))
                reminder_text = f"⏰ **Reminder Set:** {reminder_json.get('title', 'Reminder')} at {reminder_json.get('time', '09:00')} ({reminder_json.get('repeat', 'none')})"
                response_text = re.sub(r'CREATE_REMINDER:\s*\{[^}]+\}', '', response_text)
                response_text += f"\n\n{reminder_text}"
                
                # Save reminder
                try:
                    with open("data/reminders.json", "r") as f:
                        reminders = json.load(f)
                except:
                    reminders = []
                reminders.append(reminder_json)
                with open("data/reminders.json", "w") as f:
                    json.dump(reminders, f, indent=2)
            except:
                pass
        
        st.session_state.messages.append({"role": "bot", "content": response_text.strip()})
        
    except Exception as e:
        st.session_state.messages.append({"role": "bot", "content": f"❌ Sorry, an error occurred: {e}"})
    
    st.rerun()

# Welcome message if no chat
if not st.session_state.messages:
    st.markdown("""
    <div class="bot-msg">
    🤖 <b>Hi! I'm MedLink, your AI health companion.</b><br><br>
    📤 <b>Upload</b> a medical report in the sidebar<br>
    🎯 Click a <b>Quick Action</b> button above<br>
    💬 Or just <b>type</b> your question below!<br><br>
    <b>I can:</b><br>
    • 📋 Summarize your reports<br>
    • 💊 Explain medicines (with browser search)<br>
    • 🏥 Find doctors near you (opens Maps)<br>
    • ⏰ Set health reminders<br>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align:center;color:#94a3b8 !important;font-size:0.8rem;">Built with ❤️ using Gemini AI + ADK | MedLink Agent Hackathon</p>', unsafe_allow_html=True)

