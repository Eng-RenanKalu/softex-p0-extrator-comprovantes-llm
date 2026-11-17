from openai import OpenAI, APIConnectionError, APITimeoutError, APIError, AuthenticationError
from config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, LLM_TEMPERATURE, SYSTEM_PROMPT
import logging

# Configuração do sistema de logging
logging.basicConfig(
    filename='extrator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Inicializa o servidor local usando o cliente da OpenIA
cliente = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    timeout=15.0
)

# Prepara a solicitação de mensagem
def solicitacaoDeMensagem(textoUsuario):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": textoUsuario}
    ]

# Simulação de autenticação
def verificarAutenticacao():
    if LLM_API_KEY != "ollama":
        raise PermissionError("Credenciais inválidas. Acesso negado.")

# Faz a chamada ao modelo
def chamarModelo(mensagens):
    logging.info(f"Iniciando chamada ao modelo LLM ({LLM_MODEL})...");

    verificarAutenticacao()
    resposta = cliente.chat.completions.create(
        model=LLM_MODEL,
        messages=mensagens,
        temperature=LLM_TEMPERATURE,
    )

    logging.info("Resposta da LLM recebida com sucesso")

    return resposta



# Tratar o JSON retornado pelo modelo
def tratarResposta(respostaBruta):
    if not respostaBruta.choices or not respostaBruta.choices[0].message.content:
        raise ValueError("A resposta do modelo veio vazia.")
    return respostaBruta.choices[0].message.content

# Chamar as funções e passar para o main.py
def processarExtracao(textoUsuario):
    logging.info("Iniciando nova requisição de extração (tamanho do texto: %d caracteres)", len(textoUsuario))
    
    if not textoUsuario.strip():
        logging.warning("Requisição rejeitada: Texto de entrada vazio.")
        return "Erro: O texto do comprovante não pode estar vazio."
        
    mensagens = solicitacaoDeMensagem(textoUsuario)

    try:
        respostaBruta = chamarModelo(mensagens)
        textoFinal = tratarResposta(respostaBruta)
        logging.info("Extração concluída com sucesso")
        return textoFinal

    # Exibindo e armazenando os possiveis erros
    except PermissionError as erro:
        logging.error(f"Erro de Permissão Interna: {erro}")
        return f"[ERRO DE AUTENTICAÇÃO] {str(erro)} Verifique a sua LLM_API_KEY"
        
    except AuthenticationError:
        logging.error("Falha de Autenticação: Credenciais inválidas fornecidas para a API.")
        return "[ERRO DE AUTENTICAÇÃO] A chave da API foi rejeitada pelo provedor. Verifique as variáveis de ambiente"
        
    except APIConnectionError:
        logging.error("Falha de Conexão: Não foi possível alcançar o servidor do LLM.")
        return "[ERRO DE CONEXÃO] Não foi possível conectar ao LLM. Verifique se o Ollama está rodando (ex: em localhost:11434)."
        
    except APITimeoutError:
        logging.error("Falha de Timeout: O servidor do LLM demorou muito para responder.")
        return "[ERRO DE TIMEOUT] O modelo demorou muito a responder. Tente novamente."
        
    except ValueError as erro:
        logging.error(f"Erro de Validação/Configuração: {erro}")
        return f"[ERRO DE CONFIGURAÇÃO] {str(erro)}"
        
    except Exception as erro:
        logging.error(f"Erro Inesperado no processamento: {type(erro).__name__} - {str(erro)}")
        return f"[ERRO INESPERADO] Falha durante a extração: {str(erro)}"