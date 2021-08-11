import hashlib

def func_generator(filename):
    with open(filename) as file:
        value = file.readline().strip('\n')
        value_rb = ''
        while value != '':
            print(value)
            value = bytes(value, encoding='utf-8')
            value_rb = hashlib.md5()
            value_rb.update(value)
            value_rb = value_rb.hexdigest()
            yield value_rb
            value = file.readline().strip('\n')







for item in func_generator('test.txt'):
    print(item)