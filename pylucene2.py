import logging, sys
import lucene
import os
import json
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, StringField, TextField, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

# JSON data
json_data = [
    {
        "tconst": "tt0000005",
        "ordering": 10,
        "title": "Blacksmith Scene",
        "region": "US",
        "language": "\\N",
        "types": "imdbDisplay",
        "attributes": "\\N",
        "isOriginalTitle": "0",
        "titleType": "short",
        "primaryTitle": "Blacksmith Scene",
        "originalTitle": "Blacksmith Scene",
        "isAdult": 0,
        "startYear": "1893",
        "endYear": "\\N",
        "runtimeMinutes": "1",
        "genres": "Comedy,Short",
        "directors": "nm0005690",
        "writers": "\\N",
        "averageRating": 6.2,
        "numVotes": 2722,
        "directorsNames": ["William K.L. Dickson"],
        "writerNames": [None]
    },
    {
        "tconst": "tt0000022",
        "ordering": 1,
        "title": "The Blacksmiths",
        "region": "US",
        "language": "\\N",
        "types": "\\N",
        "attributes": "literal English title",
        "isOriginalTitle": "0",
        "titleType": "short",
        "primaryTitle": "Blacksmith Scene",
        "originalTitle": "Les forgerons",
        "isAdult": 0,
        "startYear": "1895",
        "endYear": "\\N",
        "runtimeMinutes": "1",
        "genres": "Documentary,Short",
        "directors": "nm0525910",
        "writers": "\\N",
        "averageRating": 5.1,
        "numVotes": 1124,
        "directorsNames": ["Louis Lumière"],
        "writerNames": [None]
    },
    {
        "tconst": "tt0000029",
        "ordering": 10,
        "title": "Repas de bébé",
        "region": "FR",
        "language": "\\N",
        "types": "imdbDisplay",
        "attributes": "\\N",
        "isOriginalTitle": "0",
        "titleType": "short",
        "primaryTitle": "Baby's Meal",
        "originalTitle": "Repas de bébé",
        "isAdult": 0,
        "startYear": "1895",
        "endYear": "\\N",
        "runtimeMinutes": "1",
        "genres": "Documentary,Short",
        "directors": "nm0525910",
        "writers": "\\N",
        "averageRating": 5.9,
        "numVotes": 3466,
        "directorsNames": ["Louis Lumière"],
        "writerNames": [None]
    }
]

def create_index(dir):
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
create_index('sample_lucene_index_2/')
retrieve('sample_lucene_index_2/', 'movies')