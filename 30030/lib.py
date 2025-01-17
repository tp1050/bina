import requests

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
def get_upc_data(barcode):
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    headers = {
        'user-agent': 'Mozilla/5.0',
        'accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None