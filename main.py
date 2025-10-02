
from src.test_runner import run_test


def test_basic_functionality():
    interval = 800
    socket_max_open_time = 3000
    update_timestamp = "true"
    custom_data_to_send_fields_sequence = '[{"leftPaddleY": 342341324, "rightPaddleY": 123456789}, {"leftPaddleY": 213,"rightPaddleY": 2341432124}]'

    file_name = run_test(
        interval=interval,
        socket_max_open_time=socket_max_open_time,
        update_timestamp=update_timestamp,
        custom_data_to_send_fields_sequence=custom_data_to_send_fields_sequence
    )

    with open(file_name, "r", encoding="utf-8") as output_file:
        output = output_file.read()
        
        lines = []
        for line in output.split('\n'):
            if line.strip():
                if 'CLIENT' in line:
                    lines.append({'content': line, 'type': 'client'})
                elif 'SERVER' in line:
                    lines.append({'content': line, 'type': 'server'})
                else:
                    lines.append({'content': line, 'type': 'other'})
        
        client_lines = [line['content'] for line in lines if line['type'] == 'client']
        server_lines = [line['content'] for line in lines if line['type'] == 'server']
        
        client_output = '\n'.join(client_lines)
        assert 'Client connected!' in client_output, "Client connection message not found"
        assert 'Received from server: {"move": 1, "start": 1}' in client_output, "Expected server response not found"
        
        server_output = '\n'.join(server_lines)
        assert 'WebSocket connection opened' in server_output, "Server connection message not found"
        assert "Choosing move: {'move': 1, 'start': 1}" in server_output, "Server response message not found"
        
        print(f"\nFound {len(client_lines)} client lines and {len(server_lines)} server lines")
        print("All assertions passed!")


if __name__ == "__main__":
    test_basic_functionality()
