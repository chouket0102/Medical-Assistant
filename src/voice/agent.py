import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt
from dotenv import load_dotenv

load_dotenv()

class MedicalAgent:
    def __init__(self):
        # Initialize your medical RAG system
        PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        
        # Load embeddings and vector store
        self.embeddings = download_hugging_face_embeddings()
        index_name = "medicalbot"
        
        self.docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=self.embeddings
        )
        
        self.retriever = self.docsearch.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 3}
        )
        
        # Initialize LLM and chains
        self.llm = OpenAI(temperature=0.4, max_tokens=500)
        
        # Medical-specific prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)
    
    async def invoque(self, message):
        """Process medical query using RAG system"""
        try:
            response = self.rag_chain.invoke({"input": message})
            return response["answer"]
        except Exception as e:
            return f"I'm sorry, I encountered an error processing your medical query: {str(e)}"
    
    def getSystemPrompt(self):
        return system_prompt
