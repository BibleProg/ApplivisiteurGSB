from requests import get
from itertools import product
from time import time

start = time()
for code in product('0123456789', repeat=4):
    code = ''.join(code)
    response = get('http://127.0.0.3/pass/guess/' + code)
    if response.status_code == 200 : break
end = time()

print("The number was " + code + " found in " + str(int(end - start)) + " seconds")

