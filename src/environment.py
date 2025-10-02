import os
import subprocess
import threading
import time
import sys
from dotenv import load_dotenv


YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def build_client():
    print(f"{BLUE}[BUILD] Building TypeScript client...{RESET}")

    load_dotenv()
    env = os.environ.copy()
    node_path = os.getenv("NODE_PATH")

    if node_path:
        node_path = node_path.strip().strip('"').strip("'")
        if os.name == 'nt':
            env["PATH"] = node_path + ";" + env["PATH"]
        else:
            env["PATH"] = node_path + "/bin:" + env["PATH"]

    def run_npm_command(cmd):
        with open(os.devnull, 'w') as devnull:
            result = subprocess.run(cmd, cwd="client", env=env, 
                                    shell=(os.name == 'nt'), 
                                    stdout=devnull, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(result.stderr)
                return False
        return True

    if not run_npm_command(["npm", "install", "typescript"]):
        return
    if not run_npm_command(["npx", "tsc"]):
        return
    
    print(f"{BLUE}[BUILD] TypeScript build completed{RESET}")


def execute_client(interval, socket_max_open_time, update_timestamp, custom_data_to_send_fields_sequence):
    timestamp = time.strftime('%H:%M:%S')
    
    process = subprocess.Popen(
        ["node", "client/dist/main.js", str(interval), str(socket_max_open_time), update_timestamp, custom_data_to_send_fields_sequence],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    while True:
        if process.stdout is None:
            break
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            timestamp = time.strftime('%H:%M:%S')
            print(f"{BLUE}[CLIENT {timestamp}] {output.strip()}{RESET}")
    
    process.wait()


def run_server():
    print(f"{YELLOW}[SERVER] Starting Python server...{RESET}")
    
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    
    process = subprocess.Popen(
        [sys.executable, "-u", "server/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=0,
        universal_newlines=True,
        env=env
    )
    
    def read_server_output():
        while True:
            if process.stdout is None:
                break
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                timestamp = time.strftime('%H:%M:%S')
                print(f"{YELLOW}[SERVER {timestamp}] {output.strip()}{RESET}")
    
    server_thread = threading.Thread(target=read_server_output, daemon=True)
    server_thread.start()
    
    return process


def stop_server(process):
    print(f"{YELLOW}[SERVER] Stopping server...{RESET}")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

