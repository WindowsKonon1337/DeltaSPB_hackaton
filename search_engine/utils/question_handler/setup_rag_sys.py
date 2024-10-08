import json

import aiohttp
from chromadb.utils.embedding_functions import \
    SentenceTransformerEmbeddingFunction
from fastapi import FastAPI
from pydantic import BaseModel
from torch.cuda import is_available

app = FastAPI()

from pydantic import BaseModel


class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    class_1: str
    class_2: str


def str_to_json(input_str):
    lines = input_str.strip().split('\n')
    result_dict = {}
    try:
        rename_dict = {
            'класс 1': 'class_1',
            'класс 2': 'class_2',
            'ответ': 'answer'
        }

        for line in lines[:2]:
            key, value = line.split(':', 1)
            result_dict[rename_dict[key.strip().lower()]] = value

        key, value = '\n'.join(lines[2:]).split(':', 1)
        result_dict[rename_dict[key.strip().lower()]] = value.replace('\n', ' ')

    except Exception as e:
        print(e)

    return result_dict


def setup_rag_sys(**kwargs):
    client = kwargs['client']
    embd_model = kwargs['embd_model']
    url = 'http://91.224.86.101:6969/v1/completions'

    collection = client.get_collection(
        'FAQ_coll',
        embedding_function=SentenceTransformerEmbeddingFunction(
            embd_model,
            device='cuda' if is_available() else 'cpu',
        )
    )

    async def get_answer_from_llm(session: aiohttp.ClientSession, prompts: dict[str, str]):
        async with session.post(url, json={'system_prompt': prompts['system_prompt'], 'user_prompt': prompts['user_prompt']}) as resp:
            return await resp.json()
        
    def get_relevant_documents(session: aiohttp.ClientSession, question: str):
        return collection.query(
            query_texts=question,
            n_results=10
        )
    
    def prepare_prompts(relevant_docs, question):
        with open('./prompts/system', encoding='utf-8') as sys_prompt_file:
            system_prompt = sys_prompt_file.read()
        with open('./prompts/user', encoding='utf-8') as sys_prompt_file:
            user_prompt_template = sys_prompt_file.read()

        context_chunk_template =\
'''
Класс 1: {class_1}
Класс 2: {class_2}
Ответ: {answer}
'''

        context_list = []

        for metadata_sample in relevant_docs['metadatas'][0]:
            context_list.append(
                context_chunk_template.format(
                    class_1=metadata_sample['class_1'],
                    class_2=metadata_sample['class_2'],
                    answer=metadata_sample['answer']
                )
            )

        user_prompt = user_prompt_template.format(
            question=question,
            context='###\n'.join(context_list)
        )

        return {'system_prompt': system_prompt, 'user_prompt': user_prompt}

    @app.post('/predict')
    async def question(req: Request):
        async with aiohttp.ClientSession() as session:
            relevant_docs = get_relevant_documents(session, req.question)

            prompts = prepare_prompts(relevant_docs, req.question)

            answer = await get_answer_from_llm(session, prompts)

            return str_to_json(answer[0]['outputs'][0]['text'])
    return question
