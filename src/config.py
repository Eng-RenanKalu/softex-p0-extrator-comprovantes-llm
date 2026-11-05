import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente na memoria do sistema
load_dotenv()

# Configuração das variáveis de ambiente
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")