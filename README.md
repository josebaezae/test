# Codacy Insights API

## Descripción
Aplicación Python que se integra con la API de Codacy para obtener métricas de un repositorio de GitHub.
Por seguridad el token de conexión al api ver3 de Codacy se almaceno en .env y no se copia a github o docker
En Codacy se reportan 2 issues de nivel medium
Running flask app with host 0.0.0.0 could expose the server publicly.
Possible binding to all interfaces.
Los cuales aun no se corrigieron para ver el seguimiento que se les da en Codacy

## Instalación y Uso

### Localmente

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/josebaezae/test.git
    cd C:\Users\joseb\DockerProyectos\test
    ```

2. Crear y activar un entorno virtual:
    ```bash
    python -m venv venv
    venv\Scripts\activate
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
    gcloud config set project projecttestapi-450605
    ```

3. Desplegar la aplicación en Google Cloud Run:
    ```bash
    gcloud run deploy codacy-app --source .
    docker build -t gcr.io/projecttestapi-450605/codacy-app .
    docker push gcr.io/projecttestapi-450605/codacy-app
    gcloud run deploy codacy-app --image gcr.io/projecttestapi-450605/codacy-app --region us-west1 --platform managed --allow-unauthenticated
	En el navegador se puede ejecutar las siguientes url cambiando localhost:8080 por la url que prorcione Cloud Run cuando ya se este en linea la aplicación.
	Para obtener información de la organización:
    http://localhost:8080/codacy/organizations/gh/josebaezae
    ```
	Para listar los repositorios de una organización:
    http://localhost:8080/codacy/repositories/gh/josebaezae
    ```
	Para obtener información sobre los archivos del repositorio:
    http://localhost:8080/codacy/files/gh/josebaezae/test    
	```
4. Desplegar la aplicación unit tests en Google Cloud Run:
    ```bash
    docker build -f Dockerfile.test -t gcr.io/projecttestapi-450605/codacy-app-test .
    gcloud auth configure-docker
    docker push gcr.io/projecttestapi-450605/codacy-app-test
    gcloud run deploy codacy-app-test --image gcr.io/projecttestapi-450605/codacy-app-test --region us-west1 --platform managed --allow-unauthenticated
	```