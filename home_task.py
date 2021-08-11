import json

class CountriesIterate:

    def __init__(self):
        self.countries_list = None

    def __iter__(self):
        self.load_json()
        return self

    def __next__(self):
        if not self.countries_list:
            raise StopIteration
        country = self.countries_list.pop()
        return f"{country['name']['common']} - https://www.wikipedia.org/{country['name']['common'].replace(' ', '_')}"

    def load_json(self):
        with open('countries.json', encoding='utf-8') as f:
            self.countries_list = json.load(f)


for i in CountriesIterate():
    print(i)







