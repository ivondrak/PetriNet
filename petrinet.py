from place import Place
from transition import Transition

class PetriNet:
    def __init__(self):
        self.places = []
        self.transitions = []

    def add_place(self, place):
        self.places.append(place)

    def add_transition(self, transition):
        self.transitions.append(transition)

    def run(self):
        for transition in self.transitions:
            transition.fire()

    def print_marking(self):
        print("Places:")
        for place in self.places:
            place.print()

