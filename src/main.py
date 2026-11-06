from extractor import enviarMsg

def iniciarLLM():
    print("--- Assistente de Extração Financeiro (P0) ---")
    print("Digire 'sair' a qualquer momento para encerrar o programa.\n")

    # Iniciar loop inifnito
    while True:
        # Entrada
        textoUsuario = input("Escreva: ")

        # Encerra o loop se o usuário digitar 'sair'
        if textoUsuario.strip().lower() == 'sair':
            print("Programa encerrado. Até logo!")
            break

        # Evitando texto vazio
        if not textoUsuario.strip():
            print("Erro, por favor digite algo válido")
            continue

        # Saida
        try:
            print("Pensando...")
            resposta = enviarMsg(textoUsuario)
            print(f"IA: {resposta}\n")
        except Exception as error:
            print(f"Erro ao comunicar com a IA: {error} \n")


if __name__ == "__main__":
    iniciarLLM()