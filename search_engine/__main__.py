import sys

import chromadb
import uvicorn
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction

sys.path.insert(1, './utils')
from utils.chroma.process_raw_data import process_raw_data
from utils.question_handler.setup_rag_sys import app, setup_rag_sys

import pandas as pd

if __name__ == '__main__':
    
    client = chromadb.HttpClient(host='localhost')
    embd_model = "cointegrated/rubert-tiny2"


    if not client.list_collections():
        process_raw_data(
            client,
            embd_model
        )

    collection = client.get_collection(
        'FAQ_coll',
        embedding_function=SentenceTransformerEmbeddingFunction(
            embd_model,
            device='cuda',
        )
    )

    # df = pd.read_excel('./data/test.xlsx')
    # df.columns = [
    #     'question',
    #     'ans_empl',
    #     'kb_question',
    #     'kb_ans',
    #     'class_1',
    #     'class_2'
    # ]

    # result = 0

    # for _, row in df.iterrows():
    #     res = collection.query(
    #         query_texts=row['question'],
    #         n_results=10
    #     )

    #     class_ans = list(map(
    #                     lambda x: {'class_1': x['class_1'], 'class_2': x['class_2']},
    #                     res['metadatas'][0]
    #                     )
    #     )

    #     for class_sample in class_ans:

    #         if class_sample['class_1'] == row['class_1'] and class_sample['class_2'] == row['class_2']:
    #             result += 1
    #             break

        # print(
        #     f"ANSWER: {class_ans} \t GT: {row['class_1']} | {row['class_2']}"
        # )

    # print(result / len(df.question.to_list()))

    setup_rag_sys(
            client=client,
            embd_model=embd_model
    )

    uvicorn.run(
        app,
        host='0.0.0.0',
        port=1337
    )