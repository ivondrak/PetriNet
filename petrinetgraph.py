import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

class GPlace:
    def __init__(self, place, x_coord, y_coord):
        self.place = place
        self.x = x_coord
        self.y = y_coord

class GTransition:
    def __init__(self, transition, x_coord, y_coord):
        self.transition = transition
        self.x = x_coord
        self.y = y_coord

class PetriNetGraph:
    def __init__(self, g_places, g_transitions, figsize=(15, 8)):
        self.graph = nx.DiGraph()
        self.figsize = figsize
        self.labels = {}
        self.places = {}
        self.tokens = {}
        self.transitions = {}
        self.edges = []
        index = 0
        for g_place in g_places:
            key = "P" + str(index)
            self.places[key] = (g_place.x, g_place.y)
            self.tokens[key] = g_place.place
            self.labels[key] = g_place.place.name
            index += 1
        index = 0
        for g_transition in g_transitions:
            key = "T" + str(index)
            self.transitions[key] = (g_transition.x, g_transition.y)
            self.labels[key] = g_transition.transition.name
            for input_place in g_transition.transition.input_places:
                for i in range(len(g_places)):
                    if g_places[i].place == input_place:
                        self.edges.append(("P" + str(i), key))
                        break
            for output_place in g_transition.transition.output_places:
                for i in range(len(g_places)):
                    if g_places[i].place == output_place:
                        self.edges.append((key, "P" + str(i)))
                        break
            index += 1
        self.graph.add_nodes_from(self.places)
        self.graph.add_nodes_from(self.transitions)
        self.graph.add_edges_from(self.edges)

    def draw_graph(self):
        fig, ax = plt.subplots(figsize=self.figsize)
        pos = {**self.places, **self.transitions}

        # Draw the places as circles
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.places.keys(), node_size=1000, node_color="lightgray", ax=ax)

        # Draw the transitions as rectangles
        for transition, coord in self.transitions.items():
            ax.add_patch(patches.Rectangle((coord[0], coord[1]), 0.2, 0.2, color="white", fill=False))

        # Draw edges and labels
        nx.draw_networkx_edges(self.graph, pos, node_size=1000, arrowstyle='->', arrowsize=10, width=1, edge_color="gray")
        nx.draw_networkx_labels(self.graph, pos, labels=self.labels, font_size=8, font_color='black')

        for place_key, coords in self.places.items():
            tokens_count = self.tokens[place_key].get_tokens()
            if tokens_count > 0:
                ax.add_patch(patches.Circle((coords[0],coords[1]), 0.1, color='red', fill=True, zorder=2))

        ax.axis('equal')
        plt.show()

