from calendar import c
from flask import g
import requests
import json
from pathlib import Path as P
from zto4.coms.net import fetch
from zto4.search.google.lib import google_barcode_serperdev
from zto4.capitals.lib import SAVE,DOMAIN
from zto4.extraction.product import extract_product_from_raw as ext 
from datetime import datetime
gtin_log_path='/tmp/accepter/gtin/gtin.log'


def google_gtin_logs(n=2000):

    gtins=sorted(
            list(set(P(gtin_log_path).read_text().split('\n'))
                 )
            )
    print(gtins)
    links=[]
    counter=0
    for g in gtins:
        counter=counter+1
        links.extend(google_barcode_serperdev(barcode=g)or [])
        if counter>n:break
    htmls=[]
    counter=0
    for l in links:
        counter=counter+1
        html=fetch(l,return_type="source")
        SAVE(obj=html,where=f"/home/c/.zto/assets/bina/sku/gserp_fetch/{DOMAIN(l)}_{g}.html")
        htmls.append(html)
        if counter>n:break
    return htmls


from glob import glob
from pathlib import Path
from zto4.extraction.product import extract_product_from_raw as ext 

import json
files=glob('/home/c/.zto/assets/bina/sku/gserp_fetch/*')
ret=[]
for f in files:
    html=Path(f).read_text()
    ret.append(ext(html=html))

with open('products.json','w') as f:
    json.dump(ret,f,ensure_ascii=False,indent=4)

    
# google_gtin_logs()
    
    
            
    


