
# Capitolist Assignment

## Description
This project builds and deploys a FastAPI application that fetches weather information using a weather API and geocoding service. The application is designed to be 

### Project Structure
- **app/** : Contains the FastAPI application code.
- **tests/** : Contains the test cases written in pytest.
- **manifest/** : Contains the Kubernetes deployment manifest files.
- **.github/workflows/** : Contains the GitHub Actions workflow files.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Docker
- Kubernetes cluster with ArgoCD installed
- GitHub account for CI/CD integration

### Installation

1. ```bash 
   git clone https://github.com/tomershukhman/capitolis.git
   ```
  
  

2. **Install dependencies:**
   ```bash
   pip install -r dependencies/requirements.txt
   ```
    if you update the requirements file, please run:
   ```bash
   ./dependencies/build_push.sh
   ```
   this script will build and push an updated base image for the app image to use.

3. **Run the application:**
    ```bash
    fastapi run fastapi dev app/main.py 
   ```

4. **Run tests:**
   ```bash
   pytest tests
   ```

## CI/CD Pipeline

### GitHub Actions
The project uses GitHub Actions for CI. The workflow is triggered upon a push to the `main` branch. The CI workflow performs the following steps:

1. **Run tests**: Ensures the code is functioning as expected.
2. **Docker build**: Builds the Docker image of the application (build multi arch images).
3. **Docker push**: Pushes the Docker image to the dockerhub `tomershukhman/capitolis` with the current commit hash.
4. **Update manifest**: Updates the `manifest/deployment.yaml` manifest with the built image.

The CI workflow file is located at `.github/workflows/main.yml`.

### Continuous Deployment (CD)
ArgoCD is installed in the Kubernetes cluster and is configured to listen to the `manifest` directory in the repository. Whenever there is a change in the manifest files, ArgoCD automatically deploys the new version of the application to the cluster.

## Usage

Once the application is running, you can access the API endpoints to fetch weather information. The FastAPI documentation is available at `/docs`

### Host
The application is hosted at `http://wheatherapi`

### Example Request
To fetch the weather information for a specific location, use the following endpoint:

```http
GET wheatherapi/weather?location=<location>
```

## Additional info

### API Keys
The application uses the OpenWeatherMap API and the GCP Geocoding API
#### Local Development
 The API keys need be stored in the `.env` file located in the root of the
 and should have the values as follows:
 ```bash
GEOCODE_API_KEY=<API_KEY>
WEATHER_API_KEY=<API_KEY>
 ```
 
The `.env` file is not committed to the repository for security reasons.:

### Kubernetes Deployment:
The deployment uses a secret named ```app-cred``` to store the API keys. The secret is created using the following command:

```bash
kubectl create secret generic app-cred \
  --from-literal=GEOCODE_API_KEY=<GEOCODE_API_KEY> \
  --from-literal=WEATHER_API_KEY=<WEATHER_API_KEY>
```

### Kubernetes cluster:
The cluster is run on Docker Desktop with Kubernetes enabled.
The cluster has the following components installed:
- ArgoCD
- nginx ingress controller
- metrics server (not nectary for this project)


