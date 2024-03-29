import threading
from typing import List, Tuple, Union, Callable
from place import Place


class Transition:
    name: str
    input_place: list[Place]
    output_places: tuple[list[Place], list[Place]]
    callback: Callable[[str], bool]
    fired: bool

    def __init__(self, name: str, input_places: list[Place], output_places: Union[List[Place], Tuple[List[Place], List[Place]]],
                 callback: Callable[[str], bool] = None):
        self.name = name
        self.input_places = input_places
        if isinstance(output_places, tuple):
            self.output_places = (output_places[0], output_places[1])
        else:
            self.output_places = (output_places, output_places)
        self.callback = callback

    def is_enabled(self):
        if not self.input_places:
            return False
        return all(place.get_tokens() > 0 for place in self.input_places)

    def fire(self, show_state: Callable[[], None] = None):
        result = True
        if self.is_enabled():
            for place in self.input_places:
                place.remove_token()
            self.fired = True
            if self.callback is not None:
                result = self.callback(self.name)
            self.fired = False
            if result is None:
                for place in self.output_places[0]:
                    place.add_token()
            else:
                if result:
                    for place in self.output_places[0]:
                        place.add_token()
                else:
                    for place in self.output_places[1]:
                        place.add_token()

    def print(self):
        print(f"Transition: {self.name}")
        print("Input Places: ")
        for place in self.input_places:
            place.print()
        print(f"Output Places: ")
        output_places = set(self.output_places[0] + self.output_places[1])
        for place in output_places:
            place.print()


class P_Transition(Transition):

    lock: threading.Lock

    def __init__(self, name: str, input_places: list, output_places: Union[List, Tuple],
                 callback: Callable[[str], bool] = None, lock: threading = None):
        super().__init__(name, input_places, output_places, callback)
        self.fired = False
        self.lock = lock

    def fire(self, show_state: Callable[[], None] = None):
        result = False
        if not self.deduct_tokens(show_state):
            # cannot fire due to insufficient tokens
            return
        if self.callback is not None:
            result = self.callback(self.name)
        self.fired = False
        with self.lock:
            if result is None:
                for place in self.output_places[0]:
                    place.add_token()
            else:
                if result:
                    for place in self.output_places[0]:
                        place.add_token()
                else:
                    for place in self.output_places[1]:
                        place.add_token()
            if show_state is not None:
                show_state()

    def deduct_tokens(self, show_state: Callable[[], None]):
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
