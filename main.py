# This is a sample Python script.
from petrinet import PetriNet, P_PetriNet
from place import Place
from transition import Transition, P_Transition
from petrinetgraph import PetriNetGraph, GPlace, GTransition


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def run_petrinet():

    pn = P_PetriNet()

    p00 = Place("Customer", 1)
    p01 = Place("Customer")
    p02 = Place("Customer")
    p03 = Place("Customer")
    pn.add_place(p00)
    pn.add_place(p01)
    pn.add_place(p02)
    pn.add_place(p03)

    p10 = Place("Salesman", 1)
    p11 = Place("Salesman")
    p12 = Place("Salesman")
    p13 = Place("Salesman")
    pn.add_place(p10)
    pn.add_place(p11)
    pn.add_place(p12)
    pn.add_place(p13)

    p20 = Place("Order")
    p21 = Place("Order")
    pn.add_place(p20)
    pn.add_place(p21)

    p40 = Place("Accountant", 1)
    p50 = Place("Financing")
    p60 = Place("Car")
    p70 = Place("Protocol")
    pn.add_place(p40)
    pn.add_place(p50)
    pn.add_place(p60)
    pn.add_place(p70)

    car_selection = P_Transition("Car selection", [p00, p10], [p01, p11, p20, p21], transition_fired)
    car_ordering = P_Transition("Car ordering", [p11, p21], [p12, p60], transition_fired)
    get_financing = P_Transition("Get financing", [p01, p20], [p02, p50], transition_fired)
    checking_payment = P_Transition("Checking payment", [p02, p12, p40, p50], [p13, p03], transition_fired)
    car_hand_over = P_Transition("Car hand over", [p13, p03, p60], [p70], transition_fired)

    pn.add_transition(checking_payment)
    pn.add_transition(car_hand_over)
    pn.add_transition(car_selection)
    pn.add_transition(car_ordering)
    pn.add_transition(get_financing)

    g_places = [GPlace(p00, 1, 1), GPlace(p10, 1, 2),
                GPlace(p01, 3, 1), GPlace(p20, 3, 2), GPlace(p11, 3, 3), GPlace(p21, 3, 4),
                GPlace(p02, 5, 1), GPlace(p50, 5, 2), GPlace(p40, 5, 3), GPlace(p12, 5, 4), GPlace(p60, 5, 5),
                GPlace(p03, 7, 1), GPlace(p13, 7, 2),
                GPlace(p70, 9, 2)]

    g_transitions = [GTransition(car_selection, 2, 1),
                     GTransition(get_financing, 4, 1),
                     GTransition(car_ordering, 4, 4),
                     GTransition(checking_payment, 6, 1),
                     GTransition(car_hand_over, 8, 2)]

    png = PetriNetGraph(g_places, g_transitions)
    png.draw_graph()

    pn.print_marking()
    pn.run(png.draw_graph)
    pn.print_marking()


def transition_fired(transition_name):
    print(f"Transition {transition_name} fired!")


if __name__ == '__main__':
    run_petrinet()
