from haystack.nodes import Crawler
from haystack.pipelines import Pipeline
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import Crawler, PreProcessor, BM25Retriever, FARMReader


crawler = Crawler(
    urls=["https://www.jomashop.com/montblanc-heritage-brown-dial-mens-watch-128671.html"],
    crawler_depth=1,
    output_dir="crawled_files",
)


document_store = InMemoryDocumentStore(use_bm25=True)


preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="word",
    split_length=500,
    split_respect_sentence_boundary=True,
)

indexing_pipeline = Pipeline()
indexing_pipeline.add_node(component=crawler, name="crawler", inputs=['File'])
indexing_pipeline.add_node(component=preprocessor,
                           name="preprocessor", inputs=['crawler'])
indexing_pipeline.add_node(component=document_store,
                           name="document_store", inputs=['preprocessor'])


indexing_pipeline.run()

retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(
    model_name_or_path="deepset/roberta-base-squad2-distilled", use_gpu=False)

query_pipeline = Pipeline()
query_pipeline.add_node(component=retriever,
                        name="retriever", inputs=["Query"])
query_pipeline.add_node(component=reader, name="reader",
                        inputs=["retriever"])


results = query_pipeline.run(query="how much is the montblanc watch?")

print("\nQuestion: ", results["query"])
print("\nAnswers:")
for answer in results["answers"]:
    print("- ", answer.answer)
print("\n\n")
