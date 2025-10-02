import re


class WriteSaveOutput:
    def __init__(self, file, original_stdout):
        self.file = file
        self.original_stdout = original_stdout
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    def write(self, data):
        self.original_stdout.write(data)
        clean_data = self.ansi_escape.sub('', data)
        self.file.write(clean_data)
        self.original_stdout.flush()
        self.file.flush()
    
    def flush(self):
        self.original_stdout.flush()
        self.file.flush()