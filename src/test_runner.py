from datetime import datetime
import sys

from src.environment import build_client, execute_client, run_server, stop_server
from src.write_save_output import WriteSaveOutput


def run_test(interval: int, socket_max_open_time: int, update_timestamp: str, custom_data_to_send_fields_sequence: str):
    file_name = "test_outputs/output_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    with open(file_name, "w", encoding="utf-8") as output_file:
        original_stdout = sys.stdout
        sys.stdout = WriteSaveOutput(output_file, original_stdout)

        server_process = run_server()
        build_client()
        execute_client(interval, socket_max_open_time, update_timestamp, custom_data_to_send_fields_sequence)
        stop_server(server_process)
        
        sys.stdout = original_stdout

        return file_name