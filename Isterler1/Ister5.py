from CreateGraph.Graph import orcid_to_author
class Ister5:

    @staticmethod
    def calculate_collaborators_count(collaboration_graph,orcid):

        collaborators = collaboration_graph[orcid_to_author[orcid]]
        collaborator_count = len(collaborators)
        print(collaborator_count)

        print(f"Number of collaborators for author {orcid_to_author[orcid].name} (ORCID: {orcid}): {collaborator_count}")

        # Optionally print all collaborators
        if collaborator_count > 0:
            print("\nCollaborators:")
            for collaborator, count in collaborators.items():
                print(f"- {collaborator.name}: {count} collaboration(s)")

        return orcid_to_author[orcid].name,orcid,collaborator_count