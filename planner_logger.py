"""
Custom logger. Creates logs with the time they were logged at.
Logs are created by calling the logger's add_to_log() function.
"""
# Standard imports
import atexit
from datetime import datetime

# Custom imports
import core

log = []

def get_time():
    """
    Returns the current time in the format of:

    Hour:Minute:Second.Milliseconds AM/PM: 
    """
    return datetime.now().strftime('%I:%M:%S.%f')[:-3] + datetime.now().strftime(' %p')

def add_to_log(message):
    """
    Prints a message to the console, and logs it.
    """
    print(f'{get_time()}: {message}')
    log.append(f'{get_time()}: {message}')

def count_logs():
    """
    Determines what number the log being created should be.
    """
    folder_path = core.logs_folder_path
    file_count = sum(1 for f in folder_path.iterdir() if f.is_file())

    return file_count

def write_log():
    """
    Writes the logs taken to a file nad saves it.
    """
    file_count = count_logs()
    log_filename = core.logs_folder_path / f'log_{file_count + 1}.txt'

    with open(log_filename, 'w', encoding='utf-8') as f:
        for line in log:
            f.write(line + '\n')

# Only writes all the logs once the program ends to prevent constant disk I/O
atexit.register(write_log)
