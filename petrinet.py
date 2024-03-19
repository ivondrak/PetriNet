from threading import Thread, Lock
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


class P_PetriNet(PetriNet):
    def __init__(self):
        super().__init__()
        self.lock = Lock()

    def add_transition(self, transition):
        super().add_transition(transition)
        transition.lock = self.lock

    def run(self, show_state=None):
        if show_state is not None:
            show_state()
        # While there is at least one transition that can fire
        while True:
            fired = False
            threads = []
            for transition in self.transitions:
                thread = Thread(target=self.run_transition, args=(transition,))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            # Check if any transition has fired in this round
            for transition in self.transitions:
                if transition.fired:
                    fired = True
                    transition.fired = False  # Reset the flag

            # If no transitions fired in this round, break the loop
            if not fired:
                break

        if show_state is not None:
            show_state()


    def run_transition(self, transition):
        transition.fire()