from collections import defaultdict

import networkx as nx
from matplotlib import pyplot as plt

from Objects.Article import Article
from Objects.Author import Author
from ReadData.data import df

collaboration_graph =None
orcid_to_author = {}

class Graph:
    @staticmethod
    def build_author_graph(df):
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
                    author = Author("0000", coauthor_name)
                    name_to_author[coauthor_name] = author
                    collaboration_graph[author] = {}


            if orcid not in orcid_to_author :
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

    @staticmethod
    def visualize_graph(collaboration_graph, title="Collaboration Network"):
        # Create NetworkX graph
        G = nx.Graph()  # Undirected graph since collaborations are bidirectional

        # Add all authors as nodes with unique identifiers
        for author in collaboration_graph.keys():
            # Create a unique identifier by combining last name, first name initial, and ORCID
            author_label = f"{author.name.split()[0][0]}_{author.name.split()[-1]}_{author.orcid}"
            G.add_node(author_label,
                       full_name=author.name,
                       orcid=author.orcid,
                       is_connected=len(collaboration_graph[author]) > 0)

        # Add edges with weights
        for author, collaborators in collaboration_graph.items():
            author_label = f"{author.name.split()[0][0]}_{author.name.split()[-1]}_{author.orcid}"
            for collaborator, weight in collaborators.items():
                collab_label = f"{collaborator.name.split()[0][0]}_{collaborator.name.split()[-1]}_{collaborator.orcid}"
                G.add_edge(author_label, collab_label, weight=weight)

        # Separate isolated and connected nodes
        isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]
        connected_nodes = [node for node in G.nodes() if G.degree(node) > 0]

        # Calculate edge widths based on weights
        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
        max_weight = max(edge_weights) if edge_weights else 1
        edge_widths = [2 * w / max_weight for w in edge_weights]

        # Significantly larger figure to accommodate more nodes
        plt.figure(figsize=(30, 20), dpi=300)

        # Use different layout strategies
        pos = nx.spring_layout(G, k=1, iterations=200, seed=42)

        # Draw nodes with size based on connection
        nx.draw_networkx_nodes(G, pos,
                               nodelist=connected_nodes,
                               node_color='lightblue',
                               node_size=500,
                               alpha=0.7)

        nx.draw_networkx_nodes(G, pos,
                               nodelist=isolated_nodes,
                               node_color='lightcoral',
                               node_size=300,
                               alpha=0.5)

        # Draw edges
        nx.draw_networkx_edges(G, pos,
                               edge_color='gray',
                               width=edge_widths,
                               alpha=0.3)

        # Create custom labels showing first initial, last name
        labels = {node: f"{node.split('_')[0]}.{node.split('_')[1]}" for node in G.nodes()}

        # Draw labels with very small font
        nx.draw_networkx_labels(G, pos,
                                labels=labels,
                                font_size=6,
                                font_color='darkblue',
                                font_weight='bold')

        plt.title(title, fontsize=20, pad=20)
        plt.axis('off')

        # Customize legend
        blue_patch = plt.plot([], [], 'o', color='lightblue', label='Connected Authors')[0]
        red_patch = plt.plot([], [], 'o', color='lightcoral', label='Isolated Authors')[0]
        plt.legend(handles=[blue_patch, red_patch], loc='best', fontsize=10)

        return G, plt

    # Not forgetting to set matplotlib to use tight layout

    if __name__=="__main__":
        orcid_to_author, name_to_author, collaboration_graph = build_author_graph(df)
        print_graph_statistics(orcid_to_author, collaboration_graph)

        G, plt = visualize_graph(collaboration_graph, "Author Collaboration Network")
        plt.tight_layout()
        plt.show()