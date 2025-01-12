from flask import Flask, render_template, jsonify, request
import json
import requests
import isbnlib
from datetime import datetime
from googletrans import Translator
from google import generate_output as go
from lib import get_product_info, get_isbn_info, save_scan_result, get_past_barcodes

app = Flask(__name__)
translator = Translator()
barcodes = get_past_barcodes()

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

        # Check if barcode was previously scanned
        if barcode in barcodes:
            return render_template('result.html', scan_result={
                'success': 'This barcode has already been scanned.',
                'data': scan_data
            })

        # Process barcode data
        scan_data.update({
            'query': barcode,
            'isbn_ret': get_isbn_info(barcode) if len(barcode) in [10, 13] else None,
            'product': get_product_info(barcode)
        })

        # Save results
        filename = save_scan_result(scan_data)
        scan_data['saved_file'] = filename

        return render_template('result.html', scan_result=scan_data)

    except Exception as e:
        return render_template('result.html', scan_result={
            'error': str(e),
            'status': 'error'
        })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="64533", debug=True)
