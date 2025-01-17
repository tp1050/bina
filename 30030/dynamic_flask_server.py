from flask import Flask, render_template, request, jsonify, redirect, url_for
import importlib.util
import os
from datetime import datetime

class DynamicFlaskServer:
    def __init__(self, dropins_dir="routes"):
        self.app = Flask(__name__)
        self.dropins_dir = dropins_dir
        self.load_builtin_routes()
        self.load_dropin_routes()
    
    def load_builtin_routes(self):
        @self.app.route('/scan')
        def scan_qr():
            return render_template('scanner.html')
        
        @self.app.route('/result')
        def show_result():
            content = request.args.get('content', '')
            timestamp = request.args.get('timestamp', '')
            return render_template('result.html', content=content, timestamp=timestamp)
        
        @self.app.route('/submit-scan', methods=['POST'])
        def submit_scan():
            data = request.json
            result = {
                'status': 'success',
                'data': {
                    'content': data['scanned_data'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            return jsonify(result)
    
    def load_dropin_routes(self):
        for filename in os.listdir(self.dropins_dir):
            if filename.endswith('.py'):
                self.load_route_module(filename)
    
    def load_route_module(self, filename):
        module_name = filename[:-3]
        spec = importlib.util.spec_from_file_location(
            module_name, 
            os.path.join(self.dropins_dir, filename)
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'setup_routes'):
            module.setup_routes(self.app)
    
    def run(self, host='0.0.0.0', port=64533):
        self.app.run(host=host, port=port, debug=True)
