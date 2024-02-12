import logging, sys
import os
import json
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, StringField, TextField, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

# Function to read JSON data from file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def create_index(dir, json_data):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    # Define field types
    title_type = FieldType()
    title_type.setStored(True)
    title_type.setTokenized(True)
    title_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    genres_type = FieldType()
    genres_type.setStored(True)
    genres_type.setTokenized(True)
    genres_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    # Index each JSON document
    for item in json_data:
        doc = Document()
        doc.add(StringField('tconst', item['tconst'], Field.Store.YES))
        doc.add(TextField('title', item['title'], title_type))
        doc.add(TextField('genres', item['genres'], genres_type))
        writer.addDocument(doc)

    writer.close()

def retrieve(storedir, query):
    searchDir = SimpleFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    parser = QueryParser('title', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "tconst": doc.get("tconst"),
            "title": doc.get("title"),
            "genres": doc.get("genres")
        })

    print(topkdocs)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Path to the JSON file
json_file_path = 'test.json'

# Read JSON data from the file
json_data = read_json_file(json_file_path)

# Directory to store the Lucene index
index_directory = 'sample_lucene_index/'

# Create Lucene index
create_index(index_directory, json_data)

# Search for documents containing the term "Blacksmith" in the title
search_query = 'Blacksmith'
retrieve(index_directory, search_query)
