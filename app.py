import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="🚀 Smart API Docs Assistant", page_icon="🚀", layout="wide")

# Enhanced CSS with better contrast and proper branding
st.markdown("""<style>
.main-header {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 50%, #1d4ed8 100%);
    padding: 2rem; border-radius: 12px; color: white; text-align: center; 
    margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(37, 99, 235, 0.4);
}
.main-header h1 {margin: 0; font-size: 2.2rem; font-weight: 700;}
.main-header p {margin: 0.8rem 0 0 0; font-size: 1rem; line-height: 1.5;}

.api-brands {
    display: flex; justify-content: center; gap: 2rem; margin: 1.5rem 0;
    flex-wrap: wrap; align-items: center;
}
.brand-item {
    display: flex; align-items: center; gap: 0.5rem; 
    background: rgba(255,255,255,0.1); padding: 0.8rem 1.2rem; 
    border-radius: 8px; backdrop-filter: blur(10px);
    font-weight: 600; font-size: 0.9rem;
}

.chat-message {
    padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; 
    background: linear-gradient(145deg, #f8fafc 0%, #e2e8f0 100%); 
    border-left: 4px solid #2563eb; 
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.1); color: #1e293b;
    font-size: 1rem; line-height: 1.6;
}

.response-header {
    background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
    color: white; padding: 1rem 1.5rem; border-radius: 8px 8px 0 0;
    font-weight: 600; font-size: 1.1rem; margin-bottom: 0;
}

.sources-section {
    background: #f1f5f9; padding: 1.5rem; border-radius: 8px;
    margin-top: 1.5rem; border: 1px solid #e2e8f0;
}

.source-item {
    background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
    border-left: 3px solid #10b981; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stButton > button {
    width: 100%; margin: 0.3rem 0; border-radius: 8px;
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white; border: none; padding: 0.8rem; font-weight: 600;
    transition: all 0.3s ease; font-size: 0.9rem;
}
.stButton > button:hover {
    transform: translateY(-2px); box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
}

.quick-questions {
    background: #f8fafc; padding: 2rem; border-radius: 12px;
    border: 1px solid #e2e8f0; margin-top: 2rem;
}
.quick-questions h3 {
    color: #1e293b; margin-bottom: 1.5rem; text-align: center;
    font-size: 1.3rem; font-weight: 700;
}

.question-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem; margin-top: 1rem;
}

.brand-claude { color: #ff6b35; }
.brand-gemini { color: #4285f4; }
.brand-github { color: #333; }

.sidebar .stMarkdown {
    background: #f1f5f9; padding: 1rem; border-radius: 8px; 
    margin: 0.5rem 0; color: #334155;
}

.status-success {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    color: white; padding: 1rem; border-radius: 8px; text-align: center;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    font-weight: 600;
}

.steps-flow {
    background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;
    margin: 1rem 0; font-size: 0.95rem; backdrop-filter: blur(10px);
}

ol, ul {
    padding-left: 1.5rem !important;
}
li {
    margin: 0.5rem 0 !important;
    line-height: 1.6 !important;
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
    
    st.markdown('''
    <div class="main-header">
        <h1>🚀 RAGify API Docs Explorer</h1>
        <p><strong>AI-Powered API Documentation Assistant</strong><br>
        Get instant answers from Claude, Gemini & GitHub documentation using advanced RAG technology</p>
        
        <div class="api-brands">
            <div class="brand-item brand-claude">
                <span>🟠</span> Anthropic Claude
            </div>
            <div class="brand-item brand-gemini">
                <span>🔵</span> Google Gemini
            </div>
            <div class="brand-item brand-github">
                <span>⚫</span> GitHub API
            </div>
        </div>
        
        <div class="steps-flow">
            <strong>Quick Start:</strong> 
            1️⃣ Add Groq API Key → 2️⃣ Load Documentation → 3️⃣ Ask Questions! 🎯
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Setup")
        
        groq_key = st.text_input(
            "🔑 Groq API Key:", 
            type="password", 
            help="Get your free API key from console.groq.com",
            placeholder="gsk_..."
        )
        
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("🚀 API Key Connected!")
        
        if st.button("📥 Load Documentation", type="primary", disabled=not groq_key):
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
        
        # API Coverage Info
        st.markdown("### 📚 Coverage")
        st.markdown("""
        **🟠 Claude API:**
        - Messages & Streaming
        - System Prompts & Tool Use
        - Function Calling
        
        **🔵 Gemini API:**
        - Content Generation
        - Embeddings & Safety
        - Chat & Function Calling
        
        **⚫ GitHub API:**
        - Repositories & Authentication  
        - Issues & Users
        - REST API Endpoints
        """)
    
    # Main interface
    if not groq_key:
        st.info("🔑 **Get Started:** Obtain your free Groq API key from https://console.groq.com")
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
        st.markdown('''
        <div class="quick-questions">
            <h3>⚡ Popular Questions</h3>
        </div>
        ''', unsafe_allow_html=True)
        
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