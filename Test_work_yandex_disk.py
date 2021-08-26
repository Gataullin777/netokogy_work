import pytest

from work_yandex_disk import yandex_disk

ya_disk = yandex_disk()

class Test_yandex_disk:

    def setup_class(self):
        print('Start testing function')

    @pytest.mark.parametrize('name_file_or_folder, response_status_code', [('qqqqq', 201), ('qqqqq', 409) ])
    def test_create_folder_or_file(self, name_file_or_folder, response_status_code):
        assert ya_disk.create_folder_or_file(name_file_or_folder) == response_status_code


    def teardown_class(self):
        print('End testing function')

