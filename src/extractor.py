from openai import OpenAI, APIConnectionError, APITimeoutError, APIError, AuthenticationError
from config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

# Inicializa o servidor local usando o cliente da OpenIA
cliente = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    timeout=15.0
)

# Prepara a solicitação de mensagem
def solicitacaoDeMensagem(textoUsuario):
    return [
        {"role": "system", "content": "Você é um assistente util e direto"},
        {"role": "user", "content": textoUsuario}
    ]

# Simulação de autenticação
def verificarAutenticacao():
    if LLM_API_KEY != "ollama":
        raise PermissionError("Credenciais inválidas. Acesso negado.")

# Faz a chamada ao modelo
def chamarModelo(mensagens):
    verificarAutenticacao()
    return cliente.chat.completions.create(
        model=LLM_MODEL,
        messages=mensagens,
        temperature=0.0,
    )

# Tratar o JSON retornado pelo modelo
def tratarResposta(respostaBruta):
    if not respostaBruta.choices or not respostaBruta.choices[0].message.content:
        raise ValueError("A resposta do modelo veio vazia.");
    return respostaBruta.choices[0].message.content

# Chamar as funções e passar para o main.py
def processarExtracao(textoUsuario):
    try:
        mensagens = solicitacaoDeMensagem(textoUsuario)
        respostaBruta = chamarModelo(mensagens)
        textoFinal = tratarResposta(respostaBruta)
        return textoFinal

    # Exibindo os possiveis erros ao usuário
    except PermissionError as erro:
        return f"[ERRO DE AUTENTICAÇÃO] {str(erro)} Verifique a sua LLM_API_KEY."
    except AuthenticationError:
        return "[ERRO DE AUTENTICAÇÃO] A chave da API foi rejeitada pelo provedor."
    except APIConnectionError:
        return "[ERRO] Não foi possível conectar ao LLM. Verifique se o Ollama está em localhost:11434."
    except APITimeoutError:
        return "[ERRO] O modelo demorou muito a responder (Timeout). Tente novamente."
    except APIError as erro:
        return f"[ERRO] Falha no serviço da IA: {str(erro)}"
    except ValueError as erro:
        return f"[ERRO] {str(erro)}"
    except Exception as erro:
        return f"[ERRO] Falha inesperada durante a extração: {str(erro)}"