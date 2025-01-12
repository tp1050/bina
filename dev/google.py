

from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import quote

def create_persian_google_urls(search_query):
    domain = 'google.com'
    params = {
        'lr': 'lang_fa',
        'cr': 'countryIR',
        'gl': 'IR',
        'hl': 'fa'
    }
    
    base_url = f'https://www.{domain}/search?q=\"{quote(search_query)}\" خرید '
    param_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    return f'{base_url}&{param_string}'

def get_search_results(search_query):
    url = create_persian_google_urls(search_query)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for div in soup.find_all('div', class_='g'):
        try:
            title = div.find('h3').text
            link = div.find('a')['href']
            snippet = div.find('div', class_='VwiC3b').text if div.find('div', class_='VwiC3b') else ''
            
            result = {
                'title': title,
                'link': link,
                'snippet': snippet
            }
            results.append(result)
        except:
            continue
    
    return results

def generate_output(search_query):
    results = get_search_results(search_query)
    
    # Generate HTML
    html_output = "<div class='search-results'>\n"
    for result in results:
        html_output += f"""
        <div class='result-item'>
            <h3><a href='{result['link']}'>{result['title']}</a></h3>
            <p class='url'>{result['link']}</p>
            <p class='snippet'>{result['snippet']}</p>
        </div>
        """
    html_output += "</div>"
    
    # Generate JSON
    json_output = json.dumps(results, ensure_ascii=False, indent=2)
    
    return {
        'html': html_output,
        'json': json_output
    }

if __name__ == "__main__":
    search_term = "3838824364186"
    output = generate_output(search_term)
    
    # Print HTML
    print("HTML Output:")
    print(output['html'])
    print("\nJSON Output:")
    print(output['json'])
