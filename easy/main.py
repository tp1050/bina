from flask import Flask, jsonify, render_template,  redirect,request
from zto4.extraction.barcode2 import  get_product_by_barcode
import json
import pandas as pd
from functools import lru_cache
from datetime import datetime

app = Flask(__name__)

@app.route('/inventories', methods=['GET'])
def view_inventories():
    import glob
    import os
    from collections import Counter
    
    # Get all inventory files
    inventory_files = glob.glob('/tmp/accepter/gtins/invet_*.inventory')
    
    inventories = {}
    for inv_file in inventory_files:
        inventory_name = os.path.basename(inv_file).replace('invet_', '').replace('.inventory', '')
        
        with open(inv_file, 'r') as f:
            barcodes = f.read().splitlines()
            # Count unique barcodes
            barcode_counts = Counter(barcodes)
            
        inventories[inventory_name] = dict(barcode_counts)
    
    return render_template('inventories.html', inventories=inventories)

@app.route('/')
def indexer():
    paths = []
    for route in app.url_map.iter_rules():
        paths.append({
            'url': str(route),
            'name': str(route).lstrip('/')
        })
    return render_template('indexer.html', paths=paths)


@app.route('/add_to_inventory', methods=['POST'])
def add_to_inventory():
    inventory_name = request.form.get('inventory')
    barcode = request.form.get('barcode')
    
    if inventory_name and barcode:
        filename = f'/tmp/accepter/gtins/invet_{inventory_name}.inventory'
        with open(filename, 'a+') as f:
            f.write(f'{barcode}\n')
        
        return redirect(f'/gtin/{barcode}')
    
    return redirect('/')

@app.route('/gtin', methods=['GET']) 
@app.route('/gtin/<barcode>', methods=['GET'])
def gtin(barcode=None):
    if barcode:
        with open('/tmp/accepter/gtin/gtin.log', 'a+') as f:f.write(f'{barcode}\n')

        product_info = get_product_by_barcode(barcode)
        
        if product_info:            
            return render_template('product_view2.html', data=product_info)
    return render_template('scanner3.html')



app.run(debug=True,port="64533",host="0.0.0.0")
