from src.test_case import TestCase


test_cases = [
    TestCase(
        name="Single exchange and data save test",
        interval=2000,
        socket_max_open_time=3000,
        update_timestamp="true",
        custom_data_to_send_fields_sequence='[]',
        assertions=[
            (lambda lines, client_lines, socket_server_lines, data_server_lines: any('Client connected!' in line for line in client_lines), "Client connection message not found"),
            (lambda l, c, s, d: any('WebSocket connection opened' in line for line in s), "Server connection message not found"),
            (lambda l, c, s, d: sum(1 for line in s if "Choosing move: {'move': -1, 'start': 1}" in line) == 1, "Server response message should appear once"),
            (lambda l, c, s, d: sum(1 for line in c if 'Received from server: {"move": -1, "start": 1}' in line) == 1, "Expected server response not found"),
            (lambda l, c, s, d: any('Received game state' in line for line in d), "Data server success message not found"),
        ]
    ),
    TestCase(
        name="Test if moves are chosen correctly",
        interval=1200,
        socket_max_open_time=3000,
        update_timestamp="true",
        custom_data_to_send_fields_sequence='[{"leftPaddleY": 70, "ballY": 0}, {"leftPaddleY": 50,"ballY": 200}]',
        assertions=[
            (lambda l, c, s, d: sum(1 for line in c if 'Received from server: {"move": 1, "start": 1}' in line) == 1, "Wrong 1st server response"),
            (lambda l, c, s, d: sum(1 for line in c if 'Received from server: {"move": -1, "start": 1}' in line) == 1, "Wrong 2nd server response")
        ]
    ),
    TestCase(
        name="Test if server responses are in correct order",
        interval=1200,
        socket_max_open_time=3000,
        update_timestamp="true",
        custom_data_to_send_fields_sequence='[{"leftPaddleY": 70, "ballY": 0}, {"leftPaddleY": 50,"ballY": 200}]',
        assertions=[
            (lambda l, c, s, d: (
                [i for i, line in enumerate(c) if 'Received from server: {"move": 1, "start": 1}' in line][0] <
                [i for i, line in enumerate(c) if 'Received from server: {"move": -1, "start": 1}' in line][0]
            ), "Wrong order of server responses"),
        ]
    ),
    TestCase(
        name="Test latency",
        interval=100,
        socket_max_open_time=3000,
        update_timestamp="true",
        custom_data_to_send_fields_sequence='[]',
        assertions=[
            (lambda l, c, s, d: sum(1 for line in c if 'Received from server' in line) > 25, "Too few responses:"),
        ]
    ),
]


if __name__ == "__main__":
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        if test_case.run(verbose=True):
            passed += 1
        else:
            failed += 1
    
    print(f"Test Results: {passed} passed, {failed} failed")
    
