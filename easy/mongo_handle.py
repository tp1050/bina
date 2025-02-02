from pymongo import MongoClient
from functools import lru_cache

class BeautyDB:
    def __init__(self):
        self.client = MongoClient('mongodb://beauty_user:beauty123@localhost:27017')
        self.db = self.client.beauty_products
        self.products = self.db.products
    
    @lru_cache(maxsize=1000)
    def lookup(self, code):
        product = self.products.find_one({'code': code})
        if product:
            return {
                'name': product.get('product_name'),
                'brand': product.get('brands'),
                'description': product.get('generic_name'),
                'images': [
                    product.get('image_url'),
                    product.get('image_ingredients_url')
                ],
                'category': product.get('categories'),
                'manufacturer': product.get('manufacturing_places'),
                'ingredients': product.get('ingredients_text', '').split(','),
                'barcode': code,
                'source': 'OpenBeautyFacts'
            }
        return None
