
### Create a virtual environment for the app:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the dependencies:
```bash
pip install -r requirements.txt
```

### Install sqllite3 and sample db
```bash
brew install sqlite3
sqlite3 chinook.db
```
### Run the script to install the sample db
```bash
.read Chinook_Sqlite.sql
```

## Containerize the Application
### Docker build streamlit app
```bash
docker build -t streamlit .
```


### Docker run the streamlit app
```bash
docker run -p 8501:8501 streamlit
```

### Deploy to azure
```bash
az acr create --name sdiregistry --resource-group sdi-dce --sku standard --admin-enabled true

az acr build --file Dockerfile --registry sdiregistry --image llmdemoimage .
``````