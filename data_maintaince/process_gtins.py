from flask import g
import requests
import json
from pathlib import Path as P
from zto4.coms.net import fetch
from zto4.search.google.lib import google_barcode_serperdev
from zto4.capitals.lib import SAVE,DOMAIN
from datetime import datetime
gtin_log_path='/tmp/accepter/gtin/gtin.log'


def google_gtin_logs():

    gtins=sorted(
            list(set(P(gtin_log_path).read_text().split('\n'))
                 )
            )
    links=[]
    for g in gtins:
        links.extend(google_barcode_serperdev(barcode=g))
    htmls=[]
    for l in links:
        html=fetch(l,return_type="source")
        SAVE(obj=html,where=f'/home/c/.zto/assets/bina/sku/gserp_fetch/{DOMAIN(l)}_{g}_{datetime.now().ctime()}.html')
        htmls.append(html)
    
    
            
    


