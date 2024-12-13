from collections import defaultdict

from Article import Article
from Author import Author


def build_author_graph(df):
    orcid_to_author = {}
    name_to_author = {}
    collaboration_graph = defaultdict(lambda: defaultdict(int))

    for orcid, name in zip(df["orcid"], df["author_name"]):
        name = name.strip()
        orcid = orcid.strip()

        if orcid not in orcid_to_author:
            author = Author(orcid, name)
            orcid_to_author[orcid] = author
            name_to_author[name] = author #aynı adda olanlarda burada her eklenen nesne bir öncekini eziyor.
            collaboration_graph[author] = {}

    for row in df.itertuples():
        orcid = row.orcid.strip()
        main_author = orcid_to_author[orcid]

        coauthors = row.coauthors.strip('[]').replace("'", "").split(',')
        coauthors = [name.strip() for name in coauthors]

        if len(coauthors) > 1:
            coauthors.pop(row.author_position - 1)

        article = Article(row.doi, row.paper_title, coauthors)
        main_author.articles.add(article)

    for row in df.itertuples():
        orcid = row.orcid.strip()
        main_author = orcid_to_author[orcid]

        coauthors = row.coauthors.strip('[]').replace("'", "").split(',')
        coauthors = [name.strip() for name in coauthors]

        if len(coauthors) > 1:
            coauthors.pop(row.author_position - 1)

        # Collaboration graph'ı güncelle
        for coauthor_name in coauthors:
            if coauthor_name in name_to_author:
                coauthor = name_to_author[coauthor_name] ##en son olan nesneyi tutar o ad la.
                if coauthor.orcid != main_author.orcid:
                    collaboration_graph[main_author][coauthor] = collaboration_graph[main_author].get(coauthor, 0) + 1
                    collaboration_graph[coauthor][main_author] = collaboration_graph[coauthor].get(main_author, 0) + 1

    return orcid_to_author, name_to_author, collaboration_graph

def print_graph_statistics(orcid_to_author, collaboration_graph):
    print("\nGraph Statistics:")
    print(f"Total number of authors: {len(orcid_to_author)}")

    # Count isolated and connected authors
    isolated_authors = []
    connected_authors = []

    for orcid, author in orcid_to_author.items():
        collaborators = collaboration_graph[author]
        if collaborators:
            connected_authors.append(author)
        else:
            isolated_authors.append(author)

    print(f"Connected authors: {len(connected_authors)}")
    print(f"Isolated authors: {len(isolated_authors)}")

    # Print connected authors' statistics
    print("\nConnected Authors:")
    for author in connected_authors:
        collaborators = collaboration_graph[author]
        print(f"\nAuthor: {author.name} ({author.orcid})")
        print(f"Number of collaborators: {len(collaborators)}")
        for coauthor, weight in collaborators.items():
            print(f"  - {coauthor.name}: {weight} collaboration(s)")

    # Print isolated authors
    print("\nIsolated Authors:")
    for author in isolated_authors:
        print(f"- {author.name} ({author.orcid})")