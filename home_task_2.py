import hashlib

def hash_file(filename):
    h = hashlib.md5()

    with open(filename, 'rb') as file:
        chuck = 0
        while chuck != b'':
            chuck = file.read(1024)
            h.update(chuck)

    return h.hexdigest()

# message = hash_file('iterators.py')
# print(message)


def read_hash_string(filename):
    with open(filename, encoding='utf-8') as file:
        while True:
            value = file.readline().strip('\n')
            if value == '':
                break
            else:
                print(value)
                value = bytes(value, encoding='utf-8')
                value_rb = hashlib.md5()
                value_rb.update(value)
                value_rb = value_rb.hexdigest()
                print(value_rb)


#read_hash_string('test.txt')


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