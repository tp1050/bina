from flask import Flask, render_template,  redirect
from zto4.extraction import ext_jsonld_product as e1
from zto4.extraction import ext_presta_product as e2
import json
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
        product_info = get_product_info(barcode, inventory_manager)
        if product_info:            
            product_json = json.dumps(product_info, indent=2)
            return render_template('gtin_result.html', 
                                product=product_info, 
                                product_json=product_json)
    
    return render_template('gtin_scanner.html')


app.run(debug=True,port="49090")

