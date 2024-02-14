import logging, sys
logging.disable(sys.maxsize)

import lucene
import os
import json
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.search import TermRangeQuery
from org.apache.lucene.search import WildcardQuery
from org.apache.lucene.util import BytesRef

def retrieve(storedir, field, search_value):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    if field == "start_year" and " TO " in search_value: # range search
        start, end = search_value.split(" TO ")
        parsed_query = TermRangeQuery(field, BytesRef(start.encode('utf-8')), BytesRef(end.encode('utf-8')), True, True)
    elif "*" in search_value: # wildcard search
        parser = QueryParser(field, StandardAnalyzer())
        parsed_query = parser.parse(search_value)
        wildcard_query = WildcardQuery(parsed_query.getTerm(field))
    else: # basic text search
        parser = QueryParser(field, StandardAnalyzer())
        parsed_query = parser.parse(search_value)

    if "*" in search_value:
        topDocs = searcher.search(wildcard_query, 10).scoreDocs
    else:
        topDocs = searcher.search(parsed_query, 10).scoreDocs

    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "title": doc.get("title"),
            "synopsis": doc.get("synopsis"),
            "region": doc.get("region"),
            "start_year": doc.get("start_year"),
            "genres": doc.get("genres"),
            "directors_names": doc.get("directors_names"),
            "writer_names": doc.get("writer_names")
        })
    
    print(topkdocs)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Checking to make sure a search query is provided.
if len(sys.argv) <= 1:
    print("Please enter a search query.")
    print("For a basic text search, enter a search query with the format 'Field:\"search_value\"'.")
    print("For a range search on start_year, enter a search query with the format 'start_year:[YYYY TO YYYY]'.")
    print("For a wildcard search, enter a search query with the format 'Field:*value*'.")
    sys.exit(1)

query_arg = ' '.join(sys.argv[1:])
# Checking for the right format of the query
if ":" not in query_arg:
    print("For a basic text search, enter a search query with the format 'Field:\"search_value\"'.")
    print("For a range search on start_year, enter a search query with the format 'start_year:[YYYY TO YYYY]'.")
    print("For a wildcard search, enter a search query with the format 'Field:*value*'.")
    sys.exit(1)

if "start_year" in query_arg and " TO " in query_arg: # range search
    field, search_value = query_arg.split(":", 1)
    search_value = search_value.strip('[')
    search_value = search_value.strip(']')
else: # text search
    field, search_value = query_arg.split(":", 1)
    search_value = search_value.strip('"')

retrieve('imdb_lucene_index/', field, search_value)