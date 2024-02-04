#Package imports
from pymongo import MongoClient
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#This processes the mongoDB atlas objects and converts them into the lists of user data we want to analyze.
def get_database():
    client = MongoClient("mongodb+srv://test_user:test_pass@dreamcluster.vfcbjke.mongodb.net/?retryWrites=true&w=majority")
    db = client.dreamDB.dreams
    return db
def get_dream_content(username):
    db = get_database()
    userData = db.find({'username': username})
    userData = list(userData)
    dreamContent = [data.get('dreamContent', None) for data in userData]
    return dreamContent

#This builds off the bert pre-trained language model and the cosine_similarity package from sci-kit to generate an association score for 
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')
def agent(dream_log, word):
    def get_embedding(text):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(1)
        return embeddings
    def calculate_similarity(text1, text2):
        embedding1 = get_embedding(text1)
        embedding2 = get_embedding(text2)
        similarity = cosine_similarity(embedding1.detach().numpy(), embedding2.detach().numpy())
        return similarity[0][0]
    return calculate_similarity(dream_log, word)


def scores(username):
    results = []
    analytical = agent("".join(get_dream_content(username)), "analytical")
    ambition = agent("".join(get_dream_content(username)), "ambition")
    fear = agent("".join(get_dream_content(username)), "fear")
    happy = agent("".join(get_dream_content(username)), "happy")
    sad = agent("".join(get_dream_content(username)), "sad")
    anger = agent("".join(get_dream_content(username)), "anger")
    adventure = agent("".join(get_dream_content(username)), "adventure")
    results.append(analytical)
    results.append(ambition)
    results.append(fear)
    results.append(happy)
    results.append(sad)
    results.append(anger)
    results.append(adventure)
    return results
