def search(self, query):
    results = []

    # match based on words
    for text in self.texts:
        if any(word in text.lower() for word in query.lower().split()):
            results.append(text)

    # ensure table + image always included
    for text in self.texts:
        if "Table:" in text or "Image:" in text:
            if text not in results:
                results.append(text)

    return results[:5]
