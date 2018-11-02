from flask import Flask, request
import logging
import hashlib
import random

node = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
m = hashlib.sha256()
m.update(str(random.randint(0, 100)).encode('utf-8'))


@node.route('/block', methods=['GET','POST'])
def block():
    ip = request.remote_addr

    if request.method == 'POST':
        try:
            print(ip,request.data.decode('utf-8'))
        except TypeError:
            print("data error")
    else:
        block_number = str(int(request.args['block_number']))
        print(ip, block_number)

    return "0\n"
if __name__ == "__main__":
    node.config['SECRET_KEY'] = m.hexdigest()
    node.run(host="0.0.0.0", port=80)
