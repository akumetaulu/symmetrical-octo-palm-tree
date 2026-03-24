import subprocess
import random
import time
import psutil
import signal

BASH_SCRIPT = "./push"

WINDOW = 1.0          # control window seconds
TARGET_MIN = 85
TARGET_MAX = 99

def get_tree_cpu_percent(proc, interval=0.2):
    """Return CPU usage of process + children"""
    procs = [proc] + proc.children(recursive=True)
    total = 0.0

    for p in procs:
        try:
            total += p.cpu_percent(interval=None)
        except psutil.NoSuchProcess:
            pass

    time.sleep(interval)

    for p in procs:
        try:
            total += p.cpu_percent(interval=None)
        except psutil.NoSuchProcess:
            pass

    return total


def suspend_tree(proc):
    for p in [proc] + proc.children(recursive=True):
        try:
            p.suspend()
        except psutil.NoSuchProcess:
            pass


def resume_tree(proc):
    for p in [proc] + proc.children(recursive=True):
        try:
            p.resume()
        except psutil.NoSuchProcess:
            pass


# start bash script
process = subprocess.Popen(["bash", BASH_SCRIPT])
proc = psutil.Process(process.pid)

cpu_count = psutil.cpu_count()

target = random.randint(TARGET_MIN, TARGET_MAX)
last_change = time.time()

print(f"CPU cores: {cpu_count}")
print(f"Initial target CPU: {target}%")

try:
    while process.poll() is None:

        if time.time() - last_change >= 60:
            target = random.randint(TARGET_MIN, TARGET_MAX)
            last_change = time.time()
            print(f"New CPU target: {target}%")

        cpu = get_tree_cpu_percent(proc) / cpu_count

        if cpu > 0:
            ratio = min(target / cpu, 1)
        else:
            ratio = 1

        run_time = WINDOW * ratio
        sleep_time = WINDOW - run_time

        resume_tree(proc)
        time.sleep(run_time)

        if sleep_time > 0:
            suspend_tree(proc)
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    try:
        process.send_signal(signal.SIGTERM)
    except:
        pass
