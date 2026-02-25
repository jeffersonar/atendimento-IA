import requests
import json
import os
from rag_engine import RagEngine

class LlamaClient:
    def __init__(self, base_url="http://localhost:11434", model="llama3.1:8b", pdf_path="documentacao/base_conhecimento.pdf"):
        self.base_url = base_url
        self.model = model
        self.rag_engine = RagEngine(pdf_path)
        
        # Tenta carregar o banco vetorial existente
        if not self.rag_engine.load_vector_store():
            print("Banco vetorial não encontrado. Iniciando ingestão do PDF...")
            try:
                self.rag_engine.ingest_pdf()
                print("Ingestão concluída com sucesso!")
            except Exception as e:
                print(f"Erro ao processar PDF: {e}")

    def generate_response(self, prompt):
        # Busca trechos relevantes no PDF usando RAG
        relevant_chunks = self.rag_engine.search(prompt, k=3)
        context_text = "\n\n".join(relevant_chunks)

        if not context_text:
            context_text = "Nenhuma informação relevante encontrada no documento."

        # Monta o prompt com contexto específico
        system_instruction = (
            "Você é um especialista técnico no catálogo da FRM (rolamentos e mancais).\n"
            "Use APENAS as informações do contexto abaixo para responder.\n"
            "Se a resposta não estiver no contexto, diga que não encontrou a informação no catálogo.\n"
            "Seja preciso com números e tabelas.\n"
            "Responda em português.\n\n"
            "--- CONTEXTO DO CATÁLOGO ---\n"
            f"{context_text}\n"
            "--- FIM DO CONTEXTO ---\n"
        )

        full_prompt = f"{system_instruction}\n\nPergunta do usuário: {prompt}"

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,  # Muito baixo para precisão técnica
                "num_ctx": 4096      # Aumenta janela de contexto se necessário
            }
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com o Llama: {e}")
            return None

if __name__ == "__main__":
    # Teste
    client = LlamaClient()
    
    print("--- Teste: Pergunta Técnica ---")
    # Substitua pela pergunta real que faça sentido para o seu PDF
    pergunta = "Em um sistema industrial que utiliza um rolamento rígido de esferas 6205-2RS operando a 3.600 rpm sob carga radial constante de 2.800 N e carga axial de 900 N, considerando: Fator de aplicação moderado (Ka = 1,2) Vida nominal requerida de 20.000 horas Lubrificação por graxa NLGI 2 Temperatura média de operação de 85°C Explique detalhadamente: Como determinar a carga dinâmica equivalente (P), considerando os fatores X e Y apropriados. Como calcular a vida nominal L10 em milhões de rotações e convertê-la para horas. Como verificar se o rolamento atende à vida requerida, considerando o coeficiente de confiabilidade (a1 = 0,62 para 95% de confiabilidade). Quais seriam os impactos na vida útil caso houvesse desalinhamento angular de 0,5°. Como a temperatura de operação influencia a viscosidade do lubrificante e o fator de modificação de vida (aISO)."
    print(f"Pergunta: {pergunta}")
    resposta = client.generate_response(pergunta)
    print(f"Resposta: {resposta}\n")
