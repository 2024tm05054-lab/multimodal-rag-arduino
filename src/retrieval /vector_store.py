import numpy as np

class VectorStore:
    def __init__(self):
        self.texts = []
        self.vectors = []

    def embed(self, text):
        # simple fake embedding (for demo)
        return np.array([len(text)])

    def add_documents(self, texts):
        for t in texts:
            self.texts.append(t)
            self.vectors.append(self.embed(t))

    def search(self, query, top_k=3):
        query_vec = self.embed(query)

        scores = []
        for i, vec in enumerate(self.vectors):
            score = np.dot(query_vec, vec)
            scores.append((score, self.texts[i]))

        scores.sort(reverse=True, key=lambda x: x[0])
        return [t[1] for t in scores[:top_k]]
