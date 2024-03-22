class Transition:

    def __init__(self, name, input_places=(), output_places=(), callback=None):
        self.name = name
        self.input_places = input_places
        self.output_places = output_places
        self.callback = callback

    def add_input_place(self, place):
        self.input_places.append(place)

    def add_output_place(self, place):
        self.output_places.append(place)

    def is_enabled(self):
        if not self.input_places:
            return False
        return all(place.get_tokens() > 0 for place in self.input_places)

    def fire(self, show_state=None):
        if self.is_enabled():
            for place in self.input_places:
                place.remove_token()
            if self.callback is not None:
                self.callback(self.name)
            for place in self.output_places:
                place.add_token()

    def print(self):
        print(f"Transition: {self.name}")
        print("Input Places: ")
        for place in self.input_places:
            place.print()
        print(f"Output Places: ")
        for place in self.output_places:
            place.print()

class P_Transition(Transition):

    def __init__(self, name, input_places=(), output_places=(), callback=None, lock=None):
        super().__init__(name, input_places, output_places, callback)
        self.fired = False
        self.lock = lock

    def fire(self, show_state=None):
        if not self.deduct_tokens(show_state):
            # cannot fire due to insufficient tokens
            return
        if self.callback is not None:
            self.callback(self.name)
        self.fired = False
        with self.lock:
            for place in self.output_places:
                place.add_token()
            if show_state is not None:
                show_state()

    def deduct_tokens(self, show_state):
        with self.lock:  # using the same lock object from PetriNet class
            if all(place.tokens > 0 for place in self.input_places):
                for place in self.input_places:
                    place.remove_token()
                self.fired = True
                if show_state is not None:
                    show_state()
                return True
            else:
                return False