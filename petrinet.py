from threading import Thread, Lock
from typing import List, Callable
from place import Place
from transition import Transition, P_Transition


class PetriNet:
    places: List[Place]
    transitions: List[Transition]

    def __init__(self):
        self.places = []
        self.transitions = []

    def add_place(self, place: Place):
        self.places.append(place)

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def run(self, show_state: Callable[[], None] = None):
        while any(transition.is_enabled() for transition in self.transitions):
            for transition in self.transitions:
                if transition.is_enabled():
                    if show_state is not None:
                        show_state()
                    transition.fire()
        if show_state is not None:
            show_state()

    def reset(self):
        for place in self.places:
            place.reset()

    def print_marking(self):
        print("Places:")
        for place in self.places:
            if place.get_tokens() > 0:
                place.print()


class P_PetriNet(PetriNet):
    lock: Lock

    def __init__(self):
        super().__init__()
        self.lock = Lock()

    def add_transition(self, transition: P_Transition):
        super().add_transition(transition)
        transition.lock = self.lock

    def run(self, show_state: Callable[[], None] = None):
        if show_state is not None:
            show_state()
        while any(transition.is_enabled() for transition in self.transitions):
            threads = []
            for transition in self.transitions:
                thread = Thread(target=self.run_transition, args=(transition, show_state,))
                thread.start()
                threads.append(thread)
            # Wait for all threads to complete
            for thread in threads:
                thread.join()

    def run_transition(self, transition: P_Transition, show_state: Callable[[], None]):
        transition.fire(show_state)
