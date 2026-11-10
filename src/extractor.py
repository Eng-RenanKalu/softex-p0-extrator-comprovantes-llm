from openai import OpenAI
from config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

# Inicializa o servidor local usando o cliente da OpenIA
cliente = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY
)

# Prepara a solicitação de mensagem
def solicitacaoDeMensagem(textoUsuario):
    return [
        {"role": "system", "content": "Você é um assistente util e direto"},
        {"role": "user", "content": textoUsuario}
    ]

# Faz a chamada ao modelo
def chamarModelo(mensagens):
    return cliente.chat.completions.create(
        model=LLM_MODEL,
        messages=mensagens,
        temperature=0.0,
    )

# Tratar o JSON retornado pelo modelo
def tratarResposta(respostaBruta):
    return respostaBruta.choices[0].message.content

# Chamar as funções e passar para o main.py
def processarExtracao(textoUsuario):
    mensagens = solicitacaoDeMensagem(textoUsuario)
    respostaBruta = chamarModelo(mensagens)
    textoFinal = tratarResposta(respostaBruta)
    return textoFinal