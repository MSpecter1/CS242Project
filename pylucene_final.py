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

def parse_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def create_index(movies, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    for movie in movies:
        tconst = movie['tconst']
        ordering = movie['ordering']
        title = movie['title']
        region = movie['region']
        language = movie['language']
        types = movie['types']
        attributes = movie['attributes']
        isOriginalTitle = movie['isOriginalTitle']
        titleType = movie['titleType']
        primaryTitle = movie['primaryTitle']
        originalTitle = movie['originalTitle']
        isAdult = movie['isAdult']
        startYear = movie['startYear']
        endYear = movie['endYear']
        runtimeMinutes = movie['runtimeMinutes']
        genres = movie['genres']
        directors = movie['directors']
        writers = movie['writers']
        averageRating = movie['averageRating']
        numVotes = movie['numVotes']
        directorsNames = movie['directors Names']
        writerNames = movie['writer Names']

        doc = Document()
        doc.add(Field('Tconst', str(tconst), contextType))
        doc.add(Field('Ordering', str(ordering), contextType))
        doc.add(Field('Title', str(title), contextType))
        doc.add(Field('Region', str(region), contextType))
        doc.add(Field('Language', str(language), contextType))
        doc.add(Field('Types', str(types), contextType))
        doc.add(Field('Attributes', str(attributes), contextType))
        doc.add(Field('Is Original Title', str(isOriginalTitle), contextType))
        doc.add(Field('Title Type', str(titleType), contextType))
        doc.add(Field('Primary Title', str(primaryTitle), contextType))
        doc.add(Field('Original Title', str(originalTitle), contextType))
        doc.add(Field('Is Adult', str(isAdult), contextType))
        doc.add(Field('Start Year', str(startYear), contextType))
        doc.add(Field('End Year', str(endYear), contextType))
        doc.add(Field('Runtime Minutes', str(runtimeMinutes), contextType))
        doc.add(Field('Genres', str(genres), contextType))
        doc.add(Field('Directors', str(directors), contextType))
        doc.add(Field('Writers', str(writers), contextType))
        doc.add(Field('Average Rating', str(averageRating), contextType))
        doc.add(Field('Num Votes', str(numVotes), contextType))
        doc.add(Field('Directors Names', str(directorsNames), contextType))
        doc.add(Field('Writer Names', str(writerNames), contextType))
        writer.addDocument(doc)
    writer.close()

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Title', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "Tconst": doc.get("Tconst"),
            "Ordering": doc.get("Ordering"),
            "Title": doc.get("Title"),
            "Region": doc.get("Region"),
            "Language": doc.get("Language"),
            "Types": doc.get("Types"),
            "Attributes": doc.get("Attributes"),
            "Is Original Title": doc.get("Is Original Title"),
            "Title Type": doc.get("Title Type"),
            "Primary Title": doc.get("Primary Title"),
            "Original Title": doc.get("Original Title"),
            "Is Adult": doc.get("Is Adult"),
            "Start Year": doc.get("Start Year"),
            "End Year": doc.get("End Year"),
            "Runtime Minutes": doc.get("Runtime Minutes"),
            "Genres": doc.get("Genres"),
            "Directors": doc.get("Directors"),
            "Writers": doc.get("Writers"),
            "Average Rating": doc.get("Average Rating"),
            "Num Votes": doc.get("Num Votes"),
            "Directors Names": doc.get("Directors Names"),
            "Writer Names": doc.get("Writer Names")
        })
    
    print(topkdocs)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
json_data = parse_json('test.json')
create_index(json_data ,'sample_lucene_index/')
retrieve('sample_lucene_index/', 'Blacksmith')