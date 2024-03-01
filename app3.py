import streamlit as st
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import FARMReader, BM25Retriever, PreProcessor, Crawler
from haystack.pipelines import Pipeline

# Streamlit UI setup
st.title("Haystack URL Crawler and QA System")

# Initialize the Document Store
document_store = InMemoryDocumentStore(use_bm25=True)

# Input for URL
url = st.text_input("Enter URL to crawl", "")

if st.button("Crawl and Prepare"):
    # Initialize Crawler
    crawler = Crawler(output_dir="crawled_data")
    # Crawl the given URL
    documents = crawler.crawl(urls=[url], crawler_depth=0)

    # Initialize PreProcessor
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=200,
        split_respect_sentence_boundary=True
    )

    # Process documents
    processed_docs = []
    for document in documents:
        processed_docs.extend(preprocessor.process(document))

    # Write processed documents to the document store
    document_store.write_documents(processed_docs)

    st.success("Crawled, processed, and stored documents.")

# Input for the user's question
question = st.text_input("Enter your question", "")

if question:
    # Initialize Retriever and Reader
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(
        model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

    # Define the QA Pipeline
    qa_pipeline = Pipeline()
    qa_pipeline.add_node(component=retriever,
                         name="BM25Retriever", inputs=["Query"])
    qa_pipeline.add_node(component=reader, name="FARMReader",
                         inputs=["BM25Retriever"])

    # Run the pipeline
    results = qa_pipeline.run(query=question)

    # Display answers
    st.write("Answers:")
    for answer in results['answers']:
        st.write(f"{answer.answer} - Score: {round(answer.score, 4)}")
