import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

st.set_page_config(
    page_title="Institutional SFO Intelligence Platform", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {background-color: #f8fafc;}
    h1 {color: #0f172a; font-weight: 800; font-size: 2.2rem;}
    h3 {color: #334155; font-weight: 600;}
    .stAlert {border-radius: 8px;}
    .metric-card {background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# Sidebar Control Panel
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/permanent-job.png", width=64)
    st.markdown("### **System Control Panel**")
    st.info("Autonomous Micro-RAG search layer built for verified institutional single-family office intelligence.")
    
    if not GROQ_API_KEY:
        GROQ_API_KEY = st.text_input("Enter Groq API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### **Platform Metrics**")
    st.metric(label="Verified SFO Records", value="55")
    st.metric(label="Retrieval Engine", value="FAISS (Local)")
    st.metric(label="Inference Model", value="Llama-3.1-8b")

st.title("💼 Institutional Single-Family Office Intelligence")
st.markdown("##### Executive Search & Due Diligence Discovery Layer")
st.write("")

if not GROQ_API_KEY:
    st.warning("⚠️ **Access Restricted:** Please map your `GROQ_API_KEY` in environment variables or use the sidebar input to initialize queries.")
else:
    @st.cache_resource
    def initialize_rag_resources():
        """Cache indexing pipelines to limit initialization overhead loops"""
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db_path = "app/database/vectorstore/faiss_index"
        if os.path.exists(db_path):
            return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        return None

    vector_store = initialize_rag_resources()
    
    if vector_store is None:
        st.error("🚨 **Infrastructure Error:** Vector database index artifacts missing. Ensure `datasets/vectorstore/faiss_index` is properly generated.")
    else:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant", temperature=0.0)
        
        template = """You are a strict, elite institutional investment relations agent.
Your task is to answer the User Query *only* if the Database Context explicitly contains verified records matching the criteria.

Strict Guardrail Rules:
1. If the database context does not contain direct, verified evidence addressing the query, you MUST respond with EXACTLY and ONLY this sentence:
"I cannot find a verified single-family office record matching these specific attributes in the production intelligence database."
2. Do not speculate, do not list unverified or loosely related firms, and do not extrapolate international investments or advisory services into healthcare or other unstated sectors.
3. Keep the response factual, concise, and strictly grounded in the provided context.

Database Context Layer:
{context}

User Query: {question}
Factual Professional Response:"""

        prompt = PromptTemplate.from_template(template)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        def format_docs(docs):
            return "\n\n---\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # Quick Suggestion Chips for Better User Experience
        st.markdown("**💡 Quick Query Suggestions:** Click any option below to test real intelligence extraction:")
        col1, col2, col3 = st.columns(3)
        
        selected_query = ""
        with col1:
            if st.button("🔍 Find MSD Capital"):
                selected_query = "Find verified data on MSD Capital"
        with col2:
            if st.button("🔍 Search Venture Mandates"):
                selected_query = "What are the core venture capital investment mandates?"
        with col3:
            if st.button("🔍 Check Verification Notes"):
                selected_query = "Show verification notes and websites for available records"

        query = st.text_input("Or enter your custom natural language target query:", value=selected_query, placeholder="e.g., 'Find verified data on family offices focused on tech investments'")
        
        if query:
            with st.spinner("🔄 Analyzing multi-label patterns & isolating verification vectors..."):
                try:
                    response = rag_chain.invoke(query)
                    st.markdown("### 📋 Executive Intelligence Report")
                    
                    # Styled output container
                    with st.container():
                        st.success(response)
                        
                except Exception as e:
                    st.error(f"**Pipeline Runtime Exception:** {str(e)}")