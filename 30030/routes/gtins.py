import requests
from flask import Response, render_template, jsonify, request, redirect, url_for
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests as r
import datetime
from bs4 import BeautifulSoup as BS




def get_basic_gtin(barcode):
    try:
        url = f"https://barcode-list.com/barcode/EN/barcode-{barcode}/Search.htm"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BS(response.text, 'html.parser')
            product= {
                'name':soup.find_all('meta')[1]['content'].split("This code meet the following products:")[1],
                'gtin':barcode,
                'source':url,
                'timestamp':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            with open("/tmp/accepter/gtins/jsons/basic_{barcode}.json","w") as j:json.dump(product,j)
            return product
    except Exception as e:
        print(e)
    return None



def setup_routes(app):
    @app.route('/gtin', methods=['GET']) 
    @app.route('/gtin/<barcode>', methods=['GET'])
    def gtin(barcode=None):
        if barcode:
            product_info = get_basic_gtin(barcode)#search_cogita(barcode)
            if product_info:            
                product_json = json.dumps(product_info, indent=2)
                return render_template('gtin_result.html', 
                                product=product_info, 
                                product_json=product_json)
        
        return render_template('gtin_scanner.html')
    




# def get_product():
#     product={
#         "name":"",
#         "brand":"",
#         "description":"",
#         "images":[],
#         "category":"",
#         "manufacturer":"",
#         "ingredients":[],
#         "gtin":"",
#     }
#     return product
    
    
# def extract_next_data(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     next_data = soup.find('script', {'id': '__NEXT_DATA__'})
    
#     if next_data:
#         json_data = json.loads(next_data.string)
#         return json_data
#     return None


# def setup_routes(app):
#     @app.route('/gtin', methods=['GET']) 
#     @app.route('/gtin/<barcode>', methods=['GET'])
#     def gtin_barcode(barcode=None):
#         if barcode:
#             product_info = get_basic_gtin(barcode)#search_cogita(barcode)
#             if product_info:            
#                 product_json = json.dumps(product_info, indent=2)
#         return render_template('gtin_result.html', 
#                                 product=product_info, 
#                                 product_json=product_json)
# def search_openbeauty(barcode):
#     """Retrieve product data from Open Beauty Facts"""
#     url = f"https://world.openbeautyfacts.org/api/v3/product/{barcode}.json"
#     product=get_product()
#     try:
#         response = requests.get(url, timeout=5)
#         return response.json() if response.status_code == 200 else None
#     except requests.RequestException:
#         return product

# def search_cogita(barcode):
        
#     product=get_product()
#     try:
#         resp=r.get(f"https://www.qogita.com/products/?query={barcode}")

#         n=extract_next_data(resp.content)
#         data=n["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]["results"][0]
#         product["brand"]=data["brandName"]
#         product["name"]=data["name"]
#         product["images"].append(data["imageUrl"])
#         product["category"]=data["categoryName"]
#         product["gtin"]=data["gtin"]
#         product["source"]="qogita"
#         product["last_update"]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     except Exception as e:
#         print(e)
#     return product

# def setup_routes(app):
#     @app.route('/gtin', methods=['GET']) 
#     @app.route('/gtin/<barcode>', methods=['GET'])
#     def gtin_barcode(barcode=None):
#         if barcode:
#             product_info = get_basic_gtin(barcode)#search_cogita(barcode)
#             if product_info:            
#                 product_json = json.dumps(product_info, indent=2)
#         return render_template('gtin_result.html', 
#                                 product=product_info, 
#                                 product_json=product_json)
#         return render_template('gtin_scanner.html')
#  def gtin_scanner():
        
# # def setup_routes(app):
# #     @app.route('/gtin_scanner', methods=['GET'])
# #     def gtin_scanner():
# #         return render_template('gtin_scanner.html')
# #     @app.route('/gtin/<barcode>')
# #     def gtin_barcode(barcode):
# #             product_info=[]
# #             product_info.append( search_cogita(barcode))
# #             return Response(json.dumps(product_info, indent=2), mimetype='application/json')








# # def search_cogita(barcode):
# #     import requests as r
# #     import datetime
# #     product={
# #     "name":"",
# #     "brand":"",
# #     "description":"",
# #     "images":[],
# #     "category":"",
# #     "manufacturer":"",
# #     "ingredients":[],
# #     "gtin":"",
# #     }
# #     try:



# def get_product():
#     product={
#         "name":"",
#         "brand":"",
#         "description":"",
#         "images":[],
#         "category":"",
#         "manufacturer":"",
#         "ingredients":[],
#         "gtin":"",
#     }
#     return product
    
    
# def extract_next_data(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     next_data = soup.find('script', {'id': '__NEXT_DATA__'})
    
#     if next_data:
#         json_data = json.loads(next_data.string)
#         return json_data
#     return None


# def setup_routes(app):
#     @app.route('/gtin', methods=['GET']) 
#     @app.route('/gtin/<barcode>', methods=['GET'])
#     def gtin_barcode(barcode=None):
#         if barcode:
#             product_info = get_basic_gtin(barcode)#search_cogita(barcode)
#             if product_info:            
#                 product_json = json.dumps(product_info, indent=2)
#         return render_template('gtin_result.html', 
#                                 product=product_info, 
#                                 product_json=product_json)
# def search_openbeauty(barcode):
#     """Retrieve product data from Open Beauty Facts"""
#     url = f"https://world.openbeautyfacts.org/api/v3/product/{barcode}.json"
#     product=get_product()
#     try:
#         response = requests.get(url, timeout=5)
#         return response.json() if response.status_code == 200 else None
#     except requests.RequestException:
#         return product

# def search_cogita(barcode):
        
#     product=get_product()
#     try:
#         resp=r.get(f"https://www.qogita.com/products/?query={barcode}")

#         n=extract_next_data(resp.content)
#         data=n["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]["results"][0]
#         product["brand"]=data["brandName"]
#         product["name"]=data["name"]
#         product["images"].append(data["imageUrl"])
#         product["category"]=data["categoryName"]
#         product["gtin"]=data["gtin"]
#         product["source"]="qogita"
#         product["last_update"]=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     except Exception as e:
#         print(e)
#     return product

# def setup_routes(app):
#     @app.route('/gtin', methods=['GET']) 
#     @app.route('/gtin/<barcode>', methods=['GET'])
#     def gtin_barcode(barcode=None):
#         if barcode:
#             product_info = get_basic_gtin(barcode)#search_cogita(barcode)
#             if product_info:            
#                 product_json = json.dumps(product_info, indent=2)
#         return render_template('gtin_result.html', 
#                                 product=product_info, 
#                                 product_json=product_json)
#         return render_template('gtin_scanner.html')
#  def gtin_scanner():
        
# # def setup_routes(app):
# #     @app.route('/gtin_scanner', methods=['GET'])
# #     def gtin_scanner():
# #         return render_template('gtin_scanner.html')
# #     @app.route('/gtin/<barcode>')
# #     def gtin_barcode(barcode):
# #             product_info=[]
# #             product_info.append( search_cogita(barcode))
# #             return Response(json.dumps(product_info, indent=2), mimetype='application/json')








# # def search_cogita(barcode):
# #     import requests as r
# #     import datetime
# #     product={
# #     "name":"",
# #     "brand":"",
# #     "description":"",
# #     "images":[],
# #     "category":"",
# #     "manufacturer":"",
# #     "ingredients":[],
# #     "gtin":"",
# #     }
# #     try:
# #         resp=r.get("https://www.qogita.com/products/?query={barcode}")
# #         n=extract_next_data(resp.content)
# #         data=n["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]["results"][0]
# #         product["brand"]=data["brandName"]
# #         product["name"]=data["name"]
# #         product["images"].append(data["imageUrl"])
# #         product["category"]=data["categoryName"]
# #         product["gtin"]=data["gtin"]
# #         product["source"]="Cogita"
# #         product["last_update"]=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #         return product
# #     except Exception as e:
# #         print(e)
# #         return product

# # def save_scan_history(product_info):
# #     """Save product scan to history file"""
# #     history_file = 'scan_history.json'
# #         resp=r.get("https://www.qogita.com/products/?query={barcode}")
# #         n=extract_next_data(resp.content)
# #         data=n["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]["results"][0]
# #         product["brand"]=data["brandName"]
# #         product["name"]=data["name"]
# #         product["images"].append(data["imageUrl"])
# #         product["category"]=data["categoryName"]
# #         product["gtin"]=data["gtin"]
# #         product["source"]="Cogita"
# #         product["last_update"]=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #         return product
# #     except Exception as e:
# #         print(e)
# #         return product

# # def save_scan_history(product_info):
# #     """Save product scan to history file"""
# #     history_file = 'scan_history.json'
#     try:
#         with open(history_file, 'a') as f:
#             json.dump(product_info, f)
#             f.write('\n')
#     except Exception as e:
#         print(f"Error saving scan history: {e}")

# def setup_routes(app):
#     @app.route('/qogita')
#     def beauty_scanner():
#         return render_template('beauty_scanner.html')
    
#     @app.route('/qogita/<barcode>', methods=['GET', 'POST'])
#     def beauty_lookup(barcode):
#         # Retrieve and consolidate product info
#         product_info = search_cogita(barcode)
        
#         # Save scan history
#         save_scan_history(product_info)
        
#         return render_template('beauty_result.html', product=product_info)

#     @app.route('/api/qogita/<barcode>')
#     def beauty_api(barcode):
#         product_info = consolidate_product_data(barcode)
#         return Response(json.dumps(product_info, indent=2), mimetype='application/json')

#     @app.route('/beauty/history')
#     def beauty_history():
#         try:
#             with open('scan_history.json', 'r') as f:
#                 history = [json.loads(line) for line in f]
#             return render_template('beauty_history.html', scans=history)
#         except FileNotFoundError:
#             return render_template('beauty_history.html', scans=[])
