from torch.cuda import is_available
import chromadb
import chromadb.api
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction
import pandas as pd


def get_metadatas(df: pd.DataFrame):
    result = list()

    for _, row in df.iterrows():
        result.append(
            {
                'theme': row['theme'],
                'answer': row['answer'],
                'class_1': row['class_1'],
                'class_2': row['class_2']
            }
        )

    return result


def process_raw_data(
        client: chromadb.api.ClientAPI,
        embd_model: str
    ):

    client.create_collection(
        'FAQ_coll',
        embedding_function=SentenceTransformerEmbeddingFunction(
            embd_model,
            device='cuda' if is_available() else 'cpu'
        )
    )

    try:

        df = pd.read_excel('./data/knowlege_base.xlsx')

        df.columns = ['theme', 'question', 'answer', 'class_1', 'class_2']

        collection = client.get_collection(
            'FAQ_coll',
            embedding_function=SentenceTransformerEmbeddingFunction(
                embd_model,
                device='cuda' if is_available() else 'cpu',

            )
        )

        collection.add(
            documents=df.question.to_list(),
            metadatas=get_metadatas(df),
            ids=[str(idx) for idx in range(0, len(df.question.to_list()))]
        )

    except:
        client.delete_collection('FAQ_coll')
