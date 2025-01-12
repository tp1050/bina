from flask import Flask, render_template, jsonify, request
import json
from regex import P
import requests
import isbnlib
from datetime import datetime
from googletrans import Translator
from google import generate_output as go
# from googlesearch import search
from lib import get_product_info, get_isbn_info, save_scan_result
app = Flask(__name__)
translator = Translator()

# from pathlib import Path
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan')
def scan():
    return render_template('scan3.html')

@app.route('/submit-scan', methods=['POST'])
def submit_scan():
    try:
        scan_data = request.json
        barcode = scan_data['scanned_data']
        print(f"Recived barcode: {barcode}")
        # Try ISBN first
        scan_data['isbn_ret'] = get_isbn_info(barcode) if len(barcode) in [10, 13] else None
        print(scan_data['isbn_ret'])
        # Try product lookup if ISBN fails
        scan_data['product']=get_product_info(barcode)
        print(scan_data['product'])
        # If both fail, try Google search
        gserp=go(barcode)
        if gserp:scan_data['GSERP']=gserp.get("html")
        scan_data['query']=barcode
        print(scan_data['GSERP'])
        filename = save_scan_result(scan_data)
        scan_data['saved_file'] = filename
        # response = requests.post('https://accepter.thesoole.ir/upload', json=scan_data)
        return jsonify({"status": "success", "data": scan_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="64533", debug=True)
