import os
import sys
from dotenv import load_dotenv

# Carrega as variáveis de ambiente na memoria do sistema
load_dotenv()

# Configuração das variáveis de ambiente
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")

# Validação (fail-fast)
erros = []

if not LLM_BASE_URL:
    erros.append("- LLM_BASE_URL (ex: http://localhost:11434)")

if not LLM_API_KEY:
    erros.append("- LLM_API_KEY (ex: ollama)")
    
if not LLM_MODEL:
    erros.append("- LLM_MODEL (ex: qwen2.5:3b)")

if erros:
    print("\n[ERRO DE CONFIGURAÇÃO] As seguintes variáveis não foram encontradas no arquivo .env:")
    for error in erros:
        print(f"{error}")
    print("\nPor favor, verifique se o arquivo .env exsite e está preenchido corretamente")
    sys.exit(1)