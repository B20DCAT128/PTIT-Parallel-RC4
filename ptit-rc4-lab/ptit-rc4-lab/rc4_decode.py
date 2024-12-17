import sys
import subprocess
def ksa(key):
    """Key Scheduling Algorithm (KSA)"""
    key_length = len(key)
    T = [key[i % key_length] for i in range(256)]  
    S = list(range(256)) 
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256 
        S[i], S[j] = S[j], S[i]  
    return S

def prga(S):
    """Pseudo-Random Generation Algorithm (PRGA)"""
    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def rc4(key, ciphertext):
    """RC4 Decryption"""
    key = [ord(c) for c in key]
    S = ksa(key)
    keystream = prga(S)
    return ''.join([chr(ord(c) ^ next(keystream)) for c in ciphertext])

if __name__ == "__main__":
    try:
        with open("key.txt", "r") as f:
            stored_key = f.readline().strip()
            expected_plaintext = f.readline().strip()
    except FileNotFoundError:
        print("Khong tim thay file chua ban ma!")
        sys.exit(1)

    key = input("Nhap khoa K de giai ma: ")

    try:
        with open("ciphertext.txt", "r") as f:
            ciphertext = f.read()
            ciphertext = ''.join(chr(int(ciphertext[i:i+2], 16)) for i in range(0, len(ciphertext), 2))
        plaintext = rc4(key, ciphertext)
        if plaintext == expected_plaintext:
            print(f"\nKet qua giai ma: {plaintext}")
            subprocess.run(["cat", "/home/check.txt"])
            sys.exit(0)
        else:
            print(f"\nKet qua giai ma: {plaintext}")
            sys.exit(1)

    except FileNotFoundError:
        print("Khong tim thay file chua ban ma!")
        sys.exit(1)
    except Exception as e:
        print(f"Lỗi khi giải mã: {e}")
        sys.exit(1)

