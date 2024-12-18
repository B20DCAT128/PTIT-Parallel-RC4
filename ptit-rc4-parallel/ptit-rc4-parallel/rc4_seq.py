import time
import os
import csv

def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = 0
    j = 0
    keystream = []
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    return bytes([char ^ keystream[k] for k, char in enumerate(data)])

def generate_data(size_mb):
    return bytearray([i % 256 for i in range(size_mb * 1024 * 1024)])

def measure_rc4(size_mb, key):
    data = generate_data(size_mb)
    start_time = time.time()
    rc4(key, data)
    end_time = time.time()
    return end_time - start_time

def write_to_csv_vertical(filename, sizes, results):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Size (MB)", "Time (s)"])
        for i, size in enumerate(sizes):
            writer.writerow([size, results[i]])

file_sizes = [10, 15, 25, 30]
results = []
key = input("Nhap key:")
key = key.encode()
for size in file_sizes:
    result = measure_rc4(size,key) 
    results.append(result)

write_to_csv_vertical("rc4_results.csv", file_sizes, results)
print(f"Ket qua duoc luu vao file rc4_results.csv")
