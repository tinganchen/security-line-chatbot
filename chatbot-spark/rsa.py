from Crypto.Hash import SHA
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import base64

encode_gbk_utf8 = 'utf-8'  
key_num = 1024  
 
 
# RSA public / private key - generation
def RSA_Create_Key():
    random_generator = Random.new().read  
    rsa = RSA.generate(key_num, random_generator) 
    private_pem = rsa.exportKey()  
    with open('master-private.pem', 'wb') as f:
        f.write(private_pem)
 
    public_pem = rsa.publickey().exportKey()
    with open('master-public.pem', 'wb') as f:
        f.write(public_pem)
        
    # same as master's generation，or can define another RSA instance
    private_pem = rsa.exportKey()
    with open('ghost-private.pem', 'wb') as f:
        f.write(private_pem)
 
    public_pem = rsa.publickey().exportKey()
    with open('ghost-public.pem', 'wb') as f:
        f.write(public_pem)
 
 
# ghost uses public key to encrypt message
def RSA_gKey_Encrypt(message):
    with open('ghost-public.pem', 'rb') as f:
        key = f.read()
        rsakey = RSA.importKey(key)  # import read-in public key
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # generate object
        # encrypt message，must be byte to be encrypted (other than str)
        ## message (str) -> message (byte) -> cipher text
        cipher_text = base64.b64encode(cipher.encrypt(
            message.encode(encoding=encode_gbk_utf8)))
        return cipher_text
 
 
# ghost uses private key to decrypt message
def RSA_gKey_Decrypt(cipher_text):
    with open('ghost-private.pem', 'rb') as f:
        key = f.read()
        rsakey = RSA.importKey(key)  # import read-in private key
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # generate object
        # message (str) <- message (byte) <- cipher text
        text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR")
        return text.decode(encoding=encode_gbk_utf8)
 
 
# master uses private key to sign up
def RSA_mKey_Sign(message):
    with open('master-private.pem', 'rb') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(message.encode(encoding=encode_gbk_utf8))
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)  
    return signature
 
 
# master uses public key to verify the signature
def RSA_mKey_CheckSign(message, signature):
    with open('master-public.pem', 'rb') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        verifier = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(message.encode(encoding=encode_gbk_utf8))
        is_verify = verifier.verify(digest, base64.b64decode(signature))
    return is_verify
 
 
if __name__ == "__main__":
 
    '''
    # Large document
    try:
        with open('test_100MB.txt','rb') as f:
            while True:
                message = f.read(64) #key_num
                #rsa code
    except EOFError:
        pass
    '''
    message = 'hello world !'
    RSA_Create_Key()
    try:
        cipher_text = RSA_gKey_Encrypt(message)
        print(cipher_text.decode("utf-8"))
        text = RSA_gKey_Decrypt(cipher_text)
        print(text)
 
        signature = RSA_mKey_Sign(message)
        print(signature)
        is_verify = RSA_mKey_CheckSign(message, signature)
        print(is_verify)
    except:
        print('rsa run error')
