import streamlit as st
import os

class RAGifyUI:
    def __init__(self):
        st.set_page_config(page_title="🚀 RAGify", page_icon="🚀", layout="wide")
        self._inject_styles()
    
    def _inject_styles(self):
        st.markdown("""<style>
        .stApp { background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1); animation: shift 15s infinite; }
        @keyframes shift { 0%, 100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
        .main .block-container { background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 25px; padding: 2rem; }
        .chat-message { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; border-radius: 20px; margin: 1rem 0; }
        .stButton > button { background: linear-gradient(135deg, #667eea, #764ba2) !important; color: white !important; border-radius: 15px !important; padding: 1rem !important; font-weight: 700 !important; }
        .stButton > button:hover { background: linear-gradient(135deg, #FF6B6B, #4ECDC4) !important; transform: translateY(-2px) !important; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #e3f2fd, #42a5f5) !important; }
        [data-testid="stSidebar"] .stButton > button { background: #1976d2 !important; color: white !important; }
        [data-testid="stSidebar"] .stButton > button:hover { background: #138496 !important; color: white !important; }
        .stTextInput input { background: rgba(255,255,255,0.9) !important; color: #333 !important; border-radius: 15px !important; }
        .api-column { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 15px; margin: 0.5rem; }
        h1 { background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
        </style>""", unsafe_allow_html=True)
    
    def render_header(self):
        st.markdown("# 🚀 RAGify API Docs Explorer")
        st.markdown("### AI-Powered API Documentation Assistant")
    
    def render_api_coverage(self):
        col1, col2, col3 = st.columns(3)
        apis = [
            ("🟡 Anthropic Claude", ["API Messages", "Streaming", "Tool Use", "Prompts"]),
            ("🔵 Google Gemini", ["Generate Content", "Embeddings", "Safety", "Functions"]),
            ("⚫ GitHub API", ["Repositories", "Auth", "Issues", "Users"])
        ]
        
        for col, (title, items) in zip([col1, col2, col3], apis):
            with col:
                st.markdown(f'<div class="api-column"><h3>{title}</h3><ul>{"".join(f"<li>{item}</li>" for item in items)}</ul></div>', unsafe_allow_html=True)
    
    def render_sidebar(self, groq_key=""):
        with st.sidebar:
            st.markdown("### ⚙️ Setup")
            groq_key = st.text_input("🔑 Groq API Key:", type="password", value=groq_key, placeholder="gsk_...")
            
            if groq_key:
                os.environ["GROQ_API_KEY"] = groq_key
                st.success("🚀 Connected!")
            
            load_clicked = st.button("🔥 Load Documentation", disabled=not groq_key)
            
            if st.session_state.get('docs_loaded'):
                st.success("✅ Ready")
            else:
                st.warning("⚠️ Load docs first")
            
            reset_clicked = st.button("🔄 Reset")
            return groq_key, load_clicked, reset_clicked
    
    def render_main_interface(self, groq_key, docs_loaded):
        if not groq_key:
            st.info("🔑 Get your free Groq API key from console.groq.com")
            return None
        if not docs_loaded:
            st.info("📚 Click 'Load Documentation' to start!")
            return None
        
        return st.text_input("💬 Ask about API documentation:", placeholder="How do I authenticate with Claude API?")
    
    def render_response(self, result):
        if not result: return
        st.markdown(f'<div class="chat-message">{result["response"]}</div>', unsafe_allow_html=True)
        
        if result.get("sources"):
            for i, src in enumerate(result["sources"][:3]):
                with st.expander(f"📄 {src['source']} • {src['similarity']:.0%}"):
                    st.markdown(f"**{src['title']}**")
                    st.markdown(f"[{src['url']}]({src['url']})")
    
    def render_quick_questions(self, callback):
        st.markdown("### ⚡ Popular Questions")
        questions = [
            ("🟡 Claude Messages", "How does Anthropic Messages API work with system prompts?"),
            ("🔵 Gemini Content", "What is Google Gemini generate-content API?"),
            ("⚫ GitHub Repos", "How to create repositories using GitHub REST API?"),
            ("🟡 Claude Tools", "How to implement function calling with Claude API?"),
            ("🔵 Gemini Safety", "How to configure Gemini safety settings?"),
            ("⚫ GitHub Issues", "How to manage GitHub issues with API?")
        ]
        
        cols = st.columns(3)
        for i, (label, question) in enumerate(questions):
            with cols[i % 3]:
                if st.button(label, key=f"q_{i}"):
                    callback(question)
    
    def show_loading_progress(self, text, value):
        return st.progress(value), st.empty().text(text)
    
    def show_success(self, message):
        st.markdown(f'<div style="background: linear-gradient(135deg, #00F260, #0575E6); color: white; padding: 1rem; border-radius: 10px; text-align: center; font-weight: 700;">{message}</div>', unsafe_allow_html=True)