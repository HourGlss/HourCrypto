import hashlib
import secrets
import string

def buildpow(index,timestamp,effort,data,previous_hash):
    m = hashlib.sha256()
    m.update((str(index) + str(timestamp) + str(effort) + str(data) + str(previous_hash)).encode('utf-8'))
    return m
def validate(block):
    if block.index == 0:
        return True
    pow = buildpow(block.index,block.timestamp,block.effort,block.data,block.previous_hash)
    if block.proof_of_work == pow.hexdigest():
        return True
    print("bad block",block.index)
    return False

def random_str():
    # Generate a random size string from 3 - 27 characters long
    rand_str = ''
    for i in range(0, 1 + secrets.randbelow(25)):
        rand_str += string.ascii_lowercase[secrets.randbelow(26)]  # each char is a random downcase letter [a-z]
    return rand_str

def genhash(index,timestamp,data,last_hash):
    effort = random_str()
    return effort, buildpow(index,timestamp,effort,data,last_hash)

def leadingzeroes(digest):
    n = 0
    result = ''.join(format(x, '08b') for x in bytearray(digest))
    for c in result:
        if c == '0':
            n += 1
        else:
            break
    return n

def createHexdigest(s):
    m = hashlib.sha256()
    m.update(s.encode('utf-8'))
    secret_key = m.hexdigest()
    return secret_key

def validate_blockchain(blockchain):
    previous = ""
    for i in range(0,len(blockchain)-1):
        block = blockchain[i]
        if block.index == 0:
            previous = block.hash
            continue
        else:
            previous = blockchain[i-1].hash
        if not validate(block):
            return False

        transactions = block.data['transactions']

        for transaction in transactions:
            if transaction['from'] == "network" and transaction['amount'] != 1:
                return False
        if previous != block.previous_hash:
            return False
    return True

def validate_signature(public_key, signature, message):
    """Verifies if the signature is correct. This is used to prove
    it's you (and not someone else) trying to do a transaction with your
    address. Called when a user tries to submit a new transaction.
    """
    public_key = (base64.b64decode(public_key)).hex()
    signature = base64.b64decode(signature)
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    # Try changing into an if/else statement as except is too broad.
    try:
        return vk.verify(signature, message.encode())
    except:
        return False