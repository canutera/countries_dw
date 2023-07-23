import requests
import json
from src.country import Country


class CountriesHook:
    '''
    CountriesHook
    ------------- 
    en: a hook class that makes request at countries endpoint that returns all available countries

    pt: uma classe hook que faz uma requisição no endpoint que da countries api 
    que retorna um json com todos os países disponíveis

    Attributes
    ----------
    raw_data : list[dict]
        parsed json recieved from all countries end point

    Methods 
    -------
    get_countries -> list[dict]
        returns a list of dictionaries of all countries

        this list will be saved as a json file in root

    load_from_json -> list[dict]
        returns a list of dictionaries of all countries 

        data will be loaded from a json file in root

    get_index_of_country -> dict
        keyword:str
            keyword to search in common name of country

        returns a dict with all matched countries and respective indexes



    '''
    raw_data: list[dict]
    tables: list[str] = [ 'names', 'native_names', 'top_level_domains', 'codes', 'independency_table',
                          'un_membership_table',  'currencies', 'idds', 'capital', 'alt_spellings', 
                          'regions', 'languages', 'translations', 'lat_lng', 'general_information',
                          'borders',  'demonyms', 'maps', 'gini_index', 'car_information',  'timezones', 
                          'continents', 'flags', 'coat_of_arms', 'postal_codes',]

    def __init__(self) -> None:
        try:
            self.load_from_json()
        except FileNotFoundError:
            self.get_countries()

    def load_from_json(self) -> None:
        '''Attempts to load countries from a json file'''
        with open('data/countries.json', encoding='utf-8') as f:
            self.raw_data = json.load(f)
        return self.raw_data

    def get_countries(self) -> list[dict]:
        '''
        en : Returns a list of dicts with all countries listed in rest_countries api
        pt_br: Retorna um lista de dicionários com todos os países listados na api rest_countries
        '''
        URL = 'https://restcountries.com/v3.1/all'
        self.raw_data = requests.get(url=URL).json()

        with open('data/countries.json', 'w') as f:
            json.dump(self.raw_data, f)

        return self.raw_data

    def get_index_of_country(self, keyword: str):
        '''Search a country by keyword

        Parameters
        ----------
        keyword : str
            keyword used to search a country

        Returns
        -------
        dict
            a dict with matched countries by common name and respective indexes
        '''
        names = [i['name']['common'] for i in self.raw_data]
        filtered_values = filter(lambda x: keyword.lower() in x.lower(), names)
        return {i: names.index(i) for i in filtered_values}
    
    def parse_countries(self):
        self.countries = [Country(i) for i in self.raw_data]
       
