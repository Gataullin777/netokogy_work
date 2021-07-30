from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv

name_file = 'phonebook_raw.csv'

def sorting(name_file):
    with open(name_file, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    #pprint(contacts_list)
    #print('+++++++')
    #for i in contacts_list:
        #print(i)

    #print()
    #print(' WORK DATA')
    #print()

    data_list_1 = []
    for info_list in contacts_list:
        #print(info_list)

        if len(info_list[0].split(' ')) == 2:
            # print(f"result = {info_list[0].split(' ')}")

            finish_list = info_list[0].split(' ')
            info_list[0] = finish_list[0]
            info_list[1] = finish_list[1]
            #print(f' if_1 = {info_list}')
            #print()
            data_list_1.append(info_list)

        elif len(info_list[0].split(' ')) == 3:
            # print(f"result = {info_list[0].split(' ')}")

            finish_list = info_list[0].split(' ')
            info_list[0] = finish_list[0]
            info_list[1] = finish_list[1]
            info_list[2] = finish_list[2]
            #print(f' if_2 = {info_list}')
            #print()
            data_list_1.append(info_list)

        elif len(info_list[1].split(' ')) == 2:
            # print(f"result = {info_list[0].split(' ')}")

            finish_list = info_list[1].split(' ')
            info_list[1] = finish_list[0]
            info_list[2] = finish_list[1]
            #print(f' if_2 = {info_list}')
            #print()
            data_list_1.append(info_list)


        else:
            #print(f' else = {info_list}')
            #print()
            data_list_1.append(info_list)


    #print('++++++++++++++++++++++++++++++++++')

    data_list_2 = []
    for i in data_list_1:
        pattern_phone = r'(8|\+7)\s*\(*(\d{1,3})\)*[-\s]*(\d{1,3})?[-\s]?(\d{1,2})[-\s]*(\d{1,3})\s*\(*(\w+\.)*\s*(\d+)*\)*'
        sub_phone = r'+7(\2)\3\4\5 \6\7'
        temp_list = []
        for text in i:
            phone = re.sub(pattern_phone, sub_phone, text)
            #print(phone)
            temp_list.append(phone)
        data_list_2.append(temp_list)


    #for i in data_list_2:
        #print(i)
        #print(len(i))


    data_list_dictionary = []
    for list_ in data_list_2:
        data_list_dictionary.append({f'{list_[0]}, {list_[1]}' : [list_[2], list_[3], list_[4], list_[5], list_[6]]})



    #pprint(data_list_dictionary)

    #print('++++++++++++++++++++++++++++++++++')

    temp_list = []
    data_dictionary_sorted = {}
    for i in data_list_dictionary:

        for k, l in i.items():
            # print(f'k = {k}')
            # print(f'l = {l}')
            if k in temp_list:
                value = data_dictionary_sorted[k]
                data_dictionary_sorted[k] = value + l
                # print('if block')

            else:
                temp_list.append(k)
                data_dictionary_sorted[k] = l
                # print('else block')

        #print(temp_list)

    #pprint(data_dictionary_sorted)

    #print('++++++++++++++++++++++++++++++++++')

    data_list_finish = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
    for key, value in data_dictionary_sorted.items():
        temporary_list = ['-', '-', '-', '-', '-', '-', '-']

        lastname_and_firstname_list = key.split(',')
        lastname = lastname_and_firstname_list[0].strip(' ')
        temporary_list[0] = lastname
        #print(lastname)

        firstname = lastname_and_firstname_list[1].strip(' ')
        temporary_list[1] = firstname
        #print(firstname)

        surname = value[0]
        temporary_list[2] = surname

        organization = value[1]
        temporary_list[3] = organization

        for i in range(2, len(value)):

            search_text = value[i]

            pattrern_position = r'\w+\s\w+\s'
            position = re.match(pattrern_position, search_text)
            #print(position)
            if position is not None:
                temporary_list[4] = value[i]


            pattern_phone_number = r'(8|\+7)\s*\(*(\d{1,3})\)*[-\s]*(\d{1,3})?[-\s]?(\d{1,2})[-\s]*(\d{1,3})\s*\(*(\w+\.)*\s*(\d+)*\)*'
            phone_number = re.match(pattern_phone_number, search_text)
            if phone_number is not None:
                temporary_list[5] = value[i]

            pattern_email = r'\w+[@]\w+\.'
            email = re.search(pattern_email, search_text)
            #print(key)
            if email is not None:
                temporary_list[6] = value[i]
            #print(temporary_list[6])

            #print(f'{key} = {len(value)} +++ {email} +++ value = {value[i]}')

        data_list_finish.append(temporary_list)

    #print(data_list_finish)
    data_list_finish.pop(1)
    for i in data_list_finish:
        print(i)

    return data_list_finish
def write_csv(list_):
    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(list_)

if __name__=='__main__':
    sorted_data_list = sorting(name_file)
    write_csv(sorted_data_list)




# # TODO 2: сохраните получившиеся данные в другой файл
# # код для записи файла в формате CSV
# with open("phonebook.csv", "w") as f:
#   datawriter = csv.writer(f, delimiter=',')
#   # Вместо contacts_list подставьте свой список
#   datawriter.writerows(contacts_list)