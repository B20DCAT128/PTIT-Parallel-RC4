import sys
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
        name = input("Nhap ho va ten: ")
        student_id = input("Nhap ma so sinh vien: ")
        class_name = input("Nhap lop: ")
        plaintext = f"{name}{student_id}{class_name}"

        print(f"\nBan ro: {plaintext}")

        key = input("Nhap khoa K: ")
        ciphertext = rc4(key, plaintext)

        with open("ciphertext.txt", "w") as f:
            f.write(''.join(format(ord(c), '02x') for c in ciphertext))
        with open("key.txt", "w") as f:
            f.write(f"{key}\n{plaintext}")

        print("\nBan ma da duoc luu vao ciphertext.txt")
    except Exception as e:
        print(f"Loi khi ma hoa: {e}")
        sys.exit(1) 
