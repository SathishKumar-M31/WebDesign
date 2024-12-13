from flask import Flask, render_template, request, jsonify
from src.url_validator import validate_url
from src.seo_analyzer import SEOAnalyzer

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_url():
    """
    Analyze the provided URL for SEO parameters
    
    Returns:
        JSON response with SEO analysis
    """
    url = request.form.get('url')
    
    # Validate URL
    if not validate_url(url):
        return jsonify({
            'error': 'Invalid URL. Please enter a valid URL.',
            'status': 'error'
        }), 400
    
    # Perform SEO Analysis
    try:
        analyzer = SEOAnalyzer(url)
        
        # Fetch webpage
        if not analyzer.fetch_webpage():
            return jsonify({
                'error': 'Could not fetch webpage. Please check the URL.',
                'status': 'error'
            }), 400
        
        # Analyze SEO
        seo_params = analyzer.analyze_seo()
        suggestions = analyzer.generate_suggestions()
        
        return jsonify({
            'seo_params': seo_params,
            'suggestions': suggestions,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)