from flask import g
import requests
import json
from pathlib import Path as P
from zto4.coms.net import fetch
from zto4.search.google.lib import google_barcode_serperdev

from torch import gt
gtin_log_path='/tmp/accepter/gtin/gtin.log'


def google_gtin_logs():
    gtins=sorted(
            list(set(P(gtin_log_path).read_text().split('\n'))
                 )
            )
    results=[google_barcode_serperdev(barcode=g) for g in gtins:
        google_barcode_serperdev
    
            
    


