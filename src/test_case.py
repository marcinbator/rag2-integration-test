from src.test_runner import run_test


class TestCase:
    def __init__(self, name, interval, socket_max_open_time, update_timestamp, 
                 custom_data_to_send_fields_sequence, assertions):
        self.name = name
        self.interval = interval
        self.socket_max_open_time = socket_max_open_time
        self.update_timestamp = update_timestamp
        self.custom_data_to_send_fields_sequence = custom_data_to_send_fields_sequence
        self.assertions = assertions
    
    def run(self, verbose=False):
        if verbose:
            print(f"Running test case: {self.name}")
        
        lines, client_lines, socket_server_lines, data_server_lines = run_test(
            interval=self.interval,
            socket_max_open_time=self.socket_max_open_time,
            update_timestamp=self.update_timestamp,
            custom_data_to_send_fields_sequence=self.custom_data_to_send_fields_sequence,
            verbose=verbose
        )
        
        try:
            for assertion_lambda, error_message in self.assertions:
                if not assertion_lambda(lines, client_lines, socket_server_lines, data_server_lines):
                    raise AssertionError(error_message)
            
            print(f"Test '{self.name}' passed!")
            return True
        
        except AssertionError as e:
            print(f"Test '{self.name}' failed: {e}")
            return False