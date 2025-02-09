from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Zortom22111357",
        database="products_db"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    if request.method == 'POST':
        brand_name = request.form['brand_name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO brands (brand_name) VALUES (%s)", (brand_name,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Brand added successfully!', 'success')
        return redirect(url_for('add_brand'))
    return render_template('add_brand.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT brand_id, brand_name FROM brands")
    brands = cursor.fetchall()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        gtin = request.form['gtin']
        brand_id = request.form['brand_id']
        
        # Insert product
        cursor.execute("""
            INSERT INTO products (name, description, gtin, brand_id)
            VALUES (%s, %s, %s, %s)
        """, (name, description, gtin, brand_id))
        
        product_id = cursor.lastrowid
        
        # Handle images
        images = request.form.getlist('image_urls')
        for image_url in images:
            if image_url.strip():
                cursor.execute("INSERT INTO images (url) VALUES (%s)", (image_url,))
                image_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO product_images (product_id, image_id) VALUES (%s, %s)",
                    (product_id, image_id)
                )
        
        conn.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('add_product'))
    
    cursor.close()
    conn.close()
    return render_template('add_product.html', brands=brands)

if __name__ == '__main__':
    app.run(debug=True)
