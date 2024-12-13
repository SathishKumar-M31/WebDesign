import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)

class SEOAnalyzer:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.response = None
        logging.info(" *****      2      ***** ")
        
    def fetch_webpage(self):
        """
        Fetch webpage content
        
        Returns:
            bool: True if successful, False otherwise
        """
        logging.info(" *****      3     ***** ")
        try:
            logging.info(" *****      4     ***** ")
            self.response = requests.get(
                self.url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=10
            )
            self.response.raise_for_status()
            
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            logging.info(" *****      5     ***** ")
            
            return True
        except requests.RequestException:
            return False
    
    def analyze_seo(self):
        """
        Analyze SEO parameters
        
        Returns:
            dict: SEO analysis results
        """
        logging.info(" *****      6     ***** ")
        logging.info(f"***** Self attributes: {self.__dict__} *****")
        if not self.soup:
            logging.info(" *****      7     ***** ")
            if not self.fetch_webpage():
                logging.info(" *****      8     ***** ")
                return {}
        
        # Basic SEO parameters
        logging.info(self)
        seo_params = {
            'Title': self._get_title(),
            'Title Length': self._get_title_length(),
            'Meta Description': self._get_meta_description(),
            'H1 Tags': self._count_h1_tags(),
            'Images with Alt': self._images_with_alt(),
            'External Links': self._count_external_links(),
            'Page Load Time': self._get_page_load_time(),
            'Mobile Friendly': self._check_mobile_friendly(),
        }
        logging.info(" *****      9    ***** ")
        return seo_params
    
    def _get_title(self):
        """Get page title"""
        title = self.soup.title.string if self.soup.title else "No Title"
        return title
    
    def _get_title_length(self):
        """Get title length and check optimal range"""
        title = self._get_title()
        length = len(title)
        return f"{length} chars ({'Optimal' if 50 <= length <= 60 else 'Improve'})"
    
    def _get_meta_description(self):
        """Get meta description"""
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        desc = meta_desc['content'] if meta_desc else "No Meta Description"
        return f"{desc[:100]}... ({'Good' if 150 <= len(desc or '') <= 160 else 'Improve'})"
    
    def _count_h1_tags(self):
        """Count H1 tags"""
        h1_tags = self.soup.find_all('h1')
        return f"{len(h1_tags)} tags ({'Optimal' if 1 <= len(h1_tags) <= 2 else 'Improve'})"
    
    def _images_with_alt(self):
        """Check images with alt text"""
        images = self.soup.find_all('img')
        images_with_alt = [img for img in images if img.get('alt')]
        return f"{len(images_with_alt)}/{len(images)} with alt ({'Good' if len(images_with_alt) == len(images) else 'Improve'})"
    
    def _count_external_links(self):
        """Count external links"""
        base_domain = urllib.parse.urlparse(self.url).netloc
        links = self.soup.find_all('a', href=True)
        
        # Filter external links
        external_links = [
            link for link in links 
            if link['href'].startswith('http') and 
            base_domain not in link['href']
        ]
        
        return f"{len(external_links)} external links"
    
    def _get_page_load_time(self):
        """Estimate page load time"""
        try:
            return f"{round(self.response.elapsed.total_seconds() * 1000, 2)} ms"
        except:
            return "N/A"
    
    def _check_mobile_friendly(self):
        """Check mobile friendliness"""
        meta_viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        return "Yes" if meta_viewport else "No"
    
    def generate_suggestions(self):
        """Generate SEO improvement suggestions"""
        suggestions = [
            "Optimize title length between 50-60 characters",
            "Add descriptive meta description (150-160 characters)",
            "Ensure 1-2 H1 tags per page",
            "Add alt text to all images",
            "Create internal linking structure",
            "Improve page load speed",
            "Ensure mobile responsiveness"
        ]
        return suggestions