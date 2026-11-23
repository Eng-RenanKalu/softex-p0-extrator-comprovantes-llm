# Extrator de Comprovantes Financeiros (P0 Softex - Nível Avançado)

Uma aplicação de terminal que extrai dados financeiros essenciais (valor, data, estabelecimento e categoria) a partir do texto bruto de comprovantes (Pix, recibos de cartão, transferências) utilizando Inteligência Artificial local.

## 🧠 Por que usar LLM?

Um comprovante Pix tem um formato completamente diferente de um extrato de banco ou de um recibo de mercado. A IA atua como um interpretador semântico, capaz de ler textos desestruturados e classificar os dados em uma estrutura unificada, independente da fonte original.

## 🛠️ Tecnologias, Arquitetura e Qualidade de Código

* **Linguagem:** Python (Paradigma Funcional e execução via terminal com loop controlado por sentinela).
* **LLM Local:** Ollama (Modelo `qwen2.5:3b`). Roda localmente (`localhost`: 11434), garantindo privacidade e custo zero.
* **Clean Code:** Utilização intensiva de *Type Hints* e *Docstrings* (`typing`) para garantir previsibilidade e manutenção do código.
* **Monitoramento:** Sistema de `logging` implementado para auditoria técnica (salvo em `extrator.log`), mantendo o terminal do usuário limpo.
* **Fail-Fast:** Validação imediata de variáveis de ambiente e regras de negócio antes de acionar conexões de rede.

## 📁 Estrutura do Projeto

```text
├── src/
│   ├── config.py           # Gerenciamento de variáveis de ambiente e prompts
│   ├── extractor.py        # Lógica central de IA, logs e orquestração de extração
│   ├── main.py             # Interface de terminal (CLI) e loop de execução
│   └── test_extractor.py   # Suíte de testes unitários com Mock
├── .env.example            # Template de variáveis de ambiente
├── .gitignore              # Omissão de logs e credenciais
└── README.md               # Documentação principal
```

## ⚙️ Instalação e Configuração

1. **Pré-requisitos:** [Python 3.8+](https://www.python.org/downloads/) e [Ollama](https://ollama.com/) instalados no seu computador.
2. **Baixe o modelo da IA:** No terminal, execute:

```bash
ollama run qwen2.5:3b
```

3. **Clone o repositório e acesse a pasta:**

```bash
git clone https://github.com/Eng-RenanKalu/softex-p0-extrator-comprovantes-llm
cd softex-p0-extrator-comprovantes-llm
```

4. **Instale as dependências:**

```bash
pip install openai python-dotenv
```

5. **Configuração de Acesso (.env):**
Copie o arquivo `.env.example` e renomeie-o para `.env`.
**Atenção:** Preencha a variável `LLM_API_KEY` exatamente com a palavra `ollama`. Essa configuração é obrigatória para a validação de segurança da aplicação.

## 🚀 Como Executar

Com o Ollama rodando em segundo plano, inicie o programa acessando a pasta `src`:

```bash
python src/main.py
```

## 📊 Exemplo de Entrada e Saída

**Entrada do Usuário (Texto Bruto colado no terminal):**

> Transferência realizada com sucesso. Data: 12/10/2026. Recebedor: Mercado do Zé. Valor: R$ 45,90. Categoria não informada.

**Saída da Aplicação:**

> Estabelecimento: Mercado do Zé
> Valor: R$ 45,90
> Data: 12/10/2026
> Categoria: Alimentação / Supermercado

## 🛡️ Tratamento de Erros e Resiliência

A aplicação lida com cenários de falha de duas formas distintas:

* **Falhas de Rede (Indisponibilidade do LLM):** Se o Ollama for encerrado ou demorar muito para responder, a aplicação captura exceções da OpenAI (`APIConnectionError` e `APITimeoutError`) e exibe uma mensagem amigável sem quebrar o fluxo.
* **Falhas de Autenticação (Mock Local):** Como o Ollama possui "porta aberta", criamos um simulador local: se a `LLM_API_KEY` for diferente de `ollama`, o sistema aborta a requisição via `PermissionError`. A aplicação também trata `AuthenticationError`, facilitando a migração futura para provedores pagos em nuvem.

## 🧪 Testes Automatizados (Mock)

O projeto conta com uma suíte de testes locais utilizando `unittest` e `unittest.mock.patch`. A estratégia permite validar a lógica do código em frações de segundo, sem consumir recursos de rede ou tokens da IA, garantindo isolamento total.

Para rodar os testes:

```bash
python src/test_extractor.py
```