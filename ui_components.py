import streamlit as st
import os
from typing import Dict, Any, List

class RAGifyUI:
    """UI Components for RAGify API Docs Explorer"""
    
    def __init__(self):
        self.setup_page_config()
        self.inject_custom_styles()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="🚀 Smart API Docs Assistant", 
            page_icon="🚀", 
            layout="wide"
        )
    
    def inject_custom_styles(self):
        """Inject custom CSS styles"""
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

        /* ENHANCED LIGHT BLUE SIDEBAR STYLING */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e3f2fd 0%, #bbdefb 25%, #90caf9 50%, #64b5f6 75%, #42a5f5 100%) !important;
            border-right: 3px solid #1976d2 !important;
            position: relative !important;
        }

        [data-testid="stSidebar"] > div {
            background: transparent !important;
            padding: 2.5rem 2rem !important;
            position: relative;
            z-index: 1;
        }

        /* Enhanced Sidebar Headers */
        [data-testid="stSidebar"] h3 {
            color: #0d47a1 !important;
            font-weight: 800 !important;
            font-size: 1.6rem !important;
            margin-bottom: 2rem !important;
            text-align: center !important;
            text-shadow: none !important;
            letter-spacing: 0.5px !important;
        }

        /* Sidebar Text with Dark Blue Colors */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: #1a237e !important;
            font-weight: 600 !important;
            text-shadow: none !important;
        }

        /* Sidebar Strong Text */
        [data-testid="stSidebar"] strong {
            color: #0d47a1 !important;
            font-weight: 700 !important;
            text-shadow: none !important;
        }

        /* Enhanced Sidebar Buttons with White Font */
        [data-testid="stSidebar"] .stButton > button {
            background: #1976d2 !important;
            color: white !important;
            border: 2px solid #1976d2 !important;
            border-radius: 10px !important;
            padding: 1.2rem !important;
            font-weight: 700 !important;
            width: 100% !important;
            margin: 1rem 0 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 20px rgba(25, 118, 210, 0.3) !important;
            text-transform: none !important;
            letter-spacing: 0.8px !important;
            font-size: 15px !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #138496 !important;
            border-color: #138496 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(23, 162, 184, 0.3) !important;
            color: white !important;
        }

        /* Force white text for ALL sidebar buttons */
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] .stButton > button:hover,
        [data-testid="stSidebar"] .stButton > button:active,
        [data-testid="stSidebar"] .stButton > button:focus {
            color: white !important;
        }

        /* Sidebar Input Fields */
        [data-testid="stSidebar"] .stTextInput input {
            background: white !important;
            color: #495057 !important;
            border: 2px solid #ced4da !important;
            border-radius: 6px !important;
            padding: 0.75rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stSidebar"] .stTextInput input:focus {
            border-color: #17a2b8 !important;
            box-shadow: 0 0 0 0.2rem rgba(23, 162, 184, 0.25) !important;
            background: white !important;
        }

        [data-testid="stSidebar"] .stTextInput input::placeholder {
            color: #6c757d !important;
        }

        /* Enhanced Alert Boxes in Sidebar */
        [data-testid="stSidebar"] .stSuccess > div {
            background: #17a2b8 !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 1rem !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(23, 162, 184, 0.2) !important;
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] .stWarning > div {
            background: #ffc107 !important;
            color: #212529 !important;
            border-radius: 6px !important;
            padding: 1rem !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2) !important;
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] .stInfo > div {
            background: #6c757d !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 1rem !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(108, 117, 125, 0.2) !important;
            font-weight: 600 !important;
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

        /* Text inputs - Main interface with BLACK text for better readability */
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.9) !important;
            backdrop-filter: blur(10px) !important;
            border: 2px solid rgba(255,255,255,0.3) !important;
            border-radius: 15px !important;
            color: #333333 !important;
            font-weight: 600 !important;
            padding: 1rem !important;
            font-size: 16px !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #4ECDC4 !important;
            box-shadow: 0 0 20px rgba(78, 205, 196, 0.5) !important;
            background: rgba(255,255,255,0.95) !important;
            color: #333333 !important;
        }

        /* Force black text for ALL main text inputs */
        .stTextInput > div > div > input,
        .stTextInput > div > div > input:focus,
        .stTextInput > div > div > input:active {
            color: #333333 !important;
        }

        /* Placeholder text styling */
        .stTextInput > div > div > input::placeholder {
            color: #666666 !important;
            opacity: 0.8 !important;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #4ECDC4, #45B7D1) !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            border: 2px solid rgba(255,255,255,0.3) !important;
        }

        /* Markdown styling */
        p, li {
            color: rgba(255,255,255,0.9) !important;
            font-weight: 500 !important;
        }
        </style>""", unsafe_allow_html=True)
    
    def render_header(self):
        """Render the main header section"""
        st.markdown("# 🚀 RAGify API Docs Explorer")
        st.markdown("### AI-Powered API Documentation Assistant")
        st.markdown("Get instant answers from **Claude**, **Gemini** & **GitHub** documentation using advanced RAG technology")
    
    def render_api_coverage(self):
        """Render the API coverage display with emoji icons or font icons"""
        col1, col2, col3 = st.columns(3)
        
        # OPTION 1: Using emoji icons (simplest fix)
        with col1:
            st.markdown("""
            <div class="api-column">
                <h3 style="margin-top:0; text-align:center;">
                    🧠 Anthropic Claude
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="api-column">
                <h3 style="margin-top:0; text-align:center;">
                    💎 Google Gemini
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="api-column">
                <h3 style="margin-top:0; text-align:center;">
                    🐙 GitHub API
                </h3>
            </div>
            """, unsafe_allow_html=True)
    
    def render_api_coverage_with_font_awesome(self):
        """Alternative: Using Font Awesome icons from CDN"""
        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="api-column">
                <h3 style="margin-top:0; text-align:center;">
                    <i class="fas fa-robot" style="color:#FFA500; margin-right:10px;"></i>
                    Anthropic Claude
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="api-column">
                <h3 style="margin-top:0; text-align:center;">
                    <i class="fab fa-google" style="color:#4285F4; margin-right:10px;"></i>
                    Google Gemini
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="api-column">
                <h3 style="margin-top:0; text-align:center;">
                    <i class="fab fa-github" style="color:#333; margin-right:10px;"></i>
                    GitHub API
                </h3>
            </div>
            """, unsafe_allow_html=True)
    
    def render_api_coverage_with_streamlit_images(self):
        """Alternative: Using st.image() with online images"""
        col1, col2, col3 = st.columns(3)
        
        # You can use publicly available logo URLs
        with col1:
            try:
                st.image("https://upload.wikimedia.org/wikipedia/commons/7/7a/Anthropic_logo.svg", 
                        width=50, caption="Anthropic Claude")
            except:
                st.markdown("🧠 **Anthropic Claude**")
        
        with col2:
            try:
                st.image("https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", 
                        width=50, caption="Google Gemini")
            except:
                st.markdown("💎 **Google Gemini**")
        
        with col3:
            try:
                st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", 
                        width=50, caption="GitHub API")
            except:
                st.markdown("🐙 **GitHub API**")
    
    def render_sidebar(self, groq_key: str = None) -> str:
        """Render the sidebar and return the API key"""
        with st.sidebar:
            st.markdown("### ⚙️ Setup for your Groq LLM")
            
            groq_key = st.text_input(
                "🔑 Groq API Key:", 
                type="password", 
                help="Get your free API key from console.groq.com/keys",
                placeholder="gsk_...",
                value=groq_key or ""
            )
            
            if groq_key:
                os.environ["GROQ_API_KEY"] = groq_key
                st.success("🚀 API Key Connected!")
            
            load_docs_clicked = st.button("📥 Load Documentation", type="primary", disabled=not groq_key)
            
            if st.session_state.get('docs_loaded', False):
                st.markdown('<div class="status-success">✅ Documentation Ready</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Load documentation first")
            
            st.markdown("---")
            
            reset_clicked = st.button("🔄 Reset Application")
            
            # Enhanced API Coverage Info
            st.markdown("### 📚 Documentation Coverage")
            st.markdown("""
            **🟡 Anthropic Claude:**
            - [API Messages](https://docs.anthropic.com/en/api/messages)
            - [Messages Streaming](https://docs.anthropic.com/en/api/messages-streaming)  
            - [Tool Use & Function Calling](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
            - [Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
            
            **🔵 Google Gemini:**
            - [Generate Content API](https://ai.google.dev/api/generate-content)
            - [Embeddings](https://ai.google.dev/gemini-api/docs/embeddings)
            - [Safety Settings](https://ai.google.dev/docs/safety_setting_gemini)
            - [Function Calling](https://ai.google.dev/docs/function_calling)
            
            **⚫ GitHub API:**
            - [Repositories](https://docs.github.com/en/rest/repos)
            - [Authentication](https://docs.github.com/en/rest/authentication)
            - [Issues Management](https://docs.github.com/en/rest/issues)
            - [Users](https://docs.github.com/en/rest/users)
            """)
            
            return groq_key, load_docs_clicked, reset_clicked
    
    def render_main_interface(self, groq_key: str, docs_loaded: bool):
        """Render the main chat interface"""
        if not groq_key:
            st.info("🔑 **Get Started:** Obtain your free Groq API key from https://console.groq.com/keys")
            return None
        
        if not docs_loaded:
            st.info("📚 **Next Step:** Click 'Load Documentation' to initialize the knowledge base!")
            return None
        
        st.markdown("### 💬 Ask Your Question")
        
        query = st.text_input(
            "Enter your question about API documentation:",
            value=st.session_state.get('current_query', ''),
            placeholder="e.g., How do I authenticate with Claude API using system prompts?",
            key="main_query"
        )
        
        return query
    
    def render_response(self, result: Dict[str, Any]):
        """Render the AI response and sources"""
        if not result:
            return
        
        st.markdown('<div class="response-header">🤖 AI Response</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-message">{result["response"]}</div>', 
                   unsafe_allow_html=True)
        
        if result.get("sources"):
            st.markdown('''
            <div class="sources-section">
                <h4 style="margin-top:0; color:#1e293b;">📖 Documentation Sources</h4>
            </div>
            ''', unsafe_allow_html=True)
            
            for i, source in enumerate(result["sources"], 1):
                with st.expander(f"📄 {source['source']} • {source['similarity']:.0%} relevance"):
                    st.markdown(f"**📌 Title:** {source['title']}")
                    st.markdown(f"**🔗 URL:** [{source['url']}]({source['url']})")
    
    def render_quick_questions(self, on_question_click):
        """Render popular questions section"""
        st.markdown("### ⚡ Popular Questions")
        
        questions = [
            ("🟡 Claude Messages API", "How does the Anthropic Messages API work with system prompts and role structure?"),
            ("🔵 Gemini Content Generation", "What is the Google Gemini generate-content API and how do I use it?"),
            ("⚫ GitHub Repository Management", "How do I create and manage repositories using GitHub REST API with authentication?"),
            ("🟡 Claude Tool Use", "How to implement function calling and tool use with Claude API including JSON schema?"),
            ("🔵 Gemini Safety Settings", "How do I configure safety settings and content filtering in Gemini API?"),
            ("⚫ GitHub Issues API", "How to create, update and manage issues using GitHub API with labels and assignees?")
        ]
        
        cols = st.columns(3)
        for i, (label, question) in enumerate(questions):
            with cols[i % 3]:
                if st.button(label, key=f"q_{i}"):
                    on_question_click(question)
    
    def show_info_message(self, message: str):
        """Show info message"""
        st.info(message)
    
    def show_loading_progress(self, progress_text: str, progress_value: float):
        """Show loading progress"""
        progress = st.progress(progress_value)
        status = st.empty()
        status.text(progress_text)
        return progress, status
    
    def show_success_status(self, message: str):
        """Show success status"""
        st.markdown(f'<div class="status-success">{message}</div>', unsafe_allow_html=True)