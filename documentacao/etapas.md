# Etapas de Desenvolvimento

## 1. Configuração do Ambiente
- [ ] Definir framework web Flask.
- [ ] Criar ambiente virtual Python.
- [ ] Criar arquivo `requirements.txt` com as dependências necessárias (ex: `fastapi`, `uvicorn`, `requests` ou biblioteca cliente do Ollama).

## 2. Integração com Llama 3.1:8b
- [ ] Verificar pré-requisitos para rodar o modelo Llama 3.1:8b (ex: instalação do Ollama localmente).
- [ ] Criar função para comunicar com o modelo (enviar prompt e receber resposta).

## 3. Desenvolvimento da API
- [ ] Criar endpoint POST (ex: `/api/chat`).
- [ ] Definir estrutura do JSON de entrada (ex: `{"prompt": "sua pergunta"}`).
- [ ] Implementar lógica para chamar o modelo Llama com o prompt recebido.
- [ ] Formatar a resposta do modelo em Markdown dentro de um JSON (ex: `{"response": "**Resposta em Markdown**..."}`).

## 4. Testes e Validação
- [ ] Testar endpoint com ferramentas como cURL ou Postman.
- [ ] Validar se a resposta está no formato JSON correto e se o conteúdo é Markdown.

## 5. Documentação e Finalização
- [ ] Atualizar README.md com instruções de como rodar a aplicação.
