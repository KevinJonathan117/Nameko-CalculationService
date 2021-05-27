from nameko.rpc import rpc
from nameko.events import event_handler, EventDispatcher


class PrimeService:
    name = "prime_service"

    dispatch = EventDispatcher()

    @event_handler("calculation_service", "meong_event")
    def handle_event_method(self, payload):
        print(payload)

    @event_handler("calculation_service", "prime_palindrome_event")
    def handle_prime_palindrome(self, payload):
        print(payload)
        print(self.is_prime(payload))
        self.dispatch("calculation_result_event", self.is_prime(payload))

    @rpc
    def is_prime(self, num):
        factor = 0
        for i in range(1, num + 1):
            if num % i == 0:
                factor += 1

        return factor == 2
