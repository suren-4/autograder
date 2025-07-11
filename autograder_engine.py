from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def grade_answer(model_answer, student_answer):
    model_embedding = model.encode([model_answer])[0]
    student_embedding = model.encode([student_answer])[0]
    
    similarity = cosine_similarity([model_embedding], [student_embedding])[0][0]
    score = round(similarity * 10, 2)  # scale to 10
    return score, similarity
