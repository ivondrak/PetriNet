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

    def fire(self):
        if self.is_enabled():
            for place in self.input_places:
                place.remove_token()
            if self.callback:
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
