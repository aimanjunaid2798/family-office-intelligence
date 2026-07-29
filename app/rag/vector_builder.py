import os
import logging
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_production_vector_store():
    input_csv = 'datasets/validated/final_clean_evaluation_v2.csv'
    output_db_dir = 'app/database/vectorstore/faiss_index'
    
    if not os.path.exists(input_csv):
        logging.error(f"Vector Ingestion Interrupted: Source {input_csv} not found. Check pipeline pipeline sequence.")
        return
        
    logging.info("Loading validated production family office data...")
    df = pd.read_csv(input_csv)
    
    if 'final_status' in df.columns:
        df = df[df['final_status'] == 'Verified']
    
    documents = []
    for idx, row in df.iterrows():
        name = row.get('name', 'Unknown SFO')
        website = row.get('website', 'N/A')
        notes = row.get('validation_notes', 'No formal baseline verification notes recorded.')
        
        # Structural design block for precision retrieval mapping
        page_content = f"Family Office Name: {name}\nWebsite: {website}\nVerification Context: {notes}"
        
        doc = Document(
            page_content=page_content,
            metadata={"sfo_name": name, "source_file": input_csv, "index_id": idx}
        )
        documents.append(doc)
        
    if not documents:
        logging.warning("No verified records found in the source dataset file to generate indices.")
        return

    logging.info(f"Generating localized mini embeddings for {len(documents)} qualifying SFOs...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_store = FAISS.from_documents(documents, embeddings)
    os.makedirs(output_db_dir, exist_ok=True)
    vector_store.save_local(output_db_dir)
    logging.info(f"Vector serialization pipeline complete! Target: {output_db_dir}")

if __name__ == "__main__":
    build_production_vector_store()