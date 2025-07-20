import threading
import time

# Shared data
shared_array = []
array_lock = threading.Lock()

# Writer thread function
def writer():
    for i in range(10):
        with array_lock:
            shared_array.append(i)
            print(f"[Writer] Wrote: {i}")
        time.sleep(0.1)

# Reader function in main thread
def reader():
    last_read_index = 0
    while True:
        with array_lock:
            new_data = shared_array[last_read_index:]
            if new_data:
                print(f"[Reader] Read: {new_data}")
                last_read_index += len(new_data)
        time.sleep(0.2)

# Start writer thread
writer_thread = threading.Thread(target=writer)
writer_thread.start()

# Run reader in main thread
reader()
