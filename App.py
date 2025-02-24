from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
import os
import logging
from flask import Flask, render_template, request, jsonify
from llm_service import generate_product_description

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.form
        product_name = data.get('product_name', '').strip()
        keywords = data.get('keywords', '').strip()
        tone = data.get('tone', 'neutral')

        # Validate inputs
        if not product_name or not keywords:
            return jsonify({
                'success': False,
                'error': 'Product name and keywords are required'
            }), 400

        # Split and clean keywords
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        if not keyword_list:
            return jsonify({
                'success': False,
                'error': 'At least one valid keyword is required'
            }), 400

        # Generate description
        description = generate_product_description(
            product_name=product_name,
            keywords=keyword_list,
            tone=tone
        )

        return jsonify({
            'success': True,
            'description': description
        })

    except Exception as e:
        logger.error(f"Error generating description: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate description. Please try again.'
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
