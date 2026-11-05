from extractor import enviarMsg

# Nota: A resposta do modelo no terminal afirma ser o "Claude, modelo de linguagem da Anthropic" acredito ser uma crise de identidade
# do modelo o que significa que os criadores do Qwen usaram conversas geradas por modelos gigantes e muito mais caros
# para ensinar o Qwen a falar de forma natural.

def testarLLM():
    print("Enviando mensagem para a LLM local...")
    
    # Texto fixo para testar
    mensagemTeste = "Olá! Diz-me apenas me diga seu nome e o seu modelo, numa frase curta."
    
    try:
        resposta = enviarMsg(mensagemTeste)
        
        print("\n--- Resposta do Modelo ---")
        print(resposta)
        print("--------------------------\n")
        
    except Exception as erro:
        print(f"\nErro ao comunicar com o modelo: {erro}")

if __name__ == "__main__":
    testarLLM()