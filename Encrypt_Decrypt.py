# ==========================
# File Encryption/Decryption
# ==========================
# This program encrypts or decrypts files using a simple block cipher.
# It processes files in 64-bit blocks, padding the last block if necessary.
# Users can specify input and output filenames and choose the operation.

# Sample P-array and S-boxes (replace with your actual arrays)
p = [
    0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344,
    0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89,
    0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C,
    0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917,
    0x9216D5D9, 0x8979FB1B
]

s = [
    [0]*256,  # S-box 0 placeholder
    [0]*256,  # S-box 1 placeholder
    [0]*256,  # S-box 2 placeholder
    [0]*256   # S-box 3 placeholder
]

# Simple key array
key = [
    0x4B7A70E9, 0xB5B32944, 0xDB75092E, 0xC4192623,
    0xAD6EA6B0, 0x49A7DF7D, 0x9CEE60B8, 0x8FEDB266,
    0xECAA8C71, 0x699A17FF, 0x5664526C, 0xC2B19EE1,
    0x193602A5, 0x75094C29
]

# --------------------------
# Function to calculate F(L)
# --------------------------
def calculate(L):
    # Uses the 4 S-boxes to compute a value based on L
    temp = s[0][L >> 24]
    temp = (temp + s[1][(L >> 16) & 0xff]) % (1 << 32)
    temp = temp ^ s[2][(L >> 8) & 0xff]
    temp = (temp + s[3][L & 0xff]) % (1 << 32)
    return temp

# --------------------------
# Encrypt a 64-bit block
# --------------------------
def encrypt_block(data):
    L = data >> 32
    R = data & 0xffffffff
    for i in range(16):
        L = L ^ p[i]
        L1 = calculate(L)
        R = R ^ calculate(L1)
        L, R = R, L
    L, R = R, L
    L = L ^ p[17]
    R = R ^ p[16]
    return (L << 32) | R

# --------------------------
# Decrypt a 64-bit block
# --------------------------
def decrypt_block(data):
    L = data >> 32
    R = data & 0xffffffff
    for i in range(17, 1, -1):
        L = L ^ p[i]
        L1 = calculate(L)
        R = R ^ calculate(L1)
        L, R = R, L
    L, R = R, L
    L = L ^ p[0]
    R = R ^ p[1]
    return (L << 32) | R

# --------------------------
# Encrypt a file
# --------------------------
def encrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while chunk := f_in.read(8):  # read 64-bit blocks
            if len(chunk) < 8:
                chunk = chunk.ljust(8, b'\0')  # pad last block
            block = int.from_bytes(chunk, byteorder='big')
            encrypted = encrypt_block(block)
            f_out.write(encrypted.to_bytes(8, byteorder='big'))

# --------------------------
# Decrypt a file
# --------------------------
def decrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while chunk := f_in.read(8):
            block = int.from_bytes(chunk, byteorder='big')
            decrypted = decrypt_block(block)
            f_out.write(decrypted.to_bytes(8, byteorder='big').rstrip(b'\0'))

# --------------------------
# Interactive menu
# --------------------------
def main():
    print("=== File Encryptor/Decryptor ===")
    operation = input("Type 'e' to encrypt or 'd' to decrypt: ").strip().lower()
    infile = input("Enter input filename: ").strip()
    outfile = input("Enter output filename: ").strip()

    if operation == 'e':
        encrypt_file(infile, outfile)
        print(f"File encrypted successfully to '{outfile}'")
    elif operation == 'd':
        decrypt_file(infile, outfile)
        print(f"File decrypted successfully to '{outfile}'")
    else:
        print("Invalid option. Please type 'e' or 'd'.")

# Run the program
if __name__ == "__main__":
    main()
