import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RagEngine:
    def __init__(self, pdf_path, persist_directory="./chroma_db"):
        self.pdf_path = pdf_path
        self.persist_directory = persist_directory
        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = None

    def ingest_pdf(self):
        """Lê o PDF, divide em chunks e salva no banco vetorial."""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {self.pdf_path}")

        print("Carregando PDF...")
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()

        print(f"Dividindo {len(documents)} páginas em chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Total de chunks criados: {len(chunks)}")

        print("Criando embeddings e salvando no ChromaDB...")
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_function,
            persist_directory=self.persist_directory
        )
        print("Ingestão concluída!")

    def load_vector_store(self):
        """Carrega o banco vetorial existente."""
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_function
            )
            return True
        return False

    def search(self, query, k=3):
        """Busca os k trechos mais relevantes para a pergunta."""
        if not self.vector_store:
            if not self.load_vector_store():
                print("Banco vetorial não encontrado. Execute ingest_pdf() primeiro.")
                return []
        
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

if __name__ == "__main__":
    # Exemplo de uso para ingestão (rodar uma vez)
    pdf_file = "documentacao/base_conhecimento.pdf"
    
    if os.path.exists(pdf_file):
        rag = RagEngine(pdf_file)
        # Descomente a linha abaixo para criar o banco na primeira vez
        # rag.ingest_pdf()
        
        # Teste de busca
        rag.load_vector_store()
        res = rag.search("Qual o diâmetro do eixo?")
        print(res)
    else:
        print(f"Coloque o PDF em {pdf_file} para testar.")
