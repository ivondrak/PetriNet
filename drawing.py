import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx


def draw_petri_net():
    fig, ax = plt.subplots(figsize=(15, 8))

    # Define a directed graph
    G = nx.DiGraph()

    labels = {"P00": "Customer", "P01": "Customer", "P02": "Customer", "P03": "Customer",
              "P10": "Salesman", "P11": "Salesman", "P12": "Salesman", "P13": "Salesman",
              "P20": "Order", "P21": "Order",
              "P40": "Accountant", "P50": "Financing", "P60": "Car", "P70": "Protocol",
              "T1": "Car selection", "T2": "Get financing", "T3": "Car ordering", "T4": "Payment checking",
              "T5": "Car handover"}

    # Define places and transitions
    places = {"P00": (1, 1), "P10": (1, 2),
              "P01": (3, 1), "P20": (3, 2), "P11": (3, 3), "P21": (3, 4),
              "P02": (5, 1), "P50": (5, 2), "P40": (5, 3), "P12": (5, 4), "P60": (5, 5),
              "P03": (7, 1), "P13": (7, 2),
              "P70": (9, 2)}
    transitions = {"T1": (2, 1), "T2": (4, 1), "T3": (4, 4), "T4": (6, 2), "T5": (8, 2)}

    # Add nodes to the graph
    G.add_nodes_from(places)
    G.add_nodes_from(transitions)

    # Define edges (or arcs in Petri net). Manually entered here.
    edges = [("P00", "T1"), ("P10", "T1"),
             ("T1", "P01"), ("T1", "P11"), ("T1", "P20"), ("T1", "P21"),
             ("P01", "T2"), ("P20", "T2"), ("P11", "T3"), ("P21", "T3"),
             ("T3", "P12"), ("T3", "P60"), ("T2", "P02"), ("T2", "P50"),
             ("P02", "T4"), ("P50", "T4"), ("P12", "T4"), ("P40", "T4"),
             ("T4", "P03"), ("T4", "P13"),
             ("P60", "T5"), ("P03", "T5"), ("P13", "T5"),
             ("T5", "P70")]

    G.add_edges_from(edges)
    pos = {**places, **transitions}

    # Draw the places as circles
    nx.draw_networkx_nodes(G, pos, nodelist=places.keys(), node_size=1000, node_color="lightgray", ax=ax)

    # Draw the transitions as rectangles
    for transition, coord in transitions.items():
        ax.add_patch(patches.Rectangle((coord[0], coord[1]), 0.2, 0.2, color="white", fill=False))

    # Draw edges and labels
    #nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_edges(G, pos, node_size=1000, arrowstyle='->', arrowsize=10, width=1, edge_color="lightgray")

    #nx.draw_networkx_labels(G, pos, ax=ax)

    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='black')

    plt.show()


draw_petri_net()
