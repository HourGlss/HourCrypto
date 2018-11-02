
import requests

xml = """<?xml version='1.0' encoding='utf-8'?>
<a>test</a>"""
headers = {'Content-Type': 'application/xml'} # set what your server accepts
requests.post('http://127.0.0.1/block', data=xml, headers=headers).text
requests.get('http://127.0.0.1/block?block_number=20')