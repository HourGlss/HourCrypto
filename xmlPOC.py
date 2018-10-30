import defusedxml.ElementTree as et
tree = et.parse('scratch.xml')
root = tree.getroot()
blocks = []

class Block(object):
    def __init__(self, id=0, foo=0, bar=0, trans=0):
        self.id = int(id)
        self.foo = float(foo)
        self.bar = str(bar)
        self.transactions = trans

    def importxml(self, block_xml):
        self.id = block_xml.find('id').text
        self.bar = block_xml.find('bar').text
        self.foo = block_xml.find('foo').text
        import_transactions = block_xml.find('transactions')
        transactions = []
        for transaction in import_transactions:
            t_from = transaction.find('from').text
            t_to = transaction.find('to').text
            t_amount = int(transaction.find("amount").text)
            transactions.append({'from': t_from, 'to': t_to, 'amount': t_amount})
        self.transactions = transactions

    def exportxml(self,tabs):
        xml = "\t" * tabs +"<block>\n"
        tabs += 1
        xml += "\t" * tabs +"<id>{}</id>\n".format(self.id)
        xml += "\t" * tabs +"<foo>{}</foo>\n".format(self.foo)
        xml += "\t" * tabs +"<bar>{}</bar>\n".format(self.bar)
        xml += "\t" * tabs +"<transactions>\n"
        tabs += 1
        for trans in self.transactions:
            xml += "\t" * tabs + "<trans>\n"
            xml += "\t" * (tabs+1) + "<from>{}</from>\n".format(trans['from'])
            xml += "\t" * (tabs+1) + "<to>{}</to>\n".format(trans['to'])
            xml += "\t" * (tabs+1) + "<amount>{}</amount>\n".format(trans['amount'])
            xml += "\t" * tabs+ "</trans>\n"
        tabs -= 1
        xml += "\t" * tabs +"</transactions>\n"
        tabs -= 1
        xml += "\t" * tabs +"<block>\n"
        return xml

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "id:{},foo:{},bar:{},trans:{}".format(self.id, self.foo, self.bar, str(self.transactions))

for block_xml in root.findall('block'):
    b = Block()
    b.importxml(block_xml)
    blocks.append(b)
xml = '<?xml version="1.0"?>\n'
xml += '<data>\n'
for block in blocks:

    xml += block.exportxml(1)
xml += '</data>'
print(xml)

