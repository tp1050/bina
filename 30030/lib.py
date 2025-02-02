import requests
from bs4 import BeautifulSoup
import json
from bs4 import BeautifulSoup
import requests as r
import datetime


def extract_prestashop_json(js_content):
    """Extract prestashop JSON data from JavaScript content"""
    # Find the prestashop variable declaration
    start_marker = "var prestashop = "
    end_marker = ";"
    
    # Extract the JSON string
    start_index = js_content.find(start_marker) + len(start_marker)
    end_index = js_content.find(end_marker, start_index)
    json_str = js_content[start_index:end_index]
    
    # Parse the JSON data
    data = json.loads(json_str)
    
    # Extract relevant product information
    product_info = {
        'name': data['page']['meta']['title'],
        'description': data['page']['meta']['description'],
        'url': data['urls']['current_url'],
        'category': [item['title'] for item in data['breadcrumb']['links']],
      
    }
    
    return product_info

product={
    "name":"",
    "brand":"",
    "description":"",
    "images":[],
    "category":"",
    "manufacturer":"",
    "ingredients":[],
    "gtin":"",
    }
def search_brocade(barcode):
    url = f"https://www.brocade.io/api/items/{barcode}"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None
def search_upc(barcode):
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    headers = {
        'user-agent': 'Mozilla/5.0',
        'accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def search_openbeauty(barcode):
    """Retrieve product data from Open Beauty Facts"""
    url = f"https://world.openbeautyfacts.org/api/v3/product/{barcode}.json"
    
    try:
        response = requests.get(url, timeout=5)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException:
        return None

def search_torob(barcode):
    resp=r.get(f"https://www.torob.com/search/?q={barcode}")
    n=extract_next_data(resp.content)
    data=n["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]["results"][0]
    return data
def search_google():
    return 

def extract_next_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    next_data = soup.find('script', {'id': '__NEXT_DATA__'})
    
    if next_data:
        json_data = json.loads(next_data.string)
        return json_data
    return None
def search_cogita(barcode):

    product={
    "name":"",
    "brand":"",
    "description":"",
    "images":[],
    "category":"",
    "manufacturer":"",
    "ingredients":[],
    "gtin":"",
    }
    try:
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.128 Mobile Safari/537.36'
        # }

        # resp = r.get("https://www.qogita.com/products/?query={barcode}", headers=headers)
        resp = r.get("https://www.qogita.com/products/?query={barcode}")

        n=extract_next_data(resp.content)
        with open("n.json", "w") as f:
            json.dump(n, f)

        data=n["props"]["pageProps"]["dehydratedState"]["queries"][4]["state"]["data"]["results"][0]
        product["brand"]=data["brandName"]
        product["name"]=data["name"]
        product["images"].append(data["imageUrl"])
        product["category"]=data["categoryName"]
        product["gtin"]=data["gtin"]
        product["source"]="Cogita"
        product["last_update"]=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return product
    except Exception as e:
        print(e)
        return product