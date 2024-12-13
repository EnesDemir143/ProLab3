class Author:
    def __init__(self, orcid, name):
        self.orcid = orcid
        self.name = name
        self.articles = set()  # Using set to prevent duplicate articles
