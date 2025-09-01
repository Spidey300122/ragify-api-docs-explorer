import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="🚀 Smart API Docs Assistant", page_icon="🚀", layout="wide")

# Clean, classic styling
st.markdown("""<style>
.chat-message {
    padding: 1.2rem; border-radius: 8px; margin: 1rem 0; 
    background: #f8fafc; border-left: 4px solid #3b82f6; 
    border: 1px solid #e2e8f0; color: #1e293b;
}

.stButton > button {
    width: 100%; margin: 0.2rem 0; border-radius: 6px;
    background: #3b82f6; color: white; border: none; 
    padding: 0.6rem; font-weight: 500;
}
.stButton > button:hover {
    background: #2563eb;
}

.status-success {
    background: #10b981; color: white; padding: 0.8rem; 
    border-radius: 6px; text-align: center; font-weight: 500;
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
    
    # Simple brand display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🟠 Anthropic Claude**  \n*Messages, Streaming, Tool Use*")
    with col2:
        st.markdown("**🔵 Google Gemini**  \n*Generation, Embeddings, Safety*") 
    with col3:
        st.markdown("**⚫ GitHub API**  \n*Repos, Issues, Authentication*")
    
    st.markdown("---")
    st.info("**Quick Start:** 1️⃣ Add Groq API Key → 2️⃣ Load Documentation → 3️⃣ Ask Questions!")
    
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