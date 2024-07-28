import numpy as np
from sympy import Matrix


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def text_to_numbers(text):
    return [(ord(char) - 65) % 26 + 1 for char in text.upper() if char != " "]


def numbers_to_text(numbers, spaces):
    text = "".join(chr((num - 1) % 26 + 65) for num in numbers)
    for index in spaces:
        text = text[:index] + " " + text[index:]
    return text


def hill_encrypt(plaintext, key_matrix):
    spaces = [i for i, char in enumerate(plaintext) if char == " "]
    plaintext = plaintext.replace(" ", "")
    plaintext_numbers = text_to_numbers(plaintext)
    plaintext_matrix = np.array(plaintext_numbers).reshape(-1, len(key_matrix))
    encrypted_matrix = np.dot(plaintext_matrix, key_matrix) % 26
    encrypted_numbers = list(encrypted_matrix.flatten())
    ciphertext = numbers_to_text(encrypted_numbers, spaces)
    return ciphertext


def hill_decrypt(ciphertext, key_matrix):
    spaces = [i for i, char in enumerate(ciphertext) if char == " "]
    ciphertext = ciphertext.replace(" ", "")
    ciphertext_numbers = text_to_numbers(ciphertext)
    ciphertext_matrix = np.array(ciphertext_numbers).reshape(-1, len(key_matrix))
    det = int(np.round(np.linalg.det(key_matrix)))

    if gcd(det, 26) == 1:
        key_matrix_inv = Matrix(key_matrix).inv_mod(26)
        decrypted_matrix = np.dot(ciphertext_matrix, key_matrix_inv) % 26
        decrypted_numbers = list(decrypted_matrix.flatten())
        plaintext = numbers_to_text(decrypted_numbers, spaces)
        return plaintext
    else:
        raise ValueError("Matriks kunci tidak memiliki invers modulo 26.")


key = np.array([[5, 6], [2, 3]])
plaintext = "ZAZ BCA"
ciphertext = hill_encrypt(plaintext, key)
print("Ciphertext:", ciphertext)

try:
    decrypted_text = hill_decrypt(ciphertext, key)
    print("Decrypted Text:", decrypted_text)
except ValueError as e:
    print(e)
