import os
import time
import subprocess
from datetime import datetime

TARGET_DIR = '/autofs'
EXPECTED_SHARE_FOLDER = 'vault'
SLEEP_DURATION = 60  # Time between checks
STANDBY_COUNT = 15  # Number of checks before disk is disconnected
POWEROFF_COMMAND = 'uhubctl -l 1-1 -a off -r 100'

def run():
    count = 0
    while True:
        is_mounted = check_mount()

        if is_mounted:
            print(f'{datetime.now()} disk is mounted')
            count = 0
        else:
            count += 1
            print(f'{datetime.now()} disk is not mounted, count: {count}')
            
            if count >= STANDBY_COUNT:
                print(f'{datetime.now()} Powering off USB devices')
                process = subprocess.Popen(POWEROFF_COMMAND.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                count = 0

        time.sleep(SLEEP_DURATION)

def check_mount():
    with os.scandir(TARGET_DIR) as dir_entries:
        for entry in dir_entries:
            if entry.name != EXPECTED_SHARE_FOLDER:
                continue

            info = entry.stat()
            if info.st_size == 4096:
                return True
            else:
                return False


if __name__ == '__main__':
    run()

