
```
# 1. Criar o ambiente virtual
python -m venv env

# 2. Ativar o ambiente virtual
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar o app.py 
streamlit run app.py

# 5. Disponibilizar em um DNS externo
ngrok http 8501

```

```
docker-compose up -d
```