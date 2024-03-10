import gradio as gr
import json
import pandas as pd
import numpy as np
from bert_index import *
from pylucene_search import *

list_data_obj = json.load(open("../CS242 Final Combined IMDB Dataset (nulls replaced).json"))
search_index = search_bert_index()
search_index.read_index("multi_full_index_no_mask.index")

pylucene_search_index = search_pylucene_index()
pylucene_index = "imdb_lucene_index/"

class test_obj:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def method_call(radio_button, num_results, inp):
    if radio_button == "PyLucene":
        # place_holder_obj = [
        #     test_obj(1, 1),
        #     test_obj(2, 2),
        #     test_obj(3, 3)
        # ]
        # movie_pylucene_results = [
        #     {
        #         "score": 0.95,
        #         "title": "The Shawshank Redemption",
        #         "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        #         "region": "USA",
        #         "start_year": "1994",
        #         "genres": ["Drama"],
        #         "directors_names": ["Frank Darabont"],
        #         "writer_names": ["Stephen King", "Frank Darabont"]
        #     },
        #     {
        #         "score": 0.92,
        #         "title": "The Godfather",
        #         "synopsis": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        #         "region": "USA",
        #         "start_year": "1972",
        #         "genres": ["Crime", "Drama"],
        #         "directors_names": ["Francis Ford Coppola"],
        #         "writer_names": ["Mario Puzo", "Francis Ford Coppola"]
        #     }
        # ]

        movie_pylucene_results = pylucene_search_index.retrieve(inp, num_results=num_results)


        # return pd.DataFrame([t.__dict__ for t in place_holder_obj])
        return pd.DataFrame(movie_pylucene_results)

    elif radio_button == "Bert":
        # movie_indexes = search_index.search(inp, num_results=num_results)
        # movie_bert_results = []
        # for index in movie_indexes[0]:
        #     movie_bert_results.append(list_data_obj[index])
        # for i in range(len(movie_bert_results)):
        #     t_const_id = movie_bert_results[i]["tconst"]
        #     movie_bert_results[i]["URL"] = f"https://www.imdb.com/title/{t_const_id}"
        place_holder_obj = [
            test_obj(1, 1),
            test_obj(2, 2),
            test_obj(3, 3)
        ]
        return pd.DataFrame([t.__dict__ for t in place_holder_obj])
        # return pd.DataFrame(movie_bert_results)

    return pd.DataFrame([{
        "Error": "Make Sure to Select A search Method"
    }])

demo = gr.Interface(
    fn=method_call,
    inputs=[
        gr.Radio(["PyLucene", "Bert"], label="Search Method", info="Choose how to look up"),
        gr.Number(value=0, label="Number Results", info="How many Results"),
        gr.Textbox(placeholder="Horror Movies", label="Search Engine", info="What you are looking up")
    ],
    outputs="dataframe"
)

if __name__ == "__main__":
    demo.launch(server_port=8080)
