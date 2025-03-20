import os
import sys
import hashlib
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)

#Calculate hash for the password
def hash_data(data):

    sha = hashlib.sha256()
    sha.update(data.encode('utf-8'))
    return sha.digest()

def encrypt(key, plaintext, associate_data):
    """Encrypts binary or text data using AES-GCM."""
    iv = os.urandom(12)  # Generate a random IV
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
    ).encryptor()
    
    encryptor.authenticate_additional_data(associate_data)
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()  # No .encode() needed
    return iv, ciphertext, encryptor.tag

def decrypt(iv, tag, key, ciphertext, associate_data):
    """Decrypts binary or text data using AES-GCM."""
    try:
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
        ).decryptor()
        
        decryptor.authenticate_additional_data(associate_data)
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext  # Return raw binary data
    except:
        print("Authentication tag verification failed. The data may be corrupted or the password is wrong.")
        return b''  # Return empty bytes on error


def mainencrypt(key, input_file, output_file):
    """Encrypts any file type."""
    data = b"authenticated but not encrypted payload"
    with open(input_file, "rb") as original:
        plaintext = original.read()  # Read binary content
    # Encrypt the binary data
    iv, ciphertext, tag = encrypt(key, plaintext, data)
    with open(output_file, "wb") as encrypted:
        encrypted.write(iv)  # Write IV
        encrypted.write(ciphertext)  # Write Ciphertext
        encrypted.write(tag)  # Write Tag

def maindecrypt(key, input_file, output_file):
    """Decrypts any file type."""
    data = b"authenticated but not encrypted payload"
    
    with open(input_file, "rb") as original:
        iv = original.read(12)  # Read IV (12 bytes)
        ciphertext = original.read()  # Read Ciphertext + Tag
        tag = ciphertext[-16:]  # Extract Tag (last 16 bytes)
        encrypted_data = ciphertext[:-16]  # Extract Ciphertext
    # Decrypt the binary data
    plaintext = decrypt(iv, tag, key, encrypted_data, data)
    if plaintext == "Error in decryption.":
        return  # Stop execution if decryption fails
    with open(output_file, "wb") as decrypted:
        decrypted.write(plaintext)  # Write binary output

def main():

    # The user needs to give 5 arguments
    if len(sys.argv) != 5:
        print("Please insert the arguments in this order: python/python3 -script.py -operation -password -input_file -output_file")
        return
    
    operation = sys.argv[1] # Type of operation
    password = sys.argv[2] # Given password
    input_file = sys.argv[3] # Input file 
    output_file = sys.argv[4] # Output file

    key = hash_data(password) # Calculates the key to a given password

    # Check if the input file exists
    try:
        with open(input_file, 'r'):
            pass
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' does not exist.")
        return
    
    # Check what operation is needed or if its valid at all
    if operation == "encrypt":
        mainencrypt(key, input_file, output_file)
        print(f"Encryption complete. Output written to {output_file}")
    elif operation == "decrypt":
        maindecrypt(key, input_file, output_file)
        print(f"Decryption complete. Output written to {output_file}")
    else:
        print("Invalid operation. Use encrypt or decrypt.")

if __name__ == '__main__':
    main()