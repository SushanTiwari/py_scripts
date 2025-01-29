import os
import streamlit as st
from pypdf import PdfReader
from chromadb import Client, Settings
from chromadb.utils import embedding_functions
import ollama
from typing import List, Dict, Tuple

# Page configuration
st.set_page_config(page_title="DeepSeek R1 Chat", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()
if "collection" not in st.session_state:
    try:
        # Initialize ChromaDB
        client = Client(Settings(
            persist_directory="./knowledge_base",
            is_persistent=True
        ))
        # Initialize the embedding function
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        # Create or get collection
        st.session_state.collection = client.get_or_create_collection(
            name="docs",
            embedding_function=sentence_transformer_ef
        )
    except Exception as e:
        st.error(f"Error initializing ChromaDB: {str(e)}")
        st.stop()

def get_collection_info() -> Tuple[int, List[str]]:
    """Get information about the current ChromaDB collection"""
    try:
        all_ids = st.session_state.collection.get()
        return len(all_ids['ids']), all_ids['metadatas']
    except Exception as e:
        st.error(f"Error getting collection info: {str(e)}")
        return 0, []

def process_pdf(pdf_file) -> int:
    """Process a PDF file and store its contents in ChromaDB"""
    # Check if file was already processed
    if pdf_file.name in st.session_state.processed_files:
        st.info(f"📘 {pdf_file.name} was already processed")
        return 0

    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split text into chunks (1000 characters each)
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

        if not chunks:
            st.warning(f"No text extracted from {pdf_file.name}")
            return 0

        # Generate unique IDs for each chunk
        ids = [f"{pdf_file.name}_{i}" for i in range(len(chunks))]

        # Store in ChromaDB with metadata
        metadata = [{"source": pdf_file.name, "chunk": i} for i in range(len(chunks))]

        # Debug info
        st.write(f"Adding {len(chunks)} chunks to ChromaDB...")

        st.session_state.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadata
        )

        # Mark file as processed
        st.session_state.processed_files.add(pdf_file.name)

        # Verify the chunks were added
        count, _ = get_collection_info()
        st.write(f"Total documents in collection: {count}")

        return len(chunks)
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return 0

def query_chromadb(query: str, n_results: int = 3) -> Tuple[List[str], List[Dict]]:
    """Query ChromaDB for relevant context"""
    try:
        # Debug info
        count, _ = get_collection_info()
        if count == 0:
            st.warning("No documents in the knowledge base yet. Please upload some PDFs first.")
            return [], []

        st.write(f"Querying ChromaDB (total documents: {count})...")

        results = st.session_state.collection.query(
            query_texts=[query],
            n_results=min(n_results, count)  # Make sure we don't request more results than we have documents
        )

        if not results or 'documents' not in results or not results['documents']:
            st.warning("Query returned no results")
            return [], []

        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if 'metadatas' in results else []

        return documents, metadatas
    except Exception as e:
        st.error(f"Error querying knowledge base: {str(e)}")
        st.error("Full error details:", exc_info=True)
        return [], []

def generate_response(prompt: str, context: str, sources: List[str]) -> str:
    """Generate response using the Deepseek model"""
    try:
        formatted_prompt = (
            f"Context from the documents:\n{context}\n\n"
            f"Question: {prompt}\n\n"
            f"Answer: Please provide a detailed response based on the context provided above. "
            f"Focus on information from the documents."
        )

        response = ollama.chat(
            model='deepseek-r1:1.5b',
            messages=[
                {
                    'role': 'user',
                    'content': formatted_prompt,
                },
            ]
        )

        # Add sources to the response
        answer = response['message']['content']
        if sources:
            unique_sources = list(set(sources))
            source_text = "\n\nSources: " + ", ".join(unique_sources)
            answer += source_text

        return answer
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I apologize, but I encountered an error while generating the response."

def main():
    # Sidebar for file upload and knowledge base management
    with st.sidebar:
        st.header("📚 Knowledge Base Management")

        # Display collection info
        count, metadatas = get_collection_info()
        st.write(f"Documents in knowledge base: {count}")

        # Display currently processed files
        if st.session_state.processed_files:
            st.write("Processed Files:")
            for file in st.session_state.processed_files:
                st.write(f"✅ {file}")

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type="pdf",
            accept_multiple_files=True,
            key="pdf_uploader"
        )

        if uploaded_files:
            for pdf_file in uploaded_files:
                if pdf_file.name not in st.session_state.processed_files:
                    with st.spinner(f"Processing {pdf_file.name}..."):
                        num_chunks = process_pdf(pdf_file)
                        if num_chunks > 0:
                            st.success(f"✅ Processed {pdf_file.name} into {num_chunks} chunks")

        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # Main chat interface
    st.title("🤖 DeepSeek R1 Chat")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask your question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get relevant context
        with st.spinner("🔍 Searching knowledge base..."):
            contexts, metadatas = query_chromadb(prompt)
            if not contexts:
                st.warning("No relevant information found in the uploaded documents.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I couldn't find any relevant information in the uploaded documents. Please try rephrasing your question or upload relevant documents."
                })
                return

            full_context = "\n".join(contexts)
            sources = [meta["source"] for meta in metadatas] if metadatas else []

        # Generate response
        with st.spinner("🤔 Thinking..."):
            response = generate_response(prompt, full_context, sources)

        # Add assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
