
class PetriNet:
    def __init__(self):
        self.places = []
        self.transitions = []

    def add_place(self, place):
        self.places.append(place)

    def add_transition(self, transition):
        self.transitions.append(transition)

    def run(self):
        while any(transition.is_enabled() for transition in self.transitions):
            for transition in self.transitions:
                transition.fire()

    def step_by_step(self, showstate=None):
        while any(transition.is_enabled() for transition in self.transitions):
            for transition in self.transitions:
                if transition.is_enabled():
                    showstate()
                    transition.fire()
        showstate()

    def print_marking(self):
        print("Places:")
        for place in self.places:
            if place.get_tokens() > 0:
                place.print()
