from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    plaintext = request.form['plaintext']
    # Save plaintext to a file
    with open('plaintext.txt', 'w') as file:
        file.write(plaintext)
    # Your encryption logic here
    return render_template('result.html', plaintext=plaintext, aes_cipher='...', des_cipher='...', rsa_cipher='...', md5_hash='...', sha256_hash='...')

if __name__ == '__main__':
    app.run(debug=True)
