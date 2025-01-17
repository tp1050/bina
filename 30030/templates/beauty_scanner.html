import requests
from flask import render_template

def get_product_details(barcode):
    url = f"https://api.barcodefinder.info/product/{barcode}"
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY'
    }
    
    response = requests.get(url, headers=headers)
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
            'raw_data': data  # Store full response for additional fields
        }
    return None

# Rest of the code remains the same
