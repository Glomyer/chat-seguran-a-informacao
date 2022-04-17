import os
from subprocess import Popen, PIPE


read, write = os.pipe()

client_instance = Popen(["python client.py", ""], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
client_instance.communicate(input=b'sdasd')
print(type(b'\n'))

