import requests
from flask import render_template, jsonify
import os
from datetime import datetime

class ProductLookup:
    def __init__(self):
        self.api_key = os.getenv('BARCODEFINDER_API_KEY', 'YOUR_API_KEY')
        self.base_url = "https://api.barcodefinder.info/product"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    def get_product_details(self, barcode):
        url = f"{self.base_url}/{barcode}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'title': data.get('name', ''),
                'brand': data.get('brand', ''),
                'description': data.get('description', ''),
                'images': [data.get('image')] if data.get('image') else [],
                'category': data.get('category', ''),
                'manufacturer': data.get('manufacturer', ''),
                'ingredients': data.get('ingredients', '').split(',') if data.get('ingredients') else [],
                'barcode': barcode,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'raw_data': data
            }
        return None

def save_scan_history(product_info):
    history_file = 'scan_history.json'
    try:
        with open(history_file, 'a') as f:
            json.dump(product_info, f)
            f.write('\n')
    except Exception as e:
        print(f"Error saving scan history: {e}")

def setup_routes(app):
    product_lookup = ProductLookup()

    @app.route('/beauty')
    def beauty_scanner():
        return render_template('beauty_scanner.html')

    @app.route('/beauty/<barcode>')
    def beauty_lookup(barcode):
        product_info = product_lookup.get_product_details(barcode)
        if product_info:
            save_scan_history(product_info)
        return render_template('beauty_result.html', product=product_info)

    @app.route('/api/beauty/<barcode>')
    def beauty_api(barcode):
        product_info = product_lookup.get_product_details(barcode)
        return jsonify(product_info if product_info else {"error": "Product not found"})

    @app.route('/beauty/history')
    def beauty_history():
        try:
            with open('scan_history.json', 'r') as f:
                history = [json.loads(line) for line in f]
            return render_template('beauty_history.html', scans=history)
        except FileNotFoundError:
            return render_template('beauty_history.html', scans=[])
