from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

app = Flask(__name__)

ALLOWED_CODACY_BASE_URLS = ['https://app.codacy.com/api/v3/']

def is_codacy_base_url_allowed(base_url):
    parsed_url = urlparse(base_url)
    allowed = False
    for allowed_base in ALLOWED_CODACY_BASE_URLS:
        allowed_parsed = urlparse(allowed_base)
        if parsed_url.scheme == allowed_parsed.scheme and parsed_url.netloc == allowed_parsed.netloc and parsed_url.path.startswith(allowed_parsed.path):
            allowed = True
            break
    return allowed

@app.after_request
def add_header(response):
    response.headers['Vary'] = 'Cookie'
    return response

@app.route('/codacy/<provider>/<remote_org_name>', methods=['GET'])
def get_codacy_insights(provider, remote_org_name):
    try:
        codacy_api_token = os.getenv('CODACY_API_TOKEN')
        headers = {
            'Accept': 'application/json',
            'api-token': codacy_api_token
        }
        url = f'https://app.codacy.com/api/v3/organizations/{provider}/{remote_org_name}'

        if not is_codacy_base_url_allowed(url):
            return jsonify({'error': 'URL no permitida'}), 400

        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({'error': 'No se pudieron obtener los datos de Codacy.', 'details': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
