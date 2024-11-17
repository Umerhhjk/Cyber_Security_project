from sympy import primerange, gcd
import random

def prime_generator(limit):
    
    """ Generate two distinct random primes from a specified range. """
    
    primes_list = list(primerange(0, limit))
    return random.sample(primes_list, 2)

def mod_inverse(e, phi):
    
    """ Calculate the modular inverse of e modulo phi using brute-force search. """
    
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Modular inverse does not exist.")

def RSA_keys(limit=9999):
    
    """ Generate RSA public and private keys along with modulus. """
    
    p, q = prime_generator(limit)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    e = random.randint(3, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)
    
    d = mod_inverse(e, phi_n)
    
    return (e, n), (d, n), n, p, q, phi_n

# def encode_message(message):
    
#     """ Convert the message to a list of ASCII values. """
    
#     return [ord(c) for c in message]

def encode_message_utf8(message):
    """ Encode a message as a list of integers using UTF-8 encoding. """
    return list(message.encode('utf-8'))


def decode_message_utf8(encoded_bytes):
    """ Decode a list of UTF-8 encoded integers back to a string. """
    # Convert the list of integers back to bytes, then decode using UTF-8
    return bytes(encoded_bytes).decode('utf-8')


def encrypt_message(encoded_message, e, n):
    
    """ Encrypt the encoded message using the public key (e, n). """
    
    return [pow(c, e, n) for c in encoded_message]

def decrypt_message(ciphertext, d, n):
    
    """ Decrypt the list of integers in ciphertext using the private key (d, n). """
    
    return [pow(c, d, n) for c in ciphertext]

# def convert_ciphertext_to_hex(ciphertext):
    
#     """ Convert the list of ciphertext integers to a hexadecimal string. """
    
#     return ''.join(format(c, 'x') for c in ciphertext)

def main():
    public_key, private_key, n, p, q, phi_n = RSA_keys()
    
    print("Public Key:", public_key)
    print("Private Key:", private_key)
    print("Modulus n:", n)
    print("Phi of n:", phi_n)
    print("p:", p)
    print("q:", q)
    
    
    """First calculate number of bytes.
        partition it into blocks of size <= n
        encrypt each block
        """
    message = "My name is Khan and I am not a terrorist."
    
    encoded_message = encode_message_utf8(message)
    
    ciphertext = encrypt_message(encoded_message, *public_key)
    print("Ciphertext array:", ciphertext)
    
    #ciphertext_hex = convert_ciphertext_to_hex(ciphertext)
    #print("Ciphertext as Hexadecimal string:", ciphertext_hex)
    
    decrypted_bytes = decrypt_message(ciphertext, *private_key)
    decrypted_message = decode_message_utf8(decrypted_bytes)
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()
