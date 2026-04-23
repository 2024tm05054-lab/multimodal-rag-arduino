def search(self, query):
    results = []

    for text in self.texts:
        if any(word in text.lower() for word in query.lower().split()):
            results.append(text)

    return results[:3]
