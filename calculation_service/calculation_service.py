from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler


class CalculationService:

    name = "calculation_service"

    prime_service = RpcProxy("prime_service")
    palindrome_service = RpcProxy("palindrome_service")

    dispatch = EventDispatcher()

    result = {
        'is_prime': None,
        'is_palindrome': None
    }

    # Choreography
    @event_handler("prime_service", "calculation_result_event")
    def handle_prime_result(self, payload):
        self.result['is_prime'] = payload

    @event_handler("palindrome_service", "calculation_result_event")
    def handle_palindrome_result(self, payload):
        self.result['is_palindrome'] = payload

    @rpc
    def is_prime_palindrome_choreo(self, num):
        self.dispatch("prime_palindrome_event", num)

        # wait for result
        while self.result['is_prime'] is None or self.result['is_palindrome'] is None:
            continue

        self.result['is_prime_palindrome'] = self.result['is_prime'] and self.result['is_palindrome']

        return self.result

    # PubSub
    @rpc
    def dispatch_method(self, payload):
        self.dispatch("meong_event", payload)

    # Orchestration
    @rpc
    def is_prime_palindrome(self, num):
        result = {
            'is_prime': self.prime_service.is_prime(num),
            'is_palindrome': self.palindrome_service.is_palindrome(num),
            'is_prime_palindrome': self.prime_service.is_prime(num) and self.palindrome_service.is_palindrome(num)
        }

        return result
