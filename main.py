from pprint import pprint



documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
      ]

directories = {
        '1': ['2207 876234', '11-2'],
        '2': ['10006'],
        '3': []
      }


def people(number_document):
    def search_people(number_document):
        for num in documents:
            if num['number'] == number_document:
                return num['name']

    if search_people(number_document):
        return f'Владелец : {search_people(number_document)}'

    else:
        return 'такого документа не существует!'


def shelf(number_document):

    def search():  # Аргумент номер документа, возвращает номер полки где оно храниться
        for numb_shelf in directories.keys():
            if number_document in directories[numb_shelf]:
                return numb_shelf

    if search():
        return (f'Документ находиться в полке под номером {search()} ')

    elif search() is None:
        return ('Документа под таким номером не существует!')


def print_list_data():
    for i in documents:
        print(f"{i['type']} \"{i['number']}\" \"{i['name']}\"  ")


def add_data(type_doc, number, name, num_shelf ):

    def search():
        for i in directories.keys():
            if num_shelf == i:
                return num_shelf

    if search():
        documents.append({'type': type_doc, 'number': number, 'name': name})
        directories[num_shelf].append(documents[-1]['number'])
        return (f'Данные успешно добавлены в полку {num_shelf}')

    else:
        return 'Полки под таким номером не существует!!!'


def delete(number_document):

    def search():
        for numb_shelf in directories.keys():
            if number_document in directories[numb_shelf]:
                return numb_shelf


    if search():
        directories[search()].remove(number_document)
        for num in documents:
            if num['number'] == number_document:
                documents.remove(num)
                return 'Данные удалены'

    else:
        return 'Увы, документа под таким номером не существует!!!'


def move(number_document, number_shelf ):


    def search():  # Аргумент номер документа, возвращает номер полки где оно храниться

        for numb_shelf in directories.keys():
            if number_document in directories[numb_shelf]:
               return numb_shelf

    if search():

        if number_shelf in directories.keys():
            directories[search()].remove(number_document)        # 1    в таком виде функция работает нормально,
            directories[number_shelf].append(number_document)    # 2    если поменять 1 и 2 местами, при меремещении документа на 3 -ю полку,
            return 'Данные перемещены'                                                       #       обратно в другую полку переместить не получается???
        else:
            return 'Полки под таким номером не существует!!!'

    else:
        return 'Документа под таким номером не существует!!!'

    #print(directories)


def  add_shelf(number_shelf):


    if number_shelf in directories.keys():
        return 'Полка под таким номером уже существует!'

    else:
        directories.setdefault(number_shelf,[])
        return 'Новая полка создана'


def work_on_documents():

    try:

        while True:
            #print(documents)
            #print(directories)

            print('Введите пожалуйста цифру, которая принадлежит соответствующей операции: \n'
                '1 - Введите номер документа и я покажу кому она принадлежит.\n'
                '2 - Введите номер документа и я покажу номер полки, на которой он находится.\n'
                '3 - Вывести список всех документов. \n'
                '4 - Создать новый документ: ( Введите номер, тип, имя владельца и номер полки нового документа ).\n'
                '5 - Введите номер документа которую хотите удалить\n'
                '6 - Введите номер документа которую хотите переместить в другую полку и номер полки куда хотите переместить.\n'
                '7 - Введите номер новой полки.\n'
                '8 - Текущее состояние directories и documents ')


            number = int(input('Введите цифру: '))

            if number == 1:
                number_document = input('Ведите номер документа: ')
                result_people = people(number_document)
                print(result_people)

            elif number == 2:
                number_document = input('Ведите номер документа: ')  # это строка, могут быть ошибки при выводе
                result_shelf = shelf(number_document)
                print(result_shelf)
                print()

            elif number == 3:
                print_list_data()
                print()

            elif number == 4:
                type_doc = input('Введите тип документа: ')
                number = input('Введите номер документа: ')
                name = input('Введите имя владельца: ')
                num_shelf = input('Введите номер полки на котором будет лежать документ: ')
                result_add_data = add_data(type_doc, number, name, num_shelf )
                print(result_add_data)

            elif number == 5:
                number_document = input('Введите номер документа которую хотите удалить: ')
                result_delete = delete(number_document)
                print(result_delete)

            elif number == 6:
                number_document = input('Введите номер документа: ')
                number_shelf = input('Введите номер полки куда хотите данный документ перенести: ')
                result_move = move(number_document, number_shelf)
                print(result_move)

            elif number == 7:
                number_shelf = input('Введите номер новой полки: ')
                result_add_shelf = add_shelf(number_shelf)
                print(result_add_shelf)

            elif number == 8:
                pprint(directories)
                pprint(documents)
                print()
                print()

            else:
                print('Вы ввели не ту цифру, будьте внимательны!')
                print()

    except:
        work_on_documents()

if __name__=='__main__':
    work_on_documents()


