class Article:
    def __init__(self, doi, name, coauthors):
        self.doi = doi
        self.name = name
        self.coauthors = set(coauthors)  # Using set to prevent duplicate coauthors