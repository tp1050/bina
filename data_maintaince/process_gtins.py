from calendar import c
from flask import g
import requests
import json
from pathlib import Path as P
from zto4.coms.net import fetch
from zto4.search.google.lib import google_barcode_serperdev
from zto4.capitals.lib import SAVE,DOMAIN
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
google_gtin_logs()
    
    
            
    


