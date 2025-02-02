from flask import Flask, jsonify, render_template,  redirect
from sympy import product
from zto4.extraction.barcode import get_product_by_barcode
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
        product_info=get_product_by_barcode(barcode)
        if product_info:            
            return render_template('table_view.html', data=product_info)
            # return render_template('gtin_result.html', 
            #                     product=product_info, 
            #                     product_json=product_json)
    
    return render_template('gtin_scanner.html')


app.run(debug=True,port="64533")
