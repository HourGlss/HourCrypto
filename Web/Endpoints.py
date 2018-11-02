from flask import Flask, request
import json
import requests
import logging
import inspect

import Utilities.Utility as Utility
import User_classes.User as User
import Mining_classes.Variables as variables
node = Flask(__name__)
def start(a):
    global node
    node.config['SECRET_KEY'] = Utility.createHexdigest(User.password)
    node.run(host="0.0.0.0", port=variables.PORT)





log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@node.route('/txion', methods=['GET', 'POST'])
def transaction():
    func = inspect.currentframe().f_back.f_code
    #TODO add logging to transactions, currently we can't send and receive blocks. One problem at a time.
    if request.method == 'POST':
        # On each new POST request, we extract the transaction data
        new_txion = request.get_json()
        # Then we add the transaction to our list
        if Utility.validate_signature(new_txion['from'], new_txion['signature'], new_txion['message']):
            variables.PENDING_TRANSACTIONS.append(new_txion)
            # Because the transaction was successfully
            # submitted, we log it to our console
            print("New transaction")
            print("FROM: {0}".format(new_txion['from']))
            print("TO: {0}".format(new_txion['to']))
            print("AMOUNT: {0}\n".format(new_txion['amount']))
            # Then we let the client know it worked out

            # Push to all other available nodes
            for node_url in variables.PEER_NODES:
                if node_url != request.remote_addr:
                    try:
                        headers = {"Content-Type": "application/json"}
                        requests.post(node_url + ":" + str(User.PORT) + "/txion", json=new_txion, headers=headers)
                    except:
                        pass
            return "Transaction submission successful\n"
        else:
            return "Transaction submission failed. Wrong signature\n"
    # Send pending transactions to the mining process
    elif request.method == 'GET' and request.args.get("update") == User.public_key:
        pending = json.dumps(variables.PENDING_TRANSACTIONS)
        # Empty transaction list
        variables.PENDING_TRANSACTIONS = []
        return pending


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

@node.route('/balances', methods=['GET'])
def get_balance():
    func = inspect.currentframe().f_back.f_code
    ip = request.remote_addr
    logging.info("{} looked at balances".format(ip))
    working = variables.BLOCKCHAIN
    balances = {}
    balances_json = []

    for block in working:
        if block.index != 0:
            data = block.data
            for transaction in data:
                to = transaction['to']
                source = transaction['from']
                amount = transaction['amount']


                if type(amount) == type("string"):
                    amount = eval(amount)

                if to in balances:
                    balances[to] += amount
                else:
                    balances[to] = amount
                if source != "network":
                    balances[source] -= amount

    for k, v in balances.items():
        account = {
            "address": str(k),
            "amount": str(v)
        }
        balances_json.append(account)

    return json.dumps(balances_json)