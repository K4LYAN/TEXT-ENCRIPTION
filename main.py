from flask import Flask, render_template, request
from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    plaintext = request.form['plaintext']
    aes_key = get_random_bytes(16)  # 16 bytes key for AES
    des_key = get_random_bytes(8)   # 8 bytes key for DES

    # RSA keys generation
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Encrypt using AES
    aes_cipher = aes_encrypt(plaintext, aes_key)

    # Encrypt using DES
    des_cipher = des_encrypt(plaintext, des_key)

    # Encrypt using RSA
    rsa_cipher = rsa_encrypt(plaintext, public_key)

    return render_template('result.html', plaintext=plaintext,
                           aes_cipher=aes_cipher.hex(),
                           des_cipher=des_cipher.hex(),
                           rsa_cipher=rsa_cipher,)

def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext

def des_encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
    return ciphertext

def rsa_encrypt(plaintext, public_key):
    rsa_public_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
    ciphertext = cipher_rsa.encrypt(plaintext.encode())
    return ciphertext.hex()

if __name__ == '__main__':
    app.run(debug=True)
