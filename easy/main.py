from flask import Flask, jsonify, render_template,  redirect
from zto4.extraction.barcode import  get_product_by_barcode
import json
import pandas as pd
from functools import lru_cache
from datetime import datetime

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

        product_info = get_product_by_barcode(barcode)
        
        if product_info:            
            return render_template('product_view.html', data=product_info)
    return render_template('scanner.html')



app.run(debug=True,port="64533",host="0.0.0.0")
