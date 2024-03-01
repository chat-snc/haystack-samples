import streamlit as st
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import FARMReader, TransformersQueryClassifier, Crawler, BM25Retriever, PreProcessor
from haystack.pipelines import ExtractiveQAPipeline, QuestionAnswerGenerationPipeline, Pipeline
from haystack.utils import launch_es

# Initialize Document Store
document_store = InMemoryDocumentStore(use_bm25=True)


# Initialize Crawler
crawler = Crawler(output_dir="crawled_data")

# Streamlit UI
st.title("Haystack URL Crawler and QA System")

url = st.text_input("Enter URL to crawl", "")

if st.button("Crawl and Prepare"):
    # Crawl the given URL
    crawler = Crawler(
        urls=[url],
        crawler_depth=0,
        output_dir="crawled_files",
    )
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=500,
        split_respect_sentence_boundary=True,
    )

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_node(
        component=crawler, name="crawler", inputs=['File'])
    indexing_pipeline.add_node(component=preprocessor,
                               name="preprocessor", inputs=['crawler'])
    indexing_pipeline.add_node(component=document_store,
                               name="document_store", inputs=['preprocessor'])

    indexing_pipeline.run()
    st.success("Crawled and stored documents.")

question = st.text_input("Enter your question", "")

if question:
    # # Initialize Reader
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(
        model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

    query_pipeline = Pipeline()
    query_pipeline.add_node(component=retriever,
                            name="retriever", inputs=["Query"])
    query_pipeline.add_node(component=reader, name="reader",
                            inputs=["retriever"])

    # Execute query
    prediction = query_pipeline.run(query=question)

    #
    #

    # Display answers
    st.write("Answers:")
    for answer in prediction['answers']:
        st.write(answer.answer, "-", round(answer.score, 4))
