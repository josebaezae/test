# Codacy Insights API

## Descripción
Aplicación Python que se integra con la API de Codacy para obtener métricas de un repositorio de GitHub.

## Instalación y Uso

### Localmente

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Crear y activar un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Ejecutar la aplicación:
    ```bash
    python app.py
    ```

### Docker

1. Construir la imagen Docker:
    ```bash
    docker build -t codacy-app .
    ```

2. Ejecutar el contenedor Docker:
    ```bash
    docker run -p 8080:8080 codacy-app
    ```

### Google Cloud Run

1. Autenticarse en Google Cloud:
    ```bash
    gcloud auth login
    ```

2. Configurar el proyecto de Google Cloud:
    ```bash
    gcloud config set project [YOUR_PROJECT_ID]
    ```

3. Desplegar la aplicación en Google Cloud Run:
    ```bash
    gcloud run deploy codacy-app --source .
    ```

## Pruebas Unitarias

### Archivo `test_app.py`

```python
import unittest
from app import app

class CodacyAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_codacy_insights(self):
        response = self.app.get('/codacy/github/remote_org_name')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
