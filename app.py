import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="🚀 Smart API Docs Assistant", page_icon="🚀", layout="wide")

# Ultra Vibrant Theme
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* Main app background - Electric gradient */
.stApp {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7, #DDA0DD, #98D8C8);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    font-family: 'Inter', sans-serif;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Main content container - Glassmorphism */
.main .block-container {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 25px;
    padding: 2.5rem;
    margin: 1rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

/* Chat messages - Neon style */
.chat-message {
    padding: 2rem; 
    border-radius: 20px; 
    margin: 1.5rem 0; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; 
    border: 2px solid rgba(255,255,255,0.3);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}

.chat-message::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Buttons - Electric neon */
.stButton > button {
    width: 100% !important; 
    margin: 0.5rem 0 !important; 
    border-radius: 15px !important;
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important; 
    border: 2px solid rgba(255,255,255,0.3) !important; 
    padding: 1rem !important; 
    font-weight: 700 !important;
    font-size: 16px !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4) !important;
    transform: translateY(-5px) scale(1.02) !important;
    box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4) !important;
    border-color: rgba(255,255,255,0.5) !important;
}

/* Success status - Glowing */
.status-success {
    background: linear-gradient(135deg, #00F260, #0575E6);
    color: white; 
    padding: 1.5rem; 
    border-radius: 15px; 
    text-align: center; 
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(0, 242, 96, 0.4);
    border: 2px solid rgba(255,255,255,0.3);
    font-size: 18px;
}

/* Sidebar - Multiple selectors for compatibility */
.css-1d391kg, 
[data-testid="stSidebar"],
.css-1d391kg > div,
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 30%, #16213e 70%, #0f0f23 100%) !important;
    border-right: 3px solid #4ECDC4 !important;
    box-shadow: 5px 0 20px rgba(78, 205, 196, 0.2) !important;
}

/* Sidebar content wrapper */
[data-testid="stSidebar"] > div > div {
    background: transparent !important;
    padding: 1rem !important;
}

/* All sidebar text elements */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: rgba(255, 255, 255, 0.95) !important;
    font-weight: 500 !important;
}

/* Sidebar headers specifically */
[data-testid="stSidebar"] h3 {
    color: #4ECDC4 !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 0 10px rgba(78, 205, 196, 0.5) !important;
    background: linear-gradient(135deg, #4ECDC4, #45B7D1) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: 2px solid #4ECDC4 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 0.8rem 1.2rem !important;
    margin: 0.75rem 0 !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #4ECDC4, #45B7D1) !important;
    border-color: white !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 30px rgba(78, 205, 196, 0.5) !important;
}

/* Sidebar text inputs */
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: rgba(15, 15, 35, 0.9) !important;
    border: 2px solid #4ECDC4 !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px) !important;
}

[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
    border-color: #45B7D1 !important;
    box-shadow: 0 0 20px rgba(78, 205, 196, 0.6) !important;
    background: rgba(15, 15, 35, 1) !important;
}

/* Sidebar input labels */
[data-testid="stSidebar"] .stTextInput > label {
    color: #4ECDC4 !important;
    font-weight: 600 !important;
}

/* Sidebar success messages */
[data-testid="stSidebar"] .stSuccess > div {
    background: linear-gradient(135deg, #00F260, #0575E6) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 700 !important;
    text-align: center !important;
    box-shadow: 0 8px 20px rgba(0, 242, 96, 0.4) !important;
    padding: 1rem !important;
}

/* Sidebar warnings */
[data-testid="stSidebar"] .stWarning > div {
    background: linear-gradient(135deg, #FF6B6B, #FFE66D) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4) !important;
    padding: 1rem !important;
}

/* Sidebar markdown blocks */
[data-testid="stSidebar"] .stMarkdown {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(78, 205, 196, 0.4) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    margin: 0.8rem 0 !important;
    backdrop-filter: blur(10px) !important;
}

/* Sidebar dividers */
[data-testid="stSidebar"] hr {
    border: none !important;
    height: 3px !important;
    background: linear-gradient(90deg, transparent, #4ECDC4, transparent) !important;
    margin: 2rem 0 !important;
    border-radius: 2px !important;
}

/* Force sidebar background for all elements */
[data-testid="stSidebar"] * {
    border-color: rgba(78, 205, 196, 0.3) !important;
}

/* Headers - Rainbow text */
h1 {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 800 !important;
    font-size: 3rem !important;
    text-align: center !important;
    margin-bottom: 0 !important;
}

h2, h3 {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 700 !important;
}

/* Info boxes - Holographic */
.stInfo {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    border-radius: 15px !important;
    color: white !important;
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
}

/* Warning boxes - Neon orange */
.stWarning {
    background: linear-gradient(135deg, #FF6B6B, #FFE66D) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    border-radius: 15px !important;
    color: white !important;
    box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3) !important;
}

/* Text inputs - Glowing */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.15) !important;
    backdrop-filter: blur(10px) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    border-radius: 15px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 1rem !important;
    font-size: 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #4ECDC4 !important;
    box-shadow: 0 0 20px rgba(78, 205, 196, 0.5) !important;
}

/* Custom response header */
.response-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 1rem 2rem;
    border-radius: 15px 15px 0 0;
    font-size: 1.2rem;
    font-weight: 700;
    text-align: center;
    border: 2px solid rgba(255,255,255,0.3);
    border-bottom: none;
}

