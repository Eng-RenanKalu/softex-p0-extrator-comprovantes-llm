# Extrator de Comprovantes Financeiros (P0 Softex)

Uma aplicação de terminal que extrai dados financeiros essenciais (valor, data, estabelecimento e categoria) a partir do texto bruto de comprovantes (Pix, recibos de cartão, transferências) utilizando Inteligência Artificial local.

## 🧠 Por que usar LLM?

Um comprovante Pix tem um formato completamente diferente de um extrato de banco ou de um recibo de mercado. A IA atua como um interpretador semântico, capaz de ler textos desestruturados e classificar os dados em uma estrutura unificada, independente da fonte original.

## 🛠️ Tecnologias e Decisões de Arquitetura

* **Linguagem:** Python (Paradigma Funcional e execução via terminal com loop controlado por sentinela).
* **LLM:** Ollama (Modelo `qwen2.5:3b`). Roda localmente (`localhost`: 11434), garantindo privacidade e custo zero com tokens.
* **Orquestração e Tratamento de Erros:** Estratégia "Fail-Fast" para variáveis de ambiente na configuração e validações de rede/timeout tratadas diretamente no orquestrador principal, isolando as responsabilidades de extração e comunicação.

## ⚙️ Instalação e Configuração

1. **Pré-requisitos:** Python 3.8+ e [Ollama](https://ollama.com/) instalados no seu computador.
2. **Baixe o modelo da IA:** Abra o terminal e execute o comando abaixo para instalar o modelo:
```bash
ollama run qwen2.5:3b

```


3. **Clone o repositório:**
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA>

```


4. **Instale as dependências:**
```bash
pip install openai python-dotenv

```


5. **Configuração de Acesso (.env):**
Copie o arquivo `.env.example` e renomeie-o para `.env`.
**Atenção:** Preencha a variável `LLM_API_KEY` exatamente com a palavra `ollama`. Essa configuração é obrigatória para o funcionamento da barreira de autenticação do projeto.

## 🚀 Como Executar

Com o Ollama rodando em segundo plano, inicie o programa pelo terminal:

```bash
python main.py

```

## 📊 Exemplo de Entrada e Saída

**Entrada do Usuário (Texto Bruto colado no terminal):**

> Transferência realizada com sucesso. Data: 12/10/2026. Recebedor: Mercado do Zé. Valor: R$ 45,90. Categoria não informada.

**Saída da Aplicação:**

> Estabelecimento: Mercado do Zé
> Valor: R$ 45,90
> Data: 12/10/2026
> Categoria: Alimentação / Supermercado

## 🛡️ Tratamento de Erros (Testes Reais vs Simulados)

Para cumprir as exigências de tratamento de falhas, a aplicação lida com cenários de indisponibilidade e acesso negado de duas formas distintas:

* **Testes Reais (Indisponibilidade do LLM):** Se o serviço local do Ollama for encerrado ou demorar mais de 15 segundos para responder, o programa captura as falhas técnicas da biblioteca OpenAI (`APIConnectionError` e `APITimeoutError`) e exibe uma mensagem amigável ao usuário sem quebrar a aplicação, permitindo nova tentativa.
* **Testes Simulados (Falha de Autenticação):** Serviços locais como o Ollama funcionam com "porta aberta" e ignoram credenciais inválidas. Para demonstrar o tratamento de falha de credencial ausente/inválida, implementamos um simulador no código: se a `LLM_API_KEY` for diferente de `ollama`, o sistema bloqueia a requisição antes de enviá-la e gera um `PermissionError`. A aplicação também está preparada com `AuthenticationError` oficial, facilitando uma futura migração para APIs pagas.