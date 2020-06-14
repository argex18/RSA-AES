import os
from traceback import print_exc
from base64 import b64decode, b64encode
import json

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA512

def runAESencryption(input_path, output_path, pemkeys=None):
    """
    Run AES encryption

    Parameters:
    input_path = the path to the file containing the data -> str
    output_path = the path to the file where to output the encrypted data -> str
    pemkeys = the rsa keys needed to encrypt/decrypt the iv (Initialitation Vector) and the aes key.
    If not specified, it's automatically obtained by the standard path to the file 'rsakeys.pem'. -> Union [str, list]

    Returns:
    The byte string of encrypted data. None in case of failure. -> bytes   
    """
    encrypted_text = None
    try:
        plain_text = None

        if not isinstance(input_path, str):
            raise TypeError('ERROR: input_path must be a path to a file to encrypt (str)')
        if not isinstance(output_path, str) or not output_path.endswith('.json'):
            raise TypeError('ERROR: output_path must be a path to a file of json format (str)')

        if pemkeys != None:
            if isinstance(pemkeys, str):
                rsakeys = readRSAkeys(pemkeys)
            elif isinstance(pemkeys, list):
                rsakeys = pemkeys
            else:
                raise TypeError('ERROR: pemkeys must be of type str or list')
        else:
            rsakeys = generateRSAkeys('pemkeys.pem')
        
        public_key = rsakeys[0]
        private_key = rsakeys[1]

        aes_key = get_random_bytes(16)
        aes = AES.new(aes_key, AES.MODE_CBC)

        if os.path.exists(input_path):
            with open(input_path, 'rb') as f:
                plain_text = f.read()
            # The data are first padded by a block size of 16 bytes
            # (needed to perform the AES encryption/decryption)
            # then encrypted.

            # The AES operative mode is Cipher Block Chaining.
            # It requires an IV (Initialitation Vector) of 16 bytes
            # to perform the first round of encryption unpredictably
            encrypted_text = aes.encrypt( pad(data_to_pad=plain_text, block_size=AES.block_size) )
            iv = aes.iv

            # Problems with encoding
            rsa = PKCS1_OAEP.new(public_key, SHA512)
            if rsa.can_encrypt():
                aes_key = rsa.encrypt(aes_key)
                iv = rsa.encrypt(iv)
            else:
                raise KeyError('ERROR: Invalid keys passed')

            result = json.dumps({'ct': str( b64encode(encrypted_text), encoding='ascii' ), 'iv': str( b64encode(iv), encoding='ascii' ), 'key': str( b64encode(aes_key), encoding='ascii' )}, indent=5)

            with open(output_path, 'wb') as f:
                f.write( result.encode('utf-8-sig') )
        else:
            raise FileNotFoundError('ERROR: the input file does not exist')
    except Exception:
        print_exc()
    finally:
        return encrypted_text