/* Sources section */
.sources-section {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid rgba(255,255,255,0.2);
    margin-top: 1rem;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #4ECDC4, #45B7D1) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
}

/* Columns for API info */
.api-column {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid rgba(255,255,255,0.2);
    margin: 0.5rem;
    color: white;
    font-weight: 600;
}

/* Markdown styling */
p, li {
    color: rgba(255,255,255,0.9) !important;
    font-weight: 500 !important;
}

/* Selection highlighting */
::selection {
    background: rgba(78, 205, 196, 0.3);
    color: white;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #4ECDC4, #45B7D1);
}
</style>""", unsafe_allow_html=True)

def init_session():
    defaults = {'rag_assistant': None, 'conversation': [], 'docs_loaded': False, 'current_query': ""}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def load_docs():
    try:
        from src.scraper import APIDocsScraper
        from src.embeddings import EmbeddingsManager
        from src.rag import SmartAPIAssistant
        from src.utils import API_DOCS_URLS
        
        progress = st.progress(0)
        status = st.empty()
        
        status.text("🔧 Initializing...")
        scraper = APIDocsScraper(delay=0.5)
        progress.progress(0.25)
        
        status.text("📋 Collecting documentation...")
        urls = [url for urls_list in API_DOCS_URLS.values() for url in urls_list]
        progress.progress(0.5)
        
        status.text(f"📖 Processing {len(urls)} pages...")
        docs = [doc for url in urls if 'error' not in (doc := scraper.scrape_url(url))]
        progress.progress(0.75)
        
        status.text("🧠 Creating knowledge base...")
        embeddings = EmbeddingsManager()
        docs_added = embeddings.add_documents(docs)
        st.session_state.rag_assistant = SmartAPIAssistant()
        st.session_state.docs_loaded = True
        progress.progress(1.0)
        
        status.markdown(f'<div class="status-success">✨ Ready! Loaded {docs_added} documentation chunks</div>', unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return False

def process_question(question: str):
    st.session_state.current_query = question
    if st.session_state.rag_assistant:
        with st.spinner("🔍 Searching knowledge base..."):
            try:
                result = st.session_state.rag_assistant.search_and_respond(question, st.session_state.conversation)
                st.session_state.last_result = result
                st.session_state.last_query = question
                st.session_state.conversation.extend([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": result["response"]}
                ])
            except Exception as e:
                st.error(f"⚠️ Error processing question: {e}")

def main():
    init_session()
    
    # Clean header without complex HTML
    st.markdown("# 🚀 RAGify API Docs Explorer")
    st.markdown("### AI-Powered API Documentation Assistant")
    st.markdown("Get instant answers from **Claude**, **Gemini** & **GitHub** documentation using advanced RAG technology")
    
    # Vibrant API coverage display with glassmorphism
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="api-column">
            <h3 style="margin-top:0; text-align:center;">🟠 Anthropic Claude</h3>
            <ul style="list-style:none; padding:0;">
                <li>🔸 API Messages</li>
                <li>🔸 Messages Streaming</li>
                <li>🔸 Tool Use & Function Calling</li>
                <li>🔸 Prompt Engineering</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="api-column">
            <h3 style="margin-top:0; text-align:center;">🔵 Google Gemini</h3>
            <ul style="list-style:none; padding:0;">
                <li>🔹 Generate Content API</li>
                <li>🔹 Embeddings</li>
                <li>🔹 Safety Settings</li>
                <li>🔹 Function Calling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="api-column">
            <h3 style="margin-top:0; text-align:center;">⚫ GitHub API</h3>
            <ul style="list-style:none; padding:0;">
                <li>⚪ Repositories</li>
                <li>⚪ Authentication</li>
                <li>⚪ Issues Management</li>
                <li>⚪ Users</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("**Quick Start:** 1️⃣ Add Groq API Key → 2️⃣ Load Documentation → 3️⃣ Ask Questions!")
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Setup")
        
        groq_key = st.text_input(
            "🔑 Groq API Key:", 
            type="password", 
            help="Get your free API key from console.groq.com/keys",
            placeholder="gsk_..."
        )
        
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("🚀 API Key Connected!")
        
        if st.button("🔥 Load Documentation", type="primary", disabled=not groq_key):
            if load_docs():
                st.rerun()
        
        if st.session_state.docs_loaded:
            st.markdown('<div class="status-success">✅ Documentation Ready</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Load documentation first")
        
        st.markdown("---")
        
        if st.button("🔄 Reset Application"):
            st.session_state.clear()
            st.rerun()
        
        # Enhanced API Coverage Info
        st.markdown("### 📚 Documentation Coverage")
        st.markdown("""
        **🟠 Anthropic Claude:**
        - API Messages
        - Messages Streaming  
        - Tool Use & Function Calling
        - Prompt Engineering Overview
        
        **🔵 Google Gemini:**
        - Generate Content API
        - Embeddings
        - Safety Settings
        - Function Calling
        
        **⚫ GitHub API:**
        - Repositories
        - Authentication
        - Issues Management
        - Users
        """)
    
    # Main interface
    if not groq_key:
        st.info("🔑 **Get Started:** Obtain your free Groq API key from https://console.groq.com/keys")
        return
    
    if not st.session_state.docs_loaded:
        st.info("📚 **Next Step:** Click 'Load Documentation' to initialize the knowledge base!")
        return
    
    # Enhanced chat interface
    st.markdown("### 💬 Ask Your Question")
    
    query = st.text_input(
        "Enter your question about API documentation:",
        value=st.session_state.current_query,
        placeholder="e.g., How do I authenticate with Claude API using system prompts?",
        key="main_query"
    )
    
    if query and query != st.session_state.get('last_processed_query', ''):
        st.session_state.last_processed_query = query
        process_question(query)
    
    # Enhanced results display
    if hasattr(st.session_state, 'last_result'):
        st.markdown('<div class="response-header">🤖 AI Response</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-message">{st.session_state.last_result["response"]}</div>', 
                   unsafe_allow_html=True)
        
        if st.session_state.last_result["sources"]:
            st.markdown('''
            <div class="sources-section">
                <h4 style="margin-top:0; color:#1e293b;">📖 Documentation Sources</h4>
            </div>
            ''', unsafe_allow_html=True)
            
            for i, source in enumerate(st.session_state.last_result["sources"], 1):
                with st.expander(f"📄 {source['source']} • {source['similarity']:.0%} relevance"):
                    st.markdown(f"**📌 Title:** {source['title']}")
                    st.markdown(f"**🔗 URL:** [{source['url']}]({source['url']})")
    
    # Enhanced quick questions
    if st.session_state.docs_loaded:
        st.markdown("### ⚡ Popular Questions")
        
        questions = [
            ("🟠 Claude Messages API", "How does the Anthropic Messages API work with system prompts and role structure?"),
            ("🔵 Gemini Content Generation", "What is the Google Gemini generate-content API and how do I use it?"),
            ("⚫ GitHub Repository Management", "How do I create and manage repositories using GitHub REST API with authentication?"),
            ("🟠 Claude Tool Use", "How to implement function calling and tool use with Claude API including JSON schema?"),
            ("🔵 Gemini Safety Settings", "How do I configure safety settings and content filtering in Gemini API?"),
            ("⚫ GitHub Issues API", "How to create, update and manage issues using GitHub API with labels and assignees?")
        ]
        
        cols = st.columns(3)
        for i, (label, question) in enumerate(questions):
            with cols[i % 3]:
                if st.button(label, key=f"q_{i}"):
                    process_question(question)
                    st.rerun()

if __name__ == "__main__":
    main()