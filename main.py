
from src.test_runner import run_test


def test_basic_functionality():
    interval = 800
    socket_max_open_time = 3000
    update_timestamp = "true"
    custom_data_to_send_fields_sequence = '[{"leftPaddleY": 342341324, "rightPaddleY": 123456789}, {"leftPaddleY": 213,"rightPaddleY": 2341432124}]'

    lines, client_lines, server_lines = run_test(
        interval=interval,
        socket_max_open_time=socket_max_open_time,
        update_timestamp=update_timestamp,
        custom_data_to_send_fields_sequence=custom_data_to_send_fields_sequence,
        verbose=True
    )
        
    client_output = '\n'.join(client_lines)
    assert 'Client connected!' in client_output, "Client connection message not found"
    assert 'Received from server: {"move": 1, "start": 1}' in client_output, "Expected server response not found"
    
    server_output = '\n'.join(server_lines)
    assert 'WebSocket connection opened' in server_output, "Server connection message not found"
    assert "Choosing move: {'move': 1, 'start': 1}" in server_output, "Server response message not found"
        


if __name__ == "__main__":
    test_basic_functionality()
