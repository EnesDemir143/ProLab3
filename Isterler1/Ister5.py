class Ister5:

    @staticmethod
    def calculate_collaborators_count(collaboration_graph, author=None):

        if author is None:
            orcid = input("Please enter the author's ORCID: ").strip()
            # Find author in orcid_to_author dict
            for auth in collaboration_graph.keys():
                if auth.orcid == orcid:
                    author = auth
                    break
            if not author:
                print("Author not found with given ORCID.")
                return 0

        collaborators = collaboration_graph[author]
        collaborator_count = len(collaborators)

        print(f"Number of collaborators for author {author.name} (ORCID: {author.orcid}): {collaborator_count}")

        # Optionally print all collaborators
        if collaborator_count > 0:
            print("\nCollaborators:")
            for collaborator, count in collaborators.items():
                print(f"- {collaborator.name}: {count} collaboration(s)")

        return collaborator_count