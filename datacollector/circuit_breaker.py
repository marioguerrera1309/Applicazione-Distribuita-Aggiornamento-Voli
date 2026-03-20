import time
import threading
import os
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=120, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
        self.lock = threading.Lock()
    def call(self, func, *args, **kwargs):
        print(f"DEBUG: Breaker ID {id(self)} sta gestendo la chiamata", file=os.sys.stderr)
        with self.lock:
            if self.state == 'OPEN':
                time_since_failure = time.time() - self.last_failure_time
                if time_since_failure > self.recovery_timeout:
                    self.state = 'HALF_OPEN'
                    print(f"DEBUG: Breaker {id(self)} passa a HALF_OPEN", file=os.sys.stderr)
                else:
                    raise CircuitBreakerOpenException("Circuit is open. Call denied.")
        try:
            result = func(*args, **kwargs)
        except self.expected_exception as e:
            with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.state == 'HALF_OPEN' or self.failure_count >= self.failure_threshold:
                    self.state = 'OPEN'
                raise e
        else:
            with self.lock:
                if self.state == 'HALF_OPEN':
                    self.state = 'CLOSED'
                    self.failure_count = 0
                    print(f"DEBUG: Breaker {id(self)} tornato CLOSED", file=os.sys.stderr)
            return result
class CircuitBreakerOpenException(Exception):
    pass