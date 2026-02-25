#!/bin/bash

echo "========================================="
echo "   Instalador do Bot Telegram + Ollama (RAG)   "
echo "========================================="


# 2. Baixar Imagens Docker
echo ""
echo "[2/5] Baixando imagens Docker..."
if command -v docker-compose &> /dev/null; then
    sudo docker-compose pull
else
    sudo docker compose pull
fi

if [ $? -ne 0 ]; then
    echo "Erro ao baixar imagens Docker. Verifique sua conexão com a internet."
    exit 1
fi

# 3. Subir o Docker
echo ""
echo "[3/5] Iniciando serviços Docker (Ollama)..."
# Tenta docker-compose (versão antiga/standalone) ou docker compose (plugin v2)
if command -v docker-compose &> /dev/null; then
    sudo docker-compose up -d
else
    sudo docker compose up -d
fi

if [ $? -ne 0 ]; then
    echo "Erro ao iniciar o Docker. Verifique se o Docker está instalado e rodando."
    exit 1
fi

echo "Aguardando 10 segundos para o serviço Ollama inicializar..."
sleep 10

# 4. Baixar o modelo Command-R (LLM)
echo ""
echo "[4/5] Baixando o modelo Command-R (LLM)..."
sudo docker exec -it ollama_backend ollama pull llama3.1:8b


if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "      Tudo pronto! Instalação concluída. "
    echo "========================================="
    echo "Para rodar o bot, execute:"
    echo "   python main.py"
else
    echo "Erro ao baixar os modelos do Ollama."
    exit 1
fi
