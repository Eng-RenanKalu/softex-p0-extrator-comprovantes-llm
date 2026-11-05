from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

def testarConfiguracao():
    print(f"MODELO DE LLM: {LLM_MODEL}")
    print(f"URL DA API: {LLM_BASE_URL}")
    if LLM_API_KEY:
        print("Chave da API: CARREGADA")
    else:
        print("Chave da API: ERRO")

if __name__ == "__main__":
    testarConfiguracao()