def runAESdecryption(input_path, output_path, pemkeys=None):
    """
    Run AES decryption

    Parameters:
    input_path = the path to the file containing the encrypted data -> str
    output_path = the path to the file where to output the plain data -> str
    pemkeys = the rsa keys needed to encrypt/decrypt the iv (Initialitation Vector) and the aes key.
    If not specified, it's automatically obtained by the standard path to the file 'rsakeys.pem'. -> Union [str, list]

    Returns:
    The byte string of plain data. None in case of failure. -> bytes   
    """
    plain_text = None
    try:
        encrypted_text = None

        if not isinstance(output_path, str):
            raise TypeError('ERROR: output_path must be a path to a file (str)')
        if not isinstance(input_path, str) or not input_path.endswith('.json'):
            raise TypeError('ERROR: input_path must be a path to a file of json format (str)')

        if pemkeys != None:
            if isinstance(pemkeys, str):
                rsakeys = readRSAkeys(pemkeys)
            elif isinstance(pemkeys, list):
                rsakeys = pemkeys
            else:
                raise TypeError('ERROR: pemkeys must be of type str or list')
        else:
            rsakeys = generateRSAkeys('pemkeys.pem')

        public_key = rsakeys[0]
        private_key = rsakeys[1]

        with open(input_path, 'rb') as f:
            encrypted_text = json.loads( f.read().decode('utf-8-sig') )
        
        ciphertext = b64decode( encrypted_text['ct'] )
        iv = b64decode( encrypted_text['iv'] )
        aes_key = b64decode( encrypted_text['key'] )
        
        # Problems with encoding
        rsa = PKCS1_OAEP.new(private_key, SHA512)
        result = []
        
        if rsa.can_encrypt():
            i = 0
            # The data are decrypted within a cicle
            # which loops for every 256 bytes block size (2048 bits RSA key)
            while i < len(iv):
                if len(iv[i:len(iv)]) >= 256:
                    dec_iv = rsa.decrypt(iv[i:i + 256])
                    result.append(dec_iv)
                else:
                    dec_iv = rsa.decrypt(iv[i:len(iv)])
                    result.append(dec_iv)
                    break
                i += 256
            iv = b''.join(result)

            result.clear()
            i = 0
            while i < len(aes_key): 
                if len(aes_key[i:len(aes_key)]) >= 256:
                    dec_key = rsa.decrypt(aes_key[i:i + 256])
                    result.append(dec_key)
                else:
                    dec_key = rsa.decrypt(aes_key[i:len(aes_key)])
                    result.append(dec_key)
                    break
                i += 256
            aes_key = b''.join(result)
            del result
        else:
            raise KeyError('ERROR: Invalid keys passed')
        
        # The data are decrypted by using the AES key
        # obtained by previous RSA decryption
        # then unpadded by a block size of 16 bytes
        # (needed to perform AES encryption/decryption)
        aes = AES.new(aes_key, AES.MODE_CBC, iv)
        plain_text = unpad(padded_data=aes.decrypt(ciphertext), block_size=AES.block_size)
        
        with open(output_path, 'wb') as f:
            f.write(plain_text)
    except Exception:
        print_exc()
    finally:
        return plain_text

def generateRSAkeys(output_path):
    """
    Generate the RSA key pair

    Parameters:
    output_path = the path to the pem file where to save the RSA private key. -> str

    Returns:
    A list with the RSA public key object[0] and the RSA private key object[1]. An empty list in case of failure. -> list
    """
    rsakeys = []
    try:
        if not isinstance(output_path, str) or not output_path.endswith('.pem'):
            raise Exception('ERROR: the path to output rsa pem file is not valid')

        if not os.path.exists(output_path):
            private_key = RSA.generate(2048)
            
            with open(output_path, 'wb') as f:
                f.write( private_key.exportKey(format='PEM') )
        
        rsakeys = readRSAkeys(output_path)
    except Exception:
        print_exc()
    finally:
        return rsakeys

def readRSAkeys(input_path):
    """
    Read the RSA key pair

    Parameters:
    input_path = the path to the pem file where the RSA key pair was saved. -> str

    Returns:
    A list with the RSA public key object[0] and the RSA private key object[1]. An empty list in case of failure. -> list
    """
    fkeys = []
    try:
        if not isinstance(input_path, str):
            raise TypeError('ERROR: the input path argument must be of type string')
        if not os.path.exists(input_path):
            raise FileNotFoundError('ERROR: the file does not exist')

        with open(input_path, 'rb') as  f:
            private_key = RSA.importKey( f.read() )
        # Generate the corresponding public key from private key
        public_key = private_key.publickey()

        fkeys = [public_key, private_key]
    except Exception:
        print_exc()
    finally:
        return fkeys
    
def byteTostring(stream):
    try:
        i = 0
        if not isinstance(stream, list) and not isinstance(stream, tuple):
            raise TypeError('ERROR: the stream argument must be a list or a tuple')

        while i < len(stream):
            stream[i] = str(stream[i])
            i += 1
        
        return stream
    except Exception:
        print_exc()
        return None

def removeChars(text, chars):
    try:
        if not isinstance(text, str) or not isinstance(chars, list):
            raise TypeError('ERROR: the arguments type must be: text = string, chars = list')
        
        for ch in chars:
            if ch in text:
                text = text.replace(ch, '')
        
        return text
    except Exception:
        print_exc()
        return None

if __name__ == '__main__':
    enc = runAESencryption('test.txt', 'cipher.json', 'pemkeys.pem')
    print(enc)
