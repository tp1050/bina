
import requests
from flask import Response, render_template, jsonify, request, redirect, url_for
import os
from datetime import datetime
import json
import csv
import glob
def setup_routes(app):
    @app.route('/aggregate', methods=['GET', 'POST'])
    def aggregate():
        last_csv_path = "/tmp/accepter/gtin/csv/ast_aggregate.csv"
        
        if request.method == 'POST':  # Handle refresh
            try:
                # Aggregate data from JSON files
                json_path = "/tmp/accepter/gtins/jsons/"
                files = glob.glob(f"{json_path}basic_*.json")
                
                products = {}
                for file in files:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        gtin = data['gtin']
                        products[gtin] = products.get(gtin, 0) + 1

                # Create timestamped CSV for indexing
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                dated_csv = f"/tmp/accepter/gtin/csv/{timestamp}_aggregate.csv"
                os.makedirs(os.path.dirname(dated_csv), exist_ok=True)

                # Write to both files
                for filepath in [dated_csv, last_csv_path]:
                    with open(filepath, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['GTIN', 'Count'])
                        for gtin, count in products.items():
                            writer.writerow([gtin, count])

            except Exception as e:
                return f"Error during refresh: {str(e)}", 500

        # Read and display last_aggregate.csv
        try:
            products = []
            with open(last_csv_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                products = list(reader)
            return render_template('aggregate.html', products=products)
        except FileNotFoundError:
            return "No aggregation data found. Please refresh.", 404
        except Exception as e:
            return f"Error reading aggregate data: {str(e)}", 500