import requests
from pprint import pprint


class yandex_disk:
    with open('nekot.txt', encoding='utf-8') as f:
        token = f.readline().strip('\n')
    TOKEN = token
    HOST = 'https://cloud-api.yandex.net'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

    def get_info(self):
        url = 'https://cloud-api.yandex.net/v1/disk/'
        response = requests.get(url, headers=self.headers)
        print(response.status_code)
        pprint(response.json())

    def delete_folder_or_file(self, name_folder_or_file=None):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'

        if name_folder_or_file == None:
            name_folder_or_file = input('enter the name of the folder or file you want to delete : ')

        params = {'path': f'{name_folder_or_file}', 'permanently': 'False'}
        response = requests.delete(url, headers=self.headers, params=params)

        if response.status_code == 204:
            print('Succefully')
            return 204
        else:
            print('not succesfully')
            print(response.status_code)
            return response.status_code

    def create_folder_or_file(self,name_folder_or_file=None):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'

        if name_folder_or_file == None:
            name_folder_or_file = input(' Enter name create folder:')

        params = {'path': f'{name_folder_or_file}'}
        response = requests.put(url, headers=self.headers, params=params)

        if response.status_code == 201:
            print('Succefully')
            return 201

        else:
            print('not succesfully')
            #print(response.status_code)
            return response.status_code

if __name__=='__main__':
    ya_disk = yandex_disk()
    # ya_disk.get_info()
    # ya_disk.delete_folder_or_file()
    ya_disk.create_folder_or_file()