from nameko.rpc import rpc
from nameko.events import event_handler, EventDispatcher


class PalindromeService:
    name = "palindrome_service"

    dispatch = EventDispatcher()

    @event_handler("calculation_service", "meong_event")
    def handle_event_method(self, payload):
        print(payload)

    @event_handler("calculation_service", "prime_palindrome_event")
    def handle_prime_palindrome(self, payload):
        print(payload)
        print(self.is_palindrome(payload))
        self.dispatch("calculation_result_event", self.is_palindrome(payload))

    @rpc
    def is_palindrome(self, num):
        original = num
        reverse = 0
        tmp = int(num)

        while tmp:
            left = tmp % 10
            reverse = reverse * 10 + left
            tmp = int(tmp / 10)

        return reverse == original
