import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, Any
from urllib.parse import urlparse
from .utils import logger, clean_text

class APIDocsScraper:
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            
            return {
                "url": url,
                "title": self._get_title(soup, url),
                "content": clean_text(self._get_content(soup)),
                "source": self._get_source(url)
            }
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {"url": url, "error": str(e)}
    
    def _get_title(self, soup: BeautifulSoup, url: str) -> str:
        title = soup.find('title')
        if title: return clean_text(title.get_text())
        h1 = soup.find('h1')
        if h1: return clean_text(h1.get_text())
        return urlparse(url).path.split('/')[-1] or "API Documentation"
    
    def _get_content(self, soup: BeautifulSoup) -> str:
        # Find main content
        main = soup.select_one('main, article, .content, .documentation, [role="main"]') or soup.find('body')
        if not main: return ""
        
        # Extract meaningful text
        elements = main.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'code', 'pre'])
        content = [elem.get_text().strip() for elem in elements if len(elem.get_text().strip()) > 10]
        
        return "\n\n".join(content)
    
    def _get_source(self, url: str) -> str:
        domain = urlparse(url).netloc.lower()
        if 'anthropic' in domain: return 'Claude API'
        elif 'google' in domain or 'ai.google.dev' in domain: return 'Gemini API'
        elif 'github' in domain: return 'GitHub API'
        return domain