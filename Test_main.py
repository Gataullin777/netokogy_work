from main import *
import pytest



class Test_functions_main:

    def setup_class(self):
        print('start test functions of the module main')

        print('to directories in shelf number 3, add document number "11111" ')
        directories['3'].append('11111')

        print('add in the documents test data : {"type": "passport", "number": "11111", "name": "Test name"}')
        documents.append({"type": "passport", "number": "11111", "name": "Test name"})




    @pytest.mark.parametrize('number_document, result', [('11111', "Владелец : Test name" ), ('99999', 'такого документа не существует!' )])
    def test_people(self, number_document, result):
        assert people(number_document) == result

    @pytest.mark.parametrize('number_document, result', [('11111', 'Документ находиться в полке под номером 3 '), ('99999', 'Документа под таким номером не существует!')])
    def test_shelf(self, number_document, result):
        assert shelf(number_document) == result


    @pytest.mark.parametrize('type_doc, number, name, num_shelf, result',
                             [
                            ('passport', '22222', 'Liza', '3', 'Данные успешно добавлены в полку 3'),
                            ('passport', '66666', 'rudolf', '5555', 'Полки под таким номером не существует!!!')
                             ]
                             )
    def test_add_data(self, type_doc, number, name, num_shelf, result):
        assert add_data(type_doc, number, name, num_shelf) == result

    @pytest.mark.parametrize('number_document, result',
                             [
                                 ('11111', 'Данные удалены'),
                                 ('11111', 'Увы, документа под таким номером не существует!!!')
                             ]
                             )
    def test_delete(self, number_document, result):
        assert delete(number_document) == result

    @pytest.mark.parametrize('number_document, number_shelf, result',
                             [
                                 ('22222', '2', 'Данные перемещены'),
                                 ('646514', '3', 'Документа под таким номером не существует!!!'),
                                 ('22222', '6464', 'Полки под таким номером не существует!!!' )
                             ]
                             )
    def test_move(self, number_document, number_shelf, result):
        assert move(number_document, number_shelf) == result

    @pytest.mark.parametrize('a, result', [('4', 'Новая полка создана'), ('1', 'Полка под таким номером уже существует!')])
    def test_add_shelf(self, a, result):
        assert add_shelf(a) == result

    def teardown_class(self):
        print('test end')

        if '11111' in directories['3']:
            print('delete from shelf number 3, document number "11111" ')
            directories['3'].remove('11111')

        if {"type": "passport", "number": "11111", "name": "Test name"} in documents:
            print('delete from documents test data : {"type": "passport", "number": "11111", "name": "Test name"}')
            documents.remove({"type": "passport", "number": "11111", "name": "Test name"})

        if '22222' in directories['2']:
            print('delete from shelf number 2, document number "22222" ')
            directories['2'].remove('22222')

        if {"type": "passport", "number": "22222", "name": "Liza"} in documents:
            print('delete from documents test data : {"type": "passport", "number": "22222", "name": "Liza"}')
            documents.remove({"type": "passport", "number": "22222", "name": "Liza"})

        print('delete from directories shelf number 4')
        directories.pop('4')

        print(documents)
        print(directories)


