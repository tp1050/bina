import requests
from flask import render_template
import json
def clean_isbn(text):
    return ''.join(c for c in text if c.isdigit() or c.upper() == 'X')

def get_book_details(isbn):
    book={}
    isbn = clean_isbn(isbn)
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
       
        if data:
            with open(f"/tmp/accepter/isbn/jsons/{isbn}.json","w") as j:
                json.dump(data,j)
            book_data = data.get(f"ISBN:{isbn}", {})
            description=','.join(
                    [ff['name'] for ff in book_data.get("subjects",[])])
            _book= {
                'cover': book_data.get('cover', {}).get('large', ''),
                'title': book_data.get('title', ''),
               
                'authors': [author.get('name', '') for author in book_data.get('authors', [])],
                'publisher': book_data.get('publishers', [{}])[0].get('name', ''),
                'publish_date': book_data.get('publish_date', ''),
                'pages': book_data.get('number_of_pages', ''),
                'isbn': isbn,
                'description':f"isbn of the book is {isbn} a book about {description}"
            }
          
        
    return _book
def setup_routes(app):
    @app.route('/isbn')
    @app.route('/isbn/<decoded_text>')
    def isbn_lookup(decoded_text=None):
        if decoded_text:
            book_info= get_book_details(decoded_text)
            return render_template('isbn_result.html', book=book_info)
        return render_template('isbn_scanner.html')
