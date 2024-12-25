from collections import defaultdict
import networkx as nx

from Objects.Article import Article
from Objects.Author import Author
from ReadData.data import df

collaboration_graph =None
orcid_to_author = {}

class Graph:
    @staticmethod
    def build_author_graph(df):
        a=000
        global orcid_to_author,collaboration_graph
        name_to_author = {}
        collaboration_graph = defaultdict(lambda: defaultdict(int))

        for orcid, name,coauthors,author_position in zip(df["orcid"], df["author_name"],df["coauthors"],df["author_position"]):
            name = name.strip()
            orcid = orcid.strip()
            coauthors = coauthors.strip('[]').replace("'", "").split(',')
            coauthors = [name.strip() for name in coauthors]

            if len(coauthors) > 1:
                coauthors.pop(author_position - 1)

            for coauthor_name in coauthors:
                if coauthor_name not in name_to_author:
                    author = Author(a, coauthor_name)
                    name_to_author[coauthor_name] = author
                    orcid_to_author[str(a)] = author
                    collaboration_graph[author] = defaultdict(int)
                    a+=1


            if orcid not in orcid_to_author :
                author = Author(orcid, name)
                orcid_to_author[orcid] = author
                name_to_author[name] = author #aynı adda olanlarda burada her eklenen nesne bir öncekini eziyor.
                collaboration_graph[author] = defaultdict(int)

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
            author_position = row.author_position
            coauthors = row.coauthors.strip('[]').replace("'", "").split(',')

            coauthors = [name.strip() for name in coauthors]

            if len(coauthors) > 1:
                coauthors.pop(author_position - 1)


            article = Article(row.doi, row.paper_title, coauthors)
            for coauthor_name in coauthors:
                main_author = name_to_author[coauthor_name]
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
                    if coauthor.orcid != main_author.orcid :
                        collaboration_graph[main_author][coauthor] = collaboration_graph[main_author].get(coauthor, 0) + 1
                        collaboration_graph[coauthor][main_author] = collaboration_graph[coauthor].get(main_author, 0) + 1

            for index in range(len(coauthors)):
                for index2 in range(index+1,len(coauthors)):
                    coauthor1 = name_to_author[coauthors[index]]
                    coauthor2 = name_to_author[coauthors[index2]]
                    collaboration_graph[coauthor1][coauthor2] = collaboration_graph[coauthor1].get(coauthor2, 0) + 1
                    collaboration_graph[coauthor2][coauthor1] = collaboration_graph[coauthor2].get(coauthor1, 0) + 1



        return orcid_to_author, name_to_author, collaboration_graph

    @staticmethod
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


    # Not forgetting to set matplotlib to use tight layout

    if __name__=="__main__":
        orcid_to_author, name_to_author, collaboration_graph = build_author_graph(df)
        print_graph_statistics(orcid_to_author, collaboration_graph)
