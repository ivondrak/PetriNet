from pypetri import PetriNet, Transition, Place


def run_petri_net():
    net = PetriNet("My Net")

    # Definujeme místa
    p1 = Place("P1")
    p2 = Place("P2")
    p3 = Place("P3")

    # Přidáme místa do sítě
    net.add_place(p1)
    net.add_place(p2)
    net.add_place(p3)

    # Definujeme přechody
    t1 = Transition("T1")
    t2 = Transition("T2")

    # Přidáme přechody do sítě
    net.add_transition(t1)
    net.add_transition(t2)

    # Definujeme počáteční a koncové body přechodů
    net.add_arc("P1", "T1")
    net.add_arc("T2", "P1")
    net.add_arc("T1", "P2")
    net.add_arc("P2", "T2")
    net.add_arc("T2", "P3")

    # Inicializujeme síť s počátečními značkami
    net.set_marking("P1", 1)

    # Spustíme síť
    while net.enabled_transitions():
        transition = net.pick_transition()
        print(f"Fire transition: {transition}")
        net.fire_transition(transition)

    print("End state reached")


if __name__ == "__main__":
    run_petri_net()
