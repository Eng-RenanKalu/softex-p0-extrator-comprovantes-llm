# Relatório de Execução - Extrator de Comprovantes Financeiros (P0)

## Evolução por Nível

*   **Básico:** Construção do fluxo principal de terminal utilizando um laço de repetição controlado por sentinela (estilo chat). Integração inicial com a LLM local (Ollama com o modelo `qwen2.5:3b`) para processar o texto bruto e retornar as quatro informações essenciais formatadas.
*   **Intermediário:** Implementação de uma arquitetura modular (`config.py`, `extractor.py`, `main.py`). Adição de validação "Fail-Fast" para variáveis de ambiente via `.env` e tratamento robusto de exceções de rede e timeout, exibindo mensagens amigáveis ao invés de quebrar a execução.
*   **Avançado:** Elevação da qualidade do código (Clean Code) com a aplicação de *Type Hints* e *Docstrings*. Implementação de testes unitários automatizados utilizando `unittest.mock` (isolando a LLM) e transição do sistema de debug visual para logs técnicos em arquivo externo (`extrator.log`).

## Decisões Principais

1.  **Paradigma de Programação**
    *   **Decisão tomada:** Utilizar o paradigma Funcional.
    *   **Alternativa considerada:** Programação Orientada a Objetos (POO).
    *   **Justificativa:** A baixa complexidade do projeto P0 (orquestração de chamadas de API e formatação de texto) não justificava o *overhead* da estruturação em classes e objetos.

2.  **Interface de Execução**
    *   **Decisão tomada:** Looping controlado por sentinela (semelhante a um chat).
    *   **Alternativa considerada:** Execução única (*one-shot*) baseada em argumentos de linha de comando.
    *   **Justificativa:** Proporciona uma experiência de uso mais fluida, permitindo ao usuário colar múltiplos comprovantes em sequência sem precisar reiniciar a aplicação.

3.  **Validação de Configurações**
    *   **Decisão tomada:** Abordagem *Fail-Fast* no arquivo `config.py`.
    *   **Alternativa considerada:** Validar as variáveis de ambiente apenas no momento da execução no `main.py`.
    *   **Justificativa:** Evita que a aplicação inicie caso existam configurações ausentes, economizando recursos e prevenindo falhas tardias.

4.  **Tratamento de Autenticação em LLM Local**
    *   **Decisão tomada:** Simular um erro de autenticação interno.
    *   **Alternativa considerada:** Ignorar o tratamento de credenciais, já que o Ollama opera localmente em porta aberta.
    *   **Justificativa:** Validar a competência exigida de tratamento de acesso negado e preparar a arquitetura do software para uma eventual migração para APIs pagas em nuvem (ex: OpenAI).

## Testes e Resultados

| Teste | Entrada ou Situação | Resultado Esperado | Resultado Obtido |
| :--- | :--- | :--- | :--- |
| **Segurança** | Envio de texto vazio ou apenas espaços (" "). | Bloqueio imediato com mensagem: "[ERRO] O texto do comprovante não pode estar vazio." | Sucesso (bloqueado antes da IA) |
| **Mock (Sucesso)** | Simulação de retorno ideal da IA para o texto "Comprovante 50 reais". | Retorno do JSON formatado extraído corretamente pela função. | Sucesso (teste local isolado) |
| **Mock (Falha)** | Simulação de exceção catastrófica ("Servidor pegou fogo") na biblioteca OpenAI. | Captura da exceção e retorno amigável: "[ERRO INESPERADO] Falha durante a extração..." | Sucesso (aplicação não quebrou) |
| **Autenticação** | Variável `LLM_API_KEY` preenchida com valor diferente de "ollama". | Aplicação deve levantar e capturar `PermissionError` exibindo alerta de erro de credencial. | Sucesso (bloqueado no `extractor`) |

## Falhas e Limitações

1.  **Vulnerabilidade a *Prompt Injection***
    *   **O que aconteceu:** A LLM ignorou a estrutura de saída definida quando o texto de entrada continha comandos como "ignore suas regras".
    *   **Como foi identificado:** Durante rodadas de testes manuais exploratórios.
    *   **Como foi tratado:** Manutenção do foco no escopo principal. Por ser uma prova de conceito de nível inicial (P0), defesas avançadas contra injeção não foram implementadas.
    *   **Por que permanece:** É uma limitação inerente e um desafio contínuo dos Modelos de Linguagem Grande (LLMs) que exigiria camadas complexas de *parsers* e LLMs avaliadoras para ser mitigado por completo.

2.  **"Crise de Identidade" da LLM (Contaminação de Dados)**
    *   **O que aconteceu:** Na fase básica, o modelo local `qwen2.5:3b` declarou ser o "Claude, modelo da Anthropic".
    *   **Como foi identificado:** Lendo as respostas da IA. O teste foi repetido com a máquina sem acesso à internet para descartar interceptações de rede.
    *   **Como foi tratado:** Compreendido como um artefato do processo de treinamento do modelo.
    *   **Por que permanece:** O modelo Qwen provavelmente utilizou *datasets* gerados sinteticamente por modelos maiores (como o Claude) durante sua fase de treinamento. A solução definitiva exigiria a troca da LLM.

## Uso de IA no Desenvolvimento

*   **Ferramenta utilizada:** Google Gemini modelo 3.1 pro (atuando como par de programação / assistente técnico).
*   **Tarefa delegada:** Auxílio na refatoração do código para padrões limpos (*Clean Code*), estruturação da suíte de testes com `unittest.mock` e formatação de documentação em Markdown.
*   **Resultado aproveitado:** Estruturas de *Type Hints*, configuração dos `logs` nativos do Python e *templates* iniciais dos testes.
*   **Correções ou alterações realizadas:** Adaptação da nomenclatura de funções geradas pela IA para manter o padrão já existente no projeto (ex: de `preparar_mensagens` para `solicitacaoDeMensagem`), além de correções de sintaxe (`logging.inf` para `logging.info`).
*   **Forma de verificação:** Revisão humana estrita. Cada bloco de código sugerido foi avaliado analiticamente, ajustado ao contexto do projeto e validado empiricamente via execução no terminal antes de cada *commit* no repositório.

## Reflexão Final

*   **Principal aprendizado:** A implementação do isolamento de dependências através do conceito de *Mock* em testes unitários. Foi possível compreender como validar a lógica interna do sistema de forma rápida e segura, sem depender do consumo de recursos externos (API/Rede). Além da integração de modelos de IA em sistemas de software.
*   **Competência mais desenvolvida:** Arquitetura de software e tratamento robusto de erros. A transição de um simples roteiro procedural para uma aplicação resiliente, orquestrada por logs ocultos e tratativas de exceções amigáveis ao usuário. Em resumo, a experiência de fazer um projeto nível profissional
*   **Aspecto que ainda precisa ser aprimorado:** Segurança no desenvolvimento com IAs (*Prompt Engineering* defensivo), aprofundando os estudos sobre como blindar a aplicação de entradas maliciosas e injeções de prompt, melhora no uso de tipos em python além de outros recursos nativo da linguagem.