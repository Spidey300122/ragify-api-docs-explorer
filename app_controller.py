import streamlit as st
import sys
import os
from typing import Optional, Dict, Any

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui_components import RAGifyUI

class RAGifyController:
    """Main controller for RAGify API Docs Explorer"""
    
    def __init__(self):
        self.ui = RAGifyUI()
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        defaults = {
            'rag_assistant': None, 
            'conversation': [], 
            'docs_loaded': False, 
            'current_query': "",
            'last_result': None,
            'last_query': None,
            'last_processed_query': None,
            'groq_key': ""
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def load_documentation(self) -> bool:
        """Load and process API documentation"""
        try:
            from src.scraper import APIDocsScraper
            from src.embeddings import EmbeddingsManager
            from src.rag import SmartAPIAssistant
            from src.utils import API_DOCS_URLS
            
            progress, status = self.ui.show_loading_progress("🔧 Initializing...", 0)
            
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
            
            self.ui.show_success_status(f"✨ Ready! Loaded {docs_added} documentation chunks")
            return True
            
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
            return False
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """Process a user question and return response"""
        st.session_state.current_query = question
        
        if not st.session_state.rag_assistant:
            return {"response": "Please load documentation first.", "sources": []}
        
        with st.spinner("🔍 Searching knowledge base..."):
            try:
                result = st.session_state.rag_assistant.search_and_respond(
                    question, 
                    st.session_state.conversation
                )
                
                st.session_state.last_result = result
                st.session_state.last_query = question
                st.session_state.conversation.extend([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": result["response"]}
                ])
                
                return result
                
            except Exception as e:
                error_msg = f"⚠️ Error processing question: {e}"
                st.error(error_msg)
                return {"response": error_msg, "sources": []}
    
    def handle_question_click(self, question: str):
        """Handle when a quick question is clicked"""
        result = self.process_question(question)
        st.session_state.last_result = result
        st.rerun()
    
    def reset_application(self):
        """Reset the application state"""
        st.session_state.clear()
        st.rerun()
    
    def run(self):
        """Main application runner"""
        # Render header and API coverage
        self.ui.render_header()
        self.ui.render_api_coverage()
        
        st.markdown("---")
        self.ui.show_info_message("**Quick Start:** 1️⃣ Add Groq API Key → 2️⃣ Hit Enter Key & Load Documentation → 3️⃣ Ask Questions!")
        
        # Handle sidebar interactions
        groq_key, load_docs_clicked, reset_clicked = self.ui.render_sidebar(
            st.session_state.get('groq_key', '')
        )
        
        # Store the API key in session state
        if groq_key:
            st.session_state.groq_key = groq_key
        
        # Handle load documentation
        if load_docs_clicked:
            if self.load_documentation():
                st.rerun()
        
        # Handle reset
        if reset_clicked:
            self.reset_application()
        
        # Render main interface
        query = self.ui.render_main_interface(
            groq_key, 
            st.session_state.get('docs_loaded', False)
        )
        
        # Process query if it's new
        if query and query != st.session_state.get('last_processed_query', ''):
            st.session_state.last_processed_query = query
            result = self.process_question(query)
            st.session_state.last_result = result
        
        # Display response if available
        if st.session_state.get('last_result'):
            self.ui.render_response(st.session_state.last_result)
        
        # Show quick questions if docs are loaded
        if st.session_state.get('docs_loaded', False):
            self.ui.render_quick_questions(self.handle_question_click)

def main():
    """Entry point for the application"""
    controller = RAGifyController()
    controller.run()

if __name__ == "__main__":
    main()