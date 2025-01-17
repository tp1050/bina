import requests
from flask import render_template, jsonify
import os
from datetime import datetime
import json

class ProductLookup:
    def __init__(self):
        # self.barcodefinder_api_key = os.getenv('BARCODEFINDER_API_KEY', 'YOUR_API_KEY')
        self.barcodefinder_url = "https://api.barcodefinder.info/product"
        self.openbeauty_url = "https://world.openbeautyfacts.org/api/v3/product"
        # self.headers = {
        #     'Authorization': f'Bearer {self.barcodefinder_api_key}'
        # }

    def format_openbeauty_data(self, data):
        product = data.get('product', {})
        return {
            'title': product.get('product_name', ''),
            'brand': product.get('brands', ''),
            'description': product.get('generic_name', ''),
            'images': [product.get('image_url')] if product.get('image_url') else [],
            'category': product.get('categories', ''),
            'manufacturer': product.get('manufacturing_places', ''),
            'ingredients': product.get('ingredients_text', '').split(',') if product.get('ingredients_text') else [],
            'barcode': product.get('code', ''),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'OpenBeautyFacts',
            'raw_data': product
        }

    def format_barcodefinder_data(self, data, barcode):
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
            'source': 'Barcodefinder',
            'raw_data': data
        }

    def get_product_details(self, barcode):
        ret=[]
        try:
           
            # Try Barcodefinder first
            # barcodefinder_response = requests.get(
            #     f"{self.barcodefinder_url}/{barcode}", 
            #     headers=self.headers,
            #     timeout=5
            # )
            
            # if barcodefinder_response.status_code == 200:
            #     ret.append( self.format_barcodefinder_data(barcodefinder_response.json(), barcode))
            
            # Fallback to OpenBeautyFacts
            openbeauty_response = requests.get(
                f"{self.openbeauty_url}/{barcode}.json",
                timeout=5
            )
            if openbeauty_response.status_code == 200:
                ret.appendopenbeauty_response.json())
            from lib import search_brocade, get_upc_data
            brocade_data = search_brocade(barcode)
            upc_data = get_upc_data(barcode)
            if brocade_data:
                ret.append( barcode)
            if upc_data:
                ret.append(upc_data)
                
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            
        return ret

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
