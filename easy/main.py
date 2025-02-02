from flask import Flask, jsonify, render_template,  redirect
from zto4.extraction.barcode import GTINLookup, get_product_by_barcode
import json
import pandas as pd
from functools import lru_cache
from datetime import datetime

# class GTINLookup:
#     def __init__(self, csv_path):
#         self.csv_path = csv_path
#         self.columns = [
#             'code', 'product_name', 'abbreviated_product_name', 
#             'generic_name', 'quantity', 'brands', 'brands_tags',
#             'categories', 'categories_tags', 'categories_en',
#             'manufacturing_places', 'manufacturing_places_tags',
#             'labels', 'labels_tags', 'labels_en',
#             'ingredients_text', 'ingredients_tags',
#             'brand_owner', 'main_category', 'main_category_en',
#             'image_url', 'image_ingredients_url'
#         ]
#         self._load_data()
    
#     def _load_data(self):
#         df = pd.read_csv(
#             self.csv_path,
#             sep='\s+',
#             usecols=self.columns,
#             on_bad_lines='skip',
#             low_memory=False,
#             dtype=str
#         )
        
#         # Keep the first occurrence of each code
#         df = df.drop_duplicates(subset=['code'], keep='first')
        
#         # Now create the index-based dictionary
#         self.products = df.set_index('code').to_dict('index')

    
#     @lru_cache(maxsize=1000)
#     def lookup(self, gtin):
#         product = self.products.get(gtin, {})
#         return {
#             'name': product.get('product_name', ''),
#             'abbreviated_name': product.get('abbreviated_product_name', ''),
#             'brand': product.get('brands', ''),
#             'brand_owner': product.get('brand_owner', ''),
#             'description': product.get('generic_name', ''),
#             'quantity': product.get('quantity', ''),
#             'categories': product.get('categories', ''),
#             'categories_en': product.get('categories_en', ''),
#             'main_category': product.get('main_category_en', ''),
#             'manufacturing_places': product.get('manufacturing_places', ''),
#             'labels': product.get('labels', ''),
#             'ingredients': product.get('ingredients_text', '').split(',') if product.get('ingredients_text') else [],
#             'images': [
#                 product.get('image_url', ''),
#                 product.get('image_ingredients_url', '')
#             ],
#             'barcode': gtin,
#             'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'source': 'OpenBeautyFacts'
#         }

from mongo_handler import BeautyDB

GTINLookup = BeautyDB()
gtin_lookup = GTINLookup('data.csv')
app = Flask(__name__)


@app.route('/')

def indexer():
    paths = []
    for route in app.url_map.iter_rules():
        paths.append({
            'url': str(route),
            'name': str(route).lstrip('/')
        })
    return render_template('indexer.html', paths=paths)




@app.route('/gtin', methods=['GET']) 
@app.route('/gtin/<barcode>', methods=['GET'])
def gtin(barcode=None):
    if barcode:
        with open('/tmp/accepter/gtin/gtin.log', 'a+') as f:f.write(f'{barcode}\n')

        product_info = [gtin_lookup.lookup(barcode)    ,get_product_by_barcode(barcode)]
        
        if product_info:            
            return render_template('product_view.html', data=product_info)
        return render_template('scanner.html')



app.run(debug=True,port="64533",host="0.0.0.0")
