import os
from dotenv import load_dotenv
import requests
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import Tuple, List, Dict
import numpy as np

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Initial documents about Nepali citizenship and taxation
INITIAL_DOCUMENTS = [
    {
        "content": """
        Nepali Citizenship Requirements:
        1. Birth in Nepal or born to Nepali parent(s)
        2. Age requirement: 16 years or above
        3. Required documents:
           - Birth certificate
           - Parents' citizenship certificates
           - Local ward recommendation
           - Recent passport-size photos
        4. Application process through local District Administration Office
        """,
        "metadata": {"type": "citizenship", "category": "requirements"}
    },
    {
        "content": """
        Nepal Tax System Overview:
        1. Income Tax Rates (FY 2023/24):
           - Individual: 1% to 36%
           - Corporate: 25% standard rate
        2. Value Added Tax (VAT):
           - Standard rate: 13%
           - Registration threshold: NPR 5 million
        3. Tax Filing Deadlines:
           - Income Tax: Poush end (mid-January)
           - VAT: Monthly filing
        """,
        "metadata": {"type": "taxation", "category": "overview"}
    },
    {
        "content": """
        नेपाली नागरिकता प्राप्त गर्ने प्रक्रिया:
        1. आवश्यक कागजातहरू:
           - जन्मदर्ता प्रमाणपत्र
           - बाबु/आमाको नागरिकता
           - स्थानीय वडाको सिफारिस
           - हालसालै खिचेको फोटो
        2. जिल्ला प्रशासन कार्यालयमा निवेदन दिनुपर्ने
        3. नागरिकता प्राप्त गर्न १६ वर्ष पूरा भएको हुनुपर्ने
        """,
        "metadata": {"type": "citizenship", "category": "process", "language": "nepali"}
    }
]

class EnhancedRAGChatbot:
    def __init__(self):
        self.name = "D-Ask AI"
        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize vector store
        self.initialize_vector_store()
        
        # Store conversation history
        self.conversation_history = []

    def initialize_vector_store(self):
        """Initialize the vector store with documents if it doesn't exist."""
        persist_directory = "chroma_db"
        
        # Check if the directory exists
        if not os.path.exists(persist_directory):
            print("Creating new vector store...")
            os.makedirs(persist_directory)
            
            # Create a new vector store with initial documents
            texts = [doc["content"] for doc in INITIAL_DOCUMENTS]
            metadatas = [doc["metadata"] for doc in INITIAL_DOCUMENTS]
            
            self.vectorstore = Chroma.from_texts(
                texts=texts,
                metadatas=metadatas,
                embedding=self.embedding_model,
                persist_directory=persist_directory
            )
            self.vectorstore.persist()
            print("Vector store initialized with initial documents")
        else:
            print("Loading existing vector store...")
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embedding_model
            )

    def add_document(self, content: str, metadata: Dict = None):
        """Add a new document to the vector store."""
        try:
            self.vectorstore.add_texts(
                texts=[content],
                metadatas=[metadata] if metadata else None
            )
            self.vectorstore.persist()
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False

    def is_nepali(self, text: str) -> bool:
        return any('\u0900' <= ch <= '\u097F' for ch in text)

    def query_gemini(self, prompt: str) -> str:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=payload)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return ""

    def get_relevant_context(self, question: str, similarity_threshold: float = 0.3) -> Tuple[str, float]:
        """Get relevant context and maximum similarity score."""
        try:
            results = self.vectorstore.similarity_search_with_relevance_scores(question, k=3)
            
            if not results:
                return "", 0.0
                
            # Convert cosine distance to similarity score (0 to 1)
            normalized_results = [
                (doc, 1 - abs(score)) # Convert distance to similarity
                for doc, score in results
            ]
            
            relevant_docs = [doc for doc, score in normalized_results if score > similarity_threshold]
            max_score = max((score for _, score in normalized_results), default=0.0)
            
            if not relevant_docs:
                return "", max_score
                
            context = "\n\n---\n\n".join(doc.page_content for doc in relevant_docs)
            return context, max_score
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return "", 0.0

    def create_conversation_prompt(self, question: str, context: str, chat_history: str, lang: str) -> str:
        """Create a dynamic prompt for any type of interaction."""
        if lang == "नेपाली":
            return f"""तपाईं {self.name} हुनुहुन्छ, एक AI सहायक जो विशेष रूपमा नेपाली नागरिकता र करसम्बन्धी जानकारी प्रदान गर्न तयार गरिएको हो। तपाईंले केवल यी विषयहरूमा मात्र जानकारी दिन सक्नुहुन्छ।

महत्वपूर्ण नियमहरू:
1. यदि प्रश्न नेपाली नागरिकता वा करसँग सम्बन्धित छैन भने, विनम्रतापूर्वक भन्नुहोस् कि तपाईं केवल यी विषयहरूमा मात्र सहयोग गर्न सक्नुहुन्छ।
2. अन्य विषयहरूमा कुनै जानकारी नदिनुहोस्।
3. सधैं विनम्र र मैत्रीपूर्ण रहनुहोस्, तर आफ्नो विशेषज्ञताको सीमामा रहनुहोस्।

पछिल्लो वार्तालाप:
{chat_history}

उपलब्ध जानकारी:
{context}

प्रश्न: {question}

कृपया माथिका नियमहरू पालना गर्दै उत्तर दिनुहोस्। यदि प्रश्न तपाईंको विशेषज्ञता भन्दा बाहिर छ भने, विनम्रतापूर्वक नागरिकता वा करसम्बन्धी प्रश्नहरू सोध्न आग्रह गर्नुहोस्।

उत्तर:"""
        else:
            return f"""You are {self.name}, an AI assistant STRICTLY specialized in Nepali citizenship and taxation information. You are NOT authorized to provide information about any other topics.

Critical Rules:
1. If a question is not about Nepali citizenship or taxation, politely decline and remind that you can only help with these specific topics.
2. DO NOT provide information about any other subjects.
3. Stay friendly but firm about your domain limitations.
4. For off-topic questions, suggest asking about citizenship or taxation instead.

Recent Conversation:
{chat_history}

Available Information:
{context}

Question: {question}

Please respond following the above rules. If the question is outside your expertise, politely redirect to citizenship or taxation topics.

Answer:"""

    def get_answer(self, question: str) -> str:
        # Determine language
        lang = "नेपाली" if self.is_nepali(question) else "English"
        
        # Get relevant context and similarity score
        context, similarity_score = self.get_relevant_context(question)
        
        # Add conversation history context (last 3 exchanges)
        chat_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history[-3:]])
        
        # Create dynamic prompt
        prompt = self.create_conversation_prompt(question, context, chat_history, lang)
        
        # Get response from Gemini
        answer = self.query_gemini(prompt)
        
        # Update conversation history
        self.conversation_history.append((question, answer))
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)
            
        return answer

# Initialize chatbot instance
chatbot = EnhancedRAGChatbot() 