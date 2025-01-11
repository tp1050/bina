from flask import Flask, render_template, jsonify, request
import json
import requests
import isbnlib
from datetime import datetime
from googletrans import Translator
from google import generate_output as go
# from googlesearch import search

app = Flask(__name__)
translator = Translator()

def translate_text(text):
    try:
        return translator.translate(text, dest='fa').text
    except:
        return text


def save_scan_result(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    query=data.get("query","")
    filename = f"scan_{query}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filename

def get_isbn_info(isbn):
    try:
        book = isbnlib.meta(isbn)
        if book:
            return {
                "type": "book",
                "isbn": isbn,
                "title": book.get("Title", ""),
                "authors": book.get("Authors", []),
                "publisher": book.get("Publisher", ""),
                "year": book.get("Year", "")
            }
    except:
        return None

def get_product_info(barcode):
    api_url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                item = data['items'][0]
                return {
                    "type": "product",
                    "barcode": barcode,
                    "title": item.get('title', ''),
                    "brand": item.get('brand', ''),
                    "description": item.get('description', '')
                }
    except:
        return None
    return None






@app.route('/scan')
def scan():
    return render_template('scan3.html')

@app.route('/submit-scan', methods=['POST'])
def submit_scan():
    scan_data = request.json
    barcode = scan_data['scanned_data']
    
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
    
    response = requests.post('https://accepter.thesoole.ir/upload', json=scan_data)
    
    return jsonify({"status": "success", "data": scan_data})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="64533", debug=True)
