from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from base64 import b64encode
import smtplib
from email.message import EmailMessage

# 1. Load RSA public key
with open('rsa_keys/public.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())

# 2. Generate AES key
aes_key = get_random_bytes(16)
cipher_aes = AES.new(aes_key, AES.MODE_EAX)

# 3. Encrypt file
with open('file_to_encrypt.txt', 'rb') as f:
    plaintext = f.read()

ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

with open('encrypted_data/file.enc', 'wb') as f:
    for x in (cipher_aes.nonce, tag, ciphertext):
        f.write(x)

# 4. Encrypt AES key with RSA public key
cipher_rsa = PKCS1_OAEP.new(public_key)
enc_key = cipher_rsa.encrypt(aes_key)

with open('encrypted_data/key.enc', 'wb') as f:
    f.write(enc_key)

# 5. Send Email with attachment
EMAIL_SENDER = "krischtien@gmail.com"
EMAIL_PASSWORD = "ttgwijzritjgwbnr"
EMAIL_RECEIVER = "samsungecha557@gmail.com"

msg = EmailMessage()
msg['Subject'] = 'Encrypted File'
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_RECEIVER
msg.set_content("File terenkripsi dan kunci AES juga sudah dienkripsi dengan RSA.")

# Attach file
with open('encrypted_data/file.enc', 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='file.enc')

with open('encrypted_data/key.enc', 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='key.enc')

# Send email via SMTP
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("Email sent!")
