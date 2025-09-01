import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="🤖 Smart API Docs Assistant", page_icon="🤖", layout="wide")

# Enhanced CSS with better contrast
st.markdown("""<style>
.main-header {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 50%, #1d4ed8 100%);
    padding: 2rem; border-radius: 12px; color: white; text-align: center; 
    margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(37, 99, 235, 0.4);
}
.main-header h1 {margin: 0; font-size: 2.2rem; font-weight: 700;}
.main-header p {margin: 0.8rem 0 0 0; font-size: 1rem; line-height: 1.5;}

.chat-message {
    padding: 1.2rem; border-radius: 10px; margin: 1rem 0; 
    background: #f8fafc; border-left: 4px solid #2563eb; 
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1); color: #1e293b;
}

.stButton > button {
    width: 100%; margin: 0.2rem 0; border-radius: 6px;
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white; border: none; padding: 0.6rem; font-weight: 600;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.sidebar .stMarkdown {
    background: #f1f5f9; padding: 0.8rem; border-radius: 8px; 
    margin: 0.3rem 0; color: #334155;
}

.status-success {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    color: white; padding: 0.8rem; border-radius: 8px; text-align: center;
    box-shadow: 0 2px 8px rgba(5, 150, 105, 0.3);
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
        urls = [url for urls_list in API_DOCS_URLS.values() for url in urls_list]  # Fixed: removed [:2] limit
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
        st.error(f"❌ Error: {e}")
        return False

def process_question(question: str):
    st.session_state.current_query = question
    if st.session_state.rag_assistant:
        with st.spinner("🔍 Searching..."):
            try:
                result = st.session_state.rag_assistant.search_and_respond(question, st.session_state.conversation)
                st.session_state.last_result = result
                st.session_state.last_query = question
                st.session_state.conversation.extend([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": result["response"]}
                ])
            except Exception as e:
                st.error(f"❌ Error: {e}")

def main():
    init_session()
    
    st.markdown('''
    <div class="main-header">
        <h1>🚀 RAGify API Docs Explorer</h1>
        <p><strong>Ask questions about API documentation (Claude, Gemini, GitHub integration help!)</strong><br>
        🟡 <strong>Anthropic:</strong> Messages, Streaming, System Prompts, Tool Use | 
        🔵 <strong>Google:</strong> Gemini Generate, Chat, Embeddings, Safety Settings | 
        ⚫ <strong>GitHub:</strong> Repos, Authentication, Issues, Users<br>
        <em>📋 Steps: 1️⃣ Create Groq key → 2️⃣ Press Enter & "Load Documentation" → 3️⃣ Wait ~30 sec → 4️⃣ Ready to go! 🔥</em></p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Compact sidebar
    with st.sidebar:
        st.header("⚙️ Setup")
        
        groq_key = st.text_input("🔑 Groq API Key:", type="password", help="Free key from console.groq.com")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("🚀 Connected!")
        
        if st.button("🔥 Load Documentation", type="primary", disabled=not groq_key):
            if load_docs():
                st.rerun()
        
        if st.session_state.docs_loaded:
            st.markdown('<div class="status-success">✅ Ready</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Load docs first")
        
        if st.button("🔄 Reset"):
            st.session_state.clear()
            st.rerun()
    
    # Main interface
    if not groq_key:
        st.info("🔑 Get your free Groq API key from https://console.groq.com")
        return
    
    if not st.session_state.docs_loaded:
        st.info("📚 Click 'Load Documentation' to start!")
        return
    
    # Chat interface
    st.subheader("💬 Ask Your Question")
    query = st.text_input("Enter your question", value=st.session_state.current_query,  # Fixed: added proper label
                         placeholder="e.g., How do I create an S3 bucket using AWS API?")
    
    if query and query != st.session_state.get('last_processed_query', ''):
        st.session_state.last_processed_query = query
        process_question(query)
    
    # Display results
    if hasattr(st.session_state, 'last_result'):
        st.markdown("### 🤖 Response")
        st.markdown(f'<div class="chat-message">{st.session_state.last_result["response"]}</div>', 
                   unsafe_allow_html=True)
        
        if st.session_state.last_result["sources"]:
            st.markdown("### 📖 Sources")
            for i, source in enumerate(st.session_state.last_result["sources"], 1):
                with st.expander(f"📄 {source['source']} ({source['similarity']:.0%} match)"):
                    st.markdown(f"**Title:** {source['title']}")
                    st.markdown(f"**URL:** [{source['url']}]({source['url']})")
    
    # Quick questions
    if st.session_state.docs_loaded:
        st.markdown("### ⚡ Quick Questions")
        
        questions = [
            ("🟡 Claude Messages", "How does the Anthropic Messages API work with system prompts and role structure?"),
            ("🔵 Gemini Embeddings", "What is the Google embed-content API, explain with task type and models?"),
            ("⚫ GitHub Repos", "How do I create and manage repositories using GitHub REST API with authentication?"),
            ("🟡 Claude Tool Use", "How to implement function calling and tool use with Claude API including JSON schema?"),
            ("🔵 Gemini Safety", "How do I configure safety settings and content filtering in Gemini API?"),
            ("⚫ GitHub Issues", "How to create, update and manage issues using GitHub API with labels and assignees?")
        ]
        
        cols = st.columns(3)
        for i, (label, question) in enumerate(questions):
            with cols[i % 3]:
                if st.button(label, key=f"q_{i}"):
                    process_question(question)
                    st.rerun()

if __name__ == "__main__":
    main()