from datetime import datetime
import sys
import os
from time import sleep

from src.environment import build_client, execute_client, run_data_server, run_socket_server, stop_server, stop_data_server
from src.write_save_output import WriteSaveOutput


def run_test(interval: int, socket_max_open_time: int, update_timestamp: str, custom_data_to_send_fields_sequence: str, verbose: bool = True, output_temporary: bool = True):
    os.makedirs("test_outputs", exist_ok=True)
    
    file_name = "test_outputs/output_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    with open(file_name, "w", encoding="utf-8") as output_file:
        original_stdout = sys.stdout
        sys.stdout = WriteSaveOutput(output_file, original_stdout, verbose)

        data_server_process = run_data_server()
        sleep(2)
        server_process = run_socket_server()
        sleep(1)
        
        build_client()
        execute_client(interval, socket_max_open_time, update_timestamp, custom_data_to_send_fields_sequence)

        stop_server(server_process)
        stop_data_server(data_server_process)
        
        sys.stdout = original_stdout

    lines = []
    client_lines = []
    socket_server_lines = []
    data_server_lines = []

    with open(file_name, "r", encoding="utf-8") as output_file:
        output = output_file.read()
        
        for line in output.split('\n'):
            if line.strip():
                if 'CLIENT' in line:
                    lines.append({'content': line, 'type': 'client'})
                    client_lines.append(line)
                elif 'SOCKET_SERVER' in line:
                    lines.append({'content': line, 'type': 'socket_server'})
                    socket_server_lines.append(line)
                elif 'DATA_SERVER' in line:
                    lines.append({'content': line, 'type': 'data_server'})
                    data_server_lines.append(line)
                else:
                    lines.append({'content': line, 'type': 'other'})
                    
    if output_temporary:
        os.remove(file_name)

    return lines, client_lines, socket_server_lines, data_server_lines
