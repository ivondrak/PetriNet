
class PetriNet:
    def __init__(self):
        self.places = []
        self.transitions = []

    def add_place(self, place):
        self.places.append(place)

    def add_transition(self, transition):
        self.transitions.append(transition)

    def run(self, show_state=None):
        if show_state is not None:
            show_state()
        while any(transition.is_enabled() for transition in self.transitions):
            for transition in self.transitions:
                transition.fire()
        if show_state is not None:
            show_state()

    def step_by_step(self, show_state=None):
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
