from openai import OpenAI
from config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

# Inicializa o servidor local usando o cliente da OpenIA
cliente = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY
)

def enviarMsg(texto):
    # Estrutura da mensagem enviada para a API
    mensagens = [
        {"role": "system", "content": "Você é um assistente útil e direto."},
        {"role": "user", "content": texto}
    ]

    # Envia a requisição
    resposta = cliente.chat.completions.create(model = LLM_MODEL, messages = mensagens, temperature = 0.0)

    # Extrai a resposta da IA
    return resposta.choices[0].message.content