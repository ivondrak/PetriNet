import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

from place import Place
from transition import Transition


class GPlace:
    place: Place
    x: int
    y: int

    def __init__(self, place: Place, x_coord: int, y_coord: int):
        self.place = place
        self.x = x_coord
        self.y = y_coord


class GTransition:
    transition: Transition
    x: int
    y: int

    def __init__(self, transition: Transition, x_coord: int, y_coord: int):
        self.transition = transition
        self.x = x_coord
        self.y = y_coord


class PetriNetGraph:
    count = 0

    graph: nx.DiGraph
    figsize: tuple[int, int]
    labels: dict[str, str]
    places: dict[str, tuple[int, int]]
    tokens: dict[str, Place]
    transitions: dict[str, tuple[int, int]]
    fired: dict[str, Transition]
    edges: list[tuple[str, str]]

    def __init__(self, g_places: list, g_transitions: list, figsize: tuple[int, int] = (15, 10)):
        self.graph = nx.DiGraph()
        self.figsize = figsize
        self.labels = {}
        self.places = {}
        self.tokens = {}
        self.transitions = {}
        self.fired = {}
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
            self.fired[key] = g_transition.transition
            self.labels[key] = g_transition.transition.name
            for input_place in g_transition.transition.input_places:
                for i in range(len(g_places)):
                    if g_places[i].place == input_place:
                        self.edges.append(("P" + str(i), key))
                        break
            output_places = set(g_transition.transition.output_places[0] + g_transition.transition.output_places[1])
            for output_place in output_places:
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
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.places.keys(), node_size=1000, node_color="lightgray",
                               ax=ax)

        # Draw the transitions as rectangles
        for transition, coord in self.transitions.items():
            width = 0.2
            height = 0.2
            ax.add_patch(patches.Rectangle((coord[0] - width / 2, coord[1] - height / 2), width, height, color="gray",
                                           fill=False))

        # Draw edges and labels
        nx.draw_networkx_edges(self.graph, pos, node_size=1000, arrowstyle='->', arrowsize=10, width=1,
                               edge_color="gray")
        label_pos = {node: (coords[0], coords[1] - 0.25) for node, coords in pos.items()}
        nx.draw_networkx_labels(self.graph, label_pos, labels=self.labels, font_size=8, font_color='black')

        for place_key, coords in self.places.items():
            tokens_count = self.tokens[place_key].get_tokens()
            if tokens_count > 0:
                ax.add_patch(patches.Circle((coords[0], coords[1]), 0.1, color='red', fill=True, zorder=2))

        for transition_key, coords in self.transitions.items():
            if self.fired[transition_key].fired:
                width = 0.1
                height = 0.1
                ax.add_patch(
                    patches.Rectangle((coords[0] - width / 2, coords[1] - height / 2), width, height, color='red',
                                      fill=True, zorder=2))

        ax.axis('equal')

    def show_graph(self):
        self.draw_graph()
        plt.show()

    def save_graph(self):
        self.draw_graph()
        self.count += 1
        filename = "petrinetgraph" + "-" + str(self.count) + ".png"
        plt.savefig(filename)
