from flask import Flask, jsonify
import requests
import os
from google.cloud import secretmanager
from urllib.parse import urlparse, quote_plus

app = Flask(__name__)

ALLOWED_CODACY_BASE_URLS = [
    'https://app.codacy.com/api/v3/organizations/',
    'https://app.codacy.com/api/v3/analysis/organizations/'
]

def is_codacy_base_url_allowed(base_url):
    parsed_url = urlparse(base_url)
    allowed = False
    for allowed_base in ALLOWED_CODACY_BASE_URLS:
        allowed_parsed = urlparse(allowed_base)
        if (parsed_url.scheme == allowed_parsed.scheme and 
            parsed_url.netloc == allowed_parsed.netloc and 
            parsed_url.path.startswith(allowed_parsed.path)):
            allowed = True
            break
    return allowed

def validate_repo_name(repo_name):
    return repo_name.replace('-', '').replace('_', '').isalnum()

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

@app.after_request
def add_header(response):
    response.headers['Vary'] = 'Cookie'
    return response

@app.route('/codacy/organizations/<provider>/<remote_org_name>', methods=['GET'])
def get_codacy_organization(provider, remote_org_name):
    try:
        if not validate_repo_name(provider) or not validate_repo_name(remote_org_name):
            return jsonify({'error': 'Nombre de proveedor o de organización no válido'}), 400

        codacy_api_token = get_secret('CODACY_API_TOKEN')
        headers = {
            'Accept': 'application/json',
            'api-token': codacy_api_token
        }
        
        provider_encoded = quote_plus(provider)
        remote_org_name_encoded = quote_plus(remote_org_name)
        
        url = f'https://app.codacy.com/api/v3/organizations/{provider_encoded}/{remote_org_name_encoded}'

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

@app.route('/codacy/repositories/<provider>/<remote_org_name>', methods=['GET'])
def get_codacy_repositories(provider, remote_org_name):
    try:
        if not validate_repo_name(provider) or not validate_repo_name(remote_org_name):
            return jsonify({'error': 'Nombre de proveedor o de organización no válido'}), 400

        codacy_api_token = get_secret('CODACY_API_TOKEN')
        headers = {
            'Accept': 'application/json',
            'api-token': codacy_api_token
        }
        
        provider_encoded = quote_plus(provider)
        remote_org_name_encoded = quote_plus(remote_org_name)
        
        url = f'https://app.codacy.com/api/v3/analysis/organizations/{provider_encoded}/{remote_org_name_encoded}/repositories'

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

@app.route('/codacy/files/<provider>/<remote_org_name>/<repo_name>', methods=['GET'])
def get_codacy_files(provider, remote_org_name, repo_name):
    try:
        if not validate_repo_name(provider) or not validate_repo_name(remote_org_name) or not validate_repo_name(repo_name):
            return jsonify({'error': 'Nombre de proveedor, organización o repositorio no válido'}), 400

        codacy_api_token = get_secret('CODACY_API_TOKEN')
        headers = {
            'Accept': 'application/json',
            'api-token': codacy_api_token
        }
        
        provider_encoded = quote_plus(provider)
        remote_org_name_encoded = quote_plus(remote_org_name)
        repo_name_encoded = quote_plus(repo_name)
        
        url = f'https://app.codacy.com/api/v3/organizations/{provider_encoded}/{remote_org_name_encoded}/repositories/{repo_name_encoded}/files'

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
# Para usarlo localmente
#    app.run(host='127.0.0.1', port=8080)
# Para usarlo en docker
     app.run(host='0.0.0.0', port=8080)
