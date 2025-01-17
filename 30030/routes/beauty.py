import requests
from flask import render_template, jsonify, request, redirect, url_for
import os
from datetime import datetime
import json

class ProductLookup:
    def __init__(self):
        self.barcodefinder_api_key = "77777"
        self.barcodefinder_url = "https://api.barcodefinder.info/product"
        self.openbeauty_url = "https://world.openbeautyfacts.org/api/v3/product"
        self.headers = {
            'Authorization': f'Bearer {self.barcodefinder_api_key}'
        }

    def get_upc_data(self, barcode):
        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
        headers = {
            'user-agent': 'Mozilla/5.0',
            'accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

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
            'raw_data': product,
            'price_history': self.get_price_history(product.get('code', ''))
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
            'raw_data': data,
            'price_history': self.get_price_history(barcode)
        }

    def format_upc_data(self, data, barcode):
        item = data['items'][0]
        return {
            'title': item.get('title', ''),
            'brand': item.get('brand', ''),
            'description': item.get('description', ''),
            'images': item.get('images', []),
            'category': item.get('category', ''),
            'manufacturer': item.get('manufacturer', ''),
            'barcode': barcode,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'UPCItemDB',
            'raw_data': item,
            'price_history': self.get_price_history(barcode)
        }

    def get_price_history(self, barcode):
        try:
            with open('price_history.json', 'r') as f:
                history = [json.loads(line) for line in f if json.loads(line)['barcode'] == barcode]
            return sorted(history, key=lambda x: x['timestamp'], reverse=True)
        except FileNotFoundError:
            return []

    def save_price_info(self, barcode, price, shop_name):
        price_data = {
            'barcode': barcode,
            'price': float(price),
            'shop': shop_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            with open('price_history.json', 'a') as f:
                json.dump(price_data, f)
                f.write('\n')
            return True
        except Exception as e:
            print(f"Error saving price info: {e}")
            return False

    def get_product_details(self, barcode):
        try:
            # Try UPC Database first
            upc_data = self.get_upc_data(barcode)
            if upc_data and upc_data.get('items'):
                return self.format_upc_data(upc_data, barcode)
            
            # Try Barcodefinder second
            barcodefinder_response = requests.get(
                f"{self.barcodefinder_url}/{barcode}", 
                headers=self.headers,
                timeout=5
            )
            
            if barcodefinder_response.status_code == 200:
                return self.format_barcodefinder_data(barcodefinder_response.json(), barcode)
            
            # Fallback to OpenBeautyFacts
            openbeauty_response = requests.get(
                f"{self.openbeauty_url}/{barcode}.json",
                timeout=5
            )
            if openbeauty_response.status_code == 200:
                return self.format_openbeauty_data(openbeauty_response.json())
                
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            
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

    @app.route('/beauty/<barcode>', methods=['GET', 'POST'])
    def beauty_lookup(barcode):
        if request.method == 'POST':
            price = request.form.get('price')
            shop = request.form.get('shop')
            product_lookup.save_price_info(barcode, price, shop)
            return redirect(url_for('beauty_lookup', barcode=barcode))

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
