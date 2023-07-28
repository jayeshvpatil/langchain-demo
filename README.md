
### Create a virtual environment for the app:
python3 -m venv .venv
source .venv/bin/activate

### Install the dependencies:
pip install -r requirements.txt

### Docker build streamlit app
docker build -t streamlit .


### Docker run the streamlit app
docker run -p 8501:8501 streamlit


### Deploy to azure
az acr create --name sdiregistry --resource-group sdi-dce --sku standard --admin-enabled true

az acr build --file Dockerfile --registry sdiregistry --image llmdemoimage .