from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

# 1. Load encrypted AES key and decrypt it
with open('rsa_keys/private.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())

with open('encrypted_data/key.enc', 'rb') as f:
    enc_key = f.read()

cipher_rsa = PKCS1_OAEP.new(private_key)
aes_key = cipher_rsa.decrypt(enc_key)

# 2. Decrypt the file
with open('encrypted_data/file.enc', 'rb') as f:
    nonce = f.read(16)
    tag = f.read(16)
    ciphertext = f.read()

cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag)

with open('decrypted_output.txt', 'wb') as f:
    f.write(plaintext)

print("File berhasil didekripsi.")
