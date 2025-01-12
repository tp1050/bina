from flask import Flask, render_template, jsonify, request
import json
import requests
import isbnlib
from datetime import datetime
from googletrans import Translator
from google import generate_output as go
import requests
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


def translate_text(text):
    try:
        return Translator.translate(text, dest='fa').text
    except:
        return text
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
    except Exception as e:
        print(e)
        return None

def save_scan_result(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    query=data.get("query","")
    filename = f"/tmp/accepter/barcode/jsons/{query}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filename


def get_past_barcodes():
    #get list of all json files in the json folder 
    #return list of barcodes
    import os
    barcodes = {}
    for file in os.listdir("/tmp/accepter/barcodes/jsons"):
        if file.endswith('.json'):
            try:
               barcodes[file.split('.')[0]]=json.load(open(f"/tmp/accepter/barcodes/jsons/{file}", "r"))
            except:
               pass
    return barcodes
