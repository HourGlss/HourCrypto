import xmltodict
import requests

# xml = """<?xml version='1.0' encoding='utf-8'?>
# <a>б</a>"""
# headers = {'Content-Type': 'application/xml'} # set what your server accepts
# print(requests.post('http://httpbin.org/post', data=xml, headers=headers).text)
# tree = et.parse('scratch.xml')


class Block(object):
    def __init__(self, id=0, foo=0, bar=0, trans=[]):
        self.id = int(id)
        self.foo = float(foo)
        self.bar = str(bar)
        self.transactions = trans

    def importXml(self, block_xml):
        for field in block_xml:
            if field != "transactions":
                block_to_add.setField(field, block_xml[field])
            else:
                for transaction in block_xml[field]['trans']:
                    transaction_to_add = {}
                    for k in transaction:
                        transaction_to_add[k] = transaction[k]
                    block_to_add.setField("transaction", transaction_to_add)


    def setField(self,field,value):
        if field == 'id':
            try:
                self.id = int(value)
            except:
                pass
        elif field == 'foo':
            try:
                self.foo = float(value)
            except:
                pass
        elif field == 'bar':
            try:
                self.bar = int(value)
            except:
                pass
        elif field == 'transaction':
            try:
                if type(value) is type({}):

                    self.transactions.append(value)
            except:
                pass


    def exportXml(self):
        block = {'block':{'id':self.id,'foo':self.foo,'bar':self.bar,'transactions':{'trans':self.transactions}}}
        return xmltodict.unparse(block)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "id:{},foo:{},bar:{},trans:{}".format(self.id, self.foo, self.bar, str(self.transactions))


xmldata = open('scratch.xml',"rb")
tree2 = xmltodict.parse(xmldata)
# root = tree.getroot()
blocks = []
for block_xml in tree2['root']['block']:
    block_to_add = Block()
    block_to_add.importXml(block_xml)
    blocks.append(block_to_add)
for block in blocks:
    print(block.exportXml())


