import multiprocessing
import os
import csv
import time

def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    output = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        output.append(byte ^ K)

    return bytes(output)


def process_block(args):
    key, block = args
    return rc4(key, block)

def divide_into_blocks(data, block_size=256):
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]

def parallel_rc4(key, data, num_processes=2, block_size=256):
    blocks = divide_into_blocks(data, block_size)
    if len(blocks[-1]) < block_size:
        blocks[-1] += b'\x00' * (block_size - len(blocks[-1]))

    with multiprocessing.Pool(processes=num_processes) as pool:
        result = pool.map(process_block, [(key, block) for block in blocks])
    return b''.join(result)

def measure_time(key, data, num_processes):
    start_time = time.time()
    parallel_rc4(key, data, num_processes=num_processes)
    end_time = time.time()
    return end_time - start_time

def add_columns_to_csv(filename, input_sizes, new_results):
    if not os.path.exists(filename):
        print("csv khong ton tai")
        return

    with open(filename, mode='r', newline='') as file:
        reader = list(csv.reader(file))
        header = reader[0]
        rows = reader[1:] 

    cores = [2, 4, 6, 8]
    for core in cores:
        if f"processes {core}" not in header:
            header.append(f"{core} processes")

    for i, row in enumerate(rows):
        for j, processes_time in enumerate(new_results[i]):
            if len(row) <= len(header) - len(cores) + j:
                row.append(f"{processes_time:.6f}") 

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    key = input("Nhap key: ")  
    key_bytes = key.encode() 

    input_sizes = [10, 15, 25, 30]
    plaintexts = [os.urandom(int(size * 1024 * 1024)) for size in input_sizes]

    results = []
    for size, plaintext in zip(input_sizes, plaintexts):
        time_results = []
        for num_processes in [2, 4, 6, 8]:
            if num_processes > multiprocessing.cpu_count():
                break
            duration = measure_time(key_bytes, plaintext, num_processes)
            time_results.append(duration)
        results.append(time_results)

    add_columns_to_csv("rc4_results.csv", input_sizes, results)
    print(f"Ket qua duoc luu vao file rc4_results.csv")